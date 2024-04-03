import pandas as pd
import streamlit as st

from langchain_core.callbacks import BaseCallbackHandler

from src.chain.conversation import sample_conversation_chain


class OpenAIChatMessageCallbackHandler(BaseCallbackHandler):
    message = ""
    message_box = None

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


# 메시지 저장(History 에 사용 가능)
def save_message(content: str, role: str):
    st.session_state["messages"].append(
        {
            "content": content,
            "role": role,
        }
    )


# 채팅 History 를 화면에 출력
def get_chat_history():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def streamlit_init():
    col1, col2 = st.columns([0.65, 0.35])

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["market"] = []  # 시장
        st.session_state["stocks"] = []  # 시장
        st.session_state["portfolio"] = []  # 유저 포트폴리오
        st.session_state["actions"] = []  # 유저 액션
        st.session_state["time"] = 0  # 시간

    with col1:
        with st.container(height=600):
            if len(st.session_state["messages"]) == 0:

                save_message(
                    """지난주 공개된 범용 인공지능 "PROMETHEUS"는 사회의 모든 측면에 큰 충격을 주었습니다. 해당 인공지능은 삼성전자, Naver, Google, OpenAI 등 세계 최고의 기술 기업과 연구 기관들이 협력하여 만들어졌습니다. PROMETHEUS의 등장은 의료, 교통, 에너지, 제조 등 다양한 분야에서 전례 없는 영향을 줄 것으로 기대됩니다. 하지만 이와 동시에 범용 인공지의 갑작스러운 출현은 많은 사람들에게 일자리 감소와 경제 불안정 등 불확실성과 불안감을 안겨주었습니다. 현재 국내 및 글로벌 주식 시장은 이 영향을 크게 요동치고 있으며, 전문가들은 PROMETHEUS 가 여러 산업에 미칠 장기적인 영향을 예측하기 어려워하고 있습니다.정부와 규제 기관은 AGI를 사회에 원활히 통합하기 위한 정책과 규제를 서둘러 마련하고 있습니다. 이처럼 혼란스럽고 예측 불가능한 상황 속에서, 여러분은 슬기로운 투자자로서 주식 시장의 거친 파도를 헤쳐나가야 합니다.
게임 방법:

1. 여러분은 2030년의 투자자가 되어, 아틀라스의 등장 직후 혼란스러운 주식 시장에 뛰어듭니다. 초기 자본금은 10억이 주어집니다.
2. 먼저, 투자할 종목을 조사하고 선택하여 자신만의 포트폴리오를 구성하세요. 
3. 그 다음, 게임 내에서 시간을 얼마나 진행할지 결정하세요. (예: 1일, 1주, 1달 등)
4. 여러분이 선택한 종목과 시간 경과에 따라, 인공지능 모델이 새로운 시나리오를 생성하고 주가를 조정할 것입니다.
5. 2~4단계를 게임 내 시간으로 10년이 될 때까지 반복하세요.
6. 10년 동안 여러분의 포트폴리오 가치를 최대한 높이는 것이 목표입니다. 현명한 투자 결정과 리스크 관리가 성공의 열쇠가 될 것입니다.

그럼 이제 게임을 시작하겠습니다. 검색하고 싶은 주식을 설명해주세요. 매턴 주식 조사는 한번만 가능하니 신중하게 해야합니다. (ex. PROMETHEUS 의 경쟁사를 개발 중인 회사는 누가 있어?, PROMETHEUS 개발 참여 기업, 등)"""
                    ,
                    "ai",
                )

            get_chat_history()

            if message := st.chat_input(""):
                save_message(message, "human")

                with st.chat_message("human"):
                    st.markdown(message)

                with st.chat_message("ai"):
                    save_message(
                        sample_conversation_chain(callbacks=[OpenAIChatMessageCallbackHandler()]).invoke(message), "ai")

    with col2:
        with st.container(height=300):
            st.title('Possible Actions')
            option = st.selectbox(
                "Skip Time",
                ("1Month", "6Month", "1Year", "3Years"),
                placeholder="Select time to skip.",
            )

        with st.container(height=300):
            df = pd.DataFrame(
                [
                    {"command": "삼성전자", "ratio": 5, "price": 300000},
                    {"command": "네이버", "ratio": 5, "price": 700000},
                    {"command": "카카오", "ratio": 3, "price": 300000},
                ]
            )
            edited_df = st.data_editor(df)

    # NOTE: 사용자 액션이 일어나는 것을 캐치 -> 변화가 있으면 json에 저장하기
    # NOTE: 수정 버튼 입력해서 그 버튼을 눌렀을 경우에만 해당 데이터를 파싱하는 방법으로 받아오기

    print(option)
    dict_output = df.to_dict('records')
    print(dict_output)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Stock-SIMZ",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    streamlit_init()
