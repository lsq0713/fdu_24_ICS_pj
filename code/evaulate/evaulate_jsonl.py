import json
from collections import Counter
import math

def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line)

def extract_text(json_obj):
    return json_obj.get('title', '') + ' ' + json_obj.get('description', '')

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

# 读取 JSONL 文件并计算词频集中度
file_path = 'data.jsonl'
tokens = []
line_count = 0

for json_obj in read_jsonl(file_path):
    if line_count >= 1000:
        break
    text = extract_text(json_obj)
    tokens.extend(tokenize(text))
    line_count += 1

word_frequencies = calculate_word_frequencies(tokens)
gini_coefficient = calculate_gini_coefficient(word_frequencies)
entropy = calculate_entropy(word_frequencies)

print(f"Gini Coefficient: {gini_coefficient}")
print(f"Entropy: {entropy}")