import json
from collections import Counter


min = 10

# 创建一个标签计数器
tag_counter = Counter()

# 遍历JSONL文件，统计每个标签的出现次数
with open('nltk_body_title_tages_answer_output_processed_with_id.jsonl', 'r') as file:
    for line in file:
        item = json.loads(line)
        tags = item['Tags']
        for tag in tags:
            tag_counter[tag] += 1

# 过滤数据，去除标签出现次数为1的行
filtered_data = []
with open('nltk_body_title_tages_answer_output_processed_with_id.jsonl', 'r') as file:
    for line in file:
        item = json.loads(line)
        tags = item['Tags']
        if all(tag_counter[tag] > min for tag in tags):
            filtered_data.append(item)

# 将过滤后的数据保存回JSONL文件
with open(str(min)+'filtered_nltk_body_title_tages_answer_output_processed_with_id.jsonl', 'w') as file:
    for item in filtered_data:
        file.write(json.dumps(item) + '\n')

print("数据过滤完成，已保存到 filtered_nltk_body_title_tages_answer_output_processed_with_id.jsonl")