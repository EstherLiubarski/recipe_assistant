from src.llm_invokers.base_llm_invoker import BaseLLMInvoker

class OpenAIInvoker(BaseLLMInvoker):
    def __init__(self, api_key:str) -> None:
        self.api_key=api_key

    def get_response(self, prompt: str) -> str:
        """Execute the prompt and get response from the LLM

        Args:
            prompt (str): prompt to invoke

        Returns:
            str: response from the LLM
        """
        return f"Response to the {prompt} with API key {self.api_key}"