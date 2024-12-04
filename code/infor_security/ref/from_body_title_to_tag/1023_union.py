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
with open('./10filtered_nltk_body_title_tages_answer_output_processed_with_id.jsonl', 'r') as f:
    data = [json.loads(line) for line in f]



# 提取标签信息
tags = [entry['Tags'] for entry in data]

# 使用MultiLabelBinarizer处理标签
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(tags)

# 使用PCA降维

# 使用已知的最佳k值进行聚类
n_clusters = 1023
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X)

# 获取聚类标签
labels = kmeans.labels_
# 将聚类标签与原始数据关联
clustered_data = list(zip(data, labels))

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
    predictions = kmeans.predict(new_X)
    return predictions

# 示例：输入新的标签进行预测
new_tags = [['tag1', 'tag2'], ['tag3', 'tag4']]
predictions = predict_new_tags(new_tags)
print(f"Predictions for new tags: {predictions}")