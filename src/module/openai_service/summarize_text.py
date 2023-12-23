import openai

from config.system import cfg_system as settings
from openai import AzureOpenAI
from config.constant import Role

def summarize(text: str,histories="None",):
    client = AzureOpenAI(
        api_key = settings.OPENAI_API_KEY,  
        api_version = "2023-05-15",
        azure_endpoint = settings.OPENAI_BASE
    )
    messages =[]
    dialog = {
        "role" : Role.SYSTEM,
        "content": "You are a helpful AI assistant that help people summarize the text. REMEMBER: Your name is Alitaa. Always introduce yourself first and answer politely" 
    }
    messages.append(dialog)
    dialog = {
        "role": Role.USER,
        "content": f"Please summarize the following text in a few sentences while keeping the language the same. The text: {text}"
    }
    messages.append(dialog)
    response = client.chat.completions.create(
        model = settings.OPENAI_CHAT_MODEL,
        messages=messages,
        max_tokens=300,
        temperature=0.2
    )
    return response




