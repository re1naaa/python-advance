import sqlite3
from models import Recipe, RecipeCreate


def create_connection():
    connection = sqlite3.connect("recipes.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            meal_type TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_table()


def create_recipe(recipe: RecipeCreate) -> int:
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO recipes (name, description, meal_type)
        VALUES (?, ?, ?)
        """,
        (
            recipe.name,
            recipe.description,
            recipe.meal_type
        )
    )

    connection.commit()
    recipe_id = cursor.lastrowid
    connection.close()

    return recipe_id


def read_recipes():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM recipes")
    rows = cursor.fetchall()

    connection.close()

    recipes = [
        Recipe(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            meal_type=row["meal_type"]
        )
        for row in rows
    ]

    return recipes


def read_recipe(recipe_id: int):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM recipes WHERE id = ?",
        (recipe_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return Recipe(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        meal_type=row["meal_type"]
    )


def update_recipe(recipe_id: int, recipe: RecipeCreate):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE recipes
        SET name = ?, description = ?, meal_type = ?
        WHERE id = ?
        """,
        (
            recipe.name,
            recipe.description,
            recipe.meal_type,
            recipe_id
        )
    )

    connection.commit()
    updated = cursor.rowcount

    connection.close()

    return updated > 0


def delete_recipe(recipe_id: int):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM recipes WHERE id = ?",
        (recipe_id,)
    )

    connection.commit()
    deleted = cursor.rowcount

    connection.close()

    return deleted > 0