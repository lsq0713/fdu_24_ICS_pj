import json

def add_id_to_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for id, line in enumerate(infile, start=1):
            data = json.loads(line)
            data['id'] = id
            json.dump(data, outfile)
            outfile.write('\n')

# Example usage
input_file = 'data.jsonl'
output_file = 'output.jsonl'
add_id_to_jsonl(input_file, output_file)