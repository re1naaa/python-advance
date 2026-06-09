from fastapi import FastAPI, HTTPException
from typing import List

import database
import models

from models import Recipe, RecipeCreate

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Recipe CRUD API"
    }


@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate):
    recipe_id = database.create_recipe(recipe)

    return models.Recipe(
        id=recipe_id,
        **recipe.dict()
    )


@app.get("/recipes/", response_model=List[Recipe])
def read_recipes():
    return database.read_recipes()


@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: int):
    recipe = database.read_recipe(recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return recipe


@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: RecipeCreate):

    updated = database.update_recipe(
        recipe_id,
        recipe
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return models.Recipe(
        id=recipe_id,
        **recipe.dict()
    )


@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):

    deleted = database.delete_recipe(recipe_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return {
        "message": "Recipe deleted successfully"
    }