import json
import re

def clean_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            cleaned_data = {
                key: re.sub(r'[^\x00-\x7F]+', '', value) if isinstance(value, str) else value
                for key, value in data.items()
            }
            outfile.write(json.dumps(cleaned_data, ensure_ascii=False) + '\n')

# 使用示例
input_file = 'stackoverflow_distinct.jsonl'
output_file = 'removed_stackoverflow_distinct.jsonl'
clean_jsonl(input_file, output_file)