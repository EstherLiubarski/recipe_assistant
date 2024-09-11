from src.core.base_prompt_populator import BasePromptPopulator
from langchain_core.prompts import ChatPromptTemplate

class ChatPromptPopulator(BasePromptPopulator):

    @staticmethod
    def format_history(history:list[dict]):
        """
        Reformat a list of dictionaries representing chat history into a list of 2-tuples.

        Args:
            history (list[dict]): A list of dictionaries where each dictionary contains:
                            - 'role' (str): Role in the conversation ('assistant' or 'user')
                            - 'content' (str): The message content

        Returns:
            list: A list of 2-tuples where each tuple consists of:
                - str: The role ('ai' or 'human')
                - str: The corresponding content/message
        """
        role_mapping = {
            'assistant': 'ai',
            'user': 'human'
        }
        
        reformatted_history = [(role_mapping.get(entry['role']), entry['content']) for entry in history]
        return reformatted_history

    def format_langchain_prompt(system_prompt: str, history: list) -> ChatPromptTemplate:
        """Formats the system prompt, chat history, and user query into a LangChain prompt template.

        Args:
            system_prompt (str): instructions to the LLM on how to respond to the query.
            history (list): previous chat history.
                Must be of one of the types of the `message` parameter in LangChain ChatPromptTemplate.

        Returns:
            ChatPromptTemplate: the prompt template with the formatted system prompt and chat history.
        """
        # Create a list of system messages
        system_tuple_list = [('system', system_prompt)]
        
        # Combine system messages with the history
        messages = system_tuple_list + history
        
        # Add user query placeholder to the end of the prompt
        messages.append(('human', '{user_query}'))
        
        prompt_template = ChatPromptTemplate.from_messages(messages)
        
        return prompt_template
