import time
from typing import Optional

import pandas as pd

from repositories.file_repository import FileRepository
from src.chain import biz_logic
import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler

from src.config import settings
from src.utils.ui import get_now_time_by_user_input_time, START_SYSTEM_TIME, STOCK_NAMES, \
    set_data_frame_by_system_price, get_portfolio_df_data


def get_game_story():
    return (
        """
        #### 게임 스토리
        지난주 공개된 범용 인공지능 "PROMETHEUS"는 사회의 모든 측면에 큰 충격을 주었습니다.  
        해당 인공지능은 삼성전자, Naver, Google, OpenAI 등 세계 최고의 기술 기업과 연구 기관들이 협력하여 만들어졌습니다.   
        PROMETHEUS의 등장은 의료, 교통, 에너지, 제조 등 다양한 분야에서 전례 없는 영향을 줄 것으로 기대됩니다.  
        하지만 이와 동시에 범용 인공지의 갑작스러운 출현은 많은 사람들에게 일자리 감소와 경제 불안정 등 불확실성과 불안감을 안겨주었습니다.   
        현재 국내 및 글로벌 주식 시장은 이 영향을 크게 요동치고 있으며, 전문가들은 PROMETHEUS 가 여러 산업에 미칠 장기적인 영향을 예측하기 어려워하고 있습니다.  
        정부와 규제 기관은 AGI를 사회에 원활히 통합하기 위한 정책과 규제를 서둘러 마련하고 있습니다.  
        이처럼 혼란스럽고 예측 불가능한 상황 속에서, 여러분은 슬기로운 투자자로서 주식 시장의 거친 파도를 헤쳐나가야 합니다.  
        
        ---
        
        #### 게임 방법:
        1. 여러분은 2030년의 투자자가 되어, 아틀라스의 등장 직후 혼란스러운 주식 시장에 뛰어듭니다. 초기 자본금은 10억이 주어집니다.
        2. 먼저, 투자할 종목을 조사하고 선택하여 자신만의 포트폴리오를 구성하세요. 
        3. 그 다음, 게임 내에서 시간을 얼마나 진행할지 결정하세요. (예: 1일, 1주, 1달 등)
        4. 여러분이 선택한 종목과 시간 경과에 따라, 인공지능 모델이 새로운 시나리오를 생성하고 주가를 조정할 것입니다.
        5. 2~4단계를 게임 내 시간으로 10년이 될 때까지 반복하세요.
        6. 10년 동안 여러분의 포트폴리오 가치를 최대한 높이는 것이 목표입니다. 현명한 투자 결정과 리스크 관리가 성공의 열쇠가 될 것입니다.
        
        ---
        
        그럼 이제 게임을 시작하겠습니다. 검색하고 싶은 주식을 설명해주세요. 
        매 턴마다 주식 조사는 한번만 가능하니 신중하게 해야합니다. (ex. PROMETHEUS 의 경쟁사를 개발 중인 회사는 뭐가 있어?, PROMETHEUS 개발 참여 기업, 등)
        """
    )


