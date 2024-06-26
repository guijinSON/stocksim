import json
import os

import numpy as np
import random

from langchain_core.prompts import PromptTemplate

from src.config.settings import get_path_join, OTHERS_DIR, PROMPT_DIR
from src.llm.azure import get_azure_gpt_chat_llm
from src.prompt.load_prompt import load_prompt


def random_market_event_chain():
    _prompt = PromptTemplate.from_template(
        """
# Persona
You need to choose a stock market event that is specifically relevant to the stock.
Subject to the following conditions, you must unconditionally follow instructions

## Condition
1) First, choose a category from the five below.
    - 정치	
    - 기업	
    - 경제	
    - 기술	
    - 자연재해	
    - 사회	
    - 국제
    
2) Then, choose an event from the category you selected.
"정치": [
    "전쟁 발생",
    "대통령 당선",
    "대통령 서거",
    "국채 발행",
    "국제 금융 기관 차입",
    "세율 인상"
],
"기업": [
    "주가 조작",
    "부도",
    "합병"
],
"경제": [
    "실업률 증가",
    "GDP 성장률 둔화",
    "소비자 물가 지수 상승",
    "금융 기관 파산",
    "은행 부도",
    "중앙 은행 이자율 증가",
    "중앙 은행 금리 인상",
    "인구 감소"
],
"기술": [
    "전쟁 무기 개발"
],
"자연재해": [
    "지진",
    "홍수",
    "태풍",
    "감염병"
],
"사회":[
    "대규모 시위",
    "테러"
],
"국제": [
    "관세 부과",
    "무역 협상 결렬",
    "국제 무역 제약",
    "국가 협약 체결",
    "정상회담 개최",
    "연준 금리 결정"
]

3) **The answer must be formatted as JSON, with a key of category and only one events.**

## Your Choices is: """
    )
    _llm = get_azure_gpt_chat_llm(model_version="4", temperature=0.0, is_stream=False)
    _chain = _prompt | _llm
    return _chain


def random_stock_event_chain():
    _prompt = PromptTemplate.from_template(
        """
# Persona
You need to choose a stock market event that is specifically relevant to the market.
Subject to the following conditions, you must unconditionally follow instructions


## Condition
1) First, choose a category from the five below.
    - 경영
    - 자본금
    - 이익
    - 기술
    - 시장 컨센서스
    
2) Then, choose an event from the category you selected.
  "경영": [
    "경영권 분쟁",
    "잦은 상호 변경",
    "사업 분할",
    "임금 체불",
    "경영진 구속",
    "대주주 장내 매도",
    "경영권 이전",
    "워크아웃 돌입",
    "회생 절차 개시",
    "자회사 매각",
    "자회사 지분 취득",
    "M&A(합병)",
    "횡령 배임",
    "분식 회계",
    "영업 정지",
    "과징금 부과",
    "소송 패소",
    "상장폐지"
  ],
  "자본금": [
    "유상증자",
    "무상 감자",
    "무상 증자",
    "제3자 배정 유상증자",
    "전환사채 발행",
    "전환사채 신규상장",
    "자본 잠식"
  ],
  "이익": [
    "적자 전환",
    "적자폭 확대",
    "적자폭 감소",
    "흑자 전환",
    "영업이익 증가",
    "실적 둔화",
    "어닝 서프라이즈",
    "어닝 쇼크"
  ],
  "기술": [
    "기술 개발 성공",
    "기술 이전",
    "신제품 개발",
    "신규 사업 진출",
    "신규 수주",
    "해외 시장 진출",
    "해외 법인 철회",
    "신기술 개발 실패",
    "기술 이전 철회",
    "대규모 리콜",
    "사업 협력 MOU",
    "대규모 설비 투자"
  ],
  "시장 컨센서스": [
    "목표가 상향",
    "목표가 하향",
    "공매도 잔고 증가",
    "공매도 잔고 감소",
    "52주 신고가",
    "52주 신저가"
  ]

3) **The answer must be formatted as JSON, with a key of category and only one events.**

## Your Choices is: """
    )
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


if __name__ == "__main__":
    random_stock_event_chain().invoke({})
