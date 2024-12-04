import json
from collections import defaultdict

# 读取 JSONL 文件
def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line)

# 统计每个标签的出现次数
def count_tags(data):
    tag_count = defaultdict(int)
    for entry in data:
        for tag in entry['tags']:
            tag_count[tag] += 1
    return tag_count

# 选择具有代表性的数据
def select_representative_data(data, tag_count, num_samples=10000):
    selected_data = []
    tag_samples = defaultdict(list)

    # 按标签分组
    for entry in data:
        for tag in entry['tags']:
            tag_samples[tag].append(entry)

    # 按标签出现次数排序
    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)

    # 计算总标签出现次数
    total_count = sum(tag_count.values())

    # 选择代表性数据
    for tag, count in sorted_tags:
        samples = tag_samples[tag]
        if len(samples) > 0:
            # 计算每个标签应选的数据量
            num_samples_for_tag = int((count / total_count) * num_samples)
            selected_data.extend(samples[:num_samples_for_tag])
            if len(selected_data) >= num_samples:
                break

    return selected_data[:num_samples]

# 将结果写入 JSONL 文件
def write_jsonl(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(json.dumps(entry, ensure_ascii=False) + '\n')

# 主函数
def main():
    file_path = '400_filtered_data.jsonl'
    output_file_path = file_path[:10]+'representative_data.jsonl'
    
    data = list(read_jsonl(file_path))
    tag_count = count_tags(data)
    representative_data = select_representative_data(data, tag_count)

    # 将结果写入文件
    write_jsonl(output_file_path, representative_data)

if __name__ == "__main__":
    main()