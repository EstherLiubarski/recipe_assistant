from abc import ABC, abstractmethod

class PromptPopulator(ABC):
    
    def format_prompt(template:str, arguments: dict) -> str:
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