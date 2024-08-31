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


def test_format_inputs_into_template_with_dict(mock_prompt_repo):
    input_dict = {
        "history": "Bot: Hello, how can I help you?",
        "query": "What's 100 ml water in grams?",
        "additional_input": "Some additional input"
    }

    prompt_template = mock_prompt_repo["alternative_dummy_template"]

    formatted_prompt = format_inputs_into_template_with_dict(prompt_template, input_dict)

    assert "What's 100 ml water in grams?" in formatted_prompt
    assert "Some additional input" in formatted_prompt
    assert "Bot: Hello, how can I help you?" in formatted_prompt


def test_call_llm(test_llm_invoker):
    formatted_prompt = "This is the prompt that will be sent to the LLM."

    llm_response = call_llm(formatted_prompt, dev_mode=True, invoker=test_llm_invoker)
    
    assert llm_response == formatted_prompt


def test_chat_bot_flow(mock_prompt_repo, test_llm_invoker):
    history = ""
    greeting = mock_prompt_repo["greeting_prompt"]
    history += f"Bot: {greeting}"

    user_query = "What's 100 ml water in grams?"
    additional_input = "Some additional input"

    input_dict = generate_input_dict(history=history, query=user_query, additional_input=additional_input)

    prompt_template = mock_prompt_repo["alternative_dummy_template"]
    formatted_prompt = format_inputs_into_template_with_dict(prompt_template, input_dict)

    llm_response = call_llm(formatted_prompt, dev_mode=True, invoker=test_llm_invoker)
    
    assert llm_response == formatted_prompt

def construct_llm(model_name):
    return ChatOpenAI(model=model_name, api_key=OPENAI_KEY)

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
user_query = "What's 100 ml water in grams?"

prompt_repo = load_prompt_repo("chat")
system_prompt = prompt_repo['system_prompt']

formatted_history = ChatPromptPopulator.format_history(history)

prompt = ChatPromptPopulator.format_langchain_prompt(system_prompt, formatted_history)

chain = ChatInputHandler.make_chain(prompt,model=construct_llm("gpt-4o-mini-2024-07-18"))

assert chain is not None

print(chain)

response = chain.invoke({"user_query":user_query})
print(response)