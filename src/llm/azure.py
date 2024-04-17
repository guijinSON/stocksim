import os
import random
from pathlib import Path
from typing import Dict, List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv
from langchain_community.cache import RedisCache, SQLiteCache, InMemoryCache
from langchain_core.globals import set_llm_cache

from src.config.settings import ROOT_DIR

load_dotenv()

gpt_35_list = [
    {
        "deployment": os.getenv("AU_GPT_35"),
        "api_key": os.getenv("AU_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("AU_AZURE_OPENAI_ENDPOINT"),
    },
    {
        "deployment": os.getenv("US_GPT_35"),
        "api_key": os.getenv("AU_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("AU_AZURE_OPENAI_ENDPOINT"),
    },
    {
        "deployment": os.getenv("SE_GPT_35"),
        "api_key": os.getenv("SE_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("SE_AZURE_OPENAI_ENDPOINT"),
    },
    {
        "deployment": os.getenv("CH_GPT_35"),
        "api_key": os.getenv("CH_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("CH_AZURE_OPENAI_ENDPOINT"),
    },
]
gpt_4_list = [
    {
        "deployment": os.getenv("AU_GPT_4"),
        "api_key": os.getenv("AU_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("AU_AZURE_OPENAI_ENDPOINT"),
    },
    {
        "deployment": os.getenv("CH_GPT_4"),
        "api_key": os.getenv("CH_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("CH_AZURE_OPENAI_ENDPOINT"),
    },
]


def get_file_cache(
    database_path: str = str(ROOT_DIR) + "/langchain_llm_cache.db",
):
    return SQLiteCache(database_path)


# NOTE LLM 답변을 캐시하는 기능
# set_llm_cache(get_file_cache())


def _random_key_set(model_version: str) -> Dict[str, str] | None:
    if model_version == "35":
        return random.choice(gpt_35_list)
    elif model_version == "4":
        return random.choice(gpt_4_list)
    else:
        return None


def _get_azure_open_ai(
    api_data: dict,
    temperature: float,
    is_stream: bool,
    callbacks: List[BaseCallbackHandler] = [],
) -> AzureChatOpenAI:
    return AzureChatOpenAI(
        openai_api_version="2024-02-01",
        azure_deployment=api_data.get("deployment"),
        azure_endpoint=api_data.get("api_base"),
        api_key=api_data.get("api_key"),
        temperature=temperature,
        streaming=is_stream,
        callbacks=callbacks,
    )


def get_azure_gpt_chat_llm(
    model_version: str = "35",
    temperature: float = 0.2,
    is_stream: bool = True,
    callbacks: List[BaseCallbackHandler] = [],
) -> AzureChatOpenAI:
    rand_api_data = _random_key_set(model_version)
    print(rand_api_data)
    llm = _get_azure_open_ai(rand_api_data, temperature, is_stream, callbacks)

    return llm
