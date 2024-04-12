import os
from pathlib import Path

from langchain.prompts import ChatPromptTemplate, PromptTemplate

from src.config.settings import PROMPT_DIR


def load_prompt(prompt_name: str, suffix: str = "json") -> PromptTemplate:
    """
    기존에 정의된 프롬프트를 로드합니다
    :return:
    """
    prompt_path = os.path.join(PROMPT_DIR, f"{prompt_name}.{suffix}")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file does not exist: {prompt_path}")

    if suffix == "json" or suffix == "yaml" or suffix == "yml":
        prompt = PromptTemplate.from_file(prompt_path)
    else:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = PromptTemplate.from_template(f.read())

    return prompt
