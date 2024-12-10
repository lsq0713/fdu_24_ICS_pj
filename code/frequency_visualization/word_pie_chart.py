import os
import matplotlib.pyplot as plt
frequency_path = '../../data/stackoverflow/word_count_output.txt'
with open(frequency_path,'r',encoding='utf-8')as file:
    lines = file.readlines()

word_and_count = []
for line in lines:
    word,count = line.strip().split(': ')
    word_and_count.append((word, int(count)))  # 将出现次数转换为整数

words, counts = zip(*word_and_count)  # 解压列表为两个单独的列表
words = words[:20]
counts = counts[:20]
# 绘制饼图
plt.pie(counts, labels=words, autopct='%1.1f%%', startangle=140)
 
# 添加标题
plt.title('Word Frequency Distribution')
 
# 显示图表
plt.show()
