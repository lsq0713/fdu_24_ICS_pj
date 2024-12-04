import json
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# 读取数据
data = []
with open('nltk_body_title_tages_answer_output_processed_with_id.jsonl', 'r') as f:
    for line in f:
        data.append(json.loads(line))

# 提取'Body'和'Title'，并将它们合并为一个文本
texts = []
scores = []
for item in data:
    text = ' '.join(item['Title']) + ' ' + ' '.join(item['Body'])
    texts.append(text)
    scores.append(item['Score'])

# 将文本向量化
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
y = torch.tensor(scores, dtype=torch.float32)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 自定义数据集类
class SparseTextDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return torch.tensor(self.X[idx].toarray(), dtype=torch.float32), self.y[idx]

train_dataset = SparseTextDataset(X_train, y_train)
test_dataset = SparseTextDataset(X_test, y_test)

# 修改批次大小为16
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

class SimpleNN(nn.Module):
    def __init__(self, input_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

input_dim = X_train.shape[1]
model = SimpleNN(input_dim)
model = model.cuda()  # 将模型移动到GPU

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.05)

num_epochs = 8

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.cuda(), labels.cuda()  # 将数据移动到GPU
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs.squeeze(), labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader)}')

# 保存模型和TfidfVectorizer
torch.save(model.state_dict(), 'simple_nn_model.pth')
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# 保存原始数据的文本和向量表示
with open('original_data.pkl', 'wb') as f:
    pickle.dump((texts, X), f)

# 测试模型
model.eval()
with torch.no_grad():
    total_loss = 0.0
    for inputs, labels in test_loader:
        inputs, labels = inputs.cuda(), labels.cuda()
        outputs = model(inputs)
        loss = criterion(outputs.squeeze(), labels)
        total_loss += loss.item()

    print(f'Test Loss: {total_loss/len(test_loader)}')
    
with torch.no_grad():
    predictions = []
    true_labels = []
    for inputs, labels in test_loader:
        inputs, labels = inputs.cuda(), labels.cuda()
        outputs = model(inputs)
        predictions.extend(outputs.squeeze().cpu().numpy())
        true_labels.extend(labels.cpu().numpy())

mse = mean_squared_error(true_labels, predictions)
print(f'Mean Squared Error: {mse}')

# 加载保存的数据
with open('original_data.pkl', 'rb') as f:
    original_texts, original_vectors = pickle.load(f)

# 新数据预测和相似度计算
def predict_and_find_similar(new_text):
    # 对新数据进行TF-IDF向量化
    new_vector = vectorizer.transform([new_text])
    
    # 计算余弦相似度
    similarities = cosine_similarity(new_vector, original_vectors)
    
    # 找到最相似的原始数据
    most_similar_idx = similarities.argmax()
    most_similar_text = original_texts[most_similar_idx]
    
    # 输出最相似的原始数据
    print(f"Most similar original text: {most_similar_text}")
    
    # 预测新数据的分数
    new_vector_tensor = torch.tensor(new_vector.toarray(), dtype=torch.float32).cuda()
    prediction = model(new_vector_tensor).item()
    
    return prediction, most_similar_text

# 示例新数据
new_text = "This is a new text to predict and find similar original data."
prediction, most_similar_text = predict_and_find_similar(new_text)
print(f"Prediction for new text: {prediction}")
print(f"Most similar original text: {most_similar_text}")
