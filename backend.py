import sqlite3


def connect():
    conn = sqlite3.connect("book_store.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, "
                "isbn INTEGER)")
    conn.commit()
    conn.close()


def view_all():
    conn = sqlite3.connect("book_store.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    conn.close()
    return books


def search(title, author, year, isbn):
    values = [value if value else "%" for value in (title, author, year, isbn)]  # If some search fields are empty,
    # they're replaced with a % symbol meaning it can be a string of 0 characters or more
    conn = sqlite3.connect("book_store.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE title LIKE ? AND author LIKE ? AND year LIKE ? AND isbn LIKE ?", values)
    books = cur.fetchall()
    conn.close()
    return books


def add(title, author, year, isbn):
    conn = sqlite3.connect("book_store.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books VALUES(NULL,?,?,?,?)", (title, author, year, isbn))
    conn.commit()
    conn.close()


def update(id, title, author, year, isbn):
    conn = sqlite3.connect("book_store.db")
    cur = conn.cursor()
    cur.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
    conn.commit()
    conn.close()


def delete(id):
    conn = sqlite3.connect("book_store.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()


connect()
