import os
import numpy as np
import pandas as pd
import streamlit as st
import torch

from src.models.DL.utils import load_dl_model, transform_input_for_dl


# ---------------------------------------------------------
# 🔧 공통: 데이터셋 & 모델 로딩 함수 (캐시 사용)
# ---------------------------------------------------------
@st.cache_resource
def load_base_dataset():
    """
    딥러닝 학습에 사용한 전처리 데이터셋을 불러옵니다.
    (0-impute + label 인코딩 버전)
    """
    csv_path = "data/processed/Customer_Churn_Dataset_0_impute_label.csv"
    df_proc = pd.read_csv(csv_path)
    return df_proc


@st.cache_resource
def load_models():
    """
    - ML 모델(pkl)
    - DL 모델(pt)
    - DL 입력 피처 목록
    을 한 번만 로딩하고 캐싱합니다.
    """
    df_proc = load_base_dataset()

    # 숫자형 컬럼만 사용 (DL 학습 때와 동일한 방식)
    numeric = df_proc.select_dtypes(include=["float64", "int64"])
    feature_cols = [c for c in numeric.columns if c != "Churn"]

    # ----- 딥러닝 모델 로드 -----
    dl_model = None
    dl_model_path = "src/models/DL/final_dl_model_label.pt"

    try:
        dl_model = load_dl_model(
<<<<<<< HEAD
        model_path=dl_model_path,
        hidden_size=50,
        )

        dl_input_size = getattr(dl_model, "input_size", dl_model.fc1.in_features)
        if len(feature_cols) > dl_input_size:
            # 학습 당시에는 컬럼이 더 적었으므로, 앞에서부터 필요한 개수만 사용
            feature_cols = feature_cols[:dl_input_size]
            
=======
            model_path=dl_model_path,
            input_size=len(feature_cols),
            hidden_size=50,  # 학습 시 사용한 hidden_size와 동일하게
        )
>>>>>>> 735c6426bef8fea877d90f11dc16e2f34c6caa2a
    except Exception as e:
        st.warning(f"⚠ 딥러닝 모델 로드 실패: {e}")

    # ----- 머신러닝 모델 로드 -----
    ml_model = None
    ml_model_path = "src/models/ML/model_dir/LGBM_model.pkl"

    if os.path.exists(ml_model_path):
        try:
            import joblib

            ml_model = joblib.load(ml_model_path)
        except Exception as e:
            st.warning(f"⚠ ML 모델 로드 실패: {e}")
    else:
        # 파일 자체가 없을 때는 조용히 None 유지
        ml_model = None

    return ml_model, dl_model, feature_cols


