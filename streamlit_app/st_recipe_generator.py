import sys
import pathlib
import streamlit as st
from typing import Literal

sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")
from src.recipe_generator.generator_script import generate_llm_recipes, load_mock_recipes

def choose_difficulty_colour(difficulty: Literal['easy, medium', 'hard']) -> str:
    """Choose the colour that corresponds to the cooking difficulty

    Args:
        difficulty (Literal): easy, medium or hard

    Returns:
        str: colour that maps to the difficulty
    """
    difficulty_mapping = {
        'easy': 'green',
        'medium': 'orange',
        'hard': 'red'
    }
    
    return difficulty_mapping.get(difficulty, 'black')

def choose_recipe_list(dev_mode:bool) -> list[dict]:
    """Choose which recipe list to return based on whether app is running in dev_mode.

    Args:
        dev_mode (bool): Whether app is in dev mode or not

    Returns:
        list[dict]: relevant list of recipe objects. 
            Load mock recipe object list from a JSON file if in dev mode.
            Invoke LLM to generate recipes if not in dev mode.
    """
    if dev_mode:
        return load_mock_recipes("mock_recipes_3.json")
    else:
        return generate_llm_recipes(
            st.session_state.ingredients_list, 
            st.session_state.recipe_style_list,
            st.session_state.allergies_list,
            num_recipes=1)

def display_generated_recipes(dev_mode=True):

    recipe_object_list = choose_recipe_list(dev_mode)

    for recipe_object in recipe_object_list:
        # TODO: put expansion state of expander into session state so that it doesn't collapse when users interact with chat bot
        with st.expander(label=f"**{recipe_object['name']}**",): 
            
            col1, col2 = st.columns(2)

            with col1:
                # Serving quantity
                st.markdown(f"Serves: **{recipe_object['serving_quantity']}**")

                # Allergens
                allergens_str = ", ".join(recipe_object['allergens'])
                st.markdown(f"Allergens: **{allergens_str}**")

            with col2:
                # Difficulty
                difficulty_colour = choose_difficulty_colour(recipe_object['difficulty'])
                st.markdown(f"Difficulty: :{difficulty_colour}[**{recipe_object['difficulty']}**]")

                # Cooking time
                st.markdown(f"Cooking time: **{recipe_object['total_time']} mins**")

            # Ingredients
            st.markdown("#### Ingredients")
            for ingredient, quantity in recipe_object['ingredients'].items():
                st.markdown(f"- **{ingredient}**: *{quantity}*")

            ### Indent the lists
            st.markdown('''
                <style>
                [data-testid="stMarkdownContainer"] ul,
                [data-testid="stMarkdownContainer"] ol {
                    list-style-position: inside;
                }
                </style>
                ''', unsafe_allow_html=True)
            
            # Instructions
            st.markdown("#### Instructions")
            for index, instruction in enumerate(recipe_object['instructions'], start=1):
                st.markdown(f"{index}. **{instruction}**")
            
            
