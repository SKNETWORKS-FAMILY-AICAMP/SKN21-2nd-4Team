import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 현재 폴더를 path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # backend 상위(src) 폴더 추가


import pandas as pd
from toDB import get_connection

csv_path = '/Users/anhyebin/Documents/SKN21/SKN21-2nd-4Team/data/interim/Customer_Churn_Dataset_0_impute.csv'



# print(os.path.exists(csv_path))


def ChurnData(csv_path):
    df = pd.read_csv(csv_path)
    print(df.columns) 
    conn = get_connection()
    df = pd.read_csv(csv_path, names=['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 
                                    'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                                    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 
                                    'MonthlyCharges', 'TotalCharges', 'numAdminTickets', 'numTechTickets', 'Churn'], header=0, skiprows=1)

    curs = conn.cursor()
    insert_sql = """

    INSERT INTO ChurnData (
    customerID, gender, SeniorCitizen, Partner, Dependents, tenure,
    PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup,
    DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract,
    PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges,
    numAdminTickets, numTechTickets, Churn)
    VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s);
        """

    for _, row in df.iterrows():
        curs.execute(insert_sql, tuple(row))
        
    conn.commit()
    conn.close()



from insert_data import ChurnData

csv_path = '/Users/anhyebin/Documents/SKN21/SKN21-2nd-4Team/data/interim/Customer_Churn_Dataset_0_impute.csv'

if __name__ == "__main__":
    ChurnData(csv_path)