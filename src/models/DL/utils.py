import numpy as np
import pandas as pd
import torch
from .model import MLPModel

# ---------------------------------------------------
# 1) 딥러닝 모델 로드 (input_size 자동 추론)
# ---------------------------------------------------
def load_dl_model(model_path, hidden_size=50):
    """
    저장된 딥러닝 모델(state_dict)을 로드하고,
    저장된 fc1.weight 크기에서 input_size를 자동 추론한다.
    """
    state = torch.load(model_path, map_location="cpu")

    if "fc1.weight" not in state:
        raise ValueError("state_dict 안에 fc1.weight가 없습니다.")

    input_size = state["fc1.weight"].shape[1]  # ex) 20

    model = MLPModel(
        input_size=input_size,
        hidden_size=hidden_size,
        output_size=1
    )

    model.load_state_dict(state)
    model.eval()

    model.input_size = input_size
    return model


# ---------------------------------------------------
# 2) 학습 데이터 템플릿 준비
# ---------------------------------------------------
_BASE_NUMERIC = None
_BASE_FEATURE_COLS = None

def _load_base_numeric():
    """
    학습 데이터(라벨 인코딩된 버전)의 숫자형 템플릿 1행을 준비한다.
    """
    global _BASE_NUMERIC, _BASE_FEATURE_COLS

    if _BASE_NUMERIC is not None:
        return

    df = pd.read_csv("data/processed/Customer_Churn_Dataset_0_impute_label.csv")
    numeric = df.select_dtypes(include=["float64", "int64"])
    feature_cols = [c for c in numeric.columns if c != "Churn"]

    _BASE_NUMERIC = numeric
    _BASE_FEATURE_COLS = feature_cols


# ---------------------------------------------------
# 3) Streamlit → DL 입력 벡터 변환
# ---------------------------------------------------
def transform_input_for_dl(user_df, feature_cols):
    """
    Streamlit 입력 9개 → DL 학습 입력(feature_cols) 형태로 변환
    - 템플릿(학습 데이터 첫 행)을 기본값으로 사용
    - 사용자가 입력한 값만 덮어쓰기
    """

    _load_base_numeric()

    base = _BASE_NUMERIC.iloc[0].copy()       # 학습 데이터 기반 템플릿 행
    cols = _BASE_FEATURE_COLS                 # 전체 feature_cols

    # -------------------------
    # 1) 사용자 입력 라벨 인코딩
    # -------------------------
    df = user_df.copy()

    df["gender"] = df["gender"].map({"Male": 1, "Female": 0})
    df["Partner"] = df["Partner"].map({"Yes": 1, "No": 0})
    df["Dependents"] = df["Dependents"].map({"Yes": 1, "No": 0})

    df["InternetService"] = df["InternetService"].map({
        "DSL": 0, "Fiber optic": 1, "No": 2
    })

    df["Contract"] = df["Contract"].map({
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2
    })

    df["PaymentMethod"] = df["PaymentMethod"].map({
        "Electronic check": 0,
        "Mailed check": 1,
        "Bank transfer (automatic)": 2,
        "Credit card (automatic)": 3
    })

    # 숫자 컬럼 (tenure, SeniorCitizen, MonthlyCharges 등)
    row_in = df.iloc[0]

    # -------------------------
    # 2) 템플릿 행 위에 사용자 값 덮어쓰기
    # -------------------------
    for col in row_in.index:
        if col in base.index and pd.notnull(row_in[col]):
            base[col] = row_in[col]

    # -------------------------
    # 3) 최종 feature_cols 순서대로 정렬하여 반환
    # -------------------------
    final_cols = feature_cols
    x = base[final_cols].values.astype(np.float32).reshape(1, -1)
    return x
