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
    "purpose":"one of generic, summarize , sentence_completion,  document_related ",
    "language":"primary language of user query vi, en ",
    "standalone_query": "Generate a standalone question or a request which is based on the new question plus the chat history."
}

REMEMBER: 
1. ONLY sentences such as chit-chat, exclamations, greetings, and goodbyes should be classified as generic. 
2. Only questions about Cortex M4 should be classified as document_related.
3. Only response in JSON format


"""
        return prompt_system_en
    def get_system_prompt_summarization(self):
        prompt_system_en = """
You are a helpful AI assistant that help people summarize the text. 
REMEMBER: Your name is Alitaa. 
Always introduce yourself first and answer politely, response and translate the summarized text if the user wants
You need to separate the greeting text and summarized text
"""
        return prompt_system_en
    def get_user_prompt_summarization(self, user_language: str, standalone_query: str):
        prompt_user_en=f"""
Please summarize the following paragraph in a few sentences in {user_language}. The text: {standalone_query}
"""
        return prompt_user_en


    def force_message(self, new_query):
        return f"New question: {new_query}"
