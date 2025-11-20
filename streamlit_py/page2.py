import streamlit as st
import pandas as pd
import torch
import sys
import os

# 모델 경로를 절대 경로로 추가
sys.path.append(os.path.abspath('src/models/dl'))
sys.path.append(os.path.abspath('src/models/ml'))

from model import MLPModel  # 모델 로드
from utils import load_model  # 유틸 함수 로드

def run(df: pd.DataFrame):
    # 페이지 설명
    st.markdown("## 🧪 신규/가상 유저 이탈 예측 (머신러닝·딥러닝)")

    st.markdown(
        """
        이 페이지에서는 **유저 정보를 직접 입력**하고,  
        입력값을 바탕으로 **두 가지 모델(ML/DL)의 예측을 비교**하는 기능을 제공합니다.  
        
        현재는 화면 구조만 만들어 둔 상태이며,  
        실제 예측 모델 파일(`.pkl`, `.h5`)은 이후에 연결할 예정입니다.
        """
    )

    # 고객 정보 입력 폼
    with st.form("input_form"):
        st.markdown("### ✏ 유저 정보 입력 폼 (샘플)")

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

        # 제출 버튼
        submitted = st.form_submit_button("🔮 이탈 확률 예측하기")

    # 제출 버튼을 누르기 전이면 함수 종료 → 아무것도 안 보여줌
    if not submitted:
        return

    # 모델 로딩
    model = MLPModel(input_size=10, hidden_size=50, output_size=1)  # 모델 초기화
    model = load_model(model, 'models/DL/final_dl_model.pt')  # 모델 파일 경로

    # 사용자 입력 데이터 처리
    user_input = [
        gender, senior, partner, dependents, tenure, internet, contract, payment, monthly
    ]
    
    # 입력값을 Tensor로 변환
    user_input_tensor = torch.tensor([user_input], dtype=torch.float32)

    # 예측
    model.eval()  # 평가 모드로 설정
    with torch.no_grad():
        prediction = model(user_input_tensor).item()  # 예측값 추출

    # 예측 결과 출력
    st.markdown("### 📉 예측 결과")
    st.metric("이탈 확률 (DL)", f"{prediction*100:.1f} %")

    # 모델 비교 (가짜 데이터 대신 실제 예측 결과로 대체)
    st.markdown("### ⚖ 모델 비교 요약")

    st.write(
        """
        - 같은 입력값을 넣었을 때 **머신러닝과 딥러닝이 서로 어떤 차이를 보이는지** 비교할 수 있습니다.  
        - 실제 서비스에서는 검증 결과(AUC, Accuracy 등)에 따라  
          **실제 운영에 사용할 모델을 결정**하게 됩니다.  
        - 일반적으로 딥러닝 모델이 더 정확하다면  
          운영에서는 딥러닝의 예측값을 기준으로 삼고,  
          머신러닝 모델은 **왜 그렇게 예측했는지 설명하는 용도로** 사용할 수 있습니다.
        """
    )
