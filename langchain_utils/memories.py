from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory,
)


def get_conversation_buffer_memory(memory_key: str):
    """
    전체 대화를 AI, Human 으로 나눠서 기억하는 Buffer Memory
    :param memory_key:
    :return:
    """
    return ConversationBufferMemory(memory_key=memory_key)


def get_conversation_summary_memory(memory_key: str):
    """
    대화 내용을 1개로 요약하는 Buffer Memory
    :param memory_key:
    :return:
    """
    return ConversationSummaryMemory(memory_key=memory_key)


def get_conversation_window_memory(memory_key: str, k: int = 5):
    """
    대화 내용의 최근 K 개 만큼만 기억하는 Buffer Memory
    :param memory_key:
    :param k:
    :return:
    """
    return ConversationBufferWindowMemory(memory_key=memory_key, k=k)


# TODO DB 에 저장
# 1) PG
# 2) REDIS
# 3) MongoDB
