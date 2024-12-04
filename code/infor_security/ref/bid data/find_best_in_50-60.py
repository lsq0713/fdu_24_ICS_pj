import json
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import random

# 读取JSONL文件
with open('./nltk_body_title_tages_answer_output_processed_with_id.jsonl', 'r') as f:
    data = [json.loads(line) for line in f]

# 提取标签信息
tags = [entry['Tags'] for entry in data]

# 将标签列表转换为字符串
tags_str = [' '.join(tag) for tag in tags]

# 使用TF-IDF向量化
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(tags_str)

# # 初始采样以找到最佳cluster的范围
# sample_size = 10000  # 可以根据实际情况调整
# sampled_indices = random.sample(range(len(tags_str)), sample_size)
# sampled_tags_str = [tags_str[i] for i in sampled_indices]
# sampled_X = vectorizer.transform(sampled_tags_str)

# # 计算不同聚类数量下的惯性值
# inertia_values = []
# max_clusters = 20  # 可以根据实际情况调整
# for n_clusters in range(1, max_clusters + 1):
#     kmeans = KMeans(n_clusters=n_clusters, random_state=42)
#     kmeans.fit(sampled_X)
#     inertia_values.append(kmeans.inertia_)

# # 绘制肘部图
# plt.figure(figsize=(10, 6))
# plt.plot(range(1, max_clusters + 1), inertia_values, marker='o')
# plt.xlabel('Number of clusters')
# plt.ylabel('Inertia')
# plt.title('Elbow Method For Optimal k (Sampled Data)')

# # 保存图像到文件
# plt.savefig('/root/processed_data/elbow_plot_sampled.png')

# # 显示图像
# plt.show()

# 根据采样结果确定最佳cluster的范围
# 例如，假设我们发现5到10个cluster是一个合理的范围
optimal_range = range(1, 400)

# 在全数据集上进行精细分析
inertia_values_full = []
for n_clusters in optimal_range:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    inertia_values_full.append(kmeans.inertia_)

# 绘制精细分析的肘部图
plt.figure(figsize=(10, 6))
plt.plot(optimal_range, inertia_values_full, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method For Optimal k (Full Data)')

# 保存图像到文件
plt.savefig('./elbow_plot_full.png')

# 显示图像
plt.show()