# ---------------------------------------------------------
# 🧪 Streamlit 페이지 메인 함수
#   app.py 에서 run(df) 형태로 호출됨
# ---------------------------------------------------------
def run(df: pd.DataFrame):
    # 모델 및 피처 정보 로드
    ml_model, dl_model, feature_cols = load_models()

    # --------------------------------------------
    # 이 페이지 설명
    # --------------------------------------------
    st.markdown("## 🧪 신규/가상 유저 이탈 예측 (머신러닝·딥러닝)")

    st.markdown(
        """
        이 페이지에서는 **유저 정보를 직접 입력**하고,  
        입력값을 바탕으로 **머신러닝(ML) / 딥러닝(DL) 모델의 이탈 확률을 비교**합니다.  
        
        - ML 모델 파일: `src/models/ML/model_dir/LGBM_model.pkl`  
        - DL 모델 파일: `src/models/DL/final_dl_model_label.pt`  
        
        모델/전처리 파일이 아직 없다면, 해당 부분은 자동으로 *"모델 준비 중"*으로 표시됩니다.
        """
    )

    # --------------------------------------------
    # ✏ 고객 정보 입력 폼
    # --------------------------------------------
    with st.form("input_form"):
        st.markdown("### ✏ 유저 정보 입력 폼")

        col1, col2, col3 = st.columns(3)

        # 첫 번째 컬럼
        with col1:
            gender = st.selectbox("성별", ["Male", "Female"])
            senior = st.selectbox("SeniorCitizen", [0, 1])
            partner = st.selectbox("Partner", ["Yes", "No"])

        # 두 번째 컬럼
        with col2:
            dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.number_input("가입개월(tenure)", 0, 120, 12)

            internet = st.selectbox(
                "InternetService", df["InternetService"].unique().tolist()
            )

        # 세 번째 컬럼
        with col3:
            contract = st.selectbox("Contract", df["Contract"].unique().tolist())
            payment = st.selectbox(
                "PaymentMethod", df["PaymentMethod"].unique().tolist()
            )
            monthly = st.number_input("MonthlyCharges", 0.0, 200.0, 70.0)

        submitted = st.form_submit_button("🔮 이탈 확률 예측하기")

    if not submitted:
        return

    # --------------------------------------------
    # 📦 입력값 → DataFrame
    # --------------------------------------------
    user_input = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "InternetService": internet,
        "Contract": contract,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
    }
    user_df = pd.DataFrame([user_input])

    # --------------------------------------------
    # 🤖 머신러닝 예측 (있으면)
    # --------------------------------------------
    ml_prob = None  # 이탈 확률(0~1)

    if ml_model is not None and transform_input_for_ml is not None:
        try:
            # 전처리 함수가 user_df를 받아서 (1, n_features) ndarray로 반환한다고 가정
            X_ml = transform_input_for_ml(user_df)  # shape: (1, n_features)
            ml_prob = float(ml_model.predict_proba(X_ml)[0, 1])
        except Exception as e:
            st.warning(f"⚠ ML 예측 중 오류: {e}")
            ml_prob = None

    # --------------------------------------------
    # 🧠 딥러닝 예측 (있으면)
    # --------------------------------------------
    dl_prob = None

    if dl_model is not None and transform_input_for_dl is not None:
        try:
            # transform_input_for_dl도 (1, len(feature_cols)) ndarray를 반환한다고 가정
            X_dl = transform_input_for_dl(user_df, feature_cols)  # shape: (1, input_size)
            X_tensor = torch.tensor(X_dl, dtype=torch.float32)

            with torch.no_grad():
                logit = dl_model(X_tensor)
                dl_prob = float(torch.sigmoid(logit).item())
        except Exception as e:
            st.warning(f"⚠ DL 예측 중 오류: {e}")
            dl_prob = None

    # --------------------------------------------
    # 📉 예측 결과 영역
    # --------------------------------------------
    st.markdown("### 📉 예측 결과")

    col_ml, col_dl = st.columns(2)

    # 머신러닝 결과 표시
    with col_ml:
        st.markdown("#### 🤖 머신러닝 모델 예측")

        if ml_prob is not None:
            ml_text = f"{ml_prob * 100:.1f} %"
        else:
            ml_text = "모델 준비 중"

        st.metric("이탈 확률 (ML)", ml_text)
        st.caption(
            "※ ML 모델/전처리 파일(`src/models/ML/*`)이 준비되면 실제 값으로 표시됩니다."
        )

    # 딥러닝 결과 표시
    with col_dl:
        st.markdown("#### 🧠 딥러닝 모델 예측")

        if dl_prob is not None:
            dl_text = f"{dl_prob * 100:.1f} %"
        else:
            dl_text = "모델 준비 중"

        st.metric("이탈 확률 (DL)", dl_text)
        st.caption(
            "※ DL 모델 파일(`src/models/DL/final_dl_model_label.pt`)과 "
            "`transform_input_for_dl`이 준비되면 실제 값으로 표시됩니다."
        )

    # --------------------------------------------
    # ⚖ ML vs DL 성능 비교 요약 (검증 데이터 기준)
    # --------------------------------------------
    st.markdown("### ⚖ 모델 비교 요약 (검증 데이터 기준)")

    # 🔸 아래 metrics 값은 예시입니다.
    #     나중에 Colab에서 계산한 실제 성능지표를 그대로 넣어주면 됩니다.
    metrics = {
        "지표": ["Accuracy", "F1-score", "AUC"],
        "머신러닝(ML)": [0.84, 0.71, 0.80],
        "딥러닝(DL)": [0.84, 0.73, 0.84],
    }

    metrics_df = pd.DataFrame(metrics).set_index("지표")

    styled = (
        metrics_df.style.format({"머신러닝(ML)": "{:.2f}", "딥러닝(DL)": "{:.2f}"})
        .highlight_max(axis=1, color="#fff3cd")
    )

    st.dataframe(styled, use_container_width=True)

    st.markdown(
        """
        - 위 수치는 **검증/테스트 데이터**에서 측정한 성능입니다.  
        - 실제 값은 Colab에서 계산한 지표로 교체해 주세요.  
        - 전반적으로 더 성능이 좋은 모델을 **운영 기본 모델**로 사용하고,  
          나머지 모델은 비교/설명용으로 활용할 수 있습니다.
        """
    )
