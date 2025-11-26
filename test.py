# #test.py
# #만든 파일, 함수 실행 test 파일


# # import logging
# # from src.models.encoding import process_all_files, setup_logger
# # import os



# # def main():
# #     setup_logger()

# #     input = "data/interim"
# #     output = "data/processed"

# #     os.makedirs(output, exist_ok=True)

# #     logging.info(f"Start processing files from {input} to {output}")

# #     try:
# #         process_all_files(input, output)
# #         logging.info("Processing completed successfully!")
# #     except Exception as e:
# #         logging.error(f"Processing failed: {e}")



# # if __name__ = "__main__":
# #     main()


# from src.backend.config import config
# from src.backend.insert_data import ChurnData

# csv_path = 'data/interim/Customer_Churn_Dataset_0_impute.csv'

# if __name__ == "__main__":
#     print("test")
#     ChurnData(csv_path)


import pandas as pd
from src.backend.toDB import get_connection

conn = get_connection()
df = pd.read_sql("SHOW TABLES", conn)
print("📌 SHOW TABLES 결과:")
print(df)

df2 = pd.read_sql("SELECT COUNT(*) AS CNT FROM customer_churn", conn)
print("\n📌 customer_churn row 수:")
print(df2)

df3 = pd.read_sql("SELECT * FROM customer_churn LIMIT 5", conn)
print("\n📌 LIMIT 5:")
print(df3)

df4 = pd.read_sql("SELECT * FROM customer_churn", conn)
print("\n📌 전체 데이터:")
print(df4.head(10))
