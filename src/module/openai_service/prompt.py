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
    "purpose":"one of retrieve_information, summarize, generic",
    "language":"language of user query vi, en",
    "standalone_query": "Generate a standalone question which is based on the new question plus the chat history."
}

REMEMBER: ONLY sentences such as chit-chat, exclamations, greetings, and goodbyes should be classified as generic.


"""
        return prompt_system_en

    def force_message(self, new_query):
        return f"New question: {new_query}"
