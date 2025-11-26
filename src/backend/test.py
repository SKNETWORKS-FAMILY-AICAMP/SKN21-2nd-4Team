import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # backend 폴더
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # src 폴더

from insert_data import ChurnData
from query_service import get_summary_stats

# csv_path = '../../data/processed/Customer_Churn_Dataset_knn.csv'
csv_path = 'C:\documents\Project\SKN21-2nd-4Team\data\processed\Customer_Churn_Dataset_knn.csv'

if __name__ == "__main__":
    ChurnData(csv_path)
    # get_summary_stats()
    

