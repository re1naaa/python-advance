from pydantic import BaseModel


class RecipeCreate(BaseModel):
    name: str
    description: str
    meal_type: str


class Recipe(RecipeCreate):
    id: int