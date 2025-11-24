import numpy as np
import torch
from .model import MLPModel


def load_dl_model(model_path, input_size, hidden_size=50):
    model = MLPModel(input_size=input_size, hidden_size=hidden_size, output_size=1)
    state = torch.load(model_path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    return model


def transform_input_for_dl(user_df, feature_cols):
    """
    Streamlit 입력값을 딥러닝 학습 때 사용한 feature_cols 순서에 맞는
    숫자 벡터로 변환.
    """
    df = user_df.copy()

    # gender
    df["gender"] = df["gender"].map({"Male": 1, "Female": 0})

    # Yes/No
    df["Partner"] = df["Partner"].map({"Yes": 1, "No": 0})
    df["Dependents"] = df["Dependents"].map({"Yes": 1, "No": 0})

    # InternetService
    df["InternetService"] = df["InternetService"].map({
        "DSL": 0, "Fiber optic": 1, "No": 2
    })

    # Contract
    df["Contract"] = df["Contract"].map({
        "Month-to-month": 0, "One year": 1, "Two year": 2
    })

    # PaymentMethod
    df["PaymentMethod"] = df["PaymentMethod"].map({
        "Electronic check": 0,
        "Mailed check": 1,
        "Bank transfer (automatic)": 2,
        "Credit card (automatic)": 3
    })

    # 숫자형만 남기기
    numeric = df.select_dtypes(include=["int64", "float64"])

    # feature_cols 기준으로 없는 컬럼은 0으로 채우고, 순서 맞추기
    for col in feature_cols:
        if col not in numeric.columns:
            numeric[col] = 0
    numeric = numeric[feature_cols]

    return numeric.values.astype(np.float32)
