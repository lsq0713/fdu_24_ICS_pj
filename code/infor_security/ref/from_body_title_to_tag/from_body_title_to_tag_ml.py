import json
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier

# 加载 JSONL 文件
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# 提取特征和标签，并对每个标签进行处理
def extract_features_and_labels(data):
    X = []
    y = []
    for item in data:
        title = ' '.join(item['Title'])
        body = ' '.join(item['Body'])
        text = title + ' ' + body
        X.append(text)
        
        # 对每个标签进行处理
        processed_tags = []
        for tag in item['Tags']:
            # 这里可以添加对每个标签的处理逻辑
            processed_tag = tag.lower()  # 例如，将标签转换为小写
            processed_tags.append(processed_tag)
        
        y.append(processed_tags)
    return X, y

# 加载数据
file_path = '10filtered_nltk_body_title_tages_answer_output_processed_with_id.jsonl'
path_prefix = file_path[0:3]
data = load_jsonl(file_path)

# 提取特征和标签
X, y = extract_features_and_labels(data)

# 将标签转换为多标签分类格式
mlb = MultiLabelBinarizer()
y_bin = mlb.fit_transform(y)

# 特征提取
vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = vectorizer.fit_transform(X)

# 使用 OneVsRestClassifier 进行多标签分类
model = OneVsRestClassifier(LogisticRegression(solver='liblinear'))
model.fit(X_tfidf, y_bin)

# 预测
y_pred = model.predict(X_tfidf)

# 评估模型
accuracy = accuracy_score(y_bin, y_pred)
print(f'Accuracy: {accuracy}')

# 保存模型
model_file = path_prefix+ 'tag_prediction_model.pkl'
joblib.dump(model, model_file)

# 保存向量化器
vectorizer_file = path_prefix + 'tfidf_vectorizer.pkl'
joblib.dump(vectorizer, vectorizer_file)

# 保存 MultiLabelBinarizer
mlb_file = path_prefix +'mlb.pkl'
joblib.dump(mlb, mlb_file)

# 加载模型并进行预测

model = joblib.load(model_file)
vectorizer = joblib.load(vectorizer_file)
mlb = joblib.load(mlb_file)

new_data = ["mysql","python"]
new_data_tfidf = vectorizer.transform(new_data)
predicted_tags_binary = model.predict(new_data_tfidf)
predicted_tags = mlb.inverse_transform(predicted_tags_binary)
print(f'Predicted Tags: {predicted_tags}')