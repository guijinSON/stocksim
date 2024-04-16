import uuid

import pandas as pd
import streamlit as st

from src.utils.chat import (
    get_game_story, get_user_input, get_game_initial_background
)
from src.utils.ui import set_data_frame_by_system_price, START_SYSTEM_TIME, STOCK_NAMES, get_step_for_step_progress, \
    get_data_frame_by_user_portfolio, get_data_frame_by_system_price


def get_chat_history():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def streamlit_init():
    col1, col2 = st.columns([0.65, 0.35])

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state[
            "background"
        ] = get_game_initial_background()
        st.session_state["market"] = []  # 시장
        st.session_state["stocks"] = []  # 시장
        st.session_state["actions"] = []  # 유저 액션
        st.session_state["system_time"] = 0  # 시간 -> 개월수로 처리
        st.session_state["user_input_time"] = ""  # 유저 입력 시간
        st.session_state["stock_info"] = 0  # 유저 포트폴리오 정보
        st.session_state["stock_info_df"] = 0  # 유저 포트폴리오 정보
        st.session_state["status"] = "STEP1"
        st.session_state["prices"] = [300000, 700000, 40000]
        st.session_state["portfolio_df_data"] = [50, 25, 25]  # 유저 포트폴리오
        st.session_state["stock_price_df_data"] = {
            'date_times': [],
            'stocks': [],
            'prices': [],
        }
        set_data_frame_by_system_price(START_SYSTEM_TIME, STOCK_NAMES, st.session_state["prices"])

    count_for_key = 0
    with col1:
        with st.container(height=1000):
            # NOTE 임의로 세션 ID 생성(서버측으로 전송은 하고 있지 않음)
            # TODO 신규 사용자라면 새로 생성해주고, 기존 사용자라면 입력받고 Chat history 불러올 수 있도록 구현해야
            session_id = uuid.uuid4()
            st.write(f"게임ID: {session_id}")
            with st.chat_message("ai"):
                st.markdown(get_game_story())
            get_user_input(count_for_key=count_for_key + 1)

    with col2:
        on = st.toggle(label="진행상황 보기")
        if on:
            with st.container(height=220):
                st.subheader("진행상황")
                st.write(f'흐른시간: {st.session_state["system_time"]}개월')

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

        with st.container(height=300):
            st.subheader("유저 액션")

            st.write("2단계에 수행하세요.")
            option = st.selectbox(
                "스킵할 시간을 선택하세요.",
                ("1Month", "6Month", "1Year", "3Years"),
                placeholder="Select time to skip.",
            )
            st.session_state["user_input_time"] = option

            portfolio_df = get_data_frame_by_user_portfolio()
            st.session_state["portfolio_df"] = st.data_editor(portfolio_df)

        with st.container(height=350):
            st.subheader("주식 가격 히스토리")
            # new_date = pd.to_datetime(START_SYSTEM_TIME) + pd.DateOffset(months=st.session_state["system_time"])
            stock_price_df = get_data_frame_by_system_price()
            st.dataframe(stock_price_df)

        with st.container(height=500):
            st.write(st.session_state["background"])
            # print(edited_df.to_dict('records'))

    # NOTE: 사용자 액션이 일어나는 것을 캐치 -> 변화가 있으면 json에 저장하기
    # NOTE: 수정 버튼 입력해서 그 버튼을 눌렀을 경우에만 해당 데이터를 파싱하는 방법으로 받아오기

    # print(option)
    # dict_output = df.to_dict('records')
    # print(dict_output)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Stock-SIMZ",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    streamlit_init()
