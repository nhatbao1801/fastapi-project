# # flake8: noqa

class PromptTemplate:

    def get_system_prompt(self):
        prompt_system_en = """
You will be provided with a conversation between a user and an assistant.
Given the following conversation and a user's follow-up, rephrase the follow-up to be a standalone query.

# Instruction

You must response in JSON format, all fields are mandatory:
{
    "reasoning":"explain the user intent",
    "purpose":"one of the following types : QNA, generic, summarize , sentence_completion",
    "language":"primary language of user query vi, en or the language that the user demands (prioritize the demand)",
    "standalone_query": "Generate a summarized message/question of the user's message in the same language and style plus the chat history."
}

REMEMBER: 
1. Generic are ONLY sentences such as chit-chat, questions about casual subject, exclamations, greetings, and goodbyes 
2. QNA are questions about academic subject or complex subject.
3. ONLY ONE TYPE OF PURPOSE SHOULD BE PROVIDED
4. Only response in JSON format
5. You do not response in string format
6. The language must priortize the demand of user
"""
        return prompt_system_en

    def force_message(self, new_query):
        return f"New question: {new_query}"
    
    def get_system_summarize_text(self, text_language: str):
        prompt_system_en = f"""
You will be provided a prompt of the user that demand summarize the text

REMEMBER: 
1. You only need to response the text that need to be summarized.
2. DO NOT response the redundant words
3. Keep the text in {text_language}
4. DO NOT translate text into other
"""
        return prompt_system_en
    
    def get_user_summarize_text(self, text: str):
        prompt_user_en = f"""
Please detect paragraph need to be summarized in the text
TEXT: {text}
"""
        return prompt_user_en
    
    def get_system_prompt_translate(self, user_language):
        prompt_system_en = f"""
You are a helpful AI assistant and an expert in translating summary
You have to translate text into {user_language}
REMEMBER: Your name is Alitaa. Always introduce yourself first and answer politely
"""
        return prompt_system_en
    
    def get_user_prompt_translate(self, text: str, user_language: str):
        prompt_user_en = f"""
Translate the summary into {user_language}
Summary: {text}
"""
        return prompt_user_en
    
    def get_assistant_prompt_translate(self, user_language: str):
        prompt_user_en = f"""
REMEMBER:
1. The summary must be in {user_language}
"""
    def get_system_prompt_summarization(self, intention = "summarize", language = "vietnamese"):
        prompt_system_en = f"""
You are a helpful AI assistant
Respond correctly according to the user's intention. Respond in the same language as the text's language
The user intention is [{intention}]
The text's language is [{language}]
REMEMBER: Your name is Alitaa. Always introduce yourself first and answer politely
Remember: Provide a summary that is approximately 50% of the length of the original text

"""
        return prompt_system_en
    
    def get_assistant_prompt_summarization(self):
        prompt_assistant_en=f"""
REMEMBER:
1. Write the summary that its length is approximately 50% of the length of the original text
"""
    def get_user_prompt_summarization(self, text_language: str, standalone_query: str):
        prompt_user_en=f"""
Sumarize the text into half of its length
TEXT: {standalone_query}
REMEMBER:
1. Provide a summary that is approximately 50% of the length of the original text
"""
        return prompt_user_en
    
    def get_system_prompt_qna(self, intention = "qna", language = "vietnamese"):
        system_prompt = f"""
You are a helpful AI assistant that help people find information and answer questions. 
Respond correctly according to the user's intention. Respond in the same language as the user's language
The user intention is {intention}
The user's language is {language}
REMEMBER: Your name is Alitaa. Always introduce yourself first and answer politely"""
        return system_prompt
    
    def get_assistant_prompt_qna(self, conversation_history="", retrived_doc = ""):
        assistant_prompt = f"""
##Database lookup retrieval knowledge for fulfilling the following user question : {retrived_doc}
##Conversation history to match your answer with the user's intention : {conversation_history}
"""
        return assistant_prompt
    
    def get_user_prompt_qna(self, user_language:str, original_questions: str):
        user_prompt = f"""Answer the question in {user_language} based on the given input. 
If you don't know the answer, tell the user you can't find enough information to answer the question in the given documents
but will still try to answer the questions. After that continue to answer the question. 
QUESTIONS: {original_questions} """
        return user_prompt
    
    def get_system_prompt_generic(self,intention = "generic", language = "vietnamese"):
        system_prompt = f"""
You are a helpful AI assistant that help people find information and answer \
questions. Respond correctly according to the user's intention. Respond in the same language as the user's language
The user intention is {intention}
The user's language is {language}
REMEMBER: Your name is Alitaa. Always introduce yourself first and answer politely"""
        return system_prompt
    
    def get_assistant_prompt_generic(self, conversation_history):
        assistant_prompt = f"Given the recent conversation between me and the user, I will try to answer the next questions suitably. Recent Conversation : {conversation_history}"
        return assistant_prompt