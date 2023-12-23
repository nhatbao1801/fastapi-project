import os
from dotenv import load_dotenv

load_dotenv(override=True)


class SystemConfig:
    """System configuration class"""

    PROJECT_NAME: str = "GPT"
    DESCRIPTION: str = "Alitaa"
    VERSION: str = "0.0.1"

    # CONFIG model
    OPENAI_KEY: str = os.environ["OPENAI_API_KEY"]
    OPENAI_BASE: str = os.environ["OPENAI_API_BASE"]
    OPENAI_API_TYPE: str = os.environ["OPENAI_API_TYPE"]
    OPENAI_API_VERSION: str = os.environ["OPENAI_API_VERSION"]
    OPENAI_CHAT_MODEL: str = os.environ["OPENAI_CHAT_MODEL"]
    TEMPERATURE: float = float(os.environ["GPT_TEMPERATURE"])
    TOP_P: float = float(os.environ["GPT_TOP_P"])
    OPENAI_SEED = int(101)
    MAX_TOKENS: int = int(os.environ["GPT_MAX_TOKENS"])
    REQUEST_TIMEOUT: int = int(os.environ["GPT_REQUEST_TIMEOUT"])
    MAX_RETRIES = int(os.environ["GPT_MAX_RETRIES"])


cfg_system = SystemConfig()
