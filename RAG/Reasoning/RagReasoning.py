import requests
from RAG.TxtReader import txtReader as TxtReader
import uuid


toolList = [
    {
        "type": "function",
        "function": {
            "name": "search_document",
            "description": "지식 베이스에서 관련 정보를 검색합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "검색할 쿼리"}
                },
                "required": ["query"]
            }
        }
    }
]

def rag_reasoning(
        messages: list,
        tools: list = toolList,
        key_path='key',
        top_p=0.8,
        temperature=0.5,
        max_tokens=4096,
        repetition_penalty=1.1,
        tool_choice="auto"
):
    url = "https://clovastudio.stream.ntruss.com/v1/api-tools/rag-reasoning"
    API_KEY = TxtReader.read_file(key_path)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-NCP-CLOVASTUDIO-REQUEST-ID": str(uuid.uuid4())
    }

    data = {
        "messages": messages,
        "tools": tools,
        "toolChoice": tool_choice,
        "topP": top_p,
        "temperature": temperature,
        "maxTokens": max_tokens,
        "repetitionPenalty": repetition_penalty,
        "includeAiFilters": True
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json().get("result", {})
        message = result.get("message", {})
        tool_calls = message.get("toolCalls", [])
        # 함수 이름과 쿼리만 분리
        tool_calls_info = []
        for call in tool_calls:
            func_name = call.get("function", {}).get("name")
            query = call.get("function", {}).get("arguments", {}).get("query")
            tool_calls_info.append({
                "function_name": func_name,
                "query": query
            })
        return {
            "role": message.get("role"),
            "content": message.get("content"),
            "thinkingContent": message.get("thinkingContent"),
            "toolCalls": tool_calls,
            "toolCallsInfo": tool_calls_info,
            "usage": result.get("usage")
        }
    else:
        raise Exception(f"오류 발생: {response.status_code} {response.text}")

# # 사용 예시
# messages = [
#     {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
#     {"role": "user", "content": "RAG Reasoning API 사용법을 알려주세요."}
# ]
#
#
# try:
#     result = rag_reasoning(messages, key_path='key')
#     print("모델 역할:", result["role"])
#     print("모델 답변:", result["content"])
#     print("모델 사고흐름:", result["thinkingContent"])
#     print("toolCalls:", result["toolCalls"])
#     print("토큰 사용량:", result["usage"])
#     print("------\n[함수 이름과 쿼리 분리 결과]")
#     for info in result["toolCallsInfo"]:
#         print(f"함수 이름: {info['function_name']}")
#         print(f"쿼리: {info['query']}")
# except Exception as e:
#     print(e)
