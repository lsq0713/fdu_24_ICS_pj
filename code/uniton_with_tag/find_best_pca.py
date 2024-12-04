import numpy as np
from sklearn.decomposition import PCA

# 读取txt文件并解析数据
data = []
with open('filtered_file_updated_tag_count.txt', 'r', encoding='utf-8') as file:
    for line in file:
        value = int(line.split(': ')[1])
        data.append([value])

print("原始数据:", data)
data = np.array(data)

# 检查数据的维度
if data.shape[1] == 1:
    print("数据是一维的，PCA无法进一步降维。")
else:
    # 创建PCA对象
    pca = PCA()

    # 拟合数据
    pca.fit(data)

    # 查看每个主成分解释的方差比例
    explained_variance_ratio = pca.explained_variance_ratio_

    # 计算累积方差解释比例
    cumulative_explained_variance = np.cumsum(explained_variance_ratio)

    # 打印结果
    print("每个主成分解释的方差比例:", explained_variance_ratio)
    print("累积方差解释比例:", cumulative_explained_variance)

    # 选择累积方差解释比例达到某个阈值（例如95%）的维度
    threshold = 0.95
    n_components = np.argmax(cumulative_explained_variance >= threshold) + 1

    print(f"应该降到 {n_components} 维以保留 {threshold*100}% 的方差。")

    # 打印每个主成分的方差
    print("每个主成分的方差:", pca.explained_variance_)