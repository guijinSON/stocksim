from langchain_community.cache import RedisCache, SQLiteCache, InMemoryCache

"""
LLM 의 답변을 임시로 저장하는 캐시영역
memories 의 내용 과는 다름. LLM 과 연동되는 영역
"""


def get_redis_cache(redis_info: str, ttl: int = 600):
    """
    prepared `pip install redis`
    :return:
    """
    return RedisCache(redis_info, ttl=ttl)


def get_file_cache(database_path: str = ".langchain.db"):
    return SQLiteCache(database_path)


def get_memory_cache():
    return InMemoryCache()
