from typing import List, Dict

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate, ChatPromptTemplate


def create_base_prompt_template(input_variables: List[str], template: str):
    return PromptTemplate(input_variables=input_variables, template=template)


def create_chat_prompt_templates(messages: List[dict]):
    return ChatPromptTemplate().from_messages(messages=messages)


def create_few_shot_prompt_templates(few_shot_prompt_formatter: PromptTemplate, examples: List[Dict[str, str]]):
    """
    example_prompt = PromptTemplate(
        input_variables=["question", "answer"], template="Question: {question}\n{answer}"
    )
    :param few_shot_prompt_formatter:
    :param examples:
    :return:
    """
    return FewShotPromptTemplate(
        examples=examples,
        example_prompt=few_shot_prompt_formatter,
    )