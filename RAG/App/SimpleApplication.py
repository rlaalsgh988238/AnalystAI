from RAG.Reasoning import RagReasoning
from RAG.Search import SearchEngine
from RAG.ReRank import RerankRequest
import MessageBuilder

#유저가 현재 구독하고 있는 Analyst
analystName = '홍길동'
#유저가 궁금한 내용
userQuery = "요즘 괜찮은 주식이 뭐야 그리고 그 주식이 왜 좋아"
#AI 프롬프트
aIPrompt = f"당신은 투자전문가 {analystName} 입니다 " + """ 
나는 홍길동 애널리스트의 AI 분신으로, 내 답변은 항상 1인칭 시점이며 오직 홍길동의 과거 리포트, 칼럼, 그리고 투자 철학에만 근거한다. 투자 자문이나 매수/매도 추천, 목표주가 제시는 반드시 과거 리포트에 나온 내용만 과거 시제로 언급하며, 답변에는 반드시 해당 리포트나 칼럼의 제목 또는 발표일 등 구체적인 근거를 밝힌다. 제공된 데이터 외의 일반 지식이나 인터넷 정보는 절대 사용하지 않으며, 근거가 없으면 모른다고 하거나 투자 원칙에 따라 답변을 거절한다. 답변은 항상 "저는 [제목/날짜]에서..." 식의 자기 인용으로 시작해 핵심 논거 2~3가지를 설명한 뒤, 마지막에 "[유의사항] 본 내용은 AI가 과거 자료를 기반으로 요약한 정보이며, 현재 시점의 투자 자문이 아닙니다. 모든 투자의 최종 결정과 책임은 투자자 본인에게 있습니다. 정확한 내용은 원문 리포트를 꼭 확인하시기 바랍니다."라는 면책 조항을 반드시 포함한다. 내 말투는 데이터 중심의 신중한 스타일을 유지하며, 투자 철학은 견고한 펀더멘털과 성장 동력을 중시하되 잠재적 위험까지 종합적으로 고려하는 균형 잡힌 성장 지향형이다.
"""
#AI 툴
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_document",
            "description": "애널리스트가 작성한 문서를 찾아 문서 출처를 적어주고 요약하는 리랭커입니다. 해당 툴을 통해 제공받은 답변을 통해 마무리하고 프롬프트에 맞게 수정해야합니다",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "요청 내용과 명시할 부분"}
                },
                "required": ["query"]
            }
        }
    }
]
# 대화 내역
messageList = [
    MessageBuilder.buildSystemMessage(aIPrompt),
    MessageBuilder.buildUserMessage(userQuery),
]

def startRagReasoning():
    # RAGReasoning 대화 내역
    print("[messageList] " + str(messageList))
    #RagReasoning 시작
    result = RagReasoning.rag_reasoning(messageList, tools)
    # 결과 로그
    print("[Result Log] " + str(result))

    if result["content"] == '':
        # 추론 로그
        print("[추론] " + str(result["thinkingContent"]))
        # 응답을 대화 내역에 추가
        content = result["content"]
        toolCalls = result["toolCalls"]
        response = MessageBuilder.buildAssistantMessage(content, toolCalls)
        messageList.append(response)
        # 알맞은 툴 실행
        for info in toolCalls:
            # 문서 검색 요청 시, 리랭크 실행
            if info['function']['name'] == 'search_document':
                toolId = info['id']
                query = info['function']['arguments']['query']
                print("[Log] Rerank 실행")
                print(f"[Log] Rerank 쿼리: {query}")
                startRerank(query, toolId)
    else:
        print("[답변] "+result["content"])


def startRerank(query, toolId):
    doc = SearchEngine.makeDoc2Json(
        SearchEngine.searchDoc([f"{query}"], analystName = f'{analystName}'),
        analystName = f'{analystName}'
    )

    queryWithDate = query + ", 해당 문서 날짜 정보"

    result = RerankRequest.rerank_documents(doc, queryWithDate)
    message = MessageBuilder.buildToolMessage("tool", result['answer'], toolId)
    messageList.append(message)
    print("[Rerank] "+ result["answer"])
    startRagReasoning()

startRagReasoning()