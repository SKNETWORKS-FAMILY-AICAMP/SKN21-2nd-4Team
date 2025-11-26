# from toDB import get_connection
# from config.config import DB_CONFIG
# from .config.config import DB_CONFIG
# from toDB import get_connection
import pandas as pd
from src.backend.toDB import get_connection
from src.backend.config.config import DB_CONFIG

def load_all_customers():
    conn = get_connection()
    test = pd.read_sql("SELECT * FROM customer_churn LIMIT 5;", conn)
    print(test)
    # print(pd.read_sql("SELECT * FROM customer_churn", conn))
    return pd.read_sql("SELECT * FROM customer_churn", conn)
