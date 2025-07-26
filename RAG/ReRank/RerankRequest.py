import requests
from RAG.TxtReader import txtReader as TxtReader

def rerank_documents(documents, query, key_path='key', max_tokens=1024):
    url = "https://clovastudio.stream.ntruss.com/v1/api-tools/reranker"
    API_KEY = TxtReader.read_file(key_path)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "documents": documents,
        "query": query,
        "maxTokens": max_tokens
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json().get("result", {})
        return {
            "answer": result.get("result"),
            "cited_documents": result.get("citedDocuments"),
            "suggested_queries": result.get("suggestedQueries"),
            "usage": result.get("usage")
        }
    else:
        raise Exception(f"오류 발생: {response.status_code} {response.text}")


# # 사용 예시
# documents = [
#     {"id": "doc1", "doc": "문서 1의 원본 내용입니다."},
#     {"id": "doc2", "doc": "문서 2의 원본 내용입니다."},
#     # ...
# ]
# query = "사용자 질문 예시입니다."
# try:
#     result = rerank_documents(documents, query, key_path='key')
#     print("모델 출력 답변:", result["answer"])
#     print("인용 문서:", result["cited_documents"])
#     print("추천 검색어:", result["suggested_queries"])
#     print("토큰 사용량:", result["usage"])
# except Exception as e:
#     print(e)

