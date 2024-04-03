# 사용자와의 대화를 나누는 Chain
from typing import List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.runnables import RunnablePassthrough

from src.llm.azure import get_azure_gpt_chat_llm
from src.parser.custom_output import custom_parser
from src.prompt.load_prompt import load_prompt
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate, ChatPromptTemplate


def sample_conversation_chain(callbacks: List[BaseCallbackHandler] = [], ):
    prompt = load_prompt("base_chat")
    llm = get_azure_gpt_chat_llm(model_version="4", callbacks=callbacks)
    return {"inputs": RunnablePassthrough()} | prompt | llm


def search_stock(inputs: str, background: str):
    prompt = PromptTemplate.from_template("""
# Persona
You are fictional story simulator. Today is 2030 and an AGI called prometheus has been developed. Given the background answer the user's questions. You may add with your imagination. However, you may not introduce new companies other then the ones provided. Always answer in formal Korean. 

### Background: 
{background}

### User Question: {inputs}
### Response:
""")
    llm = get_azure_gpt_chat_llm(model_version="4")
    chain = {"inputs": RunnablePassthrough(), "background": RunnablePassthrough()} | prompt | llm
    response = chain.invoke({"inputs": inputs, "background": background})
    print(response.__dict__)
    return response

def search_stock_verified(inputs: str):
    """
    주식 종목에 대한 검색인지 판단합니다.
    :param inputs:
    :return:
    """
    prompt = PromptTemplate.from_template("""
# Persona
You're the best linguistic analyst.
You're the best at understanding and analysing the intent of a user's speech.


## Environment
Mostly, users will ask questions in Korean, and they will ask questions related to stocks or the stock market and the economy.


## Condition
1) Whatever question the user is asking, you need to summarise the core of their intent in as short and concise a way as possible, no more than 3 sentences.
2) You need to suggest nouns or verbs that we can extract as keywords.
3) If you have information about the user, be sure to add it to your answer.
4) **Answer no to all unless this is a search for stocks**


## Important Rules
The final answer should be in JSON format, preferably in Korean, but if not, you can use English. 
No other language is required.


## Examples
{examples}


## User Question: {inputs}


Your Answer:
""")
    examples = [
        {
            "question": "삼성전자 에 대해 설명해줘",
            "answer": '{"Intent" : "종목 설명", "Keywords" : ["삼성전자", "설명"]}'
        },
        {
            "question": "현재 대한민국 주식 시장에 대해 설명해줘",
            "answer": '{"Intent" : "대한민국 주식 시장 설명", "Keywords" : ["대한민국", "주식 시장", "설명"]}'
        },
        {
            "question": "AGI 의 등장이 인간에게 미치는 영향은 어떻게 되고, 그에 따라 주식 시장은 어떤 종목들이 상승하고 하락을 하게 될까?",
            "answer": '{"Intent" : "AGI(Artificial General Intelligence) 등장에 따른 인간 사회, 주식 시장 영향", "Keywords" : [None]}'
        },
        {
            "question": "인간의 종말이 온다면, 그것은 나에게 어떤 영향을 줄것인가?",
            "answer": '{"Intent" : "I`m not sure about this.", "Keywords" : [None]}'
        },
    ]
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True)
    chain = {"inputs": RunnablePassthrough(), "examples": RunnablePassthrough()} | prompt | llm | custom_parser
    response = chain.invoke({"inputs": inputs, "examples": examples})

    return response


if __name__ == "__main__":
    print(search_stock_verified("삼성전자 주가가 어떻게 되나요?"))
    print(search_stock_verified("어디로 가야하오?"))
