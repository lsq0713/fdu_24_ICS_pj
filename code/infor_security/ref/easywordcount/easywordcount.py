import json
from collections import Counter

def count_tags_frequency(jsonl_file):
    tag_counter = Counter()
    
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            tags = data.get('Tags', '')
            if tags:
                tag_list = tags.strip('<>').split('><')
                tag_counter.update(tag_list)
    
    return tag_counter

if __name__ == "__main__":
    jsonl_file = 'cleaned_input_no_change_format.jsonl'  # 替换为你的文件路径
    tag_frequency = count_tags_frequency(jsonl_file)
    
    # 将统计数据按频率排序后保存到文件
    sorted_tag_frequency = dict(tag_frequency.most_common())
    with open('./easywordcount/tag_frequency_cleaned_input_no_change_format.json', 'w') as outfile:
        json.dump(sorted_tag_frequency, outfile, indent=4)
    
    # 打印统计数据
    for tag, count in tag_frequency.most_common():
        print(f"{tag}: {count}")