import requests
import json

serviceId = "YOUR_SERVICE_ID"  # 서비스 고유 식별자
apiUrl = f"https://kr-pub-gateway.rag.naverncp.com/api/v1/svc/{serviceId}/doc"
apiKey = "YOUR_API_KEY"

headers = {
    "Authorization": f"Bearer {apiKey}",
    "Content-Type": "application/json"
}

# 업로드할 문서 정보
data = {
    "orgid": "original-doc-id-001",      # Optional
    "title": "문서 제목 예시",              # Optional
    "file_name": "example.txt",           # Optional
    "body": "문서 본문 내용입니다.",        # Required
    "extra": {                            # Optional
        "bucket": "my-bucket",
        "key": "path/to/file.txt",
        "userField": "추가정보"
    }
}

# API 요청
response = requests.post(apiUrl, headers=headers, data=json.dumps(data))

# 결과 출력
print("Status Code:", response.status_code)
print("Response Body:", response.json())
