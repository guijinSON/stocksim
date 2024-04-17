# 사용자와의 대화를 나누는 Chain
import time
from typing import List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import load_prompt
from langchain_core.runnables import RunnablePassthrough

from src.config.settings import PROMPT_DIR
from src.llm.azure import get_azure_gpt_chat_llm
from src.parser.custom_output import custom_parser

MODEL_VERSION = '35'


def ai_error_capture(func, max_retries=5, delay_seconds=1):
    def wrapper(*args, **kwargs):
        attempts = 0
        while attempts < max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"An error occurred: {e}")
                attempts += 1
                if attempts == max_retries:
                    print("Max retries reached, function failed")
                    raise
                else:
                    print(f"Retrying... (Attempt {attempts + 1}/{max_retries})")
                    time.sleep(delay_seconds)  # 재시도 사이에 일정 시간 대기
    return wrapper

# def ai_error_capture(func):
#     def wrapper(*args, **kwargs):
#         print("Code before function execution")
#         result = func(*args, **kwargs)
#         print("Code after function execution")
#         return result
#     return wrapper


@ai_error_capture
def search_stock(
        inputs: str, background: str, callbacks: List[BaseCallbackHandler] = []
):
    prompt = load_prompt(PROMPT_DIR + "/search_stock.json")
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True, callbacks=callbacks)
    chain = (
            {"inputs": RunnablePassthrough(), "background": RunnablePassthrough()}
            | prompt
            | llm
            | custom_parser
    )
    response = chain.invoke({"inputs": inputs, "background": background})
    return response


@ai_error_capture
def update_story(time: str, background: str, callbacks: List[BaseCallbackHandler] = []):
    """
    전체 스토리를 업데이트 하는 로직
    """
    prompt = load_prompt(PROMPT_DIR + "/update_story.json")
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True, callbacks=callbacks)
    chain = (
            {"time": RunnablePassthrough(), "background": RunnablePassthrough()}
            | prompt
            | llm
    )
    response = chain.invoke({"time": time, "background": background})
    return response.content


@ai_error_capture
def update_background(background: str, new_plot: str):
    """
    백그라운드를 반영하는 로직
    """
    prompt = load_prompt(PROMPT_DIR + "/update_background.json")
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True)
    chain = (
            {"background": RunnablePassthrough(), "new_plot": RunnablePassthrough()}
            | prompt
            | llm
    )
    response = chain.invoke({"background": background, "new_plot": new_plot})
    return response.content


@ai_error_capture
def search_stock_verified(inputs: str):
    """
    주식 종목에 대한 검색인지 판단합니다.
    :param inputs:
    :return:
    """
    prompt = load_prompt(PROMPT_DIR + "/search_stock_verified.json")
    examples = [
        {"question": "삼성전자 에 대해 설명해줘", "answer": "[NO]"},
        {"question": "반도체를 다루는 회사들을 소개해줘", "answer": "[YES]"},
        {
            "question": "AGI 의 등장에 영향을 받는 회사들은 뭐가 있어?",
            "answer": "[YES]",
        },
        {
            "question": "인간의 종말이 온다면, 그것은 나에게 어떤 영향을 줄것인가?",
            "answer": "[NO]",
        },
    ]
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True)
    chain = (
            {"inputs": RunnablePassthrough(), "examples": RunnablePassthrough()}
            | prompt
            | llm
    )
    response = chain.invoke({"inputs": inputs, "examples": examples})

    return response


@ai_error_capture
def update_stock_price(background: str, new_plot: str, elapsed_time: str, price: str):
    """
    주가를 업데이트 합니다.
    """
    prompt = load_prompt(PROMPT_DIR + "/update_stock_price.json")
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True)
    chain = (
            {
                "background": RunnablePassthrough(),
                "new_plot": RunnablePassthrough(),
                "elapsed_time": RunnablePassthrough(),
                "price": RunnablePassthrough(),
            }
            | prompt
            | llm
    )
    response = chain.invoke(
        {
            "background": background,
            "new_plot": new_plot,
            "elapsed_time": elapsed_time,
            "price": price,
        }
    )

    return response.content
