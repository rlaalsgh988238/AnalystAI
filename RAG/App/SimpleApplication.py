from RAG.Reasoning import RagReasoning
from RAG.Search import SearchEngine
from RAG.ReRank import RerankRequest
import MessageBuilder

#유저가 현재 구독하고 있는 Analyst
analystName = '심청이'
#유저가 궁금한 내용
userQuery = "요즘 주식 어떻게 해야해?"
#AI 프롬프트
aIPrompt = f"당신은 투자전문가 {analystName} 입니다 " + """ 
투자 성향: 거시 경제를 분석해서 미스메치를 찾아내서 고평가 된 기업을 찾음.

어투 및 성향 -> 약간 공격적인 투자 선호, 테크 주식보다는 기존의 오래된 산업쪽에 강점이 있음. 식품, 금융 등등
"""
#AI 툴
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_document",
            "description": """
                애널리스트가 작성한 문서를 찾아 문서 출처를 적어주고 요약하는 리랭커입니다.
                해당 툴을 통해 제공받은 답변을 통해 마무리하고 프롬프트에 맞게 수정해야합니다
                리랭커에서 알맞은 답변을 찾지 못했더라도 답변을 충실히 해야합니다
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "요청 내용과 명시할 부분"}
                },
                "required": ["query"]
            }
        }
    },
    # 툴 추가 목록
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "my_portfolio",
    #         "description": """
    #             유저의 현재 포트폴리오 데이터를 가져옵니다.
    #         """,
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "query": {"type": "string", "description": "요청 내용과 명시할 부분"}
    #             },
    #             "required": ["query"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "current_stock",
    #         "description": """
    #             현재 해당 주식의 데이터를 가져옵니다.
    #         """,
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "query": {"type": "string", "description": "요청 내용과 명시할 부분"}
    #             },
    #             "required": ["query"]
    #         }
    #     }
    # },
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

    if result["content"] == '' and result["thinkingContent"] == None:
        print("[답변] 답변이 어렵습니다")
    elif result["content"] == '':
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
            # 포트폴리오 요청 시, 포트폴리오 보내주기 -> 현재 수정 필요
            elif info['function']['name'] == 'my_portfolio':
                toolId = info['id']
                query = info['function']['arguments']['query']
                print("[Log] getPortfolio 실행")
                print(f"[Log] getPortfolio 쿼리: {query}")
                getPortfolio(query, toolId)
            elif info['function']['name'] == 'stock_data':
                toolId = info['id']
                query = info['function']['arguments']['query']
                print("[Log] getCurrentStock 실행")
                print(f"[Log] getCurrentStock 쿼리: {query}")
                getCurrentStock(query, toolId)
    else:
        print("[답변] " + result["content"])



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

def getPortfolio(query, toolId):
    print()
def getCurrentStock(query, toolId):
    print()

startRagReasoning()