import uuid

import pandas as pd
import streamlit as st

from src.utils.chat import (
    get_game_story, get_game_initial_background, StreamlitChatService
)
from src.utils.ui import set_data_frame_by_system_price, START_SYSTEM_TIME, STOCK_NAMES, get_step_for_step_progress, \
    get_data_frame_by_user_portfolio, get_data_frame_by_system_price, set_balloons, set_snow


def get_chat_history():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def streamlit_init():
    if 'session_key' not in st.session_state:
        # 세션 키로 UUID 또는 현재 시각을 사용합니다.
        st.session_state['session_key'] = str(uuid.uuid4())
        st.session_state['service'] = StreamlitChatService(str(uuid.uuid4()))

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state[
            "background_history"
        ] = [get_game_initial_background(), ]
        st.session_state["prices"] = [351100, 523000, 302400, 12800, 187100, 82900]
        st.session_state[
            "stock_price_history"
        ] = [st.session_state["prices"]]
        st.session_state[
            "roi_history"
        ] = [0, ]
        st.session_state["stock_search_history"] = []  # 초기 유저 포트폴리오
        st.session_state["market"] = []  # 시장
        st.session_state["stocks"] = []  # 시장
        st.session_state["actions"] = []  # 유저 액션
        st.session_state["system_time"] = 59  # 시간 -> 개월수로 처리
        st.session_state["system_time_end"] = 60  # 시간 -> 개월수로 처리
        st.session_state["user_input_time"] = ""  # 유저 입력 시간
        st.session_state["stock_info"] = 0  # 유저 포트폴리오 정보
        st.session_state["stock_info_df"] = 0  # 유저 포트폴리오 정보
        st.session_state["status"] = "STEP1"
        st.session_state["portfolio_ratio_list"] = [0, 0, 0, 0, 0, 0]  # 초기 유저 포트폴리오
        st.session_state["user_cash"] = 50000000
        st.session_state["portfolio_df"] = None  # 초기 유저 포트폴리오
        st.session_state["stock_price_df_data"] = {
            'date_times': [],
            'stocks': [],
            'prices': [],
        }
        st.session_state["init_investment"] = 100000000
        st.session_state["total_investment"] = st.session_state["init_investment"]
        st.session_state["final_roi"] = 0
        st.session_state["ending_story"] = ""
        set_data_frame_by_system_price(START_SYSTEM_TIME, STOCK_NAMES, st.session_state["prices"])

    # TODO 신규 사용자라면 새로 생성해주고, 기존 사용자라면 입력받고 Chat history 불러올 수 있도록 구현해야
    col1, col2 = st.columns([0.35, 0.65])
    with col1:
        with st.container(height=280):
            st.markdown("##### 진행상황\n")
            st.markdown(f'###### 흐른시간: {st.session_state["system_time"]}개월 / 60개월 (5년)')

            step = get_step_for_step_progress(st.session_state["status"])
            data_df = pd.DataFrame(
                {
                    "step": [step],
                }
            )

            st.data_editor(
                data_df,
                column_config={
                    "step": st.column_config.ProgressColumn(
                        "현재 진행중인 단계",
                        width="large",
                        help="The sales volume in USD",
                        format="%f단계",
                        min_value=0,
                        max_value=4,
                    ),
                },
                hide_index=True,
            )

            st.markdown(f"현재 주식 자본금: {st.session_state['total_investment']}원")
            st.markdown(f"라운드 수익률: {st.session_state['roi_history'][-1]}%")

        with st.container(height=330):
            st.markdown("##### 유저 액션")

            st.write("2단계에 수행하는 작업입니다. 스킵할 시간을 정하고, 포트폴리오의 비율 총합을 100으로 설정해주세요.")
            option = st.selectbox(
                "스킵할 시간을 선택하세요.",
                ("1Month", "6Month", "1Year", "3Years"),
                placeholder="Select time to skip.",
            )
            st.session_state["user_input_time"] = option

            portfolio_df = get_data_frame_by_user_portfolio()
            st.session_state["portfolio_df"] = st.data_editor(portfolio_df)

        with st.container(height=330):
            st.markdown("##### 주식가격 히스토리")
            stock_price_df = get_data_frame_by_system_price()
            st.dataframe(stock_price_df)

        with st.container(height=500):
            st.markdown("##### 배경설명 히스토리")
            for background_content in st.session_state["background_history"]:
                st.write(background_content + "\n\n------------------------------------\n\n")

    with col2:
        # TODO: 흐른 시간 확인 -> 게임 종료조건 확인
        if (
                st.session_state["system_time"] >= st.session_state["system_time_end"]
                and st.session_state["status"] == "STEP1"
        ):
            st.markdown(f"### 최종 자본: {st.session_state['total_investment']}")
            st.markdown(f"### 최종 수익률: {st.session_state['final_roi']}")
            st.markdown(f"---")
            st.markdown(f"### 엔딩 스토리")
            st.markdown(f"{st.session_state['ending_story']}")


            if st.session_state['final_roi'] > 0:
                set_balloons(4)
            elif st.session_state['final_roi'] > 100:
                set_balloons(8)
            elif st.session_state['final_roi'] > 200:
                set_balloons(16)
            if st.session_state['final_roi'] < 0:
                set_snow(4)
            elif st.session_state['final_roi'] < -50:
                set_snow(8)
            elif st.session_state['final_roi'] < -100:
                set_snow(16)


        else:
            with st.container(height=1000):
                # NOTE 임의로 세션 ID 생성(서버측으로 전송은 하고 있지 않음)
                with st.chat_message("ai"):
                    st.markdown(get_game_story())
                st.session_state['service'].get_user_input()

            with st.container(height=500):
                st.subheader("대화 히스토리")
                for message in st.session_state["messages"]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])


if __name__ == "__main__":
    st.set_page_config(
        page_title="Stock-SIMZ",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    streamlit_init()
