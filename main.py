from src.chain.biz_logic import search_stock_verified

background = """
삼성전자 (005930.KS) - 삼성전자는 프로메테우스 프로젝트의 개발을 주도하며, 자사의 고성능 GPU와 NPU를 통해 AI 분야에서 기술력을 입증했습니다. 2030년 현재, 삼성은 프로메테우스를 스마트폰, 스마트 TV 등 소비자 가전 제품에 탑재해 차별화된 사용자 경험을 제공하고 있습니다. 또한, 산업용 AI 솔루션 개발에도 나서며 스마트 팩토리와 스마트 시티 분야에서 혁신을 주도하고 있습니다.

SK하이닉스 (000660.KS) - SK하이닉스는 AI 옵티마이저 프로젝트를 통해 독자적인 AGI 기술 개발에 집중하며, 메모리 반도체 설계와 AI 알고리즘을 결합하여 생산 효율성을 높이고 범용 AGI 기술 발전에 기여하고 있습니다. 현재는 프로메테우스의 발전을 지켜보며 상호 협력 가능성을 모색하고 있으며, AI 옵티마이저를 프로메테우스 수준으로 고도화하는 도전에는 시간과 노력이 필요할 것으로 예상됩니다.

네이버 (035420.KS) - 네이버의 AGI 모델 '하이퍼클로바 X'개발하여 프로메테우스와 경쟁 중이며, 성능 면에서는 아직 미흡하지만 방대한 데이터와 도메인 전문성으로 경쟁력을 갖추고 있습니다. 하이퍼클로바 X를 자사 서비스에 접목하여 혁신적인 사용자 경험을 제공하고 동시에 B2B 시장 공략을 가속화하며 글로벌 시장에진출하기 위한 계획을 세우고 있습니다.

카카오 (035720.KS) - 카카오의 AI 모델 '카카오브레인'은 현재 네이버나 프로메테우스에 비해 성능이 미흡하며, 제한된 도메인에서의 서비스만을 제공하고 있으며 AGI로의 발전 가능성은 낮아 보입니다. 카카오는 AI 기술 개발이 상대적으로 늦어진 점과 투자 규모의 한정, 인재 확보 어려움 등으로 경쟁에서 뒤처진 상황이며, 이를 극복하기 위해 공격적인 AI 투자와 인수합병을 통해 기술력과 인재 풀을 강화하고 있습니다.

LG전자 (066570.KS) - LG전자는 프로메테우스를 가전제품과 산업용 솔루션에 접목하여 세계 시장을 선도하고 있으며, 국내에서 프로메테우스의 최대 고객으로 혁신적 제품과 서비스를 출시하고 있습니다. 프로메테우스를 탑재한 엘지의 스마트 가전 제품은 사용자 행동 패턴을 학습하여 최적화된 성능과 직관적 인터페이스를 제공하며, 파트너십은 업계에서 윈-윈 전략의 모범 사례로 평가되고 있습니다.

셀바스AI (108860.KS) - 셀바스AI는 HCI 기술로 디지털 전환을 주도했지만, 프로메테우스의 등장으로 시장에서 타격을 입었고 경쟁력을 유지하기 위해 AGI 기술에 투자했으나 대형 파트너들의 전략적 파트너십으로 뒤처지기 시작했습니다. AGI의 범용성과 유연성에 비해 셀바스AI의 기술은 제한적이어서 시장에서의 점유율을 잃고 있습니다.

한글과컴퓨터 (030520.KR) - 한글과컴퓨터는 프로메테우스 AGI의 부상으로 오피스 소프트웨어 시장에서의 변화에 대응하기 위해 전략을 재조정했습니다. 기존 역량과 공공기관 및 기업 시장에서의 입지를 활용하며, 오픈 소스 커뮤니티와 협력하여 AI 기능을 플러그인으로 개발하고 '한컴구름' OS를 AGI와 연동하는 개방형 플랫폼으로 전환하고자 노력하고 있습

셀트리온 (068270.KR) - 셀트리온은 프로메테우스 AGI 기술의 도입에 대해 신중한 입장을 보이며, 의료 데이터의 민감성과 윤리적 문제를 우려하고 있습니다. 독점적 사용으로 인한 기술 격차와 접근성 문제에 대한 우려도 표명하며, 자체 연구 개발과 협력을 통해 의약품 개발에 필요한 기술을 확보하는 전략을 채택하여 환자 중심의 의료 서비스 제공을 최우선으로 삼고 있습니다.
"""

inputs = "프로메테우스의 경쟁자를 개발하는 기업은 어디인가요?"

if __name__ == "__main__":
    print(search_stock_verified(inputs=inputs, background=background))
