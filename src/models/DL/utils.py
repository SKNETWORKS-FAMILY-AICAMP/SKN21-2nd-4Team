# 데이터 로딩 / 모델 예측 및평가
import torch
from torch.utils.data import Dataset, DataLoader

# 데이터셋 클래스 정의
class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

def load_model(model, model_path):
    model.load_state_dict(torch.load(model_path))
    return model

def evaluate(model, test_loader):
    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            predicted = output.argmax(dim=1)
            correct += (predicted == target).sum().item()
            total += target.size(0)
    accuracy = 100 * correct / total
    print(f'Accuracy: {accuracy}%')
