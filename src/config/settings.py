import os
from pathlib import Path
from typing import LiteralString

CUR_DIR = Path(__file__).parent
ROOT_DIR = Path(CUR_DIR).parent.parent
PROMPT_DIR = os.path.join(ROOT_DIR, "prompts")
CONV_HISTORY_DIR = os.path.join(ROOT_DIR, "conv_history")
OTHERS_DIR = os.path.join(ROOT_DIR, "others")


def get_path_join(**args: str) -> LiteralString | str | bytes:
    return os.path.join(**args)
