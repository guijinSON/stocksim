from langchain.output_parsers import openai_functions
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser, PydanticOutputFunctionsParser
from langchain_core.utils.function_calling import convert_pydantic_to_openai_function
from pydantic import BaseModel


def get_pydantic_output_chain(prompt, model, pydantic_obj: BaseModel):
    """Get pydantic output."""
    parser = PydanticOutputFunctionsParser(pydantic_schema=pydantic_obj)
    openai_functions = [convert_pydantic_to_openai_function(pydantic_obj)]
    return prompt | model.bind(functions=openai_functions) | parser


def get_json_output_chain(prompt, model):
    return prompt | model.bind(functions=openai_functions) | JsonOutputFunctionsParser()