def get_game_initial_background():
    return (
        """
    삼성전자 (005930.KS) - 삼성전자는 프로메테우스 프로젝트의 개발을 주도하며, 자사의 고성능 GPU와 NPU를 통해 AI 분야에서 기술력을 입증했습니다. 2030년 현재, 삼성전자는 프로메테우스를 스마트폰, 스마트 TV 등 소비자 가전 제품에 탑재해 차별화된 사용자 경험을 제공하고 있습니다. 또한, 산업용 AI 솔루션 개발에도 나서며 스마트 팩토리와 스마트 시티 분야에서 혁신을 주도하고 있습니다.
    
    SK하이닉스 (000660.KS) - SK하이닉스는 AI 옵티마이저 프로젝트를 통해 독자적인 AGI 기술 개발에 집중하며, 메모리 반도체 설계와 AI 알고리즘을 결합하여 생산 효율성을 높이고 범용 AGI 기술 발전에 기여하고 있습니다. 현재는 프로메테우스의 발전을 지켜보며 상호 협력 가능성을 모색하고 있으며, AI 옵티마이저를 프로메테우스 수준으로 고도화하는 도전에는 시간과 노력이 필요할 것으로 예상됩니다.
    
    네이버 (035420.KS) - 네이버의 AGI 모델 '하이퍼클로바 X'개발하여 프로메테우스와 경쟁 중이며, 성능 면에서는 아직 미흡하지만 방대한 데이터와 도메인 전문성으로 경쟁력을 갖추고 있습니다. 하이퍼클로바 X를 자사 서비스에 접목하여 혁신적인 사용자 경험을 제공하고 동시에 B2B 시장 공략을 가속화하며 글로벌 시장에진출하기 위한 계획을 세우고 있습니다.
    
    카카오 (035720.KS) - 카카오의 AI 모델 '카카오브레인'은 현재 네이버나 프로메테우스에 비해 성능이 미흡하며, 제한된 도메인에서의 서비스만을 제공하고 있으며 AGI로의 발전 가능성은 낮아 보입니다. 카카오는 AI 기술 개발이 상대적으로 늦어진 점과 투자 규모의 한정, 인재 확보 어려움 등으로 경쟁에서 뒤처진 상황이며, 이를 극복하기 위해 공격적인 AI 투자와 인수합병을 통해 기술력과 인재 풀을 강화하고 있습니다.
    
    셀바스AI (108860.KS) - 셀바스AI는 HCI 기술로 디지털 전환을 주도했지만, 프로메테우스의 등장으로 시장에서 타격을 입었고 경쟁력을 유지하기 위해 AGI 기술에 투자했으나 대형 파트너들의 전략적 파트너십으로 뒤처지기 시작했습니다. AGI의 범용성과 유연성에 비해 셀바스AI의 기술은 제한적이어서 시장에서의 점유율을 잃고 있습니다.
    
    한글과컴퓨터 (030520.KR) - 한글과컴퓨터는 프로메테우스 AGI의 부상으로 오피스 소프트웨어 시장에서의 변화에 대응하기 위해 전략을 재조정했습니다. 기존 역량과 공공기관 및 기업 시장에서의 입지를 활용하며, 오픈 소스 커뮤니티와 협력하여 AI 기능을 플러그인으로 개발하고 '한컴구름' OS를 AGI와 연동하는 개방형 플랫폼으로 전환하고자 노력하고 있습니다.
        """
    )


class OpenAIChatMessageCallbackHandler(BaseCallbackHandler):
    message = ""
    message_box = None

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()
        # self.message_box = st.chat_message("ai")

    def on_llm_end(self, *args, **kwargs):
        append_ai_message(self.message)

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


