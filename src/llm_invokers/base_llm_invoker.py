from abc import ABC, abstractmethod

class BaseLLMInvoker(ABC):

    @abstractmethod
    def get_response(self, input_dict: dict, chain, dev_mode=True) -> str:
        """Execute the prompt and get a response from the LLM.

        Args:
            input_dict (dict): dictionary of inputs to format into the template
            chain: LLM chain to invoke
            dev_mode (bool, optional): Whether the app is running in dev mode to reduce development costs.
                - True: A mock output is returned.
                - False: The LLM is invoked.
                Defaults to True.
            
        Returns:
            str: The response from the LLM or mock output.
        """
        pass
