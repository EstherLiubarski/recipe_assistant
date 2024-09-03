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
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from src.parsers.pydantic_parsers import make_pydantic_parser

load_dotenv()
OPENAI_KEY=os.getenv("OPENAI_KEY")

def construct_llm(provider, model_name):
    if provider == "OpenAI":
        return ChatOpenAI(model=model_name, api_key=OPENAI_KEY)
    else:
        return "No provider specified"
    
def generate_recipes(ingredients_list: list, recipe_options: list, num_recipes: int) -> list[Recipe]:
    """Execute the entire recipe generator workflow to return the generated recipe

    Args:
        ingredients_list (list): list of ingredients to include in the recipes
        recipe_options (list): list of recipe styles e.g. ["Healthy", "Vegan"]
        num_recipes (int): number of different recipes to generate

    Returns:
        list: list of Pydantic recipe objects for each generated recipe
    """
    recipe_style = GeneratorInputHandler.format_recipe_style(recipe_options)

    prompt_repo = BaseTemplateRetriever.load_templates("recipe_generator")
    style_instructions_template = prompt_repo['style_instructions_template']
    style_instructions = GeneratorPromptPopulator.choose_style_instructions(recipe_options,style_instructions_template)

    recipe_instructions = prompt_repo['recipe_instructions']

    inputs_dict = GeneratorInputHandler.make_inputs_dict(
        ingredients_list = ingredients_list,
        num_recipes = num_recipes,
        recipe_style = recipe_style,)

    # parser = PydanticOutputParser(pydantic_object=Recipe)
    parser = JsonOutputParser(pydantic_object=Recipe)

    prompt = GeneratorPromptPopulator.format_langchain_prompt(
        template=recipe_instructions,
        input_variables=inputs_dict.keys(),
        format_instructions = parser.get_format_instructions(),
        style_instructions=style_instructions)

    # print("prompt:\n", prompt)

    chain = GeneratorInputHandler.make_chain(
        prompt,
        model=construct_llm("OpenAI", "gpt-4o-mini-2024-07-18"),
        parser=parser)

    invoker=OpenAIInvoker()

    response = invoker.get_response(inputs_dict, chain=chain, dev_mode=False,)
    print("llm response:", response)
    return response