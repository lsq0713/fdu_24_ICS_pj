import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import random

# 设置 headers，模拟浏览器
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding' : 'gzip, deflate, br, zstd',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Referer' : 'https://www.zhihu.com/question/38915323',
        'Sec-Ch-Ua' : '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-Ch-Ua-Mobile' : '?0',
        'Sec-Ch-Ua-Platform' : '"Windows"',
        'Sec-Fetch-Dest' : 'empty',
        'Sec-Fetch-Mode' : 'cors',
        'Sec-Fetch-Site' : 'same-origin',      
        'X-Requested-With' : 'fetch'
}

cookies = { 
    # 填写自己的session_id;BEC和_xsrf等
    'session_id' : '',
    'BEC' : '',
    '_xsrf' : '',
}
# 填自己的z_0 cookie
    
df = pd.DataFrame()
# df有三列，answer_id和content以及创建日期
df['answer_id'] = []
df['content'] = []
df['created_time'] = []

# 目标问题的 ID
question_id = 38915323

answer_ids = []

# 初始请求 URL，带上分页参数
base_url = 'https://www.zhihu.com/api/v4/questions/38915323/feeds?cursor={}&include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled&limit=5&{offset}&order=default&platform=desktop&session_id={}&ws_qiangzhisafe=1'
# 上述url中删去的 cursor = {} 和 session_id = {}填入自己的即可

# 抓包发现最后通过检查是否有参数 ： ws&qiangzhisafe=1 判断是否为安全请求

url0 = base_url.format(offset=0)

resp0 = requests.get(url0, headers=headers,cookies=cookies)
for data in resp0.json()['data']:
        answer_id = data['target']['id']
        # 添加answer_id到df中
        answer_ids.append(answer_id)
next = resp0.json()['paging']['next']

for page in range(1,400):# 每页是5条数据  根据总回答数，估计一下多少页即可
    #对第page页进行访问
    resp = requests.get(next, headers=headers,cookies=cookies)
    print('正在爬取第' + str(page) + '页')
    
    for data in resp.json()['data']:
        answer_id = data['target']['id']
        # 添加answer_id到df中
        answer_ids.append(answer_id)
    next = resp.json()['paging']['next']
    time.sleep(3) # 这里是情况可快可慢
    
# 将answer_ids写入df
df['answer_id'] = answer_ids
df.to_csv('answer_id.csv', index=True)

contents = []

batch = 0
for answer_id in answer_ids:
    print('正在爬取answer_id为{answer_id}的数据'.format(answer_id=answer_id))
    url = 'https://www.zhihu.com/question/38915323/answer/{answer_id}'.format(answer_id=answer_id)
    try:
        resp = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 查找content
        content = soup.find('div', class_='RichContent-inner').text
        contents.append(content)
        print(content)
    except Exception as e:
        print(f'爬取answer_id为{answer_id}的数据时出现异常：{e}')
        break
    
    time.sleep(random.randint(1,4))

    # 每爬取1000个回答就保存一次数据,保存在不同的文件中
    if len(contents) % 1000 == 0:
        new_data = {'answer_id': answer_ids[:len(contents)], 'content': contents}
        new_df = pd.DataFrame(new_data)
        new_df.to_csv(f'text_{batch}.csv', index=True)
        batch += 1
#汇总一下 避免爬取被断数据丢失
new_data = {'answer_id': answer_ids[:len(contents)], 'content': contents}
new_df = new_df.append(pd.DataFrame(new_data))
new_df.to_csv('text1.csv', index=True)


