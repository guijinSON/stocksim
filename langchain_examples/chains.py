from typing import List, Mapping

from langchain.chains.llm_checker.base import LLMCheckerChain
from langchain.chains.llm_math.base import LLMMathChain
from langchain_core.language_models import BaseChatModel

from langchain.chains.base import Chain
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.chains.llm_requests import LLMRequestsChain
from langchain.chains.router import MultiRouteChain, RouterChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import BaseLLMOutputParser, StrOutputParser
from langchain_core.prompts import BasePromptTemplate

"""
랭체인에서 기본적으로 제공하는 여러가지 유용한 체인이 담겨 있습니다.
"""


def get_llm_chain(
    model: BaseChatModel,
    prompt,
    llm_kwargs: dict,
    output_key: str = "text",
    output_parser: BaseLLMOutputParser = StrOutputParser,
    verbose: bool = True,
):
    """

    :param verbose:
    :param model:
    :param prompt:
    :param llm_kwargs:
    :param output_key:
    :param output_parser:
    :return:
    """
    return LLMChain(
        llm=model,
        prompt=prompt,
        output_key=output_key,
        output_parser=output_parser,
        llm_kwargs=llm_kwargs,
        verbose=verbose,
    )


def get_request_url_based_chain(
    llm_chain: LLMChain,
    url: str,
    max_text_length: int = 8000,
    verbose: bool = True,
):
    """
    needs `pip install bs4`
    :param verbose:
    :param llm_chain:
    :param url:
    :param max_text_length:
    :return:
    """
    return LLMRequestsChain(
        llm_chain=llm_chain, input_key=url, text_length=max_text_length, verbose=verbose
    )


def get_conversation_chain(
    memory: BaseMemory,
    llm: BaseChatModel,
    prompt: BasePromptTemplate,
    input_key: str = "input",
    output_key: str = "response",
    verbose: bool = True,
):
    """
    기본적인 대화를 진행하는 체인입니다.
    :param memory:
    :param llm:
    :param prompt:
    :param input_key:
    :param output_key:
    :param verbose:
    :return:
    """
    return ConversationChain(
        memory=memory,
        llm=llm,
        prompt=prompt,
        input_key=input_key,
        output_key=output_key,
        verbose=verbose,
    )


def get_sequential_chain(
    chains: List[Chain],
    strip_outputs: bool = False,
    input_key: str = "input",
    output_key: str = "output",
):
    """
    입력된 체인들을 순서대로 실행합니다.
    input_key, output_key 는 각 체인들에 입력되는 Input_key, Output_key 와 일치해야 합니다.
    :param chains:
    :param strip_outputs:
    :param input_key:
    :param output_key:
    :return:
    """
    return SimpleSequentialChain(
        chains=chains,
        strip_outputs=strip_outputs,
        input_key=input_key,
        output_key=output_key,
    )


def get_router_chain(llm_chain: LLMChain):
    return RouterChain(llm_chain=llm_chain)


def get_multi_router_chain(
    router_chain: RouterChain,
    destination_chains: Mapping[str, Chain],
    default_chain: Chain,
    silent_error: bool = False,
):
    return MultiRouteChain(
        router_chain=router_chain,
        destination_chains=destination_chains,
        default_chain=default_chain,
        silent_error=silent_error,
    )


def get_create_sql_query_chain():
    return create_sql_query_chain()


def get_llm_math_chain():
    """
    수학식 계산을 위해 Python 코드를 구성하는 체인
    python - tool 과 결합하면 해당 코드를 실제 실행한 결과를 받을 수 있음
    """
    return LLMMathChain()


def get_llm_checker_chain():
    """
    지정한 대로 체크를 수행하는 체인(결과 검증을 수행할 수 있음)
    """
    return LLMCheckerChain()
