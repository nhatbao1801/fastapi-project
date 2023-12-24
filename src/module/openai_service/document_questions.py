import openai

from src.config.system import cfg_system as settings
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI
from src.config.constant import Role

def get_embeddings(text: str):
    open_ai_endpoint = settings.OPENAI_BASE
    open_ai_key = settings.OPENAI_API_KEY

    client = openai.AzureOpenAI(
        azure_endpoint=open_ai_endpoint,
        api_key=open_ai_key,
        api_version=settings.OPENAI_API_VERSION,
    )
    embedding = client.embeddings.create(input=[text], model=settings.EMBEDDING_MODEL)
    return embedding.data[0].embedding

def hybrid_search(query: str):
    #initiate a search_client
    search_client = SearchClient(
        endpoint = settings.OPENAI_SEARCH_ENDPOINT,
        index_name=settings.SEARCH_INDEX,
        credential = AzureKeyCredential(settings.OPENAI_SEARCH_KEY))
    query = query
    vector = VectorizedQuery(
        vector= get_embeddings(query),
        k_nearest_neighbors=settings.VECTOR_PARAMETER_K, 
        fields = settings.VECTOR_SEARCH_FIELD
        )
    query_answer_count=settings.SEMANTIC_ANSWER_COUNT
    query_answer_threshold=settings.SEMANTIC_ANSWER_THRESHOLD
    query_type = settings.SEARCH_QUERY_TYPE or "semantic"
    search_results = search_client.search(
        search_text = query,
        vector_queries= [vector],
        select= ["content", "title"],
        query_type=query_type,
        query_answer= f"extractive|count-{query_answer_count},threshold-{query_answer_threshold}", 
        query_caption = "extractive",
        query_caption_highlight_enabled=settings.SEMANTIC_CAPTIONS_ENABLE,
        semantic_configuration_name=settings.SEMANTIC_CONFIG_NAME,
        semantic_max_wait_in_milliseconds= settings.SEMANTIC_MAX_WAIT,
        top= settings.SEMANTIC_TOP_DOCUMENTS
    )
    return search_results