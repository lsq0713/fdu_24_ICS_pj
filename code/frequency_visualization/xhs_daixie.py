import pandas as pd
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# # 读取CSV文件
# file_path1 = 'data/xhs/xhs_daixie.csv'
# df1 = pd.read_csv(file_path1, encoding='utf-8')

# # 提取 title 和 desc 列的数据
# titles = df1['title'].astype(str).tolist()
# descriptions = df1['description'].astype(str).tolist()
# sentences = titles + descriptions

# # 读取停用词
# stopwords_path = 'baidu_stopwords.txt'
# stopwords = set()
# with open(stopwords_path, 'r', encoding='utf-8') as file:
#     for line in file:
#         stopwords.add(line.strip())

# # 将所有评论合并成一个字符串，并进行分词，同时过滤停用词
# all_words = []
# for sentence in sentences:
#     words = jieba.lcut(sentence)
#     filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
#     all_words.extend(filtered_words)

# # 统计词频
# word_counts = Counter(all_words)

# # 将词频结果保存到CSV文件
# # 将词频结果保存到TXT文件
# with open('data/xhs/daixie_word_frequency.txt', 'w', encoding='utf-8') as file:
#     for word, freq in sorted(word_counts.items(), key=lambda item: item[1], reverse=True):
#         file.write(f"{word},{freq}\n")

# print("词频统计完成，结果已保存到 data/xhs/pachong_word_frequency.txt")



 
# 读取文件并解析数据
word_frequencies = {}
with open('data/xhs/daixie_word_frequency.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 每行格式是 "词汇:频率"
        line = line.strip()
        if line:  # 确保行不为空
            word, freq = line.split(',')
            # 将频率转换为整数
            word_frequencies[word.strip()] = int(freq.strip())
 
# 生成词云对象
path = '/System/Library/Fonts/PingFang.ttc'  # 设置支持中文的字体路径
wordcloud = WordCloud(width=1600, height=1000, font_path=path,
                      background_color='white', regexp=r'\w{2,}').generate_from_frequencies(word_frequencies)
wordcloud.to_file('data/xhs/xhs_daixie.png')

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.show()
