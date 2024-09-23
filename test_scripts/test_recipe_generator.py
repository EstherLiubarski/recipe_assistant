import pytest
import sys
import pathlib
import os
from dotenv import load_dotenv

sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")

from src.recipe_generator.generator_input_handler import GeneratorInputHandler
from src.core.base_template_retriever import BaseTemplateRetriever
from src.llm_invokers.openai_invoker import OpenAIInvoker
from src.recipe_generator.generator_prompt_populator import GeneratorPromptPopulator
from src.recipe_generator.recipe_object import Recipe
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI


OPENAI_KEY=os.getenv("OPENAI_KEY")

@pytest.mark.parametrize("input_data, expected_output", [
    (["Healthy"], "healthy"),
    (["Healthy", "Hearty"], "healthy and hearty"),
    (["Healthy", "Hearty", "Vegan"], "healthy, hearty and vegan"),
    ])
def test_format_list_to_string(input_data, expected_output):
    assert GeneratorInputHandler.format_list_to_string(input_data) == expected_output

@pytest.mark.parametrize(
    "recipe_options, style_instructions_template, expected_output",
    [
        ([], "The recipes must be {recipe_style}.", ""),
        (["Healthy"], "The recipes must be {recipe_style}.", "The recipes must be {recipe_style}."),
    ]
)
def test_choose_appropriate_prompt(recipe_options, style_instructions_template, expected_output):
    style_instructions = GeneratorPromptPopulator.choose_appropriate_prompt(
        recipe_options, style_instructions_template
    )
    print(style_instructions)
    print(expected_output)
    assert style_instructions == expected_output

def construct_llm(provider, model_name):
    if provider == "OpenAI":
        return ChatOpenAI(model=model_name, api_key=OPENAI_KEY)
    else:
        return "No provider specified"
    
ingredients_list = ["celery", "yogurt", "gnocchi", "turkey mince"]
num_recipes = 2
recipe_options = ["Healthy", "Hearty"]
allergies_list = ['Dairy']
recipe_style = GeneratorInputHandler.format_list_to_string(recipe_options)
allergies = GeneratorInputHandler.format_list_to_string(allergies_list)

prompt_repo = BaseTemplateRetriever.load_templates("recipe_generator")
style_instructions_template = prompt_repo['style_instructions_template']
style_instructions = GeneratorPromptPopulator.choose_appropriate_prompt(recipe_options,style_instructions_template)


allergies_instructions_template = prompt_repo['allergies_instructions_template']
allergies_instructions = GeneratorPromptPopulator.choose_appropriate_prompt(allergies_list,allergies_instructions_template)

recipe_instructions = prompt_repo['recipe_instructions']

inputs_dict = GeneratorInputHandler.make_inputs_dict(
    ingredients_list = ingredients_list,
    num_recipes = num_recipes,
    recipe_style = recipe_style,
    allergies=allergies)

parser = JsonOutputParser(pydantic_object=Recipe)

prompt = GeneratorPromptPopulator.format_langchain_prompt(
    template=recipe_instructions,
    input_variables=inputs_dict.keys(),
    format_instructions = parser.get_format_instructions(),
    style_instructions=style_instructions,
    allergies_instructions=allergies_instructions)

print("prompt:\n", prompt)

chain = GeneratorInputHandler.make_chain(
    prompt,
    model=construct_llm("OpenAI", "gpt-4o-mini-2024-07-18"),
    parser=parser)

invoker=OpenAIInvoker()

# response = invoker.get_response(inputs_dict, chain=chain, dev_mode=False,)
# print("llm response:", response)
response = invoker.get_response(inputs_dict, chain=chain, dev_mode=True,)
print("dev response:", response)


