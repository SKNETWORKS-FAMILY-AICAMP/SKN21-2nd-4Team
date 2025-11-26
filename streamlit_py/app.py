# main.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.backend.query_service import load_all_customers

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

import page1
import page2

# ------------------------------------
# 💡 기본 화면 설정
#  - 페이지 제목, 레이아웃 등 전체 설정
# ------------------------------------
st.set_page_config(
    page_title="📊 통신사 고객 이탈 대시보드",  # 브라우저 탭에 보이는 제목
    layout="wide"  # 화면을 가로로 넓게 쓰기
)

# ------------------------------------
# 📂 데이터 불러오기 함수
#  - 한 번 읽어두고, 재실행 시에는 캐시 사용
#  - 파일 위치: data/raw/Customer_Churn_Dataset.csv
# ------------------------------------
@st.cache_data
def load_data():
    # 이 경로에 csv 파일이 있다고 가정합니다.
    # path = "data/processed/Customer_Churn_Dataset_knn.csv"
    # df = pd.read_csv(path)
    # conn = load_all_customers()
    # df = pd.read_sql('SELECT * FROM customer_churn', conn)
    df = load_all_customers()
    # st.dataframe(df, use_container_width=True)

    # TotalCharges 컬럼을 숫자로 변환
    #  - 숫자로 안 읽히는 값은 NaN -> 0으로 처리
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

    # Churn 컬럼("Yes"/"No")를 숫자 플래그로 변환
    #  - Yes: 1 (이탈)
    #  - No : 0 (유지)
    df["ChurnFlag"] = df["Churn"].map({"Yes": 1, "No": 0})

    return df


# 실제로 데이터 한 번 로딩
# df = load_data()

# ------------------------------------
# 🔧 안전 상태에 따라 텍스트/이모지/색상 반환
#  - safety: 이탈 “안전율(%)”
# ------------------------------------
def get_status_and_color(safety: float):
    if safety >= 90:
        return "매우 안정", "🟢", "#16a34a"
    elif safety >= 85:
        return "안정", "🟢", "#22c55e"
    elif safety >= 75:
        return "보통", "🟡", "#eab308"
    elif safety >= 65:
        return "주의", "🟠", "#f97316"
    elif safety >= 50:
        return "위험", "🟠", "#ea580c"
    else:
        return "매우 위험", "🔴", "#dc2626"



# ------------------------------------
# 🏠 메인 대시보드 화면 그리는 함수
#  - 상단 요약 카드
#  - 세그먼트별 이탈율 표/그래프
#  - 오늘의 액션 포인트
# ------------------------------------


