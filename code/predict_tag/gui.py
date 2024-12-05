import joblib
import re
import jieba
from jieba import analyse
import tkinter as tk
from tkinter import messagebox

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
        messagebox.showinfo("模型加载", "已加载现有模型")
    except FileNotFoundError:
        messagebox.showerror("模型加载", "未找到现有模型，请联系管理员训练模型")
        return

    # 创建主窗口
    root = tk.Tk()
    root.title("标签预测")

    # 创建输入框
    input_label = tk.Label(root, text="请输入需要预测的文本：")
    input_label.pack(pady=10)
    input_entry = tk.Entry(root, width=50)
    input_entry.pack(pady=10)

    # 创建预测按钮
    def on_predict():
        new_text = input_entry.get().strip()
        if new_text.lower() == 'y':
            root.destroy()
            return
        # 加载停用词列表
        file_path = "./workspace/baidu_stopwords.txt"
        with open(file_path, mode='r', encoding='utf-8') as file:
            stop_words = set(file.read().splitlines())
        # 预测标签
        text = preprocess(new_text, stop_words)
        predicted_tags = predict_tags(text, vectorizer, mlb, model)
        if len(predicted_tags[0]) > 0:
            tags_str = "\n".join(predicted_tags[0])
            messagebox.showinfo("预测结果", f"预测的标签为：\n{tags_str}")
        else:
            messagebox.showinfo("预测结果", "没有找到相关tag")

    predict_button = tk.Button(root, text="预测", command=on_predict)
    predict_button.pack(pady=10)

    # 创建退出按钮
    def on_exit():
        root.destroy()

    exit_button = tk.Button(root, text="退出", command=on_exit)
    exit_button.pack(pady=10)

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()