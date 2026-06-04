import sqlite3
from models import Recipe, Category


def create_connection():

    connection = sqlite3.connect("categorys.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


create_table()


def create_category(category: Category) -> int:

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO categorys (title, director) VALUES (?, ?)", (category.title, category.director))
    connection.commit()
    category_id = cursor.lastrowid
    connection.close()
    return category_id


def read_category():

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categorys")
    rows = cursor.fetchall()
    connection.close()
    categorys = [Category(id=row[0], title=row[1], director=row[2]) for row in rows]
    return categorys


def read_recipe(recipe_id: int):

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Recipe(id=row["id"], title=row["title"], director=row["director"])

def update_category(recipe_id: int, category: Category) -> bool:

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE categorys SET title = ?, director = ? WHERE id = ?", (category.title, category.director, recipe_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0


def delete_category(recipe_id: int) -> bool:

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM categorys WHERE id = ?", (recipe_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0