from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.prompts import (
    FewShotPromptTemplate,
    PromptTemplate,
    ChatPromptTemplate,
    StringPromptTemplate,
    BasePromptTemplate,
)


def get_base_prompt(
    prompt_text: str,
    input_variables: list,
    is_validate: bool = True,
    template_format: str = "f-string",
) -> str:
    """
    기본 프롬프트를 리턴합니다.
    :param prompt_text:
    :param input_variables:
    :param is_validate:
    :param template_format:
    :return:
    """
    return PromptTemplate(
        input_variables=input_variables,
        template=prompt_text,
        validate_template=is_validate,
        template_format=template_format,
    ).format()


def get_few_shots_prompt(
    examples: list[dict],
    example_prompt: PromptTemplate,
    example_separator: str = "\n\n",
) -> str:
    """
    FewShotTemplate 을 실행해서 str 로 리턴하는 함수
    예제는 다음과 같습니다.
    examples: [{input: '' , output: ''},{input: '' , output: ''},{input: '' , output: ''}]
    example_prompt:
    :param examples: 예제가 담긴 리스트
    :param example_prompt: 예제를 표현하는 프롬프트
    :param example_separator: 각 예제를 어떻게 구분할지
    :return:
    """
    return FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        example_separator=example_separator,
        template_format="f-string",
    ).format()


def get_chat_system_message(system_text: str) -> SystemMessage:
    return SystemMessage(system_text)


def get_chat_ai_message(ai_text: str) -> AIMessage:
    return AIMessage(ai_text)


def get_chat_human_message(human_text: str) -> HumanMessage:
    return HumanMessage(human_text)


def get_chat_prompt_by_messages(**args: BaseMessage) -> ChatPromptTemplate:
    """
    get_chat_system_message, get_chat_ai_message, get_chat_human_message
    메시지 생성 함수를 통해 생성된 메시지들을 순서대로 조합하여 ChatPromptTemplate 을 리턴합니다.
    **단, SystemMessage 는 맨 처음 한번만 사용 가능하니 주의해서 사용하시기 바랍니다.**
    :param args:
    :return:
    """
    is_system_message_appended = False
    messages = []
    if len(args) < 1:
        raise Exception("입력된 메시지가 없습니다. 다시 확인해주세요.")

    for idx, item in enumerate(args):
        if idx == 0:
            if item.type == "system":
                if is_system_message_appended is False:
                    is_system_message_appended = True
                else:
                    raise Exception(
                        "System Message 는 두번 넣을 수 없습니다. \n 다시 확인해주세요."
                    )
        else:
            if item.type == "system":
                raise Exception(
                    "System Message 는 ChatPromptTemplate 의 맨 처음에만 올 수 있습니다."
                )
        messages.append(item)

    if len(messages) > 0:
        return ChatPromptTemplate.from_messages(messages=messages)


def get_prompts_merged_sequential(
    prompt_separator: str = "\n\n", **args: StringPromptTemplate
) -> PromptTemplate:
    """
    모든 PromptTemplate 들을 합쳐서 1개의 프롬프트로 바꿔줍니다.
    단, ChatPromptTemplate 을 1개의 프롬프트로 합치는 부분은 없으니 주의하시기 바랍니다.
    :param prompt_separator:
    :param args:
    :return:
    """
    if len(args) < 1:
        raise Exception("입력된 프롬프트가 없습니다. 다시 확인해주세요.")

    result = ""
    all_input_variables = []

    for idx, item in enumerate(args):
        if isinstance(item, ChatPromptTemplate):
            raise Exception("ChatPromptTemplate 형식은 Merge 할 수 없습니다.")
        result += item.format()
        result += prompt_separator
        all_input_variables.append(item.input_variables)

    return PromptTemplate(
        input_variables=all_input_variables,
        template=result,
    )


def save_prompt_to_json(prompt: BasePromptTemplate, file_name: str, file_path: str):
    """
    입력된 디렉토리 하위에 file_name.json 으로 프롬프트를 저장합니다.
    :param prompt:
    :param file_path:
    :return:
    """
    FILE_SEPARATOR = "/"
    if Path(file_path).is_dir():
        prompt.save(file_path=(file_path + FILE_SEPARATOR + file_name + ".json"))
    else:
        raise Exception(f"입력된 file_path: {file_path} 가 디렉토리가 아닙니다.")
