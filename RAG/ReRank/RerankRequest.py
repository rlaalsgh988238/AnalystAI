import requests
from RAG.TxtReader import txtReader as TxtReader

# API 엔드포인트 (예시, 실제 엔드포인트로 대체)
url = "https://clovastudio.stream.ntruss.com/v1/api-tools/reranker"

# 인증 토큰 (실제 발급받은 API 키로 대체)
API_KEY = TxtReader.read_file('key')

# 요청 헤더
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 검색한 문서 예시
documents = [
    {"id": "doc1", "doc": "문서 1의 원본 내용입니다."},
    {"id": "doc2", "doc": "문서 2의 원본 내용입니다."},
    # ... 추가 문서
]

# 사용자 쿼리
query = "사용자 질문 예시입니다."

# 요청 바디
data = {
    "documents": documents,
    "query": query,
    "maxTokens": 1024  # 선택사항, 필요시 조정
}

# POST 요청
response = requests.post(url, headers=headers, json=data)

# 응답 처리
if response.status_code == 200:
    result = response.json()
    print("모델 출력 답변:", result.get("result", {}).get("result"))
    print("인용 문서:", result.get("result", {}).get("citedDocuments"))
    print("추천 검색어:", result.get("result", {}).get("suggestedQueries"))
    print("토큰 사용량:", result.get("result", {}).get("usage"))
else:
    print("오류 발생:", response.status_code, response.text)
