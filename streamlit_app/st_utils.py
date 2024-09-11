import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def set_openai_api_key() -> None:
    """Set the OpenAI environment variable.
    """
    os.environ['OPENAI_KEY']=os.getenv("OPENAI_KEY")

def display_empty_recipes():
    st.markdown("Submit ingredients to generate a recipe")

def append_user_history():
    st.session_state.chat_history.append({"role":"user", 
                                        "content":st.session_state.user_query})