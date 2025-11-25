import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # backend 폴더
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # src 폴더

from insert_data import ChurnData

csv_path = '../../data/interim/Customer_Churn_Dataset_0_impute.csv'

if __name__ == "__main__":
    ChurnData(csv_path)

