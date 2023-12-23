from typing import Any
from openai import AzureOpenAI
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
    api_key=settings.OPENAI_KEY,
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
        if json_object:
            params["response_format"] = {"type": "json_object"}

        completion = client.chat.completions.create(**params)
        message_content = completion.choices[0].message.content
        logger.info("[x] completion response: %s", message_content)
        # if json_object:
        message_content = json.loads(message_content)
        return message_content

    except Exception as e:
        logger.error("Exception in completion: %s", e)
        raise e


def call_completion(question="", histories=None) -> Any:

    messages = build_history_chat_msg(question=question, histories=histories)
    message_response = get_chat_completion(messages=messages,
                                           max_tokens=settings.MAX_TOKENS,
                                           temperature=settings.TEMPERATURE)

    logger.info("[x] RESPONSE: %s", message_response)
    return message_response
