import pymysql
from pymysql.cursors import DictCursor
from src.backend.config.config import DB_CONFIG
import streamlit as st

# import os
# import sys

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)


# MySQL DB 연결 객체를 반환


# print(DB_CONFIG)
@st.cache_resource
def get_connection():
    try:
        # print(DB_CONFIG)
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"],
            # cursorclass=DictCursor,
            charset="utf8mb4"
        )
        return conn
    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")


