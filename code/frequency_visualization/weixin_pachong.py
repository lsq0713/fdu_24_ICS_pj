import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 读取CSV文件
file_path1 = 'data/weixin/weixin_pachong.csv'
df1 = pd.read_csv(file_path1, encoding='utf-8')

# 提取 title 和 desc 列的数据
titles = df1['title'].astype(str).tolist()
descriptions = df1['desc'].astype(str).tolist()
sentences = titles + descriptions

# 读取停用词
stopwords_path = 'baidu_stopwords.txt'
stopwords = set()
with open(stopwords_path, 'r', encoding='utf-8') as file:
    for line in file:
        stopwords.add(line.strip())

# 将所有评论合并成一个字符串，并进行分词，同时过滤停用词
all_text = ''
for sentence in sentences:
    words = jieba.lcut(sentence)
    filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
    all_text += ' '.join(filtered_words) + ' '

# 生成词云
path = '/System/Library/Fonts/PingFang.ttc'  # 设置支持中文的字体路径
wordcloud = WordCloud(width=1600, height=1000, font_path=path,
                      background_color='white', regexp=r'\w{2,}').generate(all_text)
wordcloud.to_file('data/weixin/weixin_pachong.png')

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.show()