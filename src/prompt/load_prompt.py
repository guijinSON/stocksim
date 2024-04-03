import os
from pathlib import Path

from langchain.prompts import ChatPromptTemplate, PromptTemplate

CUR_DIR = Path(__file__).parent
ROOT_DIR = Path(CUR_DIR).parent.parent
PROMPT_DIR = os.path.join(ROOT_DIR, "prompts")


def load_prompt(prompt_name: str) -> PromptTemplate:
    """
    기존에 정의된 프롬프트를 로드합니다
    :return:
    """
    prompt_path = os.path.join(PROMPT_DIR, f"{prompt_name}.txt")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file does not exist: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = PromptTemplate.from_template(f.read())

    return prompt


# if __name__ == "__main__":
#     print(load_prompt("base_chat"))
