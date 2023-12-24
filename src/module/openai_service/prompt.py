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
    "language":"primary language of user query vi, en ",
    "standalone_query": "Generate a summarized message/question of the user's message in the same language and style plus the chat history."
}

REMEMBER: 
1. Generic are ONLY sentences such as chit-chat, questions about casual subject, exclamations, greetings, and goodbyes 
2. QNA are questions about academic subject or complex subject.
3. ONLY ONE TYPE OF PURPOSE SHOULD BE PROVIDED

"""
        return prompt_system_en

    def force_message(self, new_query):
        return f"New question: {new_query}"
    
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