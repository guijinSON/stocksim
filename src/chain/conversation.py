# 사용자와의 대화를 나누는 Chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.llm.azure import get_azure_gpt_chat_llm
from src.prompt.load_prompt import load_prompt


def sample_conversation_chain():
    prompt = load_prompt("base_chat")
    llm = get_azure_gpt_chat_llm(model_version="35")
    return {"inputs": RunnablePassthrough()} | prompt | llm | StrOutputParser()


