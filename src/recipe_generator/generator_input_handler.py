from src.core.base_input_handler import BaseInputHandler

class GeneratorInputHandler(BaseInputHandler):

    def process_input(input_string:str):
        return "Processed input:", input_string
    
    def make_inputs_dict(ingredients_list:list, 
                        num_recipes: int, 
                        recipe_style: str,
                        ) -> dict:
        """Builds dictionary of inputs for chat templates

        Args:
            ingredients_list (list): list of ingredients to prioritise in the generated recipt
            num_recipes (int): number of recipes to generate
            recipe_style (str): list of adjectives describing the recipe e.g. healthy, vegan

        Returns:
            dict: dictionary with required inputs to populate the prompt template
        """
        inputs = {"ingredients_list":ingredients_list, 
                  "num_recipes": num_recipes, 
                  "recipe_style": recipe_style,}

        return inputs
    
        
    @staticmethod
    def make_chain(prompt:str, model, parser):
        """Make an LLM chain

        Args:
            prompt (str): prompt template
            model (str): OpenAI model
            parser (Optional[Union[None, PydanticOutputParser]], optional): The datamodel name to parse the LLM response into. 
                - None: No parsing will be done. Will return the response as a string
                - str: The name of the datamodel to use for parsing the output. Will return the reponse as a pydantic datamodel.
                Defaults to None.

        Returns:
            _type_: _description_
        """
        return prompt | model | parser

    @staticmethod
    def format_recipe_style(recipe_options:list) -> str:
        """Format a list of adjectives describing a recipe into a string 
        that can be formatted into a natural language prompt.
        

        Args:
            recipe_options (list): list of recipe adjectives 
                e.g. ["Healthy", "Vegan", "Hearty"]

        Returns:
            str: recipe adjectives formatted into a string
                e.g. "healthy, vegan and hearty"
        """
        recipe_options = [option.lower() for option in recipe_options]

        if len(recipe_options)==0:
            return ""
        elif len(recipe_options) == 1:
            return recipe_options[0]
        else:
            return ', '.join(recipe_options[:-1]) + ' and ' + recipe_options[-1]
        
    


