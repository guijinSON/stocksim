from typing import Type

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import (
    CommaSeparatedListOutputParser,
    NumberedListOutputParser,
    PydanticOutputParser,
    BaseOutputParser,
)
from langchain_core.output_parsers.pydantic import TBaseModel


def get_output_parser_response_csv() -> CommaSeparatedListOutputParser:
    """
    다음의 프롬프트를 요청 맨 마지막에 집어 넣는 parser 입니다.
    (
        "Your response should be a list of comma separated values, "
        "eg: `foo, bar, baz`"
    )
    :return:
    """
    return CommaSeparatedListOutputParser()


def get_output_parser_response_numbered_list() -> NumberedListOutputParser:
    """
    다음의 프롬프트를 요청 맨 마지막에 집어 넣는 parser 입니다.
    (
        "Your response should be a numbered list with each item on a new line. "
        "For example: \n\n1. foo\n\n2. bar\n\n3. baz"
    )
    :return:
    """
    return NumberedListOutputParser()


def get_output_parser_response_pydantic_obj(
    pydantic_object: Type[TBaseModel],
) -> PydanticOutputParser:
    """
    다음의 프롬프트를 요청 맨 마지막에 집어 넣는 parser 입니다.

    (The output should be formatted as a JSON instance that conforms to the JSON schema below.

    As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
    the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

    Here is the output schema:
    ```
    {schema}
    ```
    )

        :param pydantic_object:
        :return:
    """
    return PydanticOutputParser(pydantic_object=pydantic_object)


def get_output_parser_response_custom_string(
    ai_message: AIMessage,
    prefix_text: str = "",
    suffix_text: str = "",
):
    """
    AI Message 의 앞, 뒤에 원하는 문장을 집어넣는 Parser 입니다.
    """
    return prefix_text + ai_message.content.swapcase() + suffix_text
