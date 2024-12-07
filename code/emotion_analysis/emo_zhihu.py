import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np

read_file_path = '../../data/zhihu/zhihu.csv'
df = pd.read_csv(read_file_path)
# 创建一个新列来存储情感分析结果

df['sentiment'] = df['description'].apply(lambda x: SnowNLP(x).sentiments)
# SnowNLP的sentiments方法返回一个介于0和1之间的浮点数，表示正面情感的概率
# 设置一个阈值来判断是正面还是负面情感
threshold = 0.5
df['sentiment_label'] = df['sentiment'].apply(lambda x: 'positive' if x >= threshold else 'negative')
output_filename = '../../data/zhihu/emo_zhihu.csv'
# 输出结果到新的CSV文件
df.to_csv(output_filename, index=False, encoding='utf-8-sig')

df['sentiment'] = pd.to_numeric(df['sentiment'], errors='coerce')
df = df.dropna(subset=['sentiment'])
# 创建一个新的列来表示分组
bins = np.arange(0, 1.1, 0.1)  # 创建从0到1（包含1但不包含1.1）的间隔为0.1的数组
df['sentiment_bin'] = pd.cut(df['sentiment'], bins=bins, labels=bins[:-1], right=False)

sentiment_counts = df['sentiment_bin'].value_counts().sort_index()
formatted_indices = ['{:.1f}'.format(idx) for idx in sentiment_counts.index]
# 绘制柱状图
plt.figure(figsize=(10, 6))  # 设置图形大小
plt.bar(formatted_indices, sentiment_counts.values, color='skyblue')  # 绘制柱状图
plt.xlabel('Sentiment Score (0.1 Intervals)')  # 设置x轴标签
plt.ylabel('Number of Occurrences')  # 设置y轴标签
plt.title('Sentiment Distribution by 0.1 Intervals')  # 设置图表标题
plt.xticks(rotation=45)  # 旋转x轴标签以便更好地显示
plt.grid(axis='y', linestyle='--', alpha=0.7)  # 添加y轴网格线
plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域
plt.show()  # 显示图表
