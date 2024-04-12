from datetime import datetime
import os
from typing import List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_community.chat_message_histories.file import FileChatMessageHistory
from dotenv import load_dotenv

from src.config.settings import CONV_HISTORY_DIR
from src.llm.azure import get_azure_gpt_chat_llm

load_dotenv()


def _get_file_chat_message_history(session_id: str) -> FileChatMessageHistory:
    now = datetime.now().strftime("")  # Y-M-D H:M:S
    return FileChatMessageHistory(
        os.path.join(CONV_HISTORY_DIR, f"{session_id}_{now}.json")
    )


def get_basic_conversation_with_message_history(
    session_id: str,
    user_input: str,
    callbacks: List[BaseCallbackHandler] = [],
):
    basic_conv_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're an assistant who's good at Respond in 20 words or fewer",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    model = get_azure_gpt_chat_llm(model_version="4", callbacks=callbacks)
    _runnable = basic_conv_prompt | model

    with_message_history_conversations = RunnableWithMessageHistory(
        _runnable,
        _get_file_chat_message_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    with_message_history_conversations.invoke(
        {
            "session_id": session_id,
            "input": user_input,
        }
    )
