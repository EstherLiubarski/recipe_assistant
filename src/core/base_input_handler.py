from abc import ABC, abstractmethod

class BaseInputHandler(ABC):
    
    @abstractmethod
    def process_input(input_string:str):
        pass

    @abstractmethod
    def make_inputs_dict(**kwargs) -> dict:
        """Builds a dictionary of inputs based on user data

        Returns:
            dict: dictionary of inputs to populate the template
        """
        pass