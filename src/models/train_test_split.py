import pandas as pd
import os
from sklearn.model_selection import train_test_split


# --- 설정 ---
input_file = "/Users/anhyebin/Documents/SKN21/SKN21-2nd-4Team/data/processed/Customer_Churn_Dataset_0_impute_label.csv"
output_dir = "data/split"
os.makedirs(output_dir, exist_ok=True)

# --- train_test_split  ---
df = pd.read_csv(input_file)

# feature / label split
X = df.drop(columns=['Churn'])
y = df['Churn']

# train/test split (stratify=y ->  class 비율 유지)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


base_name = os.path.basename(input_file).replace(".csv", "")

# CSV 저장
X_train.to_csv(os.path.join(output_dir, f"{base_name}_X_train.csv"), index=False)
X_test.to_csv(os.path.join(output_dir, f"{base_name}_X_test.csv"), index=False)
y_train.to_csv(os.path.join(output_dir, f"{base_name}_y_train.csv"), index=False)
y_test.to_csv(os.path.join(output_dir, f"{base_name}_y_test.csv"), index=False)

print(f"{base_name} split 완료 -> CSV 저장됨")