class StreamlitChatService:
    def __init__(self, session_id):
        self._session_id = session_id
        self._file_repo = FileRepository(settings.LOGS_DIR)
        self._file_name = f"{self._session_id}.logs"
        print("서비스 생성")

    def check_is_stock_verified_question(self, message_content: str):
        message = biz_logic.search_stock_verified(message_content)
        return message.content == "[YES]"

    def write_logs(self, log_content: str, ai_response: Optional[str] = None):
        print(log_content)
        self._file_repo.create_or_append_file(self._file_name, log_content)
        if ai_response:
            self._file_repo.create_or_append_file(self._file_name, f'"""\n{ai_response}\n"""')

    def step1_check_stock_question(self, message_content: str):
        self.write_logs(f"STEP1: 주식관련 질문이 입력되었는지 확인합니다.")
        # 명령어 작성 및 명령어에 따른 동작 설정 가능
        is_stock_verified_question = self.check_is_stock_verified_question(message_content)
        if is_stock_verified_question:
            with st.chat_message("ai"):
                st.markdown("주식관련 질문을 해주셨군요!")
            response = biz_logic.search_stock(
                inputs=message_content,
                background=st.session_state["background_history"][-1],
                callbacks=[OpenAIChatMessageCallbackHandler()]
            )
            self.write_logs(f"STEP1: 주식관련 질문이 입력되었습니다. 조사결과:", response)
            st.session_state["stock_search_history"].append(response)
            st.session_state["status"] = "STEP2"

        else:
            self.write_logs(f"STEP1: 주식관련 질문이 입력되지 않아, 다시 요청합니다.")
            with st.chat_message("ai"):
                st.markdown("주식관련 질문으로 먼저 정보를 얻어보세요. 주식 관련 질문은 한 턴에 한 번 밖에 할 수 없으므로 신중하게 하셔야합니다.")
            st.session_state["status"] = "STEP1"

    def step2_update_new_story(self, message_content: str):
        if message_content != "확인했습니다.":
            with st.chat_message("ai"):
                st.markdown("유저 액션에서 스킵할 시간과 포트폴리오를 조정한 후, '확인했습니다.'를 입력해주세요.")
            return

        portfolio_dict_data = get_portfolio_df_data()
        if sum(st.session_state["portfolio_df_data"]) != 100:
            with st.chat_message("ai"):
                st.markdown("각각의 포트폴리오 비율의 합은 100이 되어야 합니다.")
            return

        stock_prices = st.session_state["stock_price_df_data"]['prices']
        stock_prices_for_prompt = list(zip(STOCK_NAMES, st.session_state["portfolio_df_data"]))
        with st.chat_message("ai"):
            st.markdown(f'선택하신 스킵 시간은 {st.session_state["user_input_time"]}, 포트폴리오는 {stock_prices_for_prompt}입니다.')

        new_plot = biz_logic.update_story(
            time=st.session_state["user_input_time"],
            background=st.session_state["background_history"][-1],
            callbacks=[OpenAIChatMessageCallbackHandler()],
        )
        st.session_state["plot_history"].append(new_plot)
        self.write_logs(f"STEP2-1: plot 갱신. new_plot:", st.session_state["plot_history"][-1])

        new_background = biz_logic.update_background(
            background=st.session_state["background_history"][-1], new_plot=st.session_state["plot_history"][-1]
        )
        st.session_state["background_history"].append(new_background)
        self.write_logs(f"STEP2-2: background 갱신. new_background:", st.session_state["background_history"][-1])

        st.session_state["system_time"] = get_now_time_by_user_input_time(st.session_state["system_time"],
                                                                          st.session_state["user_input_time"])
        new_stock_price = biz_logic.update_stock_price(
            background=st.session_state["background_history"][-1],
            new_plot=st.session_state["plot_history"][-1],
            elapsed_time=st.session_state["user_input_time"],
            price=str(stock_prices),
        )
        st.session_state["stock_price_history"].append(new_stock_price)
        self.write_logs(f"STEP2-3: 가격 갱신. new_stock_price:", st.session_state["stock_price_history"][-1])

        new_date = (pd.to_datetime(START_SYSTEM_TIME) + pd.DateOffset(months=st.session_state["system_time"])).strftime(
            '%Y-%m-%d')
        # TODO: 가격 변경하기 -> st.session_state["prices"]
        set_data_frame_by_system_price(new_date, STOCK_NAMES, st.session_state["prices"])

        st.session_state["status"] = "STEP3"

    def step3_full_step_done(self, message_content: str):
        if message_content == "계속 진행하겠습니다.":
            with st.chat_message("ai"):
                st.markdown("단계가 마무리 되었습니다. '계속 진행하겠습니다.'를 입력해주세요.")
            return
        else:
            with st.chat_message("ai"):
                st.markdown("처음 단계로 돌아가서 주식 조사를 시작해주세요.")
            st.session_state["status"] = "STEP1"
            return

    def get_user_input(self):
        message = st.chat_input("Say something", disabled=False, key=self._session_id)
        self.write_logs(f'현재 스텝: {st.session_state["status"]}')
        if message:
            match st.session_state["status"]:
                case "STEP1":
                    self.step1_check_stock_question(message_content=message)
                    # with st.spinner('Wait for it...'):
                    #     time.sleep(3)
                case "STEP2":
                    self.step2_update_new_story(message_content=message)
                    # with st.spinner('Wait for it...'):
                    #     time.sleep(5)
                case "STEP3":
                    self.step3_full_step_done(message_content=message)
        # for message in st.session_state["messages"]:
        #     with st.chat_message(message["role"]):
        #         st.markdown(message["content"])


# 메시지 저장(History 에 사용 가능)
def append_ai_message(content: str):
    st.session_state["messages"].append(
        {
            "content": content,
            "role": "ai",
        }
    )


def append_user_message(content: str):
    st.session_state["messages"].append(
        {
            "content": content,
            "role": "human",
        }
    )
