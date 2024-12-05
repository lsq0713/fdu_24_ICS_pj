import pandas as pd
from collections import Counter

# 读取 CSV 文件
df = pd.read_csv('./data/xhs_daixie_with_tag.csv', header=None, names=['title','description', 'tags'])

# 初始化一个 Counter 对象
tag_counter = Counter()

# 遍历每一行的 tags
for tags in df['tags']:
    # 将 tags 按逗号分割并去除空格
    tag_list = [tag.strip() for tag in tags.split(',')]
    # 更新 Counter
    tag_counter.update(tag_list)

# 将计数结果按频率排序
sorted_tags = tag_counter.most_common()

# 将结果保存到 txt 文件
with open('tag_counts.txt', 'w') as f:
    for tag, count in sorted_tags:
        f.write(f"{tag}: {count}\n")

print("Tag counts have been saved to 'tag_counts.txt'")