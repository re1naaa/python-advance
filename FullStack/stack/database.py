import sqlite3
from models import MovieCreate

def create_connection():
    connection = sqlite3.connect("movie.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    Create TABLE IF NOT EXISTS movies(
    id Integer PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    director TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

create_table()


def create_movie(movie : MovieCreate) -> int:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO movies (title , director) VALUES (?, ?)", (movie.title , movie.director))
    connection.commit()
    movie_id = cursor.lastrowid
    connection.close()
    return movie_id

def read_movies():

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    connection.close()
    movies = [Movie(id=row[0], title=row[1], director=row[2]) from row in rows]
    return movies

def update_movie(movie_id: int , movie: MovieCreate) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("Update movies SET title = ? , director =? Where id =?" , (movie.title, movie.director, movie_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0

def delete_movie(movie_id: int) -> bool:

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("Delete from movies Where id?", (movie_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0