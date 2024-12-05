import joblib
import re
import jieba
import csv

def preprocess(text, stop_words):
    # 去除特殊格式
    text_re = re.sub(r'[^\w\s]', '', text)
    # 分词
    words = jieba.lcut(text_re)
    # 去除停用词
    return ' '.join([word for word in words if word not in stop_words])

# 加载模型
def load_model():
    vectorizer = joblib.load("./workspace/tfidf_vectorizer.pkl")
    mlb = joblib.load("./workspace/mlb_encoder.pkl")
    model = joblib.load("./workspace/multi_output_classifier.pkl")
    return vectorizer, mlb, model

# 预测标签
def predict_tags(text, vectorizer, mlb, model):
    new_tfidf = vectorizer.transform([text])
    predicted_tags = model.predict(new_tfidf)
    predicted_tags_decoded = mlb.inverse_transform(predicted_tags)
    return predicted_tags_decoded

# 主函数
def main():
    # 尝试加载已有模型
    try:
        vectorizer, mlb, model = load_model()
        print("已加载现有模型")
    except FileNotFoundError:
        print("未找到现有模型，请联系管理员训练模型")
        return

    # 读取CSV文件
    input_file = "./data/xhs_daixie.csv"
    output_file = "./data/xhs_daixie_with_tag.csv"

    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 读取停用词列表
        file_path = "./workspace/baidu_stopwords.txt"
        with open(file_path, mode='r', encoding='utf-8') as file:
            stop_words = set(file.read().splitlines())

        # 处理每一行
        for row in reader:
            text = row[0]  # 假设文本在第一列
            processed_text = preprocess(text, stop_words)
            predicted_tags = predict_tags(processed_text, vectorizer, mlb, model)
            if predicted_tags[0]:  # 检查是否有预测的标签
                tags_str = ",".join(predicted_tags[0])
                row.append(tags_str)
                writer.writerow(row)

if __name__ == "__main__":
    main()