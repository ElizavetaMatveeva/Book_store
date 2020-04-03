import sqlite3


class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, "
                         "year INTEGER, isbn INTEGER)")

        self.conn.commit()

    def view_all(self):
        self.cur.execute("SELECT * FROM books")
        books = self.cur.fetchall()
        return books

    def search(self, title, author, year, isbn):
        values = [value if value else "%" for value in (title, author, year, isbn)]  # If some search fields are empty,
        # they're replaced with a % symbol meaning it can be a string of 0 characters or more
        self.cur.execute("SELECT * FROM books WHERE title LIKE ? AND author LIKE ? AND year LIKE ? AND isbn LIKE ?",
                         values)
        books = self.cur.fetchall()
        return books

    def add(self, title, author, year, isbn):
        self.cur.execute("INSERT INTO books VALUES(NULL,?,?,?,?)", (title, author, year, isbn))
        self.conn.commit()

    def update(self, id, title, author, year, isbn):
        self.cur.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
                         (title, author, year, isbn, id))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM books WHERE id=?", (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
