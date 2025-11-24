import pandas as pd
import os
#from sklearn.preprocessing import LabelEncoder


# ----- binary mapping ----
binary_mapping = {
    'Yes': 1,
    'No': 0,
    'Male': 1,
    'Female': 0
}


# ----- categorical column list ----
categorical_cols = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 
    'PaperlessBilling', 'PaymentMethod', 'Churn'
]



# ---- file processing ----
def process_file(input_path, output_path):
    df = pd.read_csv(input_path)


    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])


    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].map(binary_mapping).fillna(df[col])

        
    file_name = os.path.basename(input_path).replace(".csv", "_baseline.csv")
    save_path = os.path.join(output_path, file_name)


    df.to_csv(save_path, index=False)
    print(f"{save_path} 저장 완료")


# ---- data path ----
def process_all_files(input_dir, output_dir):

    #input_dir
    paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".csv")]

    #output_dir
    os.makedirs(output_dir, exist_ok=True)

    for path in paths:
        process_file(path, output_dir)





# ---- RUN ----
if __name__ == "__main__":
    input_dir = 'data/raw'
    output_dir = "data/processed"
    process_all_files(input_dir, output_dir)

