import sqlite3
from fileinput import close

from models import Movie, MovieCreate

from lesson24.database import connection


def create_connection():
    connection = sqlite3.connect("movies.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        create table if not exists movies(
            id integer primary key autoincrement
            title text not null
            director text not null
        )
    ''')

    connection.commit()
    connection.close()

create_table()

def create_movie(movie: MovieCreate) -> int:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("insert into movies (title, director) values (?, ?)", (movie.title, movie.directot))
    connection.commit()
    movie_id = cursor.lastrowid
    connection.close()
    return movie_id

def read_movies():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("select * from movies")
    rows = cursor.fetchall()
    connection.close()
    movies = [Movie(id=row[0], tilte=row[1], director=[2]) from row in rows]
    return movies

def read_movie(movie_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("select * from movies where id = ?", (movie_id))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Movie(id=row["id"], tilte=row["title"], director=["director"])
