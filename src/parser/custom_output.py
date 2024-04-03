from typing import Iterable

from langchain_core.messages import AIMessage, AIMessageChunk


def custom_parser(ai_message: AIMessage) -> str:
    """Parse the AI message."""
    return ai_message.content.swapcase() + "고맙습니다~"
