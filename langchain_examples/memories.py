from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory,
)
from langchain_community.chat_message_histories.postgres import (
    PostgresChatMessageHistory,
)
from langchain_community.chat_message_histories.redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.language_models.chat_models import BaseChatModel


def get_conversation_buffer_memory(
    chat_history: BaseChatMessageHistory,
    memory_key: str,
):
    """
    전체 대화를 AI, Human 으로 나눠서 기억하는 Buffer Memory
    :param chat_history:
    :param memory_key:
    :return:
    """
    return ConversationBufferMemory(
        return_message=True, chat_history=chat_history, memory_key=memory_key
    )


def get_conversation_summary_memory(
    chat_history: BaseChatMessageHistory,
    llm: BaseChatModel,
    summarize_step: int = 2,
    memory_key: str = "history",
):
    """
    대화 내용을 1개로 요약하는 Buffer Memory
    :param chat_history:
    :param llm:
    :param summarize_step:
    :param memory_key:
    :return:
    """
    return ConversationSummaryMemory.from_messages(
        chat_memory=chat_history,
        llm=llm,
        summarize_step=summarize_step,
        return_message=True,
        memory_key=memory_key,
    )


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
def get_chat_memory_history_from_pg(
    session_id: str,
    connection_string: str = "",
    table_name: str = "message_store",
):
    return PostgresChatMessageHistory(
        session_id=session_id,
        connection_string=connection_string,
        table_name=table_name,
    )


# 2) REDIS
def get_chat_memory_history_from_redis(
    redis_url: str,
    session_id: str,
    key_prefix: str = "message_store:",
    ttl: int = 600,
):
    return RedisChatMessageHistory(
        url=redis_url,
        session_id=session_id,
        key_prefix=key_prefix,
        ttl=ttl,
    )


# 3) MongoDB
