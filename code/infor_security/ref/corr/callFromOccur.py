import json
import numpy as np
from scipy.stats import pearsonr

# 读取JSON文件
def load_cooccurrence_matrix(file_path):
    with open(file_path, 'r') as file:
        cooccurrence_matrix = json.load(file)
    return cooccurrence_matrix

# 计算皮尔逊相关系数
def calculate_pearson_correlation(matrix):
    items = list(matrix.keys())
    n = len(items)
    correlation_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            item1 = items[i]
            item2 = items[j]
            values1 = list(matrix[item1].values())
            values2 = list(matrix[item2].values())
            corr, _ = pearsonr(values1, values2)
            correlation_matrix[i, j] = corr
    
    return correlation_matrix, items

# 保存相关矩阵为JSON文件
def save_correlation_matrix_to_json(correlation_matrix, items, file_path):
    correlation_dict = {}
    for i, item1 in enumerate(items):
        correlation_dict[item1] = {}
        for j, item2 in enumerate(items):
            correlation_dict[item1][item2] = float(correlation_matrix[i, j])
    
    with open(file_path, 'w') as file:
        json.dump(correlation_dict, file, indent=4)

# 主函数
def main():
    file_path = './corr/co_occurrence_matrix.json'  # 替换为你的JSON文件路径
    cooccurrence_matrix = load_cooccurrence_matrix(file_path)
    
    correlation_matrix, items = calculate_pearson_correlation(cooccurrence_matrix)
    
    # 保存相关矩阵为JSON文件
    output_file_path = './corr/correlation_matrix_output.json'  # 替换为你想保存的文件路径
    save_correlation_matrix_to_json(correlation_matrix, items, output_file_path)
    
    # 打印相关矩阵
    print("Items:", items)
    print("Correlation Matrix:")
    print(correlation_matrix)

if __name__ == "__main__":
    main()