from langchain.output_parsers import PydanticOutputParser

def make_pydantic_parser(pydantic_object) -> PydanticOutputParser:
        """Create a Pydantic output parser

        Args:
            pydantic_object (BaseModel): Pydantic base model schema

        Returns:
            PydanticOutputParser: Langchain output parser
        """
        return PydanticOutputParser(pydantic_object)