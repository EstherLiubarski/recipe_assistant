from src.core.base_prompt_populator import BasePromptPopulator
from langchain_core.prompts import PromptTemplate

class GeneratorPromptPopulator(BasePromptPopulator):

    @staticmethod
    def format_inputs_into_template(template:str, arguments: dict) -> str:
        """Format the arguments into the prompt template

        Args:
            template (str): prompt template
            arguments (dict): dictionary of arguments to format into the template where keys
                of dictionary match the name of the placeholders in the prompt

        Returns:
            str: populated prompt template
        """
        try:
            return template.format(**arguments)
        except KeyError as e:
            raise ValueError(f"Missing key in arguments: {e}")
        
    @staticmethod
    def choose_style_instructions(recipe_options:list, style_instructions_template:str) -> str:
        """Determines appropriate style instructions to include in the main system prompt.
        Checks if user has selected recipe specifications.

        Args:
            recipe_options (list): _description_
            style_instructions_template (str): _description_

        Returns:
            str: empty string if user doesn't specify a recipe style. 
                Otherwise, returns the style instructions template.
        """
        if recipe_options==['No Specifications']:
            return ""
        else:
            return style_instructions_template

    def format_langchain_prompt(template:str, 
                                input_variables: list, 
                                format_instructions:str,
                                style_instructions: str
                                )-> PromptTemplate:
        """Formats the template, input variables and partial variables into a LangChain prompt template.

        Args:
            template (str): instructions to the LLM on how to generate recipes
            input_variables (list): user-specified input variables to be formatted into the template.
            format_instructions (str): instructions for how to parse te LLM output
            style_instructions (str): style instructios template or empty string if user doesn't specify a recipe style.

        Returns:
            PromptTemplate: the prompt template with the formatted input and partial variables
        """
        partial_variables = {"format_instructions": format_instructions,
                             "style_instructions": style_instructions}
        
        prompt = PromptTemplate(
            template=template,
            input_variables=input_variables,
            partial_variables= partial_variables
        )
        return prompt