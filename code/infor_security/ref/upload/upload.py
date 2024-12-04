import json
import happybase
import hashlib
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HBase connection configuration
HBASE_HOST = os.getenv('HBASE_HOST', '10.176.62.236')  # Use environment variable for host
TABLE_NAME = 'cleaned_input_one_answer_one_line_small_real'

def hash_row_key(title):
    """Generate a hash value for the row key."""
    return hashlib.sha256(title.encode('utf-8')).hexdigest()

def create_table_if_not_exists(connection):
    """Check and create the HBase table if it does not exist."""
    if TABLE_NAME not in connection.tables():
        logger.info(f"Table {TABLE_NAME} does not exist. Creating table...")
        connection.create_table(
            TABLE_NAME,
            {
                'score': dict(),
                'title': dict(),
                'body': dict(),
                'tags': dict(),
                'answer_score': dict(),
                'answer_body': dict(),
                'question_line_num': dict(),
            }
        )
        logger.info(f"Table {TABLE_NAME} created successfully.")
    else:
        logger.info(f"Table {TABLE_NAME} already exists.")

def validate_json_data(data):
    """Validate the JSON data."""
    required_keys = ['Score', 'Title', 'Body', 'Tags', 'Answer_Score', 'Answer_Body', 'line_num']
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

def import_jsonl_to_hbase(file_path):
    """Import JSONL file into HBase."""
    # Connect to HBase
    connection = happybase.Connection(HBASE_HOST)
    
    # Check and create table
    create_table_if_not_exists(connection)
    
    table = connection.table(TABLE_NAME)

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            try:
                # Parse JSON data
                data = json.loads(line.strip())
                validate_json_data(data)

                row_key = hash_row_key(str(line_num))

                # Prepare data
                data_to_insert = {
                    b'score:': str(data['Score']).encode('utf-8'),
                    b'title:': data['Title'].encode('utf-8'),
                    b'body:': data['Body'].encode('utf-8'),
                    b'tags:': data['Tags'].encode('utf-8'),
                    b'answer_score:': str(data['Answer_Score']).encode('utf-8'),
                    b'answer_body:': data['Answer_Body'].encode('utf-8'),
                    b'question_line_num:': str(data['line_num']).encode('utf-8'),
                }
                
                # Insert data into HBase
                table.put(row_key, data_to_insert)

                # Log progress every 1000 rows
                if line_num % 1000 == 0:
                    logger.info(f"{line_num} rows imported.")

            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON at line {line_num}: {e}")
            except ValueError as e:
                logger.error(f"Error validating data at line {line_num}: {e}")
            except Exception as e:
                logger.error(f"Error importing line {line_num}: {e}")

    logger.info("Import completed.")

# Call the import function
import_jsonl_to_hbase('./upload/cleaned_input_one_answer_one_line_small.jsonl')