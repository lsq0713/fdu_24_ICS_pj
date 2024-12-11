# -*- coding: utf-8 -*-
import pandas as pd
from wordcloud import WordCloud
from collections import Counter

df = pd.read_csv("../../data/xhs/xhs_daixie.csv")

df['words1'] = df['title'].apply(lambda x: x.split())
df['words2'] = df['description'].apply(lambda x: x.split())

# 将所有分词结果合并为一个列表
words1 = [word for sublist in df['words1'] for word in sublist]
words2 = [word for sublist in df['words2'] for word in sublist]
all_words = words1 + words2

# 统计词频
word_counts = Counter(all_words)
d = dict(word_counts.most_common(500))

# 生成词云
path = "C:/Windows/Fonts/STKAITI.TTF"
wordcloud = WordCloud(width=1600, height=1000, background_color='white', 
                      font_path=path).generate_from_frequencies(d)
wordcloud.to_file('../../data/xhs/xhs_daixie_wordcloud.png')

