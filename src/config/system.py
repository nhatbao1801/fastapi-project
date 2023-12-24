import os
from dotenv import load_dotenv

load_dotenv(override=True)


class SystemConfig:
    """System configuration class"""

    PROJECT_NAME: str = "GPT"
    DESCRIPTION: str = "Alitaa"
    VERSION: str = "0.0.1"

    # CONFIG model
    OPENAI_API_TYPE: str = os.environ["OPENAI_API_TYPE"]
    OPENAI_BASE: str = os.environ["OPENAI_API_BASE"]
    OPENAI_API_VERSION: str = os.environ["OPENAI_API_VERSION"]
    OPENAI_CHAT_MODEL: str = os.environ["OPENAI_CHAT_MODEL"]
    OPENAI_API_KEY :str = os.environ["OPENAI_API_KEY"]
    OPENAI_SEARCH_KEY :str =os.environ["OPENAI_SEARCH_KEY"]
    OPENAI_SEARCH_ENDPOINT :str = os.environ["OPENAI_SEARCH_ENDPOINT"]
    TEMPERATURE: float = float(os.environ["GPT_TEMPERATURE"])
    MAX_TOKENS_GENERIC: int  =  int(os.environ["MAX_TOKENS_GENERIC"])
    MAX_TOKENS_QNA : int = int(os.environ["MAX_TOKENS_QNA"])
    TEMPERATURE_GENERIC : float = float(os.environ["TEMPERATURE_GENERIC"])
    TEMPERATURE_QNA : float = float(os.environ["TEMPERATURE_QNA"])
    MAX_INPUT_DOCUMENTS : int  =  int(os.environ["MAX_INPUT_DOCUMENTS"])
    MAX_PREVIOUS_QUESTIONS: int =  int(os.environ["MAX_PREVIOUS_QUESTIONS"])
    DEFAULT_LANGUAGE :str = os.environ["DEFAULT_REPSONSE_LANGUAGE"] 
    EMBEDDING_MODEL : str = os.environ["EMBEDDING_MODEL"]
    SEARCH_INDEX: str  = os.environ["SEARCH_INDEX"]
    VECTOR_PARAMETER_K : int = int(os.environ["VECTOR_PARAMETER_K"])
    VECTOR_SEARCH_FIELD: str = os.environ["VECTOR_SEARCH_FIELD"]
    SEMANTIC_ANSWER_COUNT : int = int(os.environ["SEMANTIC_ANSWER_COUNT"])
    SEMANTIC_ANSWER_THRESHOLD : float = float(os.environ["SEMANTIC_ANSWER_THRESHOLD"])
    SEMANTIC_CAPTIONS_ENABLE : bool = os.environ["SEMANTIC_CAPTIONS_ENABLE"]
    SEMANTIC_CONFIG_NAME : str = os.environ["SEMANTIC_CONFIG_NAME"]
    SEARCH_QUERY_TYPE: str = os.environ["SEARCH_QUERY_TYPE"]
    SEMANTIC_MAX_WAIT : int =  int(os.environ["SEMANTIC_MAX_WAIT"])
    SEMANTIC_TOP_DOCUMENTS: int  = int(os.environ["SEMANTIC_TOP_DOCUMENTS"]) 
    QNA_LIMIT_SCORE : float = float(os.environ["QNA_LIMIT_SCORE"])
    TOP_P: float = float(os.environ["GPT_TOP_P"])
    OPENAI_SEED = int(101)
    MAX_TOKENS: int = int(os.environ["GPT_MAX_TOKENS"])
    REQUEST_TIMEOUT: int = int(os.environ["GPT_REQUEST_TIMEOUT"])
    MAX_RETRIES = int(os.environ["GPT_MAX_RETRIES"])
    SUM_TEMPERATURE: float = float(os.environ["GPT_SUMMARY_TEMPERATURE"])


cfg_system = SystemConfig()