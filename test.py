#test.py
#만든 파일, 함수 실행 test 파일


# import logging
# from src.models.encoding import process_all_files, setup_logger
# import os



# def main():
#     setup_logger()

#     input = "data/interim"
#     output = "data/processed"

#     os.makedirs(output, exist_ok=True)

#     logging.info(f"Start processing files from {input} to {output}")

#     try:
#         process_all_files(input, output)
#         logging.info("Processing completed successfully!")
#     except Exception as e:
#         logging.error(f"Processing failed: {e}")



# if __name__ = "__main__":
#     main()


from src.backend.config import config
from src.backend.insert_data import ChurnData

csv_path = 'data/interim/Customer_Churn_Dataset_0_impute.csv'

if __name__ == "__main__":
    print("test")
    ChurnData(csv_path)