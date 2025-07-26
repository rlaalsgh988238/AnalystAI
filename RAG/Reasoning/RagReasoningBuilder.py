import requests
from RAG.Reasoning import RagReasoning

def RagReasoningBuilder(messages: list):
    try:
        result = RagReasoning.rag_reasoning(messages)
    except Exception as e:
        print(e)
