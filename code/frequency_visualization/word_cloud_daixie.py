
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud


frequency_path = '../../data/xhs/xiaohongshu_daixie_tag_counts.txt'
with open(frequency_path,'r',encoding='utf-8')as file:
    lines = file.readlines()

word_and_count = []
for line in lines:
    word,count = line.strip().split(': ')
    word_and_count.append((word, int(count)))  # 将出现次数转换为整数

# 将列表转换为字典，因为 generate_from_frequencies 需要一个字典作为输入
word_frequencies = dict(word_and_count)
# 生成词云对象
font_path = '/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf'  # 确保这个路径是正确的 
wordcloud = WordCloud(width=1600, height=1000, background_color='white', colormap='viridis',font_path=font_path)

wordcloud.generate_from_frequencies(word_frequencies)
wordcloud.to_file('../../data/xhs/xiaohongshu_daixie.png')

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.show()
