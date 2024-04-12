import os
from pathlib import Path

CUR_DIR = Path(__file__).parent
ROOT_DIR = Path(CUR_DIR).parent.parent
PROMPT_DIR = os.path.join(ROOT_DIR, "prompts")
CONV_HISTORY_DIR = os.path.join(ROOT_DIR, "conv_history")
