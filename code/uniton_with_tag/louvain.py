import json
import joblib
import matplotlib.pyplot as plt
import networkx as nx
import community as community_louvain
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from collections import defaultdict

# 读取JSONL文件
with open('./data.jsonl', 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]

# 提取标签信息
tags = [entry['tags'] for entry in data]

# 使用MultiLabelBinarizer处理标签
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(tags)

# 构建图
G = nx.Graph()
for i, entry in enumerate(data):
    for tag in entry['tags']:
        G.add_node(tag)
    for tag1 in entry['tags']:
        for tag2 in entry['tags']:
            if tag1 != tag2:
                if G.has_edge(tag1, tag2):
                    G[tag1][tag2]['weight'] += 1
                else:
                    G.add_edge(tag1, tag2, weight=1)

# 应用Louvain算法
partition = community_louvain.best_partition(G)

# 将聚类标签与原始数据关联
clustered_data = []
for entry in data:
    entry_tags = entry['tags']
    cluster_label = max(set(partition[tag] for tag in entry_tags), key=list(partition.values()).count)
    clustered_data.append((entry, cluster_label))

# 按聚类标签分组
clusters = defaultdict(list)
for entry, label in clustered_data:
    clusters[label].append(entry)

# 输出每个聚类的内容到JSONL文件
output_file = 'louvain_tag_clustered_results_sample.jsonl'
with open(output_file, 'w') as f:
    for label, entries in clusters.items():
        cluster_info = {
            'Tag_Cluster': int(label),
            'Entries': entries
        }
        f.write(json.dumps(cluster_info) + '\n')

print(f"Clustering results have been written to {output_file}")

# 保存MultiLabelBinarizer
mlb_filename = 'multilabel_binarizer_sample_louvain.joblib'
joblib.dump(mlb, mlb_filename)

print(f"MultiLabelBinarizer has been saved to {mlb_filename}")

# 输出聚类的数量
num_clusters = len(clusters)
print(f"Number of clusters: {num_clusters}")