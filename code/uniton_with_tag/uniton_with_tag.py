import json
import joblib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import silhouette_score
from collections import defaultdict

# 读取JSONL文件
with open('./data.jsonl', 'r') as f:
    data = [json.loads(line) for line in f]

# 取样本数据
sample_size = 5000  # 可以根据需要调整样本大小
sampled_data = data[:sample_size]

# 提取标签信息
tags = [entry['tags'].strip("[]").split(", ") for entry in sampled_data]

# 使用MultiLabelBinarizer处理标签
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(tags)

# 使用PCA降维
pca = PCA(n_components=100)  # 选择合适的维度数量
X_reduced = pca.fit_transform(X)

# 定义一个函数来评估不同的k值
def find_optimal_k(X, max_k=20):
    sse = []
    silhouette_scores = []
    for k in range(400, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        sse.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))
    return sse, silhouette_scores

# 找到最佳的k值
max_k = 2000  # 可以根据实际情况调整
sse, silhouette_scores = find_optimal_k(X_reduced, max_k)

# 绘制肘部图并保存
plt.figure(figsize=(12, 6))
plt.plot(range(400, max_k + 1), sse, marker='o')
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('SSE')
plt.savefig('elbow_plot_pca.png')  # Save the plot to a file
plt.close()  # Close the plot to free up memory

# 绘制轮廓系数图并保存
plt.figure(figsize=(12, 6))
plt.plot(range(400, max_k + 1), silhouette_scores, marker='o')
plt.title('Silhouette Score For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.savefig('silhouette_plot_pca.png')  # Save the plot to a file
plt.close()  # Close the plot to free up memory

# 选择最佳的k值
optimal_k = silhouette_scores.index(max(silhouette_scores)) + 400
print(f"Optimal k value based on Silhouette Score: {optimal_k}")

# 使用最佳的k值进行聚类
n_clusters = optimal_k
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X_reduced)

# 获取聚类标签
labels = kmeans.labels_
# 将聚类标签与原始数据关联
clustered_data = list(zip(sampled_data, labels))

# 按聚类标签分组
clusters = defaultdict(list)
for entry, label in clustered_data:
    clusters[label].append(entry)

# 输出每个聚类的内容到JSONL文件
output_file = str(n_clusters) + '_tag_clustered_results_sample_pca.jsonl'
with open(output_file, 'w') as f:
    for label, entries in clusters.items():
        cluster_info = {
            'Tag_Cluster': int(label),
            'Entries': entries
        }
        f.write(json.dumps(cluster_info) + '\n')

print(f"Clustering results have been written to {output_file}")

# 保存模型和MultiLabelBinarizer
model_filename = 'kmeans_model_sample_pca.joblib'
mlb_filename = 'multilabel_binarizer_sample_pca.joblib'
joblib.dump(kmeans, model_filename)
joblib.dump(mlb, mlb_filename)

print(f"Model and MultiLabelBinarizer have been saved to {model_filename} and {mlb_filename}")

# 加载模型和MultiLabelBinarizer以进行预测
def predict_new_tags(new_tags):
    new_X = mlb.transform(new_tags)
    new_X_reduced = pca.transform(new_X)
    predictions = kmeans.predict(new_X_reduced)
    return predictions

# 示例：输入新的标签进行预测
new_tags = [['tag1', 'tag2'], ['tag3', 'tag4']]
predictions = predict_new_tags(new_tags)
print(f"Predictions for new tags: {predictions}")