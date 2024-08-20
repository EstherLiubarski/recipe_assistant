import sys
import os

sys.path.append("../")

from src.core.base_template_retriever import BaseTemplateRetriever
from src.chat_bot.chat_input_handler import ChatInputHandler
from src.core.base_prompt_populator import PromptPopulator
from src.llm_invokers.openai_invoker import OpenAIInvoker

history=""
prompt_repo=BaseTemplateRetriever.load_templates("chat")
print("prompt_repo", type(prompt_repo))

greeting = prompt_repo["greeting_prompt"]
history += f"Bot: {greeting}"
print("greeting", greeting)
print("history", history)

user_query = input("Type your response: ")
additional_input = "Some additional input"

input_dict=ChatInputHandler.make_inputs_dict(history=history, query=user_query, additional_input = additional_input)
print("input dict", input_dict)

prompt_template =  prompt_repo["alternative_dummy_template"]
formatted_prompt = PromptPopulator.format_prompt(prompt_template, input_dict)

print("formatted prompt", formatted_prompt)

llm = OpenAIInvoker(api_key="key123")
llm_response = llm.get_response(formatted_prompt)

print(llm_response)







