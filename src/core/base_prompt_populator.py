from abc import ABC, abstractmethod

class BasePromptPopulator(ABC):
           
    @abstractmethod
    def format_langchain_prompt(**kwargs):
        """Format input variables into a Langchain prompt template.

        Returns:
            The formatted prompt template.
        """
        pass