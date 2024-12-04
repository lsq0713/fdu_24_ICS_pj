import pandas as pd
from bs4 import BeautifulSoup

# 读取 CSV 文件
df = pd.read_csv('output.csv')

# 定义一个函数来去除 HTML 标签
def remove_html_tags(text):
    if isinstance(text, str):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()
    return text

# 应用函数到 DataFrame 中的每一列
for column in df.columns:
    df[column] = df[column].apply(remove_html_tags)

# 保存清理后的数据到新的 CSV 文件
df.to_csv('cleaned_file.csv', index=False)