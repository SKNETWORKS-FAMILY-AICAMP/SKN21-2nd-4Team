# 모델훈련
## 데이터 로딩, 모델 저장

import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from model import MLPModel
import torch.optim as optim
import torch.nn as nn
from sklearn.model_selection import train_test_split

# 1) 데이터 불러오기  (label 인코딩 버전)
train_data = pd.read_csv('data/processed/Customer_Churn_Dataset_label.csv')

# 2) 숫자형 컬럼만 사용
train_data_numeric = train_data.select_dtypes(include=['float64', 'int64'])

# 3) 입력 / 타깃 분리
X = train_data_numeric.drop('Churn', axis=1).values   # Churn 제외
y = train_data_numeric['Churn'].values                # 0/1 레이블

# 4) train / test 분리  (Colab에서 하신 것 반영)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5) Tensor로 변환 (레이블은 (N,1) 모양으로)
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

X_test_tensor  = torch.tensor(X_test,  dtype=torch.float32)
y_test_tensor  = torch.tensor(y_test,  dtype=torch.float32).view(-1, 1)

# TensorDataset & DataLoader (train만 사용)
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader  = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 6) 모델 초기화  (입력 차원 자동 반영)
input_size = X_train_tensor.shape[1]
model = MLPModel(input_size=input_size, hidden_size=50, output_size=1)

# 7) 손실 함수 / 옵티마이저  (이진 분류용)
criterion = nn.BCEWithLogitsLoss()        # ★ MSE → BCEWithLogits
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# 8) 학습 루프
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    for data, target in train_loader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch {epoch+1}, Loss: {loss.item():.4f}')

# 9) 모델 저장 (label 버전 이름으로)
torch.save(model.state_dict(), 'models/DL/final_dl_model_label.pt')
