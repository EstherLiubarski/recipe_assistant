import streamlit as st


class State:
    def init_session_states() -> None:
        """Initiate all session state variables
        """
        session_states_init={
            "chat_history":[{"role": "assistant", "content": "Hi there, I'm your friendly recipe assistant! How can I help you?"}],
            "prompt_repo": None,
            "recipe_options":['Healthy', 'Quick', 'Hearty', 'Light', 'Vegan', 'No Specifications'],
            "ingredients_list":[],
            "recipe_style_list":[],
            "submit_ingredients": False,
            "clear_ingredients": True,
        }
        
        # Add initial session_state values to session_state
        for (name, def_val) in session_states_init.items():
            st.session_state[name] = def_val

        # Prevent state from being re-initalised
        st.session_state.state_initialised=True

