import requests
from bs4 import BeautifulSoup
import csv

def fetch_page_content(page_number):
    url = f"https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E7%88%AC%E8%99%AB&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=2169&sst0=1733110676281&lkt=1%2C1733110676179%2C1733110676179&page={page_number}"
    
    headers = {
        "Host": "weixin.sogou.com",
        "Cookie": "ABTEST=0|1732514004|v1; SUID=4AEB78CA1252A20B00000000674410D4; IPLOC=CN3100; SUID=4AEB78CAB2A7A20B00000000674410D5; SUV=000B191ECA78EA4A674410D59912A562; SNUID=0B3BA81BD1D7F891E4A634E6D1E41C9E; ariaDefaultTheme=undefined",
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
    
    response = requests.get(url, headers=headers)
    return response.text

def parse_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('div', class_='txt-box')
    extracted_data = []

    for article in articles:
        title = article.find('h3').find('a').text.strip()
        summary = article.find('p', class_='txt-info').text.strip()
        source = article.find('div', class_='s-p').find('span', class_='all-time-y2').text.strip()  # 来源
        url = article.find('h3').find('a')['href']  # 提取 URL
        
        extracted_data.append([title, summary, source, url])

    return extracted_data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['标题', '简介', '来源', 'URL'])  # 写入表头
        writer.writerows(data)

def main():
    all_articles = []
    for page in range(1, 11):  # 爬取前 20 页
        print(f"正在爬取第 {page} 页...")
        html = fetch_page_content(page)
        articles = parse_content(html)
        all_articles.extend(articles)

    save_to_csv(all_articles, 'articles.csv')
    print("数据已保存到 articles.csv")

if __name__ == "__main__":
    main()