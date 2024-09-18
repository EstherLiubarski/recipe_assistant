# Recipe Assistant - README

## Project Overview

This project is an LLM-powered recipe assistant that generates and presents recipes based on user input. The assistant is capable of handling recipe requests, preparing an LLM prompt given the inputs using Langchain, invoking LLMs for recipe generation, and presenting the generated content via a Streamlit app.

### Features:
- **Recipe Generator:** Create recipes based on user input and specific style instructions.
- **Chatbot Interface:** A conversational cooking chat bot.
- **Streamlit Integration:** A web interface for users to interact with the recipe generator and chatbot.
- **LLM Invocation:** Currently uses OpenAI to power recipe creation and chat responses, but can easily be replaced with another provider.
- **Templates System:** Predefined templates for generating prompts, chat responses, and recipes.

---

## Project Structure

```bash
src/
    ├── __init__.py
    ├── chat_bot/
    │   ├── chat_bot_script.py         # Script to execute chat bot workflow 
    │   ├── chat_input_handler.py      # Handles user inputs for chat
    │   └── chat_prompt_populator.py   # Populates templates for chat prompts
    ├── core/
    │   ├── base_input_handler.py      # Base class for input handling
    │   ├── base_prompt_populator.py   # Base class for populating prompts
    │   └── base_template_retriever.py # Base template management
    ├── llm_invokers/
    │   ├── openai_invoker.py          # LLM interaction with OpenAI API
    │   └── base_llm_invoker.py        # Base LLM invocation class
    ├── recipe_generator/
    │   ├── generator_input_handler.py # Handles input for recipe generation
    │   ├── generator_prompt_populator.py # Populates recipe-related prompts
    │   ├── generator_script.py        # Script to execute recipe generator workflow 
    │   └── recipe_object.py           # Defines recipe object structure
    ├── templates_repo/
    │   ├── chat_prompts.yml           # YAML file containing chat templates
    │   └── recipe_generator_prompts.yml # YAML file for recipe generation templates
streamlit_app/
    ├── app.py                         # Main entry point for Streamlit app
    ├── st_chat_bot.py                 # Streamlit interface for chatbot
    ├── st_recipe_generator.py         # Streamlit interface for recipe generator
    ├── st_session_state.py            # Manages Streamlit session state
    └── st_utils.py                    # Utility functions for Streamlit app
test_scripts/
    ├── test_chat_bot.py               # Tests for chat functionality
    └── test_recipe_generator.py       # Tests for recipe generator functionality
requirements.yml                       # Project package requirements
```

---

## Key Files and Directories

- **src/chat_bot/** - Chat-bot backend scripts.
- **src/recipe_generator/** - Recipe generation backend scripts.
- **src/llm_invokers/** - Invoke language models.
- **streamlit_app/** - Streamlit web-app code.
- **test_scripts/** - Unit and integration tests for the project.
- **templates_repo/** - Template files for populating chat and recipe prompts.
---

## Setup Instructions

### 1. Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/EstherLiubarski/recipe_assistant.git
cd recipe_assistant
```

### 2. Install Dependencies:

Set up your project environment using either **Conda** or a **virtual environment (venv)**:

#### **1a. Create Conda Environment:**

1. Install the required packages using Conda:

    ```bash
    conda env create -f requirements.yml
    conda activate recipe_assistant
    ```

2. Ensure all dependencies are installed as per the `requirements.yml` file.

#### **1b. Create Virtual Environment (venv):**

1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

#### **2. Install the required packages from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
### Configure OpenAI API Key

To interact with OpenAI's API, you'll need an API key. If you don't already have one, follow step 1 to obtain it:

1. **Obtain an OpenAI API Key**:

   - Go to [OpenAI’s API Key setup page](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key).
   - Follow the instructions to sign up or log in.
   - Once you’ve completed the setup, you’ll receive a secret key starting with `sk-` followed by a combination of numbers and letters.

2. **Add API Key to Configuration**:

   After obtaining your API key, configure it in your project:

   - Create a `.env` file in the base directory.
   - Add the following line to the `.env` file:

     ```plaintext
     OPENAI_KEY="your-openai-api-key"
     ```

   Replace `"your-openai-api-key"` with the actual secret key you obtained from OpenAI.

---

### 3. Running the Project

#### 1 Running the Streamlit App

To launch the Streamlit app (user interface):

```bash
streamlit run streamlit_app/app.py
```

This command will start the Streamlit server and automatically open a browser window through which you can interact with the app. 

#### 2 Recipe Generation

All Streamlit components relating to the recipe generator are managed in `streamlit_app/st_recipe_generator.py`. This script connects to the backend through `src/recipe_generator/generator_script.py`, which handles the recipe generation execution from receiving user inputs to returning a list of generated recipes. 

Calling the generator script in `dev_mode` will return a mock generated recipe rather than invoking an LLM to reduce development costs. 

#### 3 Chatbot

All Streamlit components relating to the chat bot are managed in `streamlit_app/st_chat_bot.py`. This script connects to the backend through `src/chat_bot/chat_bot_script.py`, which handles the chat bot execution from receiving user inputs to returning the chat bot response.

Calling the chat bot script in `dev_mode` will return the user query rather than invoking an LLM to reduce development costs. 

---

### 4. Running Tests

To run the test suite, use `pytest`. For example, to run chat bot tests:

```bash
pytest test_scripts/test_chat_bot.py
```

This will execute tests for the chat functionality.

To run specific test functions, speficy the function, e.g.:

```bash
pytest test_scripts/test_chat_bot.py::test_generate_input_dict
```

---
## Limitations

There is a bug with the Streamlit expanders. If the users expand/collapse an expander, and then interact with the app that forces the script to rerun, the expanders will revert to their initial state. For example:
- Recipe 1 is generated and displayed in an expander, whose initial state is collapsed. 
- User expands recipe 1.
- User submits query to the chat bot. This makes the Streamlit script rerun.
- The expander of recipe 1 is now collapsed as this is its initial state. (Ideally the expander would be expanded as that is the state in which the user left it.)

In order to retain the expansion state of the expanders, the backend needs to know the current state of the expander. However, [the current state of the expander is handled entirely in the Streamlit browser and cannot be accessed from the backend](https://discuss.streamlit.io/t/get-expanded-state-of-st-beta-expander/13177/6). Therefore, we cannot save the state of the expander in the backend, to then re-display it in that state when the script is rerun. This will continue to be a limitation until Streamlit allows the backend to know the expansion state of expanders. 

---

## Future Improvements

- **User inputs -** add allergies, number of servings and metrics as user-configurable inputs.
- **Wild card** recipes generated if users don't input any ingredients.
- **Prompt engineering** to improve LLM outputs.
    - Cooking tips
    - Fun facts about the ingredients? 
- **Replace with alternative LLMs** for flexibility of integration into other projects or environments.
- **Improved error handling** and validation for input.
- **Database integration** for
    - **User accounts -** personalise user experiences and save their preferences and history.
    - **Recipe tracking and rating-** store user-generated recipes, ratings, feedback.
    - **Data collection for model optimisation -** accumulate data for future model improvements.
- **Web scraper integration** to assist LLM-generated responses by connecting to wider web searches.
---


## Contact

For any inquiries, feel free to contact the project maintainer at e.liubarski@gmail.com.

---

