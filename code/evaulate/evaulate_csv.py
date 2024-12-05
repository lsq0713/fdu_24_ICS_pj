import csv
from collections import Counter
import math

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            yield row

def extract_text(csv_row):
    return csv_row[0] + ' ' + csv_row[1]

def tokenize(text):
    return text.split()

def calculate_word_frequencies(tokens):
    return Counter(tokens)

def calculate_gini_coefficient(frequencies):
    total_words = sum(frequencies.values())
    sorted_freqs = sorted(frequencies.values())
    cum_freqs = [sum(sorted_freqs[:i+1]) for i in range(len(sorted_freqs))]
    n = len(sorted_freqs)
    gini_sum = sum((2 * i - n + 1) * sorted_freqs[i] for i in range(n))
    return gini_sum / (n * total_words)

def calculate_entropy(frequencies):
    total_words = sum(frequencies.values())
    entropy = -sum((freq / total_words) * math.log2(freq / total_words) for freq in frequencies.values() if freq > 0)
    return entropy

# 读取 CSV 文件并计算词频集中度
file_path = './data/weixin.csv'
tokens = []
line_count = 0

for csv_row in read_csv(file_path):
    if line_count >= 1000:
        break
    text = extract_text(csv_row)
    tokens.extend(tokenize(text))
    line_count += 1

word_frequencies = calculate_word_frequencies(tokens)
gini_coefficient = calculate_gini_coefficient(word_frequencies)
entropy = calculate_entropy(word_frequencies)

print(f"Gini Coefficient: {gini_coefficient}")
print(f"Entropy: {entropy}")