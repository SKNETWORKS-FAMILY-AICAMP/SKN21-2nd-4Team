# 모델훈련
## 데이터 로딩, 모델 저장

from model import MLPModel
import torch
import torch.optim as optim
from torch.utils.data import DataLoader

# 데이터셋 로딩 (가정: 전처리된 데이터를 DataLoader에 넘겨받음)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

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
