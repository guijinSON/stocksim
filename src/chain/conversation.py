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


def search_stock(inputs: str, background: str, callbacks: List[BaseCallbackHandler] = []):
    prompt = PromptTemplate.from_template("""
# Persona
You are fictional story simulator. Today is 2030 and an AGI called prometheus has been developed. Given the background answer the user's questions. You may add with your imagination. However, you may not introduce new companies other then the ones provided. Always answer in formal Korean. 

### Background: 
{background}

### User Question: {inputs}
### Response:
""")
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True, callbacks=callbacks)
    chain = {"inputs": RunnablePassthrough(), "background": RunnablePassthrough()} | prompt | llm | custom_parser
    response = chain.invoke({"inputs": inputs, "background": background})
    return response


def update_story(time: str, background: str, callbacks: List[BaseCallbackHandler] = []):
    prompt = PromptTemplate.from_template("""
# Persona
You are fictional story simulator. You will be given a background, and elapsed time. Use your imagination to create a story how the world would have changed through the elapsed time. Be dramatic and exciting. However, you may not introduce new companies other then the ones provided. Always answer in formal Korean. 

### Background:
{background}

### Elapsed Time:
{time}
### Response: 
""")
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True, callbacks=callbacks)
    chain = {"time": RunnablePassthrough(), "background": RunnablePassthrough()} | prompt | llm
    response = chain.invoke({"time": time, "background": background})
    return response.content


def update_background(background: str, new_plot: str):
    prompt = PromptTemplate.from_template("""
# Persona
You are fictional story simulator. You will be given a background and a new plot. Refine the background and return a new one. You must not add new or delete existing companies. Every company should have at least 4 or more sentences for explantion. Always answer in formal Korean. 

### Background:
{background}

### New Plot:
{new_plot}

### New Background:
""")
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True)
    chain = {"background": RunnablePassthrough(), "new_plot": RunnablePassthrough()} | prompt | llm
    response = chain.invoke({"background": background, "new_plot": new_plot})
    return response.content


def search_stock_verified(inputs: str):
    """
    주식 종목에 대한 검색인지 판단합니다.
    :param inputs:
    :return:
    """
    #     prompt = PromptTemplate.from_template("""
    # # Persona
    # You're the best linguistic analyst.
    # You're the best at understanding and analysing the intent of a user's speech.
    #
    #
    # ## Environment
    # Mostly, users will ask questions in Korean, and they will ask questions related to stocks or the stock market and the economy.
    #
    #
    # ## Condition
    # 1) Whatever question the user is asking, you need to summarise the core of their intent in as short and concise a way as possible, no more than 3 sentences.
    # 2) You need to suggest nouns or verbs that we can extract as keywords.
    # 3) If you have information about the user, be sure to add it to your answer.
    # 4) **Answer no to all unless this is a search for stocks**
    #
    #
    # ## Important Rules
    # The final answer should be in JSON format, preferably in Korean, but if not, you can use English.
    # No other language is required.
    #
    #
    # ## Examples
    # {examples}
    #
    #
    # ## User Question: {inputs}
    #
    #
    # Your Answer:
    # """)
    prompt = PromptTemplate.from_template("""
    # Persona
    You're the best linguistic analyst.
    You will be given a question verify whether the question requires you to list stocks that fits a certain criteria.


    ## Environment
    Mostly, users will ask questions in Korean, and they will ask questions related to stocks or the stock market and the economy.

    ## Important Rules
    If the you think the question is valid asking for a list of stocks return [YES] if not return [NO].

    ## User Question: {inputs}
    Your Answer:""")
    examples = [
        {
            "question": "삼성전자 에 대해 설명해줘",
            "answer": '[NO]'
        },
        {
            "question": "반도체를 다루는 회사들을 소개해줘",
            "answer": '[YES]'
        },
        {
            "question": "AGI 의 등장에 영향을 받는 회사들은 뭐가 있어?",
            "answer": '[YES]'
        },
        {
            "question": "인간의 종말이 온다면, 그것은 나에게 어떤 영향을 줄것인가?",
            "answer": '[NO]'
        },
    ]
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True)
    chain = {"inputs": RunnablePassthrough(), "examples": RunnablePassthrough()} | prompt | llm
    response = chain.invoke({"inputs": inputs, "examples": examples})

    return response


def update_stock_price(background: str, new_plot: str, elapsed_time: str, price: dict):
    """
    주가를 업데이트 합니다.
    """
    prompt = PromptTemplate.from_template("""
### Persona
You are a story simulator. Given a background, new plot, elapsed time and original price update the price of the stocks.

### Important Rules
You must return in dictionary format exactly like the one you recieved.

### Background: 
{background}

### New Plot:
{new_plot}

### Elapsed Time:
{elapsed_time}

### Original Price:
{price}

### New Price (In exactly same format):""")

    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True)
    chain = {"background": RunnablePassthrough(), "new_plot": RunnablePassthrough(),
             "elapsed_time": RunnablePassthrough(), "price": RunnablePassthrough()} | prompt | llm
    response = chain.invoke({"background": background, "new_plot": new_plot, "elapsed_time": elapsed_time, "price": price})

    return response.content


if __name__ == "__main__":
    print(search_stock_verified("삼성전자 주가가 어떻게 되나요?"))
    print(search_stock_verified("어디로 가야하오?"))
