import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier

# 读取JSONL文件
def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# 提取特征
def extract_features(data):
    texts = []
    for item in data:
        text = item['title'] + ' ' + item['description']
        texts.append(text)
    return texts

# 计算TF-IDF
def compute_tfidf(texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

# 标签编码
def encode_tags(data):
    tags = [item['tags'] for item in data]
    mlb = MultiLabelBinarizer()
    tags_encoded = mlb.fit_transform(tags)
    return mlb, tags_encoded

# 训练模型
def train_model(tfidf_matrix, tags_encoded):
    model = MultiOutputClassifier(LogisticRegression())
    model.fit(tfidf_matrix, tags_encoded)
    return model

# 保存模型
def save_model(vectorizer, mlb, model):
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
    joblib.dump(mlb, 'mlb_encoder.pkl')
    joblib.dump(model, 'multi_output_classifier.pkl')

# 加载模型
def load_model():
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    mlb = joblib.load('mlb_encoder.pkl')
    model = joblib.load('multi_output_classifier.pkl')
    return vectorizer, mlb, model

# 预测标签
def predict_tags(text, vectorizer, mlb, model):
    new_tfidf = vectorizer.transform([text])
    predicted_tags = model.predict(new_tfidf)
    predicted_tags_decoded = mlb.inverse_transform(predicted_tags)
    return predicted_tags_decoded

# 主函数
def main():
    # 读取JSONL文件
    data = read_jsonl_file('data.jsonl')
    
    # 提取特征
    texts = extract_features(data)
    
    # 计算TF-IDF
    vectorizer, tfidf_matrix = compute_tfidf(texts)
    
    # 标签编码
    mlb, tags_encoded = encode_tags(data)
    
    # 训练模型
    model = train_model(tfidf_matrix, tags_encoded)
    
    # 保存模型
    save_model(vectorizer, mlb, model)
    
    # 加载模型
    vectorizer, mlb, model = load_model()
    
    # 预测标签
    new_text = "swift Vapor 部署 Heroku 53 构建"
    predicted_tags = predict_tags(new_text, vectorizer, mlb, model)
    print(predicted_tags)

if __name__ == "__main__":
    main()