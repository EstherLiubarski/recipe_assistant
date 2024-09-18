import sys
import pathlib
import os
from dotenv import load_dotenv
import streamlit as st

sys.path.append(f"{pathlib.Path(__file__).parent.parent.resolve()}")
from src.chat_bot.chat_bot_script import invoke_chat_bot
from st_utils import append_user_history


load_dotenv()
OPENAI_KEY=os.getenv("OPENAI_KEY")

def display_history():
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

def choose_llm_response(dev_mode:bool, user_query:str) -> str:
    """Choose which chat bot response to return based on whether app is running in dev_mode.

    Args:
        dev_mode (bool): Whether app is in dev mode or not
        user_query (str): user query

    Returns:
        str: relevant chat bot response
            Return the user query if in dev mode.
            Invoke LLM to generate chat bot response if not in dev mode.
    """
    if dev_mode:
        return user_query
    else:
        return invoke_chat_bot(user_query, st.session_state.chat_history)
            

def display_chat_bot(dev_mode=True) -> None:
    """Display the user-LLM chat

    Args:
        dev_mode (bool): whether app is running in dev mode
    """
    with st.expander(label='Chat Bot', expanded=True): 
        # Display previous chat history
        display_history()

        # Text input for user to submit query
        user_query=st.chat_input('Ask me anything, e.g. "What is 100g butter in tablespoons?"', 
                                        key="user_query",
                                        on_submit=append_user_history,)
        
        if user_query:
                
                # Get response to user query 
                llm_response = choose_llm_response(dev_mode, user_query)

                # Append LLM response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content":llm_response})
                st.rerun()