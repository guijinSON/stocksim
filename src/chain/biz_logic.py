# 사용자와의 대화를 나누는 Chain
import time
from typing import List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import load_prompt, ChatPromptTemplate
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


@ai_error_capture
def search_stock(
        inputs: str, background: str, callbacks: List[BaseCallbackHandler] = []
):
    prompt = ChatPromptTemplate.from_template(
        "\n### Persona\nYou are a fictional story simulator and also financial expert. The year is 2030, and an AGI known as Prometheus has been developed. Based on the background, answer the user's questions. You may enhance responses with your imagination. However, you must not introduce new companies other than those provided. Always answer in formal Korean.\n### Background: {background}\n### User Question: {inputs}\n### Search_Result:"
    )
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True, callbacks=callbacks)

    chain = (
            prompt | llm
    )
    response = chain.invoke({"inputs": inputs, "background": background})
    return response


@ai_error_capture
def summary_background(
        background: str
):
    prompt = ChatPromptTemplate.from_template(
        "Please summarize this Background in one paragraph write in korean.\n ### Background: {background}\n### Summarized Background:"
    )
    llm = get_azure_gpt_chat_llm(model_version='35', is_stream=True)

    chain = (
            prompt | llm
    )
    response = chain.invoke({"background": background})
    return response.content

@ai_error_capture
def ending_story(
        background: str,
        roi: float  # Added ROI as a parameter
):
    # Updated the template with the new structure
    prompt = ChatPromptTemplate.from_template(
        " # Persona\n"
        "You are a fictional story simulator and also a financial expert. At the end of the game, "
        "you should craft a concluding message for the user. Based on the background and the return on investment ('수익률'), "
        "summarize the background and write an encouraging message that will be memorable for the user. in korean\n"
        "### Background: {background}\n"
        "### Return on Investment: {roi}\n"
        "### Concluding Message:"
    )
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True)
    chain = (
            prompt | llm
    )
    response = chain.invoke({"background": background, "roi": roi})
    return response.content

# @ai_error_capture
# def update_story(time: str, background: str, callbacks: List[BaseCallbackHandler] = []):
#     """
#     전체 스토리를 업데이트 하는 로직
#     """
#     prompt = load_prompt(PROMPT_DIR + "/update_story.json")
#     llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True, callbacks=callbacks)
#     chain = (
#             {"time": RunnablePassthrough(), "background": RunnablePassthrough()}
#             | prompt
#             | llm
#     )
#     response = chain.invoke({"time": time, "background": background})
#     return response.content


@ai_error_capture
def update_background(
        background: str,
        system_time: int,
        search_result: str,
        envi_event: str = "",
        stock_event=None,
        callbacks: List[BaseCallbackHandler] = []
):
    """
    백그라운드를 반영하는 로직
    """
    prompt = ChatPromptTemplate.from_template(
        "\n### Persona\nYou are a fictional story simulator and also a financial expert. You will be provided with data affecting stock price movements, and you should rewrite a new background based on this data. Below is a description of the data. Use your imagination to craft a new background that reflects how the world might have changed over the elapsed time according to the data.\nBackground: Represents the current situation of each stock.\nElapsed Time: Shows the time period chosen by the user. The longer the period, the more freely you can use your imagination to write the new background.\nSearch_Result: You must remember this as it contains responses you provided to the user about stocks before writing the new background.\nEnvi_Event: This is an event that affects all stocks. You must consider this when writing the new background.\nStock_Event: These are events specific to individual stocks. These events are crucial to the stock price movements and must be considered in the new background. Be dramatic and exciting. However, you must not introduce new companies other than those provided. Always respond in formal Korean. Please adhere to the original format of the background when rewriting it.\n### Background: {background}\n### Elapsed Time: {system_time}\n### Search_Result: {search_result}\n### Envi_Event: {envi_event}\n### Stock_Event: {stock_event}\n### New Background: ")
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True, callbacks=callbacks)
    chain = (
            prompt | llm
    )
    response = chain.invoke({
        "background": background,
        "system_time": system_time,
        "search_result": search_result,
        "envi_event": envi_event,
        "stock_event": stock_event,
    })
    return response.content


@ai_error_capture
def search_stock_verified(inputs: str):
    """
    주식 종목에 대한 검색인지 판단합니다.
    :param inputs:
    :return:
    """
    prompt = ChatPromptTemplate.from_template(
        "\n### Persona\nYou're the financial analyst. You will be given a question to verify whether the question is related with stocks, financial market or economy.\n## Environment\nUsers will primarily ask questions in Korean related to stocks, the stock market, and the economy.\n## Important Rules\nIf you determine that the question is related with stocks, financial market or economy, return [YES] if not return [NO]. \n## User Question: {inputs}\nYour Answer:")
    llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True)
    chain = (
        prompt | llm
    )
    response = chain.invoke({"inputs": inputs})
    return response


# @ai_error_capture
# def update_stock_price(background: str, new_plot: str, elapsed_time: str, price: str):
#     """
#     주가를 업데이트 합니다.
#     """
#     prompt = load_prompt(PROMPT_DIR + "/update_stock_price.json")
#     llm = get_azure_gpt_chat_llm(model_version=MODEL_VERSION, is_stream=True)
#     chain = (
#             {
#                 "background": RunnablePassthrough(),
#                 "new_plot": RunnablePassthrough(),
#                 "elapsed_time": RunnablePassthrough(),
#                 "price": RunnablePassthrough(),
#             }
#             | prompt
#             | llm
#     )
#     response = chain.invoke(
#         {
#             "background": background,
#             "new_plot": new_plot,
#             "elapsed_time": elapsed_time,
#             "price": price,
#         }
#     )
#
#     return response.content


if __name__ == "__main__":
    print(update_stock_price("hihi", "hihi", "1Month", [30000, 40000, 60000]))
