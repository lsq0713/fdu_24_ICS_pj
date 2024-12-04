import json
from collections import Counter

# Function to read JSONL file and count tag occurrences
def count_tags(file_path):
    tag_counter = Counter()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            tags = data.get('tags', [])
            tag_counter.update(tags)
    
    return tag_counter

# Function to write sorted tag counts to a text file
def write_sorted_tags(tag_counter, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for tag, count in tag_counter.most_common():
            file.write(f"{tag}: {count}\n")

# Main function
def main():
    input_file = '400_filtered_data.jsonl'  # Replace with your JSONL file path
    output_file = 'output.txt'  # Replace with your desired output file path
    
    tag_counter = count_tags(input_file)
    write_sorted_tags(tag_counter, output_file)

if __name__ == "__main__":
    main()