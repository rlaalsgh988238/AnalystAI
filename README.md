# 미래에셋증권 x Clova AI 기반 투자 애널리스트 AI 서비스

## 개요

본 프로젝트는 **Clova AI의 Retrieval-Augmented Generation(RAG) 시스템**을 활용하여  
투자자에게 신뢰도 높은 투자 분석 및 리포트를 제공하는 **AI 투자 애널리스트 서비스**입니다.

- 최신 금융 데이터, 리서치 자료, 공시 정보 등 다양한 외부 데이터를 실시간으로 검색(Retrieval)
- 검색된 정보를 바탕으로 Clova LLM이 맞춤형 분석 및 투자 의견을 생성(Generation)
- 투자자는 쉽고 빠르게 신뢰할 수 있는 투자 인사이트를 얻을 수 있습니다.

---

## 주요 기능

1. **포트폴리오 평가 및 피드백**
    - 사용자가 보유한 주식 포트폴리오를 입력하면, AI가 위험도, 수익률, 분산 등 다양한 관점에서 평가하고 개선 방향에 대한 피드백을 제공합니다.

2. **주식 종목 추천**
    - 사용자의 투자 성향과 시장 상황을 분석하여 맞춤형 주식 종목을 추천합니다.

3. **매수/매도 조언**
    - 관심 종목이나 보유 종목에 대해 AI가 최신 데이터와 분석을 바탕으로 매수 또는 매도 타이밍에 대한 조언을 제공합니다.


---

## 시스템 아키텍처

1. **데이터 수집**
    - 한국투자증권 API를 주로 활용하여 최신 주식 시세, 종목 정보, 시장 데이터 등을 수집합니다.

2. **RAG 파이프라인**
    - Clova에서 제공하는 Retrieval-Augmented Generation(RAG) 시스템을 사용하여,  
      수집된 데이터를 기반으로 사용자의 포트폴리오 평가, 종목 추천, 매수/매도 조언을 생성합니다.
    - 파이썬 코드로 전체 파이프라인을 구성합니다.

---

## 기대 효과

- **신뢰성**: 최신 데이터와 근거 기반 답변으로 투자 판단의 신뢰성 강화
- **효율성**: 방대한 자료를 직접 찾지 않아도 쉽고 빠르게 인사이트 획득
- **맞춤화**: 투자자별 맞춤형 분석 및 추천 가능

---


## 사용 방법

### 1. 환경 준비

- 인텔리제이 IDE 사용 권장

### 2. 네이버 클로바 스튜디오 API 키 등록

1. `AnalystAI/.idea/Key/` 폴더에 `key.txt` 파일을 생성하세요.
2. 해당 파일에 클로바 스튜디오 API 키를 한 줄로 입력하세요.

### 3. 애널리스트 데이터 추가

- `AnalystAI/Docs` 폴더 내에 **애널리스트 이름(예: 심청이, 홍길동)**으로 폴더를 만들고,  
  해당 애널리스트의 투자 리포트(txt 파일)를 추가하면 됩니다.
- txt 파일명은 자유롭게 지정할 수 있습니다.

### 4. 프로그램 실행

- 다음 파일을 실행:
  ```
  AnalystAI/RAG/App/SimpleApplication.py
  ```
   위 파일은 간단한 서비스 어플리케이션 코드입니다. 

- `SimpleApplication.py`에서 아래 항목을 수정하여 사용합니다:
   - **구독 애널리스트 이름**
     ```python
     analystName = '심청이'
     ```
   - **질문/쿼리**
     ```python
     userQuery = "요즘 주식 어떻게 해야해?"
     ```
   - **AI 프롬프트(투자 스타일, 어투 등)**
     ```python
     aIPrompt = f"당신은 투자전문가 {analystName} 입니다 ..."
     ```
   - **AI 툴 목록**  
     (문서 검색, 포트폴리오 조회 등 function tool 추가 가능, 코드 내 주석 참고)

- 코드 내에서 프롬프트, 툴, 쿼리 등을 자유롭게 수정하여 다양한 시나리오를 테스트할 수 있습니다.

---

## 주요 코드 예시 (SimpleApplication.py)

```python
# 구독 Analyst, 쿼리, 프롬프트, 툴 등 자유롭게 수정 가능
analystName = '심청이'
userQuery = "요즘 주식 어떻게 해야해?"
aIPrompt = f"당신은 투자전문가 {analystName} 입니다 ..."

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_document",
            "description": "...",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "요청 내용과 명시할 부분"}
                },
                "required": ["query"]
            }
        }
    },
    # 필요시 function tool 추가 가능
]
```

---


## 참고

- Clova RAG 공식 문서: [https://api.ncloud-docs.com/docs/rag-overview)
- 미래에셋증권 공모전 안내: [https://miraeassetfesta.com/]
---

## 문의

- 프로젝트 담당자: [김민호/kmh030877@gmail.com]
- Github Issues 또는 이메일로 문의해 주세요.

