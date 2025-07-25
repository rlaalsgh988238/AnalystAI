import requests
import json

# 필수 값 입력
service_id = "YOUR_SERVICE_ID"  # 서비스 고유 식별자
api_url = f"https://YOUR_API_ENDPOINT/api/v1/svc/{service_id}/doc"

# 인증 및 기타 헤더 (공통 인증 헤더 참고)
headers = {
    "Content-Type": "application/json",
    "X-NCP-APIGW-API-KEY-ID": "YOUR_API_KEY_ID",
    "X-NCP-APIGW-API-KEY": "YOUR_API_KEY",
    # 필요 시 추가 헤더 입력
}

# 삭제할 문서 ID 목록
data = {
    "doc_ids": [
        "DOCUMENT_ID_1",
        "DOCUMENT_ID_2"
    ]
}

# API 요청 (DELETE)
response = requests.delete(api_url, headers=headers, data=json.dumps(data))

# 결과 출력
print("Status Code:", response.status_code)
print("Response Body:", response.json())
