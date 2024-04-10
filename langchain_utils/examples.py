from langchain.agents import load_tools, initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate

from langchain_utils.chains import (
    get_conversation_chain,
    get_llm_chain,
    get_sequential_chain,
)
from langchain_utils.memories import (
    get_chat_memory_history_from_redis,
    get_conversation_buffer_memory,
    get_conversation_summary_memory,
)
from src.llm.azure import get_azure_gpt_chat_llm

# Example 1: chat_history + type of chat memory + conversation_chain

## Redis 를 저장 백엔드로 사용(PG, MongoDB, Elastic 등 여러가지 가능)
chat_history = get_chat_memory_history_from_redis(
    redis_url="redis://localhost:6379/0",
    session_id="test",  # session_id 는 사용자의 고유한 ID 로 변경이 필요합니다.
    key_prefix="kakao-game",
    ttl=600,
)

## 기본 대화 저장 모델(memories) 에 구현된 여러가지 방법을 다 사용할 수 있습니다.
memory = get_conversation_buffer_memory(
    chat_history=chat_history,
    memory_key="kakao-game",
)

# 대화가 너무 길어져서 요약이 필요할 때 사용 -> 1개로 줄여줌
# 적당한 타이밍에 실행해서 필요한 맥락만 계속 가져갈 수 있도록 해야함
# get_conversation_summary_memory(
#     chat_history=chat_history, llm=None, summarize_step=5, memory_key="kakao-game"
# )

### LLM 도 구현체를 바꾸거나, 모델을 바꾸는 등 필요에 따라 바꿔가며 쓸 수 있습니다.
## 중요하고 추론이 필요한 작업: 고성능 모델(ex> gpt-4)
## 단순하고 반복적인 빠른 작업: 경량 모델(ex> gpt-3.5-turbo)

llm = get_azure_gpt_chat_llm(model_version="4", temperature=0.1, is_stream=False)

conv_chain = get_conversation_chain(
    memory=memory,
    llm=llm,
    prompt=PromptTemplate.from_template("해당 대화의 시스템 프롬프트 입력"),
)

# conv_chain.run({"input": "안녕하세요."})

chat_history_result = conv_chain.memory.load_memory_variables({})
historical_messages = chat_history_result["chat_history"]


# SimpleSequencialChain 을 이용한 여러개 체인을 연결해서 실행하기(구버전 예제입니다 -> 신버전은 LCEL 을 통해서 가능)
sample_chain_1 = get_llm_chain(
    model=llm,
    prompt=PromptTemplate(
        template="{input} 에 관해 금융 전문가의 관점에서 설명하시오. ",
        input_variables=["input"],
    ),
)

sample_chain_2 = get_llm_chain(
    model=llm,
    prompt=PromptTemplate(
        template="초등학생도 이해할 수 있을 정도로 다음 주어진 문장을 쉽게 표현해주세요. \n {input} ",
        input_variables=["input"],
    ),
)

sample_sequential_chain = get_sequential_chain(
    chains=[sample_chain_1, sample_chain_2], strip_outputs=False
)
# print(sample_sequential_chain.run({"input": "금리가 올랐다."}))


### Agent 예제 (Agent 는 툴을 포함하는 자율 행동 주체)
# 요즘은 Agent 자체를 구성하는 부분은 LangGraph 를 사용해서 구성하는것이 더 편리합니다.
# 이 예제도 이제는 과거 방식의 예제이지만, 아직까지는 사용될 수 있습니다.

# AgentType 을 이해하고 난 뒤에 사용하는 것이 중요합니다.(아니면 오작동 할 가능성이 너무 높음)
# AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION: 대화 형식으로 상호작용하는 특징이 있으며, Chat Models 와 ReACT 방법론을 이용해 Agent 를 구성함
# AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION: 위와 같은 방식이지만, 여러 개의 예제를 줄 수 있다(Agent 가 잘 동작하지 않을 시)
# AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION: 여러 입력을 가진 툴을 사용하는 Agent


sample_1_tools = load_tools(["requests"])  # requests: Langchain 에 미리 준비된 툴임

sample_1_agent = initialize_agent(
    tools=sample_1_tools,
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # ReACT 방식으로 동작하는 에이전트
    verbose=True,
)
sample_1_url = ""

# print(
#     sample_1_agent.run(
#         f"""아래 URL 에 접속해서 내용을 요약해주세요. \n {sample_1_url}"""
#     )
# )
