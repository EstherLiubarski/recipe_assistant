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
from src.parsers.pydantic_parsers import make_pydantic_parser
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_KEY=os.getenv("OPENAI_KEY")

@pytest.fixture
def recipe_options():
    return "healthy"

@pytest.fixture
def ingredients_list():
    return ["ingredient 1", "ingredient 2", "ingredient 3"]

@pytest.fixture
def input_dict():
    return {"recipe_options":"healthy", 
            "ingredients_list": ["ingredient 1", "ingredient 2", "ingredient 3"]}

def test_input_dict_maker(recipe_options, ingredients_list):
    input_dict = GeneratorInputHandler.make_inputs_dict(recipe_options, ingredients_list)
    assert input_dict=={"recipe_options":recipe_options,
                        "ingredients_list": ingredients_list}
    
def test_prompt_populator(input_dict):
    prompt_repo = BaseTemplateRetriever.load_templates("recipe_generator")
    template = prompt_repo['dummy_prompt']
    prompt = GeneratorPromptPopulator.format_inputs_into_template(template,input_dict)
    assert "Generate a healthy recipe with the following ingredients: ['ingredient 1', 'ingredient 2', 'ingredient 3']." in prompt

@pytest.mark.parametrize("input_data, expected_output", [
    (["Healthy"], "healthy"),
    (["Healthy", "Hearty"], "healthy and hearty"),
    (["Healthy", "Hearty", "Vegan"], "healthy, hearty and vegan"),
    ])
def test_format_recipe_style(input_data, expected_output):
    assert GeneratorInputHandler.format_recipe_style(input_data) == expected_output

@pytest.mark.parametrize(
    "recipe_options, style_instructions_template, expected_output",
    [
        (["No Specifications"], "The recipes must be {recipe_style}.", ""),
        (["Healthy"], "The recipes must be {recipe_style}.", "The recipes must be {recipe_style}."),
    ]
)
def test_choose_style_instructions(recipe_options, style_instructions_template, expected_output):
    style_instructions = GeneratorPromptPopulator.choose_style_instructions(
        recipe_options, style_instructions_template
    )
    assert style_instructions == expected_output

def construct_llm(provider, model_name):
    if provider == "OpenAI":
        return ChatOpenAI(model=model_name, api_key=OPENAI_KEY)
    else:
        return "No provider specified"
    
# def test_langchain_chain():
ingredients_list = ["celery", "yogurt", "gnocchi", "turkey mince"]
num_recipes = 2
recipe_options = ["Healthy", "Hearty"]
# recipe_options = ["No Specifications"]
recipe_style = GeneratorInputHandler.format_recipe_style(recipe_options)

prompt_repo = BaseTemplateRetriever.load_templates("recipe_generator")
style_instructions_template = prompt_repo['style_instructions_template']
style_instructions = GeneratorPromptPopulator.choose_style_instructions(recipe_options,style_instructions_template)

recipe_instructions = prompt_repo['recipe_instructions']

inputs_dict = GeneratorInputHandler.make_inputs_dict(
    ingredients_list = ingredients_list,
    num_recipes = num_recipes,
    recipe_style = recipe_style,)

parser = JsonOutputParser(pydantic_object=Recipe)

prompt = GeneratorPromptPopulator.format_langchain_prompt(
    template=recipe_instructions,
    input_variables=inputs_dict.keys(),
    format_instructions = parser.get_format_instructions(),
    style_instructions=style_instructions)

print("prompt:\n", prompt)

chain = GeneratorInputHandler.make_chain(
    prompt,
    model=construct_llm("OpenAI", "gpt-4o-mini-2024-07-18"),
    parser=parser)

invoker=OpenAIInvoker()

response = invoker.get_response(inputs_dict, chain=chain, dev_mode=False,)
print("llm response:", response)
response = invoker.get_response(inputs_dict, chain=chain, dev_mode=True,)
print("dev response:", response)


