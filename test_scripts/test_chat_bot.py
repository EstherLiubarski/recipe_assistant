import pytest
import sys
import pathlib
import getpass
import os

sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")

from dotenv import load_dotenv
from src.core.base_template_retriever import BaseTemplateRetriever
from src.chat_bot.chat_input_handler import ChatInputHandler
from src.chat_bot.chat_prompt_populator import ChatPromptPopulator
from src.llm_invokers.openai_invoker import OpenAIInvoker
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_KEY=os.getenv("OPENAI_KEY")

def load_prompt_repo(feature: str):
    """Load the prompt templates for a specific feature."""
    return BaseTemplateRetriever.load_templates(feature)

def generate_input_dict(history: str, query: str, additional_input: str = None) -> dict:
    """Generate the input dictionary for the chatbot."""
    return ChatInputHandler.make_inputs_dict(history=history, query=query, additional_input=additional_input)

def format_inputs_into_template_with_dict(prompt_template: str, input_dict: dict) -> str:
    """Format the prompt template with the input dictionary."""
    return ChatPromptPopulator.format_inputs_into_template(prompt_template, input_dict)

def call_llm(input_dict: str, dev_mode : bool, invoker: OpenAIInvoker) -> str:
    """Call the LLM with the formatted prompt."""
    return invoker.get_response(input_dict, dev_mode=dev_mode)

@pytest.fixture
def mock_prompt_repo():
    return load_prompt_repo("chat")


@pytest.fixture
def test_llm_invoker():
    return OpenAIInvoker()


def test_generate_input_dict():
    history = "Bot: Hello, how can I help you?"
    user_query = "What's 100 ml water in grams?"
    additional_input = "Some additional input"

    input_dict = generate_input_dict(history, user_query, additional_input)

    assert input_dict["history"] == history
    assert input_dict["query"] == user_query
    assert input_dict["additional_input"] == additional_input


def test_call_llm(test_llm_invoker):
    formatted_prompt = "This is the prompt that will be sent to the LLM."

    llm_response = call_llm(formatted_prompt, dev_mode=True, invoker=test_llm_invoker)
    
    assert llm_response == formatted_prompt

def construct_llm(provider, model_name):
    if provider == "OpenAI":
        return ChatOpenAI(model=model_name, api_key=OPENAI_KEY)
    else:
        return "No provider specified"
    
def test_reformatted_prompt():
    history = [
        {'role': 'assistant', 'content': "Hi there, I'm your friendly recipe assistant! How can I help you?"},
        {'role': 'user', 'content': 'What is swiss chard?'},
        {'role': 'assistant', 'content': 'Swiss chard is a leafy green vegetable that belongs to the same family as beets and spinach.'},
    ]
    
    formatted_history = ChatInputHandler.re(history)
    
    expected_output = [
        ('ai', "Hi there, I'm your friendly recipe assistant! How can I help you?"),
        ('human', 'What is swiss chard?'),
        ('ai', 'Swiss chard is a leafy green vegetable that belongs to the same family as beets and spinach.'),
    ]
    
    assert formatted_history == expected_output, f"Expected {expected_output}, but got {formatted_history}"

# def test_langchain_chain():
history = [{'role': 'assistant', 'content': "Hi there, I'm your friendly recipe assistant! How can I help you?"}, 
            {'role': 'user', 'content': 'What is swiss chard?'}, 
            {'role': 'assistant', 'content': 'Swiss chard is a leafy green vegetable that belongs to the same family as beets and spinach.'}, ]
formatted_history = ChatPromptPopulator.format_history(history)

user_query = "What's 100 ml water in grams?"

prompt_repo = load_prompt_repo("chat")
system_prompt = prompt_repo['system_prompt']

prompt = ChatPromptPopulator.format_langchain_prompt(system_prompt, formatted_history)

llm=construct_llm("gpt-4o-mini-2024-07-18")
chain = ChatInputHandler.make_chain(prompt,model=llm)

assert chain is not None

print(chain)

invoker=OpenAIInvoker()

response = invoker.get_response({"user_query": user_query}, chain=chain, dev_mode=False,)
print("llm response:", response)
response = invoker.get_response({"user_query": user_query}, chain=chain, dev_mode=True,)
print("dev response:", response)
