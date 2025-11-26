import os
import numpy as np
import pandas as pd
import streamlit as st
import joblib
from src.oneHotconv import one_hot


# ---------------------------------------------------------
# 🔥 1) XGB Pipeline 모델 로드 (전처리 포함)
# ---------------------------------------------------------
# 모델 전체가 Pipeline이므로, 전처리 단계(원핫/스케일링) 포함됨
# ml_model = joblib.load("src/models/ML/XGB_model.pkl")
# ml_model = joblib.load("models/ML/XGB_model.pkl")

# ---------------------------------------------------------
# 🧪 Streamlit 페이지 메인 함수 (app.py → run(df) 로 호출)
# ---------------------------------------------------------
def run(df: pd.DataFrame):

    # --------------------------------------------
    # 페이지 설명
    # --------------------------------------------
    st.markdown("## 🧪 신규 유저 이탈 예측")

    st.markdown(
        """
        이 페이지는 **고객 정보를 입력하면 XGBoost 모델이 자동으로 전처리 후 이탈 확률을 산출합니다.**
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

        phoneservice = 'No'
        multiplelines = 'No phone service'
        onlinesecurity = 'No phone service'
        onlinebackup = 'No phone service'
        deviceprotection = 'No phone service'
        techsupport = 'No phone service'
        streamingTV = 'No phone service'
        streamingmovies = 'No phone service'
        paperlessbilling = 'No'
        totalcharges = tenure * monthly
        numadmintickets = 0
        numtechtickets = 0

    if not submitted:
        return

    # --------------------------------------------
    # 📦 입력값 → DataFrame
    # (Pipeline은 RAW 형태로 받아도 됨)
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
        'PhoneService': phoneservice,
        'MultipleLines': multiplelines,
        'OnlineSecurity': onlinesecurity,
        'OnlineBackup': onlinebackup,
        'DeviceProtection': deviceprotection,
        'TechSupport': techsupport,
        'StreamingTV': streamingTV,
        'StreamingMovies': streamingmovies,
        'PaperlessBilling':paperlessbilling,
        'TotalCharges':totalcharges,
        'numAdminTickets':numadmintickets,
        'numTechTickets':numtechtickets
    }
    user_df = pd.DataFrame([user_input])
    conv = one_hot(user_df)
    

    # --------------------------------------------
    # 🤖 머신러닝(XGB) 예측
    # --------------------------------------------
    ml_prob = None
    ml_model = joblib.load("models/ML/XGB_model.pkl")
    feature_cols = joblib.load("models/ML/xgb_feature_names.pkl")
    conv = conv.reindex(columns=feature_cols, fill_value=0)


    if ml_model is not None:
        try:
            # Pipeline은 내부에서 자동 전처리함
            ml_prob = float(ml_model.predict_proba(conv)[0, 1])
        except Exception as e:
            st.warning(f"⚠ ML 예측 중 오류가 발생했습니다: {e}")
            ml_prob = None

    # --------------------------------------------
    # 📉 예측 결과 출력
    # --------------------------------------------
    st.markdown("### 📉 예측 결과")
    st.markdown("#### 🤖 머신러닝(XGBoost) 모델 예측")

    if ml_prob is not None:
        ml_text = f"{ml_prob * 100:.1f} %"
    else:
        ml_text = "모델 준비 중"

    st.metric("이탈 확률 (ML)", ml_text)
