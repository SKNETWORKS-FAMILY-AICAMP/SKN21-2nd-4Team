# SKN21-2nd-4Team

## **통신사 고객 이탈 데이터 분석 프로젝트**

### 👨‍👩‍👧‍👦 **팀원 소개**
| 팀원 1 | 팀원 2 | 팀원 3 | 팀원 4 | 팀원 5 |
|:------:|:------:|:------:|:------:|:------:|
| 우재현 | 김승룡 | 안혜빈 | 이의정 | 조남웅 |

---

## 📆 **프로젝트 정보**
- **📅 개발 기간:** 2025.11.25 ~ 2025.11.26  
- **📘 주제:** 머신러닝을 이용한 **통신사 고객 이탈률(Churn) 예측 모델 개발**

---

## 💡 **프로젝트 개요**
통신사의 **요금제 유형, 인터넷 서비스 종류, 계약 기간, 월 이용 요금, 고객 서비스 이용 패턴** 등의 데이터를 기반으로
👉 **이탈 가능성이 높은 고객을 사전에 예측**하는 머신러닝·딥러닝 모델을 구축했습니다.

---

## 🚀 **프로젝트 필요성**
신규 가입자를 유치하는 비용보다 기존 고객을 유지하는 비용이 훨씬 낮습니다.

따라서 **이탈 가능성이 높은 고객을 조기에 발견하고 대응하는 것**은
통신사의 매출 안정성과 직결되는 핵심 과제입니다.

---

## 🎯 **프로젝트 목표**
✅ 통신사 고객의 이탈 여부(Churn)를 예측하는 ML·DL 모델 개발
✅ 고객 특성별 이탈 영향 요인 분석(Feature Importance & SHAP 기반)
✅ 데이터 불균형 문제(Churn 불균형) 해결을 통한 성능 최적화
✅ 머신러닝·딥러닝 모델 비교를 통한 최적 모델 선정
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


