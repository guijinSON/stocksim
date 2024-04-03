import json

import numpy as np
import random

from langchain_core.prompts import PromptTemplate

from src.llm.azure import get_azure_gpt_chat_llm

market_event_category = ["경영", "자본금", "이익", "기술", "시장 컨센서스"]
event_data = json.loads("market_event.json")


def random_market_event_chain():
    prompt = PromptTemplate.from_template(template="""
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
{
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
}
3) **The answer must be formatted as JSON, with a key of category and only one events.**

## Your Choices is: """)
    llm = get_azure_gpt_chat_llm(model_version="35", temperature=0.0, is_stream=False)
    chain = prompt | llm
    return chain


def random_market_event():
    category = random.choice(market_event_category)
    return random.choice(event_data[category])


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
