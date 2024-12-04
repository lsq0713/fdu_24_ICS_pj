import json

# Function to clean HTML tags


# Open JSONL file and read content
with open('cleaned_input_no_change_format.jsonl', 'r') as jsonl_file:
    # Open JSONL file to write cleaned data
    with open('/easywordcount/cleaned_input_one_answer_one_line.jsonl', 'w') as jsonl_output_file:
        
        # Read JSONL file line by line
        for line_num,line in enumerate(jsonl_file,start=1):
            data = json.loads(line)
            
            # Extract basic information
            score = data['Score']
            title = data['Title']
            body = data['Body']
            tags = data['Tags']
            
            # Extract answer information
            for answer in data['Answers']:
                answer_score = answer['Score']
                answer_body = answer['Body']
                
                # Create a dictionary to store current row data
                row = {
                    'Score': score,
                    'Title': title,
                    'Body': body,
                    'Tags': tags,
                    'Answer_Score': answer_score,
                    'Answer_Body': answer_body,
                    'line_num': line_num
                }
                
                # Write row data as JSONL to output file
                jsonl_output_file.write(json.dumps(row) + '\n')