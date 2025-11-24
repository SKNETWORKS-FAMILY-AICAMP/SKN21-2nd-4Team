# page2.py
import streamlit as st
import pandas as pd


def run(df: pd.DataFrame):
    # --------------------------------------------
    # 이 페이지 설명
    # --------------------------------------------
    # 사용자가 직접 고객 정보를 입력하면,
    # 나중에 연결될 머신러닝 / 딥러닝 모델을 이용해
    # 이탈 확률을 계산해주는 페이지입니다.
    # 지금은 UI 틀(뼈대)만 만들고 모델은 아직 연결하지 않았습니다.
    st.markdown("## 🧪 신규/가상 유저 이탈 예측 (머신러닝·딥러닝)")

    st.markdown(
        """
        이 페이지에서는 **유저 정보를 직접 입력**하고,  
        입력값을 바탕으로 **두 가지 모델(ML/DL)의 예측을 비교**하는 기능을 제공합니다.  
        
        현재는 화면 구조만 만들어 둔 상태이며,  
        실제 예측 모델 파일(`.pkl`, `.h5`)은 이후에 연결할 예정입니다.
        """
    )

    # --------------------------------------------
    # ✏ 고객 정보 입력 폼
    # --------------------------------------------
    # st.form을 사용하면 여러 입력값을 묶어서 한 번에 제출할 수 있습니다.
    # col1, col2, col3 으로 나누어서 화면을 깔끔하게 정리했습니다.
    with st.form("input_form"):
        st.markdown("### ✏ 유저 정보 입력 폼")

        # 화면을 3개의 세로 컬럼으로 나눔
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

            # df에서 실제 존재하는 값들을 가져와 selectbox 생성
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

        # 제출 버튼. 눌러야 아래 예측 결과가 나타남
        submitted = st.form_submit_button("🔮 이탈 확률 예측하기")

    # 제출 버튼을 누르기 전이면 함수 종료 → 아무것도 안 보여줌
    if not submitted:
        return

    # -------------------------------------------------------------
    # 📌 예측 모델 부분 (현재는 "데모용 가짜 값" 넣어둔 상태)
    # -------------------------------------------------------------
    # 나중에 실제 모델을 연결하면:
    # 1) 입력값을 하나로 묶고
    # 2) 전처리(Encode/Scaling)
    # 3) 저장된 ML/DL 모델 불러오기
    # 4) 예측 결과 계산
    # 이 과정을 거치게 됩니다.
    #
    # 지금은 UI 작동 확인을 위해 임시 확률값을 넣어둔다.
    fake_prob_ml = 0.32  # 머신러닝 모델 예시 결과
    fake_prob_dl = 0.28  # 딥러닝 모델 예시 결과

    # --------------------------------------------
    # 📉 예측 결과 영역
    # --------------------------------------------
    st.markdown("### 📉 예측 결과")

    col_ml, col_dl = st.columns(2)

    # 머신러닝 결과 표시
    with col_ml:
        st.markdown("#### 🤖 머신러닝 모델 예측")
        st.metric("이탈 확률 (ML)", f"{fake_prob_ml*100:.1f} %")
        st.caption("예: Logistic Regression / RandomForest 등 사용 가능")

    # 딥러닝 결과 표시
    with col_dl:
        st.markdown("#### 🧠 딥러닝 모델 예측")
        st.metric("이탈 확률 (DL)", f"{fake_prob_dl*100:.1f} %")
        st.caption("예: 심층신경망(DNN) 기반 예측")

    # --------------------------------------------
    # 📊 ML vs DL 성능 비교 요약 (검증 데이터 기준)
    # --------------------------------------------
    st.markdown("### ⚖ 모델 비교 요약 (검증 데이터 기준)")

    # 예시 값 – 나중에 Colab에서 나온 실제 값으로 교체
    metrics = {
        "지표": ["Accuracy", "F1-score", "AUC"],
        "머신러닝(ML)": [0.84, 0.71, 0.80],
        "딥러닝(DL)": [0.86, 0.73, 0.82],
    }

    # 지표명을 인덱스로 세우면 0,1,2 인덱스가 사라지고 표가 더 깔끔해집니다.
    metrics_df = pd.DataFrame(metrics).set_index("지표")

    # 스타일링: 소수 둘째 자리까지 + 각 행에서 더 높은 값을 연노랑으로 강조
    styled = (
        metrics_df.style
        .format({"머신러닝(ML)": "{:.2f}", "딥러닝(DL)": "{:.2f}"})
        .highlight_max(axis=1, color="#fff3cd")
    )

    st.dataframe(styled, use_container_width=True)

    st.markdown(
        """
        - 위 수치는 **검증/테스트 데이터**에서 측정한 성능입니다.  
        - 전반적으로 딥러닝(DL) 모델이 조금 더 높은 성능을 보여,  
          운영에서는 **DL 모델을 기본 예측 모델**로 사용할 수 있습니다.  
        - 머신러닝(ML) 모델은 설명/비교용 보조 지표로 활용할 수 있습니다.
        """
    )


