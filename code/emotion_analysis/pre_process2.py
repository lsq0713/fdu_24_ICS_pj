import pandas as pd
import re
read_file_path = '../../data/stackoverflow/data.csv'
df = pd.read_csv(read_file_path)

# 定义一个函数来提取中文文本
def extract_chinese(text):
    if isinstance(text, str):
        # 使用正则表达式匹配中文字符
        chinese_text = re.findall(r'[\u4e00-\u9fff]+', text)
        # 将匹配到的中文字符拼接成字符串
        return ''.join(chinese_text)
    return None

# 应用函数到CSV文件的文本列
df['chinese_text'] = df['description'].apply(extract_chinese)
df = df.dropna(subset=['chinese_text'])
chinese_df = df[['chinese_text']]
chinese_df = chinese_df[chinese_df['chinese_text'].apply(lambda x: isinstance(x, str) and x.strip() != '')]
output_filename = '../../data/new_chinese_text.csv'
chinese_df.to_csv(output_filename, index=False, encoding='utf-8-sig')

