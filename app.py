import streamlit as st
import pandas as pd
import numpy as np
import random
from openai import OpenAI
import time
# from response import start_prompt
from response import response_generator
# Streamed response emulator

st.title('Stock-SIMZ')

col1, col2 = st.columns([0.65,0.35])

with col1:
    with st.container(height=600):
        # Initialize chat history
        client = OpenAI(api_key="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")
        
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
        
            with st.chat_message("assistant"):

                if prompt =='게임시작':
                    response = st.write_stream(response_generator(prompt))
                        
                else:
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
with col2:
    with st.container(height=300):
        st.title('Possible Actions')
    with st.container(height=300):
        st.title('Portfolio Stats')