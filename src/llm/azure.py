import os
import random
from typing import Dict

from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv

load_dotenv()

gpt_35_list = [
    {
        "deployment": os.getenv("AU_GPT_35"),
        "api_key": os.getenv("AU_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("AU_AZURE_OPENAI_ENDPOINT")
    },
    {
        "deployment": os.getenv("US_GPT_35"),
        "api_key": os.getenv("AU_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("AU_AZURE_OPENAI_ENDPOINT")
    },
    {
        "deployment": os.getenv("SE_GPT_35"),
        "api_key": os.getenv("SE_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("SE_AZURE_OPENAI_ENDPOINT")
    },
    {
        "deployment": os.getenv("CH_GPT_35"),
        "api_key": os.getenv("CH_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("CH_AZURE_OPENAI_ENDPOINT")
    }
]
gpt_4_list = [
    {
        "deployment": os.getenv("AU_GPT_4"),
        "api_key": os.getenv("AU_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("AU_AZURE_OPENAI_ENDPOINT")
    },
    {
        "deployment": os.getenv("CH_GPT_4"),
        "api_key": os.getenv("CH_AZURE_OPENAI_API_KEY"),
        "api_base": os.getenv("CH_AZURE_OPENAI_ENDPOINT")
    },
]


def _random_key_set(model_version: str) -> Dict[str, str] | None:
    if model_version == "35":
        return random.choice(gpt_35_list)
    elif model_version == "4":
        return random.choice(gpt_4_list)
    else:
        return None


def _get_azure_open_ai(api_data: dict, temperature: float, is_stream: bool) -> AzureChatOpenAI:
    return AzureChatOpenAI(
        openai_api_version="2024-02-01",
        azure_deployment=api_data.get("deployment"),
        azure_endpoint=api_data.get("api_base"),
        api_key=api_data.get("api_key"),
        temperature=temperature,
        streaming=is_stream,
    )


def get_azure_gpt_chat_llm(model_version: str = "35", temperature: float = 0.2,
                           is_stream: bool = True) -> AzureChatOpenAI:
    is_ready = False
    llm = None
    while (is_ready == False):
        rand_api_data = _random_key_set(model_version)
        llm = _get_azure_open_ai(rand_api_data, temperature, is_stream)
        response = llm.invoke("health-check")
        if response.content:
            is_ready = True

    return llm
