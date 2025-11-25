# SKN21-2nd-4Team

## **통신사 고객 이탈 데이터 분석 프로젝트**

### 👨‍👩‍👧‍👦 **팀원 소개**
|  이름  | 역 할  |   세부 역할    | Github         |
| :----: | :----: | :------------: | :------------- |
| 우재현 |  팀장  | 디렉토리 구조 설계, 데이터분석, 산출물 정리, 모델(LGBM) 학습 | [@Wjaehyun](https://github.com/Wjaehyun) |
| 김승룡 |  팀원  | 데이터전처리(결측, 이상치), 모델별 가이드라인 구축, 모델(XGBoost, SVM) 학습    | [@ksryong0](https://github.com/ksryong0) |
| 안혜빈 |  팀원  |  데이터전처리(인코딩), 모델(LogisticRegression) 학습   | [@hyebinhy](https://github.com/hyebinhy) |
| 이의정 |  팀원  |   모델(RandomForest) 학습     | [@lee910814](https://github.com/lee910814) |
| 조남웅 |  팀원  |   모델(DecisionTree) 학습, 딥러닝 학습, Streamlit 구현    | [@whskadnd](https://github.com/whskadnd) |

---

## 📆 **프로젝트 정보**
- **📅 개발 기간:** 2025.11.24 ~ 2025.11.26  
- **📘 주제:** 머신러닝, 딥러닝을 이용한 **통신사 고객 이탈률(Churn) 예측 모델 개발**

---

## 💡 **프로젝트 개요**
통신사의 큰 손실 요인인 **고객 이탈을 줄이기 위해**, 고객의 요금제·인터넷 서비스·계약 기간·월 요금·사용 패턴 데이터를 분석하여
👉 **이탈 위험이 높은 고객을 사전에 찾아내고**
👉 **통신사의 이탈률을 줄이기 위한 예측 모델(ML·DL)** 을 구축했습니다.

---

## 🎯 **프로젝트 목표**
✅ 통신사 고객의 이탈 여부(Churn)를 예측하는 ML·DL 모델 개발<br>
✅ 고객 특성별 이탈 영향 요인 분석(Feature Importance & SHAP 기반)<br>
✅ 데이터 불균형 문제(Churn 불균형) 해결을 통한 성능 최적화<br>
✅ 머신러닝·딥러닝 모델 비교를 통한 최적 모델 선정<br>
✅ 이탈 예측 결과 기반의 의사결정 인사이트 제공

---
## 🧩 **데이터 소개**
📂 **출처:** (https://www.kaggle.com/datasets/denisexpsito/telco-customer-churn-ibm)

| 컬럼명              | 설명                        |    타입   |
| :--------------- | :------------------------ | :-----: |
| customerID       | 고객 고유 ID                  |  object |
| gender           | 성별                        |  object |
| SeniorCitizen    | 고령 여부 (0=아님, 1=해당)        |  int64  |
| Partner          | 배우자 여부                    |  object |
| Dependents       | 부양 가족 여부                  |  object |
| tenure           | 가입 기간(개월)                 |  int64  |
| PhoneService     | 전화 서비스 이용 여부              |  object |
| MultipleLines    | 다중 회선 이용 여부               |  object |
| InternetService  | 인터넷 서비스 종류 (DSL/Fiber/No) |  object |
| OnlineSecurity   | 온라인 보안 서비스 이용 여부          |  object |
| OnlineBackup     | 온라인 백업 서비스 이용 여부          |  object |
| DeviceProtection | 기기 보호 서비스 이용 여부           |  object |
| TechSupport      | 기술 지원 서비스 이용 여부           |  object |
| StreamingTV      | 스트리밍 TV 서비스 이용 여부         |  object |
| StreamingMovies  | 스트리밍 영화 서비스 이용 여부         |  object |
| Contract         | 계약 유형 (월 단위/1년/2년)        |  object |
| PaperlessBilling | 종이 없는 청구 여부               |  object |
| PaymentMethod    | 결제 방식                     |  object |
| MonthlyCharges   | 월 청구 요금                   | float64 |
| TotalCharges     | 총 청구 요금                   | float64 |
| numAdminTickets  | 행정/고객센터 민원 횟수             |  int64  |
| numTechTickets   | 기술 문의/지원 요청 횟수            |  int64  |
| Churn            | 이탈 여부 (Target)            |  int64  |

---
## 💻 Streamlit 구현(화면 녹화를 할까요 말까요)
1) 📊 전체 이탈 현황 대시보드
  - 전체 고객 이탈율·유지율 확인
  - 계약/결제/인터넷 서비스별 이탈율 비교
  - 이탈율 가장 높은 세그먼트 자동 추천

2) 👤 기존 고객 조회
  - customerID로 고객 정보 조회
  - 요금제·서비스 상태 확인
  - 해당 고객이 속한 그룹의 이탈율 자동 분석
  - 이탈 방지 맞춤 대응 전략 제공

3) 🧪 신규 고객 이탈 예측
  - 신규 고객 정보 입력
  - XGBoost 기반 이탈 확률(%) 즉시 예측
  - 위험 고객 조기 식별 가능

---
💬 **팀원 소감**
- 👑 **우재현** : “~~~~.”  
- 🧐 **김승룡** : “~~~~.”  
- 😀 **안혜빈** : “~~~~.”  
- 🥰 **이의정** : “~~~~.”  
- 🤖 **조남웅** : “~~~~.”
