# 사용자와의 대화를 나누는 Chain
from typing import List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import load_prompt
from langchain_core.runnables import RunnablePassthrough

from src.config.settings import PROMPT_DIR
from src.llm.azure import get_azure_gpt_chat_llm
from src.parser.custom_output import custom_parser


def search_stock(
    inputs: str, background: str, callbacks: List[BaseCallbackHandler] = []
):
    prompt = load_prompt(PROMPT_DIR + "/search_stock.json")
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True, callbacks=callbacks)
    chain = (
        {"inputs": RunnablePassthrough(), "background": RunnablePassthrough()}
        | prompt
        | llm
        | custom_parser
    )
    response = chain.invoke({"inputs": inputs, "background": background})
    return response


def update_story(time: str, background: str, callbacks: List[BaseCallbackHandler] = []):
    """
    전체 스토리를 업데이트 하는 로직
    """
    prompt = load_prompt(PROMPT_DIR + "/update_story")
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True, callbacks=callbacks)
    chain = (
        {"time": RunnablePassthrough(), "background": RunnablePassthrough()}
        | prompt
        | llm
    )
    response = chain.invoke({"time": time, "background": background})
    return response.content


def update_background(background: str, new_plot: str):
    """
    백그라운드를 반영하는 로직
    """
    prompt = load_prompt(PROMPT_DIR + "/update_background")
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True)
    chain = (
        {"background": RunnablePassthrough(), "new_plot": RunnablePassthrough()}
        | prompt
        | llm
    )
    response = chain.invoke({"background": background, "new_plot": new_plot})
    return response.content


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
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True)
    chain = (
        {"inputs": RunnablePassthrough(), "examples": RunnablePassthrough()}
        | prompt
        | llm
    )
    response = chain.invoke({"inputs": inputs, "examples": examples})

    return response


def update_stock_price(background: str, new_plot: str, elapsed_time: str, price: dict):
    """
    주가를 업데이트 합니다.
    """
    prompt = load_prompt("update_stock_price")
    llm = get_azure_gpt_chat_llm(model_version="4", is_stream=True)
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
