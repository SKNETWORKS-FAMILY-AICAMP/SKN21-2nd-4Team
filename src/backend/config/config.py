import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# PROJECT_ROOT = Path(__file__).reslove().parent.parent.parent
# sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

# 이름, 비밀번호 설정 필요
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "1234"),
    "database": os.getenv("DB_NAME", "telco_churn"),
    "port": int(os.getenv("DB_PORT", 3306))
}

# 데이터 경로
DATA_PATH = {
    "RAW": "data/raw",
    "PROCESSED": "data/processed"
    
}

# 로깅 설정
LOG_CONFIG = {
    "level": "INFO",
    "format": "[%(asctime)s] %(levelname)s - %(message)s",
}

# Streamlit 관련
APP_CONFIG = {
    "title": "제목을 입력하세요",
    "page_icon": "📞",
    "database": os.getenv("DB_NAME", "telco_churn"),
    "port": os.getenv("DB_PORT", 3306)
}