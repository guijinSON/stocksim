from typing import List

import pandas as pd
import streamlit as st
START_SYSTEM_TIME = '2050-09-26'
STOCK_NAMES = ["삼성전자", "네이버", "카카오"]

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
    return now + st.session_state["system_time"]

def set_data_frame_by_system_price(new_date_time: str, stock_names: List[str], new_prices: List[int]):
    data = st.session_state["stock_price_df_data"]
    print("기존 stock_price_df:", data)
    print("입력받은 요소:", new_date_time, stock_names, new_prices)
    data['date_times'] += [new_date_time for _ in range(len(stock_names))]
    data['stocks'] += stock_names
    data['prices'] += new_prices
    st.session_state["stock_price_df_data"] = data

def get_data_frame_by_system_price():
    data = st.session_state["stock_price_df_data"]
    # 데이터 프레임 생성
    df = pd.DataFrame(data)
    df['date_times'] = pd.to_datetime(df['date_times']).dt.date

    print(df)

    # 피벗 테이블 생성
    pivot_df = df.pivot(index='stocks', columns='date_times', values='prices')
    st.session_state["re_render_flag"] = False
    return pivot_df

def get_data_frame_by_user_portfolio():
    stocks = STOCK_NAMES
    portfolio_df = pd.DataFrame(data=[st.session_state["portfolio_df_data"]], columns=stocks)
    return portfolio_df.reset_index(drop=True)
