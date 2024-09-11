import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")

import streamlit as st
from streamlit_tags import st_tags
from streamlit_app.st_session_state import State
from streamlit_app.st_recipe_generator import display_generated_recipes
from streamlit_app.st_chat_bot import display_chat_bot
from st_utils import display_empty_recipes

st.set_page_config(
    page_title="Recipe Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Recipe Assistant")

if "state_initialised" not in st.session_state:
    State.init_session_states()

with st.sidebar:
    with st.form(key='recipe_inputs'):
        st.session_state.ingredients_list = st_tags(label='## Enter ingredients',
                                    text='Press enter to add more ingredients',
                                    key='user_ingredients')
        
        st.session_state.recipe_style_list = st.multiselect(
            "Select recipe type", 
            options=st.session_state.recipe_options,
            )
        
        ingredients_button=st.form_submit_button(label='Generate recipes')
        if ingredients_button:
            st.session_state.submit_ingredients=True


recipe_col, chat_col = st.columns([6,4], gap="medium")

st.session_state.submit_ingredients = True

with recipe_col:
    if not st.session_state.submit_ingredients:
        display_empty_recipes()

    else:
        # TODO: error for if user hasn't submitted ingredients
        display_generated_recipes(dev_mode=False)

with chat_col:
    with st.expander(label='Chat Bot', expanded=True): 
        display_chat_bot(dev_mode=True)


