import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 读取CSV文件
file_path1 = '../../zhihu_data/程序代写+代写程序/search_comments.csv'
file_path2 = '../../zhihu_data/程序代写+代写程序/search_contents.csv'
df1 = pd.read_csv(file_path1, encoding='utf-8', header=None)
df2 = pd.read_csv(file_path2, encoding='utf-8', header=None)

comments = df1[0].astype(str).tolist()
contents = df2[0].astype(str).tolist()
sentences = comments + contents

stopwords_path = '../../baidu_stopwords.txt'
stopwords = set()
with open(stopwords_path, 'r', encoding='utf-8') as file:
    for line in file:
        stopwords.add(line.strip())
 
# 将所有评论合并成一个字符串，并进行分词，同时过滤停用词
all_text = ''
for sentence in sentences:
    words = jieba.lcut(sentence)
    filtered_words = [word for word in words if word not in stopwords]
    all_text += ' '.join(filtered_words) + ' '
 
# 生成词云
path = 'C:/Windows/Fonts/STKAITI.TTF' # 设置支持中文的字体路径
wordcloud = WordCloud(width=1600, height=1000, font_path=path,
                      background_color='white').generate(all_text)
wordcloud.to_file('../../data/zhihu/program_ghostwriting_wordcloud.png')

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.show()
