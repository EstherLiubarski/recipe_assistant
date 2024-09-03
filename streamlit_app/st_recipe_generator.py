import sys
import pathlib
import os
from dotenv import load_dotenv
import streamlit as st

sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")

from src.core.base_template_retriever import BaseTemplateRetriever
from src.recipe_generator.generator_input_handler import GeneratorInputHandler 
from src.core.base_prompt_populator import BasePromptPopulator
from src.llm_invokers.openai_invoker import OpenAIInvoker
from src.recipe_generator.generator_script import generate_recipes
# from streamlit_app.st_utils import set_openai_organisation

load_dotenv()
OPENAI_KEY=os.getenv("OPENAI_KEY")

def display_generated_recipes():

    recipe_object_list = generate_recipes(
        st.session_state.ingredients_list, 
        st.session_state.recipe_style_list,
        num_recipes=2)
    
    for recipe_object in recipe_object_list:
        with st.expander(label=recipe_object['name']):
            st.write(recipe_object['ingredients'])
            st.write(recipe_object['instructions'])
