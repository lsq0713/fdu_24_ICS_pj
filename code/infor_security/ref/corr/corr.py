import json
from collections import Counter, defaultdict
import numpy as np
from scipy.stats import pearsonr

def count_tags_frequency(jsonl_file):
    tag_counter = Counter()
    co_occurrence_matrix = defaultdict(Counter)
    
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            tags = data.get('Tags', '')
            if tags:
                tag_list = tags.strip('<>').split('><')
                tag_counter.update(tag_list)
                
                # Filter tags with frequency less than 200
                filtered_tags = [tag for tag in tag_list if tag_counter[tag] >= 200]
                
                # 统计共现矩阵
                for i, tag1 in enumerate(filtered_tags):
                    for j, tag2 in enumerate(filtered_tags):
                        if i != j:
                            co_occurrence_matrix[tag1][tag2] += 1

    
    return tag_counter, co_occurrence_matrix



def calculate_correlation_matrix(filtered_matrix, tag_counter):
    # Get the list of filtered tags
    filtered_tags = [tag for tag in tag_counter if tag_counter[tag] >= 100]
    
    # Create a numpy array for the co-occurrence matrix
    co_occurrence_array = np.zeros((len(filtered_tags), len(filtered_tags)))
    
    for i, tag1 in enumerate(filtered_tags):
        for j, tag2 in enumerate(filtered_tags):
            co_occurrence_array[i, j] = filtered_matrix[tag1][tag2]
    
    # Normalize the co-occurrence matrix
    row_sums = co_occurrence_array.sum(axis=1, keepdims=True)
    normalized_matrix = co_occurrence_array / row_sums
    
    # Calculate the Pearson correlation matrix
    correlation_matrix = np.corrcoef(normalized_matrix)
    
    return correlation_matrix, filtered_tags

if __name__ == "__main__":
    jsonl_file = 'cleaned_input_no_change_format.jsonl'  # 替换为你的文件路径
    
    print("Starting tag frequency and co-occurrence matrix calculation...")
    tag_frequency, co_occurrence_matrix = count_tags_frequency(jsonl_file)
    
    # Filter and shrink the co-occurrence matrix
    
    # Calculate the correlation matrix
    correlation_matrix, filtered_tags = calculate_correlation_matrix(co_occurrence_matrix, tag_frequency)
    
    # 将统计数据按频率排序后保存到文件
    sorted_tag_frequency = dict(tag_frequency.most_common())
    print("Tag frequency calculation completed.")
    
    # 将共现矩阵保存到文件
    with open('./corr/co_occurrence_matrix.json', 'w') as outfile:
        json.dump(co_occurrence_matrix, outfile, indent=4)
    print("Filtered and shrunk co-occurrence matrix saved to file.")
    
    # 将相关性矩阵保存到文件
    correlation_dict = {tag1: {tag2: correlation_matrix[i, j] for j, tag2 in enumerate(filtered_tags)} for i, tag1 in enumerate(filtered_tags)}
    with open('./corr/correlation_matrix.json', 'w') as outfile:
        json.dump(correlation_dict, outfile, indent=4)
    print("Correlation matrix saved to file.")
    
    # 打印统计数据
    print("Script execution completed successfully.")