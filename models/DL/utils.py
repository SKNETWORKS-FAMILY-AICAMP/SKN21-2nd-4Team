import numpy as np
import pandas as pd
import torch

from .model import MLPModel


# ---------------------------------------------------
# 1) 딥러닝 모델 로드 (input_size 자동 추론)
# ---------------------------------------------------
def load_dl_model(model_path, hidden_size: int = 50):
    """
    저장된 딥러닝 모델(state_dict)을 로드하고,
    fc1.weight의 shape에서 input_size를 자동 추론한다.
    """
    state = torch.load(model_path, map_location="cpu")

    if "fc1.weight" not in state:
        raise ValueError("state_dict 안에 'fc1.weight'가 없습니다.")

    # fc1.weight : [hidden_size, input_size]
    input_size = state["fc1.weight"].shape[1]

    model = MLPModel(
        input_size=input_size,
        hidden_size=hidden_size,
        output_size=1,
    )
    model.load_state_dict(state)
    model.eval()

    # 나중에 page2에서 참조할 수 있도록 기록
    model.input_size = input_size
    return model


# ---------------------------------------------------
# 2) Streamlit 입력 → DL 입력 벡터 변환
# ---------------------------------------------------
def transform_input_for_dl(user_df: pd.DataFrame, feature_cols):
    """
    Streamlit에서 받은 입력값(user_df)을
    딥러닝 학습 때 사용한 feature_cols 순서에 맞는
    숫자 벡터(np.ndarray, shape=(1, input_size))로 변환한다.
    """
    df = user_df.copy()

    # -------------------------
    # 1) 범주형 → 숫자 매핑
    #    (학습 때 사용한 라벨 인코딩 규칙과 맞추는 것이 중요)
    # -------------------------
    # gender
    df["gender"] = df["gender"].map({"Male": 1, "Female": 0})

    # Yes/No
    df["Partner"] = df["Partner"].map({"Yes": 1, "No": 0})
    df["Dependents"] = df["Dependents"].map({"Yes": 1, "No": 0})

    # InternetService
    df["InternetService"] = df["InternetService"].map(
        {
            "DSL": 0,
            "Fiber optic": 1,
            "No": 2,
        }
    )

    # Contract
    df["Contract"] = df["Contract"].map(
        {
            "Month-to-month": 0,
            "One year": 1,
            "Two year": 2,
        }
    )

    # PaymentMethod
    df["PaymentMethod"] = df["PaymentMethod"].map(
        {
            "Electronic check": 0,
            "Mailed check": 1,
            "Bank transfer (automatic)": 2,
            "Credit card (automatic)": 3,
        }
    )

    # SeniorCitizen, tenure, MonthlyCharges 등은 이미 숫자이므로 그대로 둔다.

    # -------------------------
    # 2) 숫자형 컬럼만 추출
    # -------------------------
    numeric = df.select_dtypes(include=["int64", "float64", "float32"]).copy()

    # -------------------------
    # 3) feature_cols 기준으로 없는 컬럼은 0으로 채우고, 순서 맞추기
    # -------------------------
    for col in feature_cols:
        if col not in numeric.columns:
            numeric[col] = 0.0

    numeric = numeric[feature_cols]

    # (1, input_size) 형태로 반환
    return numeric.values.astype(np.float32)
