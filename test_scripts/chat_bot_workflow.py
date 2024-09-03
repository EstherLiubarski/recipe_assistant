import sys
import os
import pathlib

sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")

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
formatted_prompt = PromptPopulator.format_inputs_into_template(prompt_template, input_dict)

print("formatted prompt", formatted_prompt)

llm = OpenAIInvoker(model="gpt-4o-mini-2024-07-18")
llm_response = llm.get_response(input_dict)

print(llm_response)






