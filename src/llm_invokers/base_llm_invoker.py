from abc import ABC, abstractmethod

class BaseLLMInvoker(ABC):

    @abstractmethod
    def get_response(self, prompt: str) -> str:
        """Execute the prompt and get response from the LLM

        Args:
            prompt (str): prompt to invoke

        Returns:
            str: response from the LLM
        """
        pass
