from typing import List

import pandas as pd
import streamlit as st

START_SYSTEM_TIME = '2030-09-26'
STOCK_NAMES = ["삼성전자", "SK하이닉스", "네이버", "카카오", "셀바스AI", "한글과컴퓨터"]


def get_step_for_step_progress(step: str):
    ret = 0
    if step == "STEP1":
        ret = 1
    elif step == "STEP2":
        ret = 2
    elif step == "STEP3":
        ret = 3
    return ret


def get_now_time_by_user_input_time(now: int, user_input_time: str):
    if user_input_time == "1Month":
        now += 1
    elif user_input_time == "6Month":
        now += 6
    elif user_input_time == "1Year":
        now += 12
    elif user_input_time == "3Years":
        now += 36
    st.session_state["system_time"] = now
    return now


def get_data_frame_by_system_price():
    data = st.session_state["stock_price_df_data"]
    # 데이터 프레임 생성
    df = pd.DataFrame(data)
    df['date_times'] = pd.to_datetime(df['date_times']).dt.date

    # 피벗 테이블 생성
    pivot_df = df.pivot(index='stocks', columns='date_times', values='prices')
    st.session_state["re_render_flag"] = False
    return pivot_df


def set_data_frame_by_system_price(new_date_time: str, stock_names: List[str], new_prices: List[int]):
    data = st.session_state["stock_price_df_data"]
    data['date_times'] += [new_date_time for _ in range(len(stock_names))]
    data['stocks'] += stock_names
    data['prices'] += new_prices
    st.session_state["stock_price_df_data"] = data


def get_data_frame_by_user_portfolio():
    stocks = STOCK_NAMES
    portfolio_df = pd.DataFrame(data=[st.session_state["portfolio_ratio_list"]], columns=stocks)
    return portfolio_df.reset_index(drop=True)


def set_portfolio_df_data():
    portfolio_editable_df = st.session_state["portfolio_df"]
    tmp_result = [{"종목": column, "비율": int(portfolio_editable_df[column].values[0])} for column in
                  portfolio_editable_df.columns]
    st.session_state["portfolio_ratio_list"] = portfolio_editable_df.iloc[0].tolist()

    result = {}
    for tmp in tmp_result:
        result[tmp["종목"]] = tmp["비율"]
    return result


def set_balloons(count: int = 0):
    for i in range(count):
        st.balloons()


def set_snow(count: int = 0):
    for i in range(count):
        st.snow()
