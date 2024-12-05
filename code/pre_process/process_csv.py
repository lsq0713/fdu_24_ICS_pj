import csv
import re
import jieba
from jieba import analyse

# 读取CSV文件
def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
    return rows

# 去除特殊格式
def remove_special_chars(text):
    return re.sub(r'[^\w\s]', '', text)

# 分词
def tokenize(text):
    return jieba.lcut(text)

# 加载停用词列表
def load_stop_words(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        stop_words = set(file.read().splitlines())
    return stop_words

# 去除停用词
def remove_stop_words(tokens, stop_words):
    return [word for word in tokens if word not in stop_words]

# 处理CSV文件
def process_csv(file_path, output_path, stop_words_path):
    rows = read_csv(file_path)
    stop_words = load_stop_words(stop_words_path)
    processed_rows = []

    for row in rows:
        # 去除特殊格式
        row['title'] = remove_special_chars(row['title'])
        row['description'] = remove_special_chars(row['description'])

        # 分词
        title_tokens = tokenize(row['title'])
        description_tokens = tokenize(row['description'])

        # 去除停用词
        title_tokens = remove_stop_words(title_tokens, stop_words)
        description_tokens = remove_stop_words(description_tokens, stop_words)

        # 将处理后的结果保存
        row['title'] = ' '.join(title_tokens)
        row['description'] = ' '.join(description_tokens)

        processed_rows.append(row)

    # 写入处理后的CSV文件
    with open(output_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(processed_rows)

# 主函数
if __name__ == "__main__":
    input_file = './data/xhs.csv'  # 输入的CSV文件路径
    output_file = 'output.csv'  # 输出的CSV文件路径
    stop_words_file = 'baidu_stopwords.txt'  # 停用词文件路径
    process_csv(input_file, output_file, stop_words_file)