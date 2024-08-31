from typing import Union, Optional
from src.llm_invokers.base_llm_invoker import BaseLLMInvoker


class OpenAIInvoker(BaseLLMInvoker):
    def __init__(self, 
    #              api_key:str, 
    #              model:str, 
    #              purpose:str
                 ) -> None:
        pass
    #     """Initialise LLM invoker

    #     Args:
    #         api_key (str): OpenAI API key
    #         model (str): OpenAI model
    #         purpose (str): purpose of the LLM. Choose from 
    #             - "chat_bot"
    #             - "recipe_generator"
    #     """
        # self.api_key=api_key
        # self.purpose=purpose
        # self.model=model

    def dev_mode_reponse(self, input_dict):
        return input_dict
        
    def invoke_llm(self, input_dict:dict, chain): 
        """Invoke OpenAI LLM

        Args:
            prompt (dict): dictionary of inputs to format into the template
            chain: chain to invoke
        """
        return chain.invoke(input_dict)
        

    def get_response(self, input_dict: dict, chain=None, dev_mode=False) -> str:
        """Execute the prompt and get a response from the LLM.

        Args:
            input_dict (dict): dictionary of inputs to format into the template
            chain: LLM chain to invoke. Defaults to None
            dev_mode (bool, optional): Whether the app is running in dev mode to reduce development costs.
                - True: A mock output is returned.
                - False: The LLM is invoked.
                Defaults to True.
            
        Returns:
            str: The response from the LLM or mock output.
        """
        if dev_mode:
            response = self.dev_mode_reponse(input_dict)
        else:
            response=self.invoke_llm(input_dict, chain)
        return response