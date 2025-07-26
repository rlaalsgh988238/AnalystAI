import json
import re

def buildSystemMessage(content):
    return {
        "role": "system",
        "content": content
    }

def buildToolMessage(role, content, toolCallId):
    """
    툴 메시지를 구성하는 함수

    Args:
        role (str): 메시지 역할 (예: "tool")
        content (str): 검색 결과가 포함된 JSON 문자열
        toolCallId (str): 툴 호출 ID

    Returns:
        dict: 구성된 툴 메시지
    """
    try:
        # content가 JSON 문자열인 경우 파싱
        if isinstance(content, str):
            parsed_content = json.loads(content)
        else:
            parsed_content = content

        # search_result가 있는 경우 doc 태그 형식으로 변환
        if "search_result" in parsed_content:
            formatted_text = ""
            for item in parsed_content["search_result"]:
                doc_id = item.get("id", "")
                doc_content = item.get("doc", "")

                # doc 태그로 감싸기
                formatted_text += f"<{doc_id}>{doc_content}</{doc_id}> "

            # 마지막 공백 제거
            formatted_text = formatted_text.strip()

            return {
                "content": formatted_text,
                "role": role,
                "toolCallId": toolCallId
            }
        else:
            # search_result가 없는 경우 원본 content 사용
            return {
                "content": content if isinstance(content, str) else json.dumps(content),
                "role": role,
                "toolCallId": toolCallId
            }

    except json.JSONDecodeError:
        # JSON 파싱 실패 시 원본 content 사용
        return {
            "content": content,
            "role": role,
            "toolCallId": toolCallId
        }


def buildAssistantMessage(content, toolCalls=None):
    message = {
        "role": "assistant",
        "content": content
    }
    if toolCalls is not None:
        message["toolCalls"] = toolCalls
    return message

def buildUserMessage(content):
    return {
        "role": "user",
        "content": content
    }