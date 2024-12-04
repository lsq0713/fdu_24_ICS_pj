import json

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            # 将 tags 字段从字符串转换为列表
            data['tags'] = json.loads(data['tags'])
            # 将处理后的数据写入到输出文件
            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

# 使用示例
input_file = 'input.jsonl'
output_file = 'output.jsonl'
process_jsonl(input_file, output_file)