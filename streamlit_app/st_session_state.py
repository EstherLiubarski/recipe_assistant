import streamlit as st

class State:
    def init_session_states() -> None:
        """Initiate all session state variables
        """
        session_states_init={
            "tool_description": 
                "##### The Recipe Assistant is an AI-powered tool designed to help you generate personalised recipes, "
                "answer cooking-related questions and guide you through meal preparation. \n\n "
                "##### Simply submit your available ingredients and cooking preferences to generate your recipes. "
                "Your friendly chat bot is also at your service to answer all your culinary questions. \n\n "
                "##### Happy cooking!",
            "chat_history":[{"role": "assistant", "content": "Hi there, I'm your friendly recipe assistant! How can I help you?"}],
            "prompt_repo": None,
            "recipe_options":['Healthy', 'Quick', 'Hearty', 'Light', 'Vegan', 'Vegetarian'],
            "ingredients_list":[],
            "recipe_style_list":[],
            "submit_ingredients": False,
            "clear_ingredients": True,
            "allergies_list": []
        }
        
        # Add initial session_state values to session_state
        for (name, def_val) in session_states_init.items():
            st.session_state[name] = def_val

        # Prevent state from being re-initalised
        st.session_state.state_initialised=True

