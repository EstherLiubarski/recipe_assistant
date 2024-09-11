from pydantic import BaseModel, Field
from typing import Literal

class Recipe(BaseModel):
    recipe_id: int = Field("...", description="Recipe ID")
    name: str = Field("...", description="Recipe name")
    ingredients: dict = Field("...", description="Dictionary of ingredient: quantity required for recipe as key: value pairs")
    instructions: list = Field("...", description="List of instructions in order of execution")
    serving_quantity: int = Field("...",description="How many people this recipe serves")
    total_time: int = Field("...", description="Estimated time to prepare this recipe (minutes)")
    allergens: list = Field("...", description="List of allergens found in this recipe")
    difficulty: Literal['easy', 'medium', 'hard'] = Field("...", description="Recipe level of difficulty")