import json

# 打开原始 JSONL 文件并读取内容
with open('test.jsonl', 'r') as jsonl_file:
    # 打开新的 JSONL 文件以写入数据
    with open('small_input.jsonl', 'w') as jsonl_output_file:
        
        # 逐行读取原始 JSONL 文件
        for line_num,line in enumerate(jsonl_file,start=1):
            data = json.loads(line)
            
            # 提取基本信息
            score = data['Score']
            title = data['Title']
            body = data['Body']
            tags = data['Tags']
            
            # 提取答案信息
            for answer in data['Answers']:
                answer_score = answer['Score']
                answer_body = answer['Body']
                
                # 创建一个字典来存储当前行的数据
                row = {
                    'Score': score,
                    'Title': title,
                    'Body': body,
                    'Tags': tags,
                    'Answer_Score': answer_score,
                    'Answer_Body': answer_body,
                    'Question_ID': line_num
                }
                
                # 将行数据转换为 JSON 字符串并写入新的 JSONL 文件
                jsonl_output_file.write(json.dumps(row) + '\n')