import json
from bs4 import BeautifulSoup

# Function to clean HTML tags
def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

# Open JSONL file and read content
with open('tag_frequency_cleaned_input_one_answer_one_line.jsonl', 'r') as jsonl_file:
    # Open JSONL file to write cleaned data
    with open('cleaned_input_no_change.jsonl', 'w') as jsonl_output_file:
        
        # Read JSONL file line by line
        for line in jsonl_file:
            data = json.loads(line)
            
            # Clean HTML content for 'Body' and 'Answers'
            data['Body'] = clean_html(data['Body'])
            for answer in data['Answers']:
                answer['Body'] = clean_html(answer['Body'])
            
            # Write cleaned data as JSONL to output file
            jsonl_output_file.write(json.dumps(data) + '\n')