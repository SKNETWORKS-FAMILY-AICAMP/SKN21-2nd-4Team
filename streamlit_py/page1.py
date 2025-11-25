# page1.py
import streamlit as st
import pandas as pd
import altair as alt


def get_recommendation(col_name: str, value: str) -> str:
    """가장 이탈율이 높은 조건에 대해 해결 방안 문구 생성 (Markdown 스타일 적용)"""

    if col_name == "PaymentMethod":
        if value in ["Electronic check", "Mailed check"]:
            return (
                "- 우편/전자결제 고객에게 자동이체(계좌/카드) 전환 시 소액 할인이나 포인트 제공\n"
                "- 납부일 전 알림 서비스(SMS/앱 푸시)를 제공해 연체·불편을 줄이기\n"
                "- 모바일 청구서/전자고지로 전환 시 수수료 절감 및 청구 내역 확인 편의 개선\n"
            )
        else:
            return (
                "- 현재 결제 방식 만족도에 대한 간단 설문 또는 콜 상담 진행\n"
                "- 결제 오류/불편 사항(환불 지연, 이중 청구 등) 발생 여부를 VOC·콜로그와 함께 점검\n"
            )

    elif col_name == "Contract":
        if value == "Month-to-month":
            return (
                "- 단기 계약 고객에게 1년·2년 장기 계약 전환 시 요금 할인/부가서비스 제공 제안\n"
                "- 약정 없는 상품과 장기 계약 상품의 차이를 비교표 형태로 쉽게 안내\n"
                "- 해지 의향이 있는 고객 대상 유지 프로모션 운영 및 전담 상담원 배정\n"
            )
        else:
            return (
                "- 약정 종료 시점에 맞춰 사전 안내(문자/전화)로 재계약 혜택 공지\n"
                "- 장기 계약 고객에게 추가 데이터·부가서비스 등 유지 보상 제공\n"
            )

    elif col_name == "InternetService":
        if value == "Fiber optic":
            return (
                "- 광랜(Fiber) 고객 대상 품질 모니터링(속도·지연·장애 횟수) 강화\n"
                "- 장애·품질 불만 고객 대상 무상 점검 또는 임시 요금 감면 제공\n"
                "- 과도한 요금제 사용 시 업/다운그레이드 컨설팅 제공\n"
            )
        elif value == "DSL":
            return (
                "- DSL 구간 중 불만·장애가 많은 지역은 망 증설·장비 교체 등 인프라 개선 우선 검토\n"
                "- 품질 민감 고객에게 Fiber 상품 업그레이드 프로모션 안내\n"
            )
        else:
            return (
                "- 인터넷 미이용 고객에게 결합 상품(인터넷+모바일) 안내 및 혜택 제공\n"
            )

    return (
        "- 세그먼트 기반 만족도 조사 실시\n"
        "- 동일 조건 고객의 이탈 사유(VOC/민원/콜로그)를 분석해 우선 개선 항목 선정\n"
    )



