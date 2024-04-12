from langchain_community.embeddings.cohere import CohereEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings

"""
Embeddings
1) User Query
2) Input Documents 
2가지에 대한 Embedding 이 활용되어야 하므로 많은 테스트가 필요
"""


def get_openai_embedding_model():
    return OpenAIEmbeddings(
        model="gpt-3.5-turbo",
        tiktoken_enabled=True,
        tiktoken_model_name="gpt-3.5-turbo",
    )


def get_azure_openai_embedding_model():
    return OpenAIEmbeddings(
        model="gpt-4",
        tiktoken_enabled=True,
        tiktoken_model_name="gpt-3.5-turbo",
    )


def get_cohere_embedding_model():
    return CohereEmbeddings(
        model="all",
        max_retries=3,
        request_timeout=2,
        user_agent="langchain",
    )
