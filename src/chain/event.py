import json

import numpy as np
import random

from src.config.settings import get_path_join, OTHERS_DIR
from src.llm.azure import get_azure_gpt_chat_llm
from src.prompt.load_prompt import load_prompt


def random_market_event_chain():
    _prompt = load_prompt("random_market_event")
    llm = get_azure_gpt_chat_llm(model_version="4", temperature=0.0, is_stream=False)
    _chain = _prompt | llm
    return _chain


def random_stock_event_chain():
    _prompt = load_prompt("random_stock_event")
    llm = get_azure_gpt_chat_llm(model_version="4", temperature=0.0, is_stream=False)
    _chain = _prompt | llm
    return _chain


def random_market_event():
    _market_event_category = [
        "정치",
        "기업",
        "경제",
        "기술",
        "자연재해",
        "사회",
        "국제",
    ]
    _market_event_data = json.loads(get_path_join(OTHERS_DIR, "market_event.json"))
    _category = random.choice(_market_event_category)
    return random.choice(_market_event_data[_category])


def random_stock_event():
    _stock_event_category = ["경영", "자본금", "이익", "기술", "시장 컨센서스"]
    _event_data = json.loads(get_path_join(OTHERS_DIR, "stock_event.json"))
    _category = random.choice(_stock_event_category)
    return random.choice(_event_data[_category])


def market_event_happen(t):
    linear_part_max, A, B, C = 0.3, 0.05, np.pi / 30, 1
    market = (t / 120) * linear_part_max + A * np.sin(B * t + C)
    if random.random() < market:
        return True
    else:
        return False


def related_macro_event_happen(t):
    average_value, A, B, C = 0.1, 0.05, np.pi / 30, 10
    rmacro = average_value + A * np.sin(B * t + C)
    if random.random() < rmacro:
        return True
    else:
        return False


def unrelated_macro_event_happen(t):
    average_value, A, B, C = 0.15, 0.01, np.pi / 30, 5
    urmacro = average_value + A * np.sin(B * t + C)
    if random.random() < urmacro:
        return True
    else:
        return False
