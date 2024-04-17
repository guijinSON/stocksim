import random
from typing import List


def generate_stock_event(stock_names: List[str]):
    stock_event: dict = {
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
        ],
        "이벤트 없음1": [
            "", "", "", "", "", "", ""
        ]
        # "이벤트 없음2": [
        #     "", "", "", "", "", "", ""
        # ],
        # "이벤트 없음3": [
        #     "", "", "", "", "", "", ""
        # ]
        ,
        # "이벤트 없음4": [
        #     "", "", "", "", "", "", ""
        # ]
        # ,
        # "이벤트 없음5": [
        #     "", "", "", "", "", "", ""
        # ]
        # ,
        # "이벤트 없음6": [
        #     "", "", "", "", "", "", ""
        # ]
        # ,
        # "이벤트 없음7": [
        #     "", "", "", "", "", "", ""
        # ]

    }

    event_dict = {}
    for stock in stock_names:
        random_category = random.choice(list(stock_event.keys()))
        event_dict[stock] = random.choice(stock_event[random_category])
    return event_dict

def generate_env_event():
    env_event = {
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
        "사회": [
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
        ],
        "이벤트 없음1": [
            "", "", "", "", "", "", ""
        ],
        "이벤트 없음2": [
            "", "", "", "", "", "", ""
        ],
        # "이벤트 없음3": [
        #     "", "", "", "", "", "", ""
        # ]
        # ,
        # "이벤트 없음4": [
        #     "", "", "", "", "", "", ""
        # ]
        # ,
        # "이벤트 없음5": [
        #     "", "", "", "", "", "", ""
        # ]
        # ,
        # "이벤트 없음6": [
        #     "", "", "", "", "", "", ""
        # ]
        # ,
        # "이벤트 없음7": [
        #     "", "", "", "", "", "", ""
        # ]
    }
    random_category = random.choice(list(env_event.keys()))
    random_event = random.choice(env_event[random_category])
    return random_event