def render_main(df: pd.DataFrame):
    # 전체 고객 수
    # st.dataframe(df, use_container_width=True)  
    total_customers = len(df)

    # df["ChurnFlag"] = df["Chrun"].map(binary_map)
    # 전체 이탈율 (평균값이 곧 이탈율)
    # churn_rate = df["ChurnFlag"].mean()
    churn_rate = df['ChurnFlag'].mean()
    churn_rate_pct = churn_rate * 100

    # 이탈 안전율 = 100 - 이탈율
    safety_rate_pct = 100 - churn_rate_pct

    # 이탈 고객 수
    churn_customers = int(df["ChurnFlag"].sum())

    # 현재 안전 상태(텍스트, 이모지, 색상) 결정
    status_text, status_emoji, status_color = get_status_and_color(safety_rate_pct)

    # 제목/설명
    st.markdown("## 📊 통신사 고객 이탈 메인 대시보드")
    st.markdown(
        "현재 통신사 전체 고객의 이탈 상황을 한눈에 파악하는 "
        "**메인 요약 화면**입니다."
    )
    st.markdown("---")

    # -------------------------------
    # 1) 상단 히어로 카드 (메인 강조 영역)
    #    - 왼쪽: 큰 안전율 카드
    #    - 오른쪽: 간단 숫자 요약
    # -------------------------------
    hero_col1, hero_col2 = st.columns([2, 1])

    # 왼쪽 큰 카드
    with hero_col1:
        st.markdown("### 🧭 전체 고객 유지율 현황")

        hero_html = f"""
        <div style="
            padding: 24px 28px;
            border-radius: 16px;
            background: linear-gradient(90deg, #1e293b, #0f172a);
            border: 1px solid {status_color};
            color: #f9fafb;
            ">
            <div style="font-size: 18px; margin-bottom: 4px; opacity: 0.9;">
                현재 우리 통신사의 전체 <b>유지율</b>은
            </div>
            <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px;">
                <span style="font-size: 40px; font-weight: 800;">
                    {safety_rate_pct:,.1f}%
                </span>
                <span style="font-size: 20px; font-weight: 700;">
                    ({status_emoji} {status_text} 상태)
                </span>
            </div>
            <div style="font-size: 15px; line-height: 1.5; opacity: 0.95;">
                전체 고객 중 약 <b>{churn_rate_pct:,.1f}%</b>가 이탈(Churn) 상태입니다.<br>
                장기 계약/자동이체 등 안정 고객과, 월 단위 계약/전자지불 등
                <b>고위험 고객 세그먼트</b>를 함께 관리할 필요가 있습니다.
            </div>
        </div>
        """
        # HTML로 직접 스타일 준 카드 렌더링
        st.markdown(hero_html, unsafe_allow_html=True)

    # 오른쪽 작은 요약 카드들
    with hero_col2:
        st.markdown("### 🧩 간단 요약")
        st.metric("👥 전체 고객 수", f"{total_customers:,} 명")
        st.metric("🚪 이탈 고객 수", f"{churn_customers:,} 명")
        st.metric("📉 이탈율 (Churn Rate)", f"{churn_rate_pct:,.1f} %")

    st.markdown("---")

    # -------------------------------
    # 2) 주요 KPI 카드 (한 줄 요약)
    # -------------------------------
    st.markdown("### 📌 핵심 지표 요약")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("👥 전체 고객 수", f"{total_customers:,} 명")
    k2.metric("🚪 이탈 고객 수", f"{churn_customers:,} 명")
    k3.metric("📉 이탈율 (Churn)", f"{churn_rate_pct:,.1f} %")
    k4.metric("🛡 유지율 (Retention)", f"{safety_rate_pct:,.1f} %")

    st.markdown("---")

    # -------------------------------
    # 3) 세그먼트별 이탈율 요약
    #    - 계약 형태
    #    - 결제 방식
    #    - 인터넷 서비스
    #    각각 이탈율 상위 3개만 표로 보기
    # -------------------------------
    st.markdown("### ⚠ 이탈 위험 세그먼트 요약")

    # 계약 형태별 평균 이탈율(%)
    contract_churn = (
        df.groupby("Contract")["ChurnFlag"].mean().mul(100).reset_index()
        .rename(columns={"ChurnFlag": "ChurnRate(%)"})
    )
    # 결제 방식별 평균 이탈율(%)
    payment_churn = (
        df.groupby("PaymentMethod")["ChurnFlag"].mean().mul(100).reset_index()
        .rename(columns={"ChurnFlag": "ChurnRate(%)"})
    )
    # 인터넷 서비스별 평균 이탈율(%)
    internet_churn = (
        df.groupby("InternetService")["ChurnFlag"].mean().mul(100).reset_index()
        .rename(columns={"ChurnFlag": "ChurnRate(%)"})
    )

    # 각 세그먼트에서 이탈율 상위 3개만 추출
    top_contract = contract_churn.sort_values("ChurnRate(%)", ascending=False).head(3)
    top_payment = payment_churn.sort_values("ChurnRate(%)", ascending=False).head(3)
    top_internet = internet_churn.sort_values("ChurnRate(%)", ascending=False).head(3)

    # 3개의 표를 가로로 표시
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("#### 📄 계약 형태별 이탈율(Top 3)")
        st.dataframe(
            top_contract.style.format({"ChurnRate(%)": "{:.1f} %"}),
            use_container_width=True,
        )
    with s2:
        st.markdown("#### 💳 결제 방식별 이탈율(Top 3)")
        st.dataframe(
            top_payment.style.format({"ChurnRate(%)": "{:.1f} %"}),
            use_container_width=True,
        )
    with s3:
        st.markdown("#### 🌐 인터넷 서비스별 이탈율(Top 3)")
        st.dataframe(
            top_internet.style.format({"ChurnRate(%)": "{:.1f} %"}),
            use_container_width=True,
        )

    st.markdown("---")

    # -------------------------------
    # 4) 이탈율 그래프 (Altair 바 차트)
    #    - 탭으로 구분: 계약 / 결제 방식 / 인터넷
    # -------------------------------
    st.markdown("### 📈 이탈율 시각화")
    tab1, tab2, tab3 = st.tabs(["📄 계약", "💳 결제 방식", "🌐 인터넷"])

    # 계약 형태별 바 차트
    with tab1:
        chart_contract = alt.Chart(contract_churn).mark_bar().encode(
            x=alt.X("Contract:N",title="계약 형태",axis=alt.Axis(labelAngle=0)
        ),
            y=alt.Y("ChurnRate(%):Q", title="이탈율(%)"),
            tooltip=["Contract", alt.Tooltip("ChurnRate(%):Q", format=".1f")],
        )
        st.altair_chart(chart_contract, use_container_width=True)

    # 결제 방식별 바 차트
    with tab2:
        chart_payment = alt.Chart(payment_churn).mark_bar().encode(
            x=alt.X("PaymentMethod:N", title="결제 방식", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("ChurnRate(%):Q", title="이탈율(%)"),
            tooltip=["PaymentMethod", alt.Tooltip("ChurnRate(%):Q", format=".1f")],
        )
        st.altair_chart(chart_payment, use_container_width=True)

    # 인터넷 서비스별 바 차트
    with tab3:
        chart_internet = alt.Chart(internet_churn).mark_bar().encode(
            x=alt.X("InternetService:N", title="인터넷 서비스", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("ChurnRate(%):Q", title="이탈율(%)"),
            tooltip=["InternetService", alt.Tooltip("ChurnRate(%):Q", format=".1f")],
        )
        st.altair_chart(chart_internet, use_container_width=True)

    st.markdown("---")

    # -------------------------------
    # 5) 오늘의 액션 포인트
    #    - 세그먼트 조합(계약+결제+인터넷) 중
    #      이탈율이 가장 높은 그룹 1개를 뽑아서
    #      오늘 집중 관리 대상처럼 보여주기
    #    ※ 요청: 메인 페이지 맨 아래에만 표시
    # -------------------------------
    st.markdown("### ✅ 오늘의 액션 포인트")

    # 세 필드(Contract, PaymentMethod, InternetService) 조합별 평균 이탈율 계산
    high_risk_combo = (
        df.groupby(["Contract", "PaymentMethod", "InternetService"])["ChurnFlag"]
        .mean()
        .reset_index()
    )
    high_risk_combo["ChurnRate(%)"] = high_risk_combo["ChurnFlag"] * 100

    # 이탈율이 가장 높은 조합 하나만 추출
    high_risk_combo = high_risk_combo.sort_values(
        "ChurnRate(%)", ascending=False
    ).head(1)

    # 데이터가 있을 때와 없을 때 처리
    if not high_risk_combo.empty:
        row = high_risk_combo.iloc[0]
        combo_text = (
            f"**{row['Contract']}** / **{row['PaymentMethod']}** / **{row['InternetService']}**"
        )
        combo_rate = row["ChurnRate(%)"]
    else:
        combo_text = "데이터 부족"
        combo_rate = np.nan

    # 액션 포인트를 카드 형식으로 표현
    action_html = f"""
    <div style="
        padding: 18px 22px;
        border-radius: 14px;
        background-color: #0f172a;
        border: 1px solid #4b5563;
        color: #e5e7eb;
        ">
        <div style="font-size: 18px; font-weight: 700; margin-bottom: 8px;">
            🧠 오늘 집중해서 살펴볼 고객 세그먼트
        </div>
        <div style="font-size: 15px; line-height: 1.6;">
            - 현재 이탈율이 가장 높은 조합은 {combo_text} 입니다.<br>
            - 해당 세그먼트의 이탈율은 <b>{combo_rate:,.1f}%</b> 수준으로,
              다른 고객 그룹보다 <b>우선 관리가 필요한 고위험 세그먼트</b>입니다.<br><br>
            👉 이 조합에 해당하는 고객들 대상으로<br>
            · <b>이탈 방지 프로모션</b> 제공,<br>
            · <b>요금제/결제 방식 변경 유도</b>,<br>
            · <b>서비스 품질 점검</b><br>
            등의 액션을 우선 검토하는 것이 좋습니다.
        </div>
    </div>
    """
    st.markdown(action_html, unsafe_allow_html=True)


# ------------------------------------
# 📚 왼쪽 사이드바 메뉴
#  - Main / page1 / page2 선택
# ------------------------------------
# ---------------------
# 📌 사이드바 글씨체 / 크기 / 간격 커스터마이징
# ---------------------
st.markdown("""
<style>
/* 사이드바 전체 글씨 크기 */
section[data-testid="stSidebar"] .css-16idsys, 
section[data-testid="stSidebar"] .css-1q8dd3e {
    font-size: 15px !important;
}

/* 라디오 버튼 글씨 크기 조정 */
div[role="radiogroup"] > label {
    font-size: 15px !important; 
    padding-top: 6px !important;
    padding-bottom: 6px !important;
}

/* 선택된 항목 글씨 굵게 */
div[role="radiogroup"] > label[data-selected="true"] {
    font-weight: 700 !important;
}

/* 라디오 버튼과 텍스트 사이 간격 늘리기 */
div[role="radiogroup"] > label > div:first-child {
    margin-right: 6px !important;
}
</style>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "📚 페이지 선택",
    ("Main", "page1", "page2"),
    format_func=lambda x: {
        "Main": "📊 전체 이탈 현황",
        "page1": "👤 기존 유저 조회",
        "page2": "🧪 신규 유저 조회/예측",
    }[x],
)

st.sidebar.markdown("---")

# ------------------------------------
# 🚦 페이지 라우팅
#  - 선택된 메뉴에 따라 다른 함수 실행
# ------------------------------------
df = load_data()
if menu == "Main":
    # df = load_data()
    # 메인 대시보드
    render_main(df)
elif menu == "page1":
    # page1.py 안에 정의된 run(df) 함수 호출
    page1.run(df)
elif menu == "page2":
    # page2.py 안에 정의된 run(df) 함수 호출
    page2.run(df)
