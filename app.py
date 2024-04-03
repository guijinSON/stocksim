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
                    "안녕하세요. 무엇을 도와드릴까요?",
                    "ai",
                )

            get_chat_history()

            if message := st.chat_input(""):
                save_message(message, "human")

                with st.chat_message("human"):
                    st.markdown(message)

                with st.chat_message("ai"):
                    save_message(sample_conversation_chain(callbacks=[OpenAIChatMessageCallbackHandler()]).invoke(message), "ai")

    with col2:
        with st.container(height=300):
            st.title('Possible Actions')

        with st.container(height=300):
            st.title('Portfolio Stats')


if __name__ == "__main__":
    st.set_page_config(
        page_title="Stock-SIMZ",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    streamlit_init()
