import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform

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
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
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
    data = read_jsonl_file('./data/500_filtered_data.jsonl')
    
    # 提取特征
    texts = extract_features(data)
    
    # 标签编码
    mlb, tags_encoded = encode_tags(data)
    
    # 划分训练集和测试集
    texts_train, texts_test, tags_train, tags_test = train_test_split(texts, tags_encoded, test_size=0.2, random_state=42)
    
    # 计算训练集的TF-IDF
    vectorizer, tfidf_matrix_train = compute_tfidf(texts_train)
    
    # 定义参数网格
    param_grid = {
        'estimator__C': [0.1, 1, 10],
        'estimator__penalty': ['l1', 'l2']
    }
    
    # 使用网格搜索进行超参数调优
    grid_search = GridSearchCV(MultiOutputClassifier(LogisticRegression()), param_grid, cv=5)
    grid_search.fit(tfidf_matrix_train, tags_train)
    
    # 输出最佳参数
    print("Best parameters found: ", grid_search.best_params_)
    
    # 使用最佳参数训练模型
    best_model = grid_search.best_estimator_
    
    # 保存最佳模型
    save_model(vectorizer, mlb, best_model)
    
    # 计算测试集的TF-IDF
    tfidf_matrix_test = vectorizer.transform(texts_test)
    
    # 预测测试集标签
    predicted_tags_test = best_model.predict(tfidf_matrix_test)
    
    # 计算准确率
    accuracy = accuracy_score(tags_test, predicted_tags_test)
    print(f'Model Accuracy: {accuracy:.4f}')

    # 尝试其他模型
    models = [
        ('LogisticRegression', MultiOutputClassifier(LogisticRegression())),
        ('RandomForest', MultiOutputClassifier(RandomForestClassifier())),
        ('SVM', MultiOutputClassifier(SVC(kernel='linear')))
    ]

    for name, model in models:
        model.fit(tfidf_matrix_train, tags_train)
        predicted_tags_test = model.predict(tfidf_matrix_test)
        accuracy = accuracy_score(tags_test, predicted_tags_test)
        print(f'{name} Accuracy: {accuracy:.4f}')

    # 使用随机搜索进行超参数调优
    param_dist = {
        'estimator__C': uniform(loc=0, scale=4),
        'estimator__penalty': ['l1', 'l2']
    }

    random_search = RandomizedSearchCV(MultiOutputClassifier(LogisticRegression()), param_distributions=param_dist, n_iter=50, cv=5, random_state=42)
    random_search.fit(tfidf_matrix_train, tags_train)

    # 输出最佳参数
    print("Best parameters found: ", random_search.best_params_)

    # 使用最佳参数训练模型
    best_model = random_search.best_estimator_

    # 保存最佳模型
    save_model(vectorizer, mlb, best_model)

    # 计算测试集的TF-IDF
    tfidf_matrix_test = vectorizer.transform(texts_test)

    # 预测测试集标签
    predicted_tags_test = best_model.predict(tfidf_matrix_test)

    # 计算准确率
    accuracy = accuracy_score(tags_test, predicted_tags_test)
    print(f'Random Search Model Accuracy: {accuracy:.4f}')

if __name__ == "__main__":
    main()