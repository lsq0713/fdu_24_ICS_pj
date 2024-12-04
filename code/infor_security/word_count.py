import pandas as pd
from collections import Counter
import ast

# 读取 CSV 文件
df = pd.read_csv('cleaned_file.csv')

# 初始化一个空的 Counter 对象
tag_counter = Counter()

# 遍历每一行的 tags 列
for tags in df['tags']:
    # 将字符串转换为列表
    tags_list = ast.literal_eval(tags)
    # 更新 Counter
    tag_counter.update(tags_list)

# 将词频统计结果按词频从高到低排序
sorted_tags = sorted(tag_counter.items(), key=lambda item: item[1], reverse=True)

# 统计出现 x 次的标签数量
count_counter = Counter(count for tag, count in sorted_tags)

# 将统计结果写入文件
with open('count_frequency_output.txt', 'w') as file:
    for count, freq in sorted(count_counter.items(), key=lambda item: item[0]):
        file.write(f'出现 {count} 次的标签数量: {freq}\n')

print("出现 x 次的标签数量已写入 count_frequency_output.txt 文件。")