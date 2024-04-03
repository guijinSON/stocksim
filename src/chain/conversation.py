# 사용자와의 대화를 나누는 Chain
from typing import List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.llm.azure import get_azure_gpt_chat_llm
from src.prompt.load_prompt import load_prompt
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate, ChatPromptTemplate


def sample_conversation_chain(callbacks: List[BaseCallbackHandler] = [], ):
    prompt = load_prompt("base_chat")
    llm = get_azure_gpt_chat_llm(model_version="35", callbacks=callbacks)
    return {"inputs": RunnablePassthrough()} | prompt | llm


def search_stock(inputs: str, background: str):
    prompt = PromptTemplate.from_template("""
# Persona
You are fictional story simulator. Today is 2030 and an AGI called prometheus has been developed. Given the background answer the user's questions. You may add with your imagination. However, you may not introduce new companies other then the ones provided. Always answer in formal Korean. 

### Background: 
{background}

### User Question: {inputs}
### Response:
""")
    llm = get_azure_gpt_chat_llm(model_version="4")
    chain = {"inputs": RunnablePassthrough(), "background": RunnablePassthrough()} | prompt | llm
    response = chain.invoke({"inputs": inputs, "background": background})
    print(response.__dict__)
    return response
