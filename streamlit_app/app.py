import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")
import streamlit as st
from streamlit_tags import st_tags_sidebar, st_tags
from streamlit_app.st_session_state import State
from streamlit_app.st_chat_bot import invoke_chat_bot
from streamlit_app.st_recipe_generator import display_generated_recipes
from st_utils import display_empty_recipes, append_user_history

def display_history():
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

st.set_page_config(
    page_title="Recipe Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Recipe Assistant")

if "state_initialised" not in st.session_state:
    State.init_session_states()



with st.sidebar:
    # if st.session_state.clear_ingredients:
    with st.form(key='recipe_inputs'):
        st.session_state.ingredients_list = st_tags(label='## Enter ingredients',
                                    text='Press enter to add more ingredients',
                                    # value=['Celery', 'Yoghurt', 'Sausages'],
                                    key='user_ingredients')
        
        st.session_state.recipe_style_list = st.multiselect("Select recipe type", options=st.session_state.recipe_options)
        ingredients_button=st.form_submit_button(label='Generate recipe')
        if ingredients_button:
            st.session_state.submit_ingredients=True


recipe_col, chat_col = st.columns([7,3], gap="medium")
st.write(st.session_state.submit_ingredients)

with recipe_col:
    if not st.session_state.submit_ingredients:
        display_empty_recipes()

    else:
        # TODO: error for if user hasn't submitted ingredients
        display_generated_recipes()

with chat_col:
    with st.expander(label='Chat Bot', expanded=True): # TODO: fix chat bot container layout
        display_history()
        # with st.chat_message("assistant")

        user_query=st.chat_input("Ask me anything.", 
                                    key="user_query",
                                    on_submit=append_user_history,)

        if user_query:

            # with st.chat_message("user"):
                # st.markdown(user_query)

            llm_response = invoke_chat_bot(user_query, st.session_state.chat_history)

            # with st.chat_message("assistant"):
            #     st.markdown(llm_response)

            # st.session_state.chat_history.append({"role": "user", "content":user_query})
            st.session_state.chat_history.append({"role": "assistant", "content":llm_response})
            print(st.session_state.chat_history)
            st.rerun()