def run(df: pd.DataFrame):
    # -------------------------
    # 제목 및 설명
    # -------------------------
    st.markdown("## 👤 기존 유저 정보 조회 및 이탈 위험도")

    st.markdown(
        """
        이 페이지에서는 **특정 유저(customerID)**를 조회하여  

        - 기본 정보  
        - 서비스/요금제 정보  
        - 이 유저가 속한 그룹의 이탈율(근거 EDA)과 간단 해결 방안  

        을 확인하는 용도로 사용합니다.
        """
    )

    st.markdown("---")

    # --------------------------------------------------
    # ① 조회할 고객 선택 (검색 + 선택 + 버튼)
    # --------------------------------------------------
    st.markdown("### 🔍 조회할 고객 선택")

    search_keyword = st.text_input(
        "customerID 검색(일부만 입력해도 됩니다.)",
        placeholder="예: 7590, QPYBK, HQTU ...",
    )

    customer_ids = (
        df["customerID"]
        .astype(str)
        .loc[lambda s: s.str.contains(search_keyword, case=False, na=False)]
        .sort_values()
        .unique()
    )

    if len(customer_ids) == 0:
        st.warning("검색 조건에 맞는 customerID가 없습니다. 다른 키워드를 입력해 주세요.")
        return

    default_index = 0
    if "selected_customer_id" in st.session_state:
        if st.session_state["selected_customer_id"] in customer_ids:
            default_index = list(customer_ids).index(st.session_state["selected_customer_id"])

    selected_customer_id = st.selectbox(
        "조회할 customerID를 선택하세요.",
        options=customer_ids,
        index=default_index,
    )

    clicked = st.button("🔍 이 고객 정보 조회하기")

    if clicked:
        st.session_state["selected_customer_id"] = selected_customer_id

    if "selected_customer_id" not in st.session_state:
        st.info("customerID를 선택한 뒤 **'이 고객 정보 조회하기' 버튼**을 눌러주세요.")
        return

    customer_id = st.session_state["selected_customer_id"]

    # --------------------------------------------------
    # ② 선택된 고객 정보 추출
    # --------------------------------------------------
    customer_df = df[df["customerID"] == customer_id]

    if customer_df.empty:
        st.error("선택한 customerID에 해당하는 데이터가 없습니다.")
        return

    row = customer_df.iloc[0]

    # ---------- 기본/서비스 컬럼 정의 및 세로 표 변환 ----------
    basic_cols = ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure"]
    service_cols = [
        "customerID",
        "InternetService",
        "Contract",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges",
        "Churn",
    ]

    basic_labels = {
        "customerID": "customerID",
        "gender": "성별",
        "SeniorCitizen": "시니어 여부",
        "Partner": "배우자 유무",
        "Dependents": "부양가족 유무",
        "tenure": "가입 개월(tenure)",
    }

    service_labels = {
        "customerID": "customerID",
        "InternetService": "인터넷 서비스",
        "Contract": "계약 형태",
        "PaymentMethod": "결제 방식",
        "MonthlyCharges": "월 청구요금",
        "TotalCharges": "누적 청구요금",
        "Churn": "이탈 여부",
    }

    basic_display = pd.DataFrame(
        {
            "항목": [basic_labels[c] for c in basic_cols],
            "값": [row[c] for c in basic_cols],
        }
    )

    service_display = pd.DataFrame(
        {
            "항목": [service_labels[c] for c in service_cols],
            "값": [row[c] for c in service_cols],
        }
    )

    st.markdown("---")

    # --------------------------------------------------
    # ③ 기본 정보 / 서비스·요금제 정보 (세로 표)
    # --------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📌 기본 정보")
        st.dataframe(
            basic_display,
            hide_index=True,
            use_container_width=True,
        )

    with col2:
        st.markdown("### 🧾 서비스/요금제 정보")
        st.dataframe(
            service_display,
            hide_index=True,
            use_container_width=True,
        )

    st.markdown("---")

    # --------------------------------------------------
    # ④ 이 유저가 속한 그룹의 이탈율 (근거 EDA)
    # --------------------------------------------------
    st.markdown("### 📊 이 유저가 속한 그룹의 이탈율 (근거 EDA)")

    conditions = [
        ("Contract", "Contract"),
        ("InternetService", "InternetService"),
        ("PaymentMethod", "PaymentMethod"),
    ]

    reasons = []
    for col, label in conditions:
        group_value = row[col]

        group_churn = (
            df.groupby(col)["Churn"]
            .apply(lambda s: (s == "Yes").mean() * 100)
        )

        churn_rate = float(group_churn.get(group_value, float("nan")))
        reasons.append(
            {
                "조건": f"{label}: {group_value}",
                "이탈율(%)": churn_rate,
                "컬럼": col,
                "값": group_value,
            }
        )

    reasons_df = pd.DataFrame(reasons)

    chart = (
    alt.Chart(reasons_df)
    .mark_bar()
    .encode(
        x=alt.X(
            "조건:N",
            title="조건(유저가 속한 그룹)",
            axis=alt.Axis(labelAngle=0)   # ← NEW: X축 라벨 각도 0°
        ),
        y=alt.Y("이탈율(%):Q", title="그룹 이탈율(%)"),
        tooltip=["조건", alt.Tooltip("이탈율(%):Q", format=".1f")],
    )
)


    st.altair_chart(chart, use_container_width=True)

    # --------------------------------------------------
    # ⑤ 해석 + 해결 방안 (같은 글씨체/크기)
    # --------------------------------------------------
    max_row = reasons_df.loc[reasons_df["이탈율(%)"].idxmax()]

    st.markdown("**이 유저는**")
    explanation_text = f"""
  · **{max_row['조건']}** 그룹에 속해 있으며,  
  · 이 그룹의 이탈율은 **{max_row['이탈율(%)']:.1f}%**로  
    다른 조건 대비 상대적으로 높은 편입니다.  
"""

    recommendation_text = get_recommendation(
        col_name=max_row["컬럼"],
        value=max_row["값"],
    )

    st.markdown(explanation_text)

    st.markdown("**이탈 방지 해결 방안**")
    st.markdown(recommendation_text)
