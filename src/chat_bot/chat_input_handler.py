from src.core.base_input_handler import BaseInputHandler

class ChatInputHandler(BaseInputHandler):

    def process_input(input_string:str):
        return "Processed input:", input_string
    
    def make_inputs_dict(history:list, query:str, additional_input:str=None) -> dict:
        """Builds dictionary of inputs for chat templates

        Args:
            history (list): Chat history starting with the LLM's greeting message
            query (str): user query

            FOR DEVELOPMENT PURPOSES
            additional_input (str): additional input

        Returns:
            dict: dictionary with required inputs to populate the
        """
        inputs = {
            "history": history,
            "query": query
        }

        if additional_input:
            inputs["additional_input"] = additional_input

        return inputs
        