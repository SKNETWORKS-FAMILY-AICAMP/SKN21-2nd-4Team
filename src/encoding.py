import pandas as pd
import os
import logging
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


# ----- 0) binary mapping ----
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


# ---- Logger Setup ----
def setup_logger():
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("Pipeline.log", mode='w'),
            logging.StreamHandler()
        ]
    )



# ---- 1) LabelEncoding ----
def label_encoding(df):
    le = LabelEncoder()

    for col in categorical_cols:
        if col in df.columns:

            #1-1) binary mapping
            df[col] = df[col].map(binary_mapping).fillna(df[col])
            df[col] = df[col].astype(str)
            df[col] = le.fit_transform(df[col])


            #1-2) object -> LabelEncoder
            if df[col].dtype == 'object':
                df[col] = le.fit_transform(df[col])

    return df

# ---- 2) OneHot Encoding ----
def one_hot(df):


    #binary mapping 
    for col in categorical_cols:
        if col in df.columns:
            df[col] =df[col].map(binary_mapping).fillna(df[col])
            df[col] = df[col].astype(str)

            # df = df.replace({True:1, False:0})  

    object_cols = [col for col in categorical_cols if col in df.columns and df[col].dtype == 'object']

    #OneHot    
    df = pd.get_dummies(df, columns=object_cols, drop_first=True, dtype=int)


    return df


# ---- processing file ----
def process_file(input_dir, output_dir):
    df = pd.read_csv(input_dir)


    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])

    base_name = os.path.basename(input_dir).replace(".csv","")


    # ---- LableEncoding File ----

    df_label = label_encoding(df.copy())
    save_label = os.path.join(output_dir, f"{base_name}_label.csv")
    df_label.to_csv(save_label, index=False)
    print(f"[Label]{save_label} 저장완료")


    # ---- OneHot File ----
    df_onehot = one_hot(df.copy())
    save_onehot = os.path.join(output_dir, f"{base_name}_onehot.csv")
    df_onehot.to_csv(save_onehot, index=False)
    print(f"[OneHot]{save_onehot} 저장완료")



# ---- all of file ----
def process_all_files(input_dir, output_dir):
    paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".csv")]

    os.makedirs(output_dir, exist_ok=True)

    for path in paths:
        process_file(path, output_dir)




# ---- RUN ----
if __name__ == "__main__":
    input_dir = 'data/interim'
    output_dir = 'data/processed'
    process_all_files(input_dir, output_dir)



