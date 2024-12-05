import joblib
import re
import jieba
from jieba import analyse

def preprocess(text, stop_words):
    # 去除特殊格式
    text_re = re.sub(r'[^\w\s]', '', text)
    # 分词
    words = jieba.lcut(text_re)
    # 去除停用词
    return ' '.join([word for word in words if word not in stop_words])

# 加载模型
def load_model():
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    mlb = joblib.load("mlb_encoder.pkl")
    model = joblib.load("multi_output_classifier.pkl")
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

    # 进入预测循环
    while True:
        new_text = input("请输入需要预测的文本（输入'Y'以结束程序）：").strip()
        if new_text.lower() == 'y':
            print("程序结束")
            break
        # 加载停用词列表
        file_path = "baidu_stopwords.txt"
        with open(file_path, mode='r', encoding='utf-8') as file:
            stop_words = set(file.read().splitlines())
        # 预测标签
        text = preprocess(new_text, stop_words)
        predicted_tags = predict_tags(text, vectorizer, mlb, model)
        if (len(predicted_tags[0]) > 0):
            for tag in predicted_tags[0]:
                print(tag)
        else:
            print("没有找到相关tag")

if __name__ == "__main__":
    main()