from typing import Any
from openai import AzureOpenAI
from src.config.system import cfg_system as settings
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI
from src.config.constant import Role
from src.module.openai_service.document_questions import hybrid_search
import json
from tenacity import (
    retry,
    wait_random_exponential,
    stop_after_delay
)  # for exponential backoff

from src.utils.logger import logger
from src.config.system import cfg_system as settings
from src.config.constant import Role, CommonCFG
from src.module.openai_service.prompt import PromptTemplate

prompt = PromptTemplate()

client = AzureOpenAI(
    azure_endpoint=settings.OPENAI_BASE,
    api_key=settings.OPENAI_API_KEY,
    api_version=settings.OPENAI_API_VERSION
)


def build_history_chat_msg(question,
                           histories=None,
                           ):
    system_message = prompt.get_system_prompt()
    messages = []
    dialog_system = {
        "role": Role.SYSTEM,
        "content": json.dumps(system_message, ensure_ascii=False).strip('"')
    }
    messages.append(dialog_system)

    # ! Just force return JSON, not good recommendation !!!
    # ! I can be fix with model 1106
    rule = "Please don't give an answer or comment. Just response in JSON format."
    rule_based = {
        "role": Role.USER,
        "content": rule
    }
    messages.append(rule_based)
    obey = "I won't answer any question. I won't even attempt to give answers. And I will always response in JSON format"
    obey_rule = {
        "role": Role.ASSISTANT,
        "content": obey
    }
    messages.append(obey_rule)
    # NOTE: add histories

    if histories is not None:
        for history in histories[-CommonCFG.ACCEPTED_LENGTH_HISTORY:]:
            messages.append({
                "role": Role.USER,
                "content": json.dumps(history[Role.USER].strip(),
                                      ensure_ascii=False).strip('"')
            })
            messages.append({
                "role": Role.ASSISTANT,
                "content": json.dumps(history[Role.BOT].strip(),
                                      ensure_ascii=False).strip('"')
            })

    force_sender_data = prompt.force_message(question)
    dialog_sender_data = {
        "role": Role.USER,
        "content": json.dumps(force_sender_data, ensure_ascii=False).strip('"')
    }
    messages.append(dialog_sender_data)
    logger.info("[x] Message history: %s", messages)
    # print(messages)
    return messages


@retry(wait=wait_random_exponential(min=1, max=settings.MAX_RETRIES),
       stop=stop_after_delay(5))
def get_chat_completion(messages: list[dict[str, str]],
                        max_tokens: int,
                        temperature: float,
                        stop=None,
                        json_object=False
                        ):
    try:
        params = {
            'model': settings.OPENAI_CHAT_MODEL,
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature,
            # 'stop': stop,
            # 'seed': settings.OPENAI_SEED,
        }
        # if json_object:
        #     params["response_format"] = {"type": "json_object"}

        completion = client.chat.completions.create(**params)
        message_content = completion.choices[0].message.content
        logger.info("[x] completion response: %s", message_content) 
        # if json_object:
        # print(message_content)
        message_content = json.loads(message_content)
        return message_content

    except Exception as e:
        logger.error("Exception in completion: %s", e)
        raise e


def call_completion(question="", histories=None) -> Any:

    messages = build_history_chat_msg(question=question, histories=histories)
    print(messages)
    message_response = get_chat_completion(messages=messages,
                                           max_tokens=settings.MAX_TOKENS,
                                           temperature=settings.TEMPERATURE)

    logger.info("[x] RESPONSE: %s", message_response)
    
    language = settings.DEFAULT_LANGUAGE
    if 'vi' not in message_response['language']:
        if 'en' in message_response['language']:
            language = 'english'

    if 'generic' in message_response['purpose'] :
        return generic_answer(message_response['standalone_query'],histories = histories, user_language = language)
    elif 'summarize' in message_response['purpose']:
        message_response['standalone_query'] = messages[-1]['content']
        return summarize(standalone_query=message_response['standalone_query'], histories=histories, user_language=language)
    else:    
        return document_related_answers(message_response['standalone_query'], histories = histories, user_language = language)

def generic_answer(standalone_query = "",histories=None, user_language='vietnamese'):
    client = AzureOpenAI(
    api_key = settings.OPENAI_API_KEY,  
    api_version = settings.OPENAI_API_VERSION,
    azure_endpoint = settings.OPENAI_BASE
    )
    messages =[]
    system_message_generic = prompt.get_system_prompt_generic()
    dialog = {
        "role" : Role.SYSTEM,
        "content": system_message_generic
    }
    messages.append(dialog)
    assistant_message_generic = prompt.get_assistant_prompt_generic(conversation_history=histories)
    dialog = {
        "role": Role.ASSISTANT,
        "content": assistant_message_generic
    }
    messages.append(dialog)
    
    dialog = {
        "role": Role.USER,
        "content": standalone_query
    }
    messages.append(dialog)
    response = client.chat.completions.create(
        model = settings.OPENAI_CHAT_MODEL,
        messages=messages,
        max_tokens=settings.MAX_TOKENS,
        temperature=settings.TEMPERATURE
    )
    return response

def document_related_answers(standalone_query="" ,histories = None, user_language = "vietnamese",intention = "qna"):
    search_results = hybrid_search(query=standalone_query)
    max_rrf_point=0
    for each in search_results :
        max_rrf_point = each["@search.reranker_score"]
        break
    if (max_rrf_point<settings.QNA_LIMIT_SCORE):
        return generic_answer(standalone_query = standalone_query, histories = histories, user_language=user_language,intention = intention)
    
    input_text = ""
    count=0
    for result in search_results:
        count=count+1
        if count>settings.MAX_INPUT_DOCUMENTS:
            break
        input_text = input_text + result['content'] + " "
    
    client = AzureOpenAI(
    api_key = settings.OPENAI_API_KEY,  
    api_version = settings.OPENAI_API_VERSION,
    azure_endpoint = settings.OPENAI_BASE
    )
    messages =[]
    dialog = {
        "role" : Role.SYSTEM,
        "content": prompt.get_system_prompt_qna(intention = intention, language = user_language)
        }
    messages.append(dialog)
    dialog = {
        "role": Role.USER,
        "content": prompt.get_user_prompt_qna(user_language= user_language, input_text=input_text, standalone_query= standalone_query)  
    }
    messages.append(dialog)
    if len(histories)>0:
        dialog = {
            "role": Role.ASSISTANT,
            "content": prompt.get_assistant_prompt_qna(conversation_history= histories)
        }
        messages.append(dialog)

    response = client.chat.completions.create(
        model = settings.OPENAI_CHAT_MODEL,
        messages=messages,
        max_tokens=settings.MAX_TOKENS_QNA,
        temperature=settings.TEMPERATURE_QNA
    )
    return response
def summarize(standalone_query="", histories=None, user_language='vi'):
    client = AzureOpenAI(
        api_key = settings.OPENAI_KEY,  
        api_version = settings.OPENAI_API_VERSION,
        azure_endpoint = settings.OPENAI_BASE
    )
    messages =[]
    system_message_summarization = prompt.get_system_prompt_summarization()
    dialog = {
        "role" : Role.SYSTEM,
        "content": system_message_summarization
    }
    messages.append(dialog)
    user_message_summarization = prompt.get_user_prompt_summarization(user_language, standalone_query)
    dialog = {
        "role": Role.USER,
        "content": user_message_summarization
    }
    messages.append(dialog)
    response = client.chat.completions.create(
        model = settings.OPENAI_CHAT_MODEL,
        messages=messages,
        max_tokens=settings.MAX_TOKENS,
        temperature=settings.SUM_TEMPERATURE
    )
    return response.choices[0].message.content