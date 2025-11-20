# 모델훈련
## 데이터 로딩, 모델 저장

import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from model import MLPModel
import torch.optim as optim
import torch.nn as nn

# 데이터 불러오기
train_data = pd.read_csv('data/processed/Customer_Churn_Dataset_0_impute_baseline.csv')

# 숫자형 데이터만 선택
train_data_numeric = train_data.select_dtypes(include=['float64', 'int64'])

# 입력과 타깃 분리
X = train_data_numeric.drop('Churn', axis=1).values  # Churn 컬럼 제외
y = train_data_numeric['Churn'].values  # Churn 컬럼

# 데이터 전처리 (Tensor로 변환)
X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.float32)

# TensorDataset 사용하여 (data, target) 형태로 묶기
train_dataset = TensorDataset(X_tensor, y_tensor)

# DataLoader 설정
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 모델 초기화
model = MLPModel(input_size=10, hidden_size=50, output_size=1)

# 손실 함수와 옵티마이저 정의
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 모델 훈련
for epoch in range(10):
    for data, target in train_loader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

# 모델 저장
torch.save(model.state_dict(), 'models/DL/final_dl_model.pt')
