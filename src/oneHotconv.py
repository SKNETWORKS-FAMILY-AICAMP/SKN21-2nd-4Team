import pandas as pd
from sklearn.preprocessing import OneHotEncoder



def one_hot(df):
    categorical_cols = [
        'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 
        'PaperlessBilling', 'PaymentMethod', 'Churn'
    ]

    binary_mapping = {
        'Yes': 1,
        'No': 0,
        'Male': 1,
        'Female': 0
    }

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