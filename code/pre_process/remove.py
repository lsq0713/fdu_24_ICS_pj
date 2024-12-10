import csv

# 读取CSV文件
input_file = 'data/xhs/xhs_chengxuyuan.csv'
output_file = 'data/xhs/xhs_chengxuyuan_cleaned.csv'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        cleaned_row = []
        for cell in row:
            # 清理#后面的内容
            cleaned_cell = cell.split('#')[0].strip()
            cleaned_row.append(cleaned_cell)
        writer.writerow(cleaned_row)

print(f"Cleaned CSV saved to {output_file}")