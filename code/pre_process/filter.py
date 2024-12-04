import json
from collections import defaultdict
filter_num = 400
# Step 1: Read the JSONL file
with open('data.jsonl', 'r') as file:
    data = [json.loads(line) for line in file]

# Step 2: Count tag occurrences
tag_count = defaultdict(int)
for entry in data:
    for tag in entry['tags']:
        tag_count[tag] += 1

# Step 3: Filter tags
filtered_data = []
for entry in data:
    if len(entry['tags']) == 1 and tag_count[entry['tags'][0]] < filter_num:
        continue  # Skip this entry if it has only one tag and the tag count is less than filter_num
    else:
        filtered_tags = [tag for tag in entry['tags'] if tag_count[tag] >= filter_num]
        if filtered_tags:
            entry['tags'] = filtered_tags
            filtered_data.append(entry)

# Step 4: Write the filtered data back to a JSONL file
with open(str(filter_num)+'_filtered_data.jsonl', 'w') as file:
    for entry in filtered_data:
        file.write(json.dumps(entry) + '\n')

print("Filtered data has been written to 'filtered_data.jsonl'")