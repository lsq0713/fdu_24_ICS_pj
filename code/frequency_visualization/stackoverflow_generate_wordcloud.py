# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from wordcloud import WordCloud
 
# 读取文件并解析数据
word_frequencies = {}
with open('../../data/stackoverflow/word_count_output.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 每行格式是 "词汇:频率"
        line = line.strip()
        if line:  # 确保行不为空
            word, freq = line.split(':')
            # 将频率转换为整数
            word_frequencies[word.strip()] = int(freq.strip())
 
# 生成词云对象
wordcloud = WordCloud(width=1600, height=1000, background_color='white', colormap='viridis').generate_from_frequencies(word_frequencies)
wordcloud.to_file('../../data/stackoverflow/stackoverflow_wordcloud_output.png')

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.show()
