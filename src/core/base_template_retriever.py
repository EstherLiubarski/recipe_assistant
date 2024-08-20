from abc import ABC, abstractmethod
import yaml

class BaseTemplateRetriever(ABC):

    # @abstractmethod
    def load_templates(feature:str):
        """Load the file of prompts and prompt templates.

        Args:
            feature (str): prompts and templates to load. One of:
                - "chat"
                - "recipe_generator"
        """
        file_name = "../src/templates_repo/" + feature + "_prompts.yml"
        with open(file_name, 'r') as file:
            return yaml.safe_load(file)
