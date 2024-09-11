import sys
import pathlib
import os
from dotenv import load_dotenv

sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")

from src.core.base_template_retriever import BaseTemplateRetriever
from src.chat_bot.chat_input_handler import ChatInputHandler
from src.chat_bot.chat_prompt_populator import ChatPromptPopulator
from src.llm_invokers.openai_invoker import OpenAIInvoker
from langchain_openai import ChatOpenAI


load_dotenv()
OPENAI_KEY=os.getenv("OPENAI_KEY")

def construct_llm(provider, model_name):
    if provider == "OpenAI":
        return ChatOpenAI(model=model_name, api_key=OPENAI_KEY)
    else:
        return "No provider specified"

def invoke_chat_bot(user_query:str, chat_history:list[dict]) -> str:
    """Execute the chat bot process to get a response from the chat LLM

    Args:
        user_query (str): user question to answer
        chat_history (list[dict]): the user-bot conversation so far in format
            [{"role": assistant, "content": assistant content},
             {"role": user,      "content": user content},
             {"role": assistant, "content": content},
             ...
            ]

    Returns:
        str: response from the LLM to the user query given the chat history
    """
    
    prompt_repo = BaseTemplateRetriever.load_templates("chat")

    # Prepare chat history to be in a compatible format for LLM invokation
    formatted_history = ChatPromptPopulator.format_history(chat_history)

    # Get system prompt
    system_prompt=prompt_repo['system_prompt']

    # Join system prompt and formatted chat history into an executable prompt
    prompt = ChatPromptPopulator.format_langchain_prompt(system_prompt,formatted_history)

    # Construct model
    llm=construct_llm("OpenAI", "gpt-4o-mini-2024-07-18")
    
    # Chain the model and prompt
    chain = ChatInputHandler.make_chain(prompt, llm)
    invoker=OpenAIInvoker()
    llm_response = invoker.get_response({"user_query": user_query}, chain, dev_mode=False)


    return llm_response.content