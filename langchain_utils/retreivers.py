from langchain_community.retrievers.wikipedia import WikipediaRetriever
from langchain_community.retrievers.elastic_search_bm25 import (
    ElasticSearchBM25Retriever,
)
from langchain_community.retrievers.milvus import MilvusRetriever  # Milvus VectorDB
from langchain_community.agent_toolkits.sql import toolkit as sql_toolkit
from langchain_community.agent_toolkits.github import toolkit as github_toolkit
from langchain_community.utilities.python import PythonREPL
from langchain_experimental.synthetic_data.prompts import SENTENCE_PROMPT

wikipedia_retriever = WikipediaRetriever(
    lang="ko",
    top_k_results=3,
    load_all_available_meta=True,
    doc_content_chars_max=4000,
)

# SQL, VectorDB, MongoDB, Redis
