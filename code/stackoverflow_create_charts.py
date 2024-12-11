# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
 
def plot_sorted_data(df, column_name, file_name, log_flag):
    # 按照指定列降序排列
    sorted_df = df.sort_values(by=column_name, ascending=False)
    
    # 提取指定列为一个数组
    data_array = sorted_df[column_name].values
    
    x = list(range(len(data_array)))
    
    # 画出折线图
    plt.figure(figsize=(10, 6))
    plt.plot(x, data_array, marker=',')
    
    # 添加标题和标签
    title = f'{column_name.capitalize()} in Descending Order'
    if log_flag == 1:
        title += ' (log)'
    plt.title(title)
    plt.xlabel('Index')
    plt.ylabel(column_name.capitalize())
    
    # 根据列名设置y轴的对数刻度
    if log_flag == 1:
        plt.yscale('log')
    
    plt.grid(True)  # 显示网格线
    
    # 保存图像
    plt.savefig(file_name, format='jpg')
    plt.close()
 
def main():
    # 读取CSV文件
    csv_file_path = '../data/stackoverflow/data.csv'
    df = pd.read_csv(csv_file_path)
    
    # 绘制'answers'的折线图
    plot_sorted_data(df, 'answers', '../data/stackoverflow/chart_answers.jpg', 0)
    
    # 绘制'views'的折线图
    plot_sorted_data(df, 'views', '../data/stackoverflow/chart_views.jpg', 0)
    plot_sorted_data(df, 'views', '../data/stackoverflow/chart_views_log.jpg', 1)
 
if __name__ == "__main__":
    main()
