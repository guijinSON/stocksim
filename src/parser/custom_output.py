from typing import Iterable

from langchain_core.messages import AIMessage, AIMessageChunk


def custom_parser(ai_message: AIMessage) -> str:
    """Parse the AI message."""
    return ai_message.content.swapcase() + " 포트폴리오와 시간을 업데이트 완료 후에 '확인했습니다'라고 입력해주세요."
