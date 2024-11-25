import http.client
import gzip
import io
from bs4 import BeautifulSoup

# 创建一个HTTP连接
conn = http.client.HTTPSConnection("mp.weixin.qq.com")

# 定义请求头
headers = {
    "Sec-Ch-Ua": '"Not:A-Brand";v="99", "Chromium";v="112"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close"
}

# 发送GET请求
conn.request("GET", "/s/jKiAPPuKLvVQZ8t5bVFGGQ", headers=headers) # 更改url可获取其他文章

# 获取响应
response = conn.getresponse()

# 读取响应数据
data = response.read()

# 检查响应头中的Content-Encoding
if response.getheader('Content-Encoding') == 'gzip':
    # 解压缩gzip数据
    buf = io.BytesIO(data)
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()

# 打印响应状态
print("状态:", response.status)

# 将响应数据保存为HTML文件
with open("response.html", "wb") as file:
    file.write(data)

print("响应数据已保存为 response.html")

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(data, 'html.parser')

# 去除一些无用标签
for script in soup(["script", "style", "head", "link", "img"]):
    script.decompose()  # 删除标签及其内容

# 获取清理后的HTML
cleaned_html = str(soup)

# 将清理后的HTML保存为文件
with open("cleaned_response.html", "w", encoding='utf-8') as file:
    file.write(cleaned_html)

print("清理后的响应数据已保存为 cleaned_response.html")

# 提取所有<p>标签中的文本
paragraphs = soup.find_all('p')
text_content = "\n".join([p.get_text() for p in paragraphs])

# 将提取的文本保存为文件
with open("paragraphs.txt", "w", encoding='utf-8') as file:
    file.write(text_content)

print("提取的<p>标签文本已保存为 paragraphs.txt")

# 关闭连接
conn.close()