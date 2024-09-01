from abc import ABC, abstractmethod

class BasePromptPopulator(ABC):
           
    @abstractmethod
    def format_langchain_prompt():
        pass