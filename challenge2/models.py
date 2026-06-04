from pydantic import BaseModel

class Category(BaseModel):
    title: str
    director: str

class Recipe(Category):
    id: int