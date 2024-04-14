from langchain_core.messages import AIMessage


def custom_parser(
    ai_message: AIMessage,
    prefix: str = "",
    suffix: str = " 포트폴리오와 시간을 업데이트 완료 후에 '확인했습니다'라고 입력해주세요.",
) -> str:
    """Parse the AI message."""
    return prefix + ai_message.content.swapcase() + suffix
