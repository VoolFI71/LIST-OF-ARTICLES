import sqlite3

with sqlite3.connect("db/database.db") as db:
    cursor = db.cursor()
    db.execute("DROP TABLE IF EXISTS chat")
    cursor.execute(""" CREATE TABLE IF NOT EXISTS logins(nick TEXT PRIMARY KEY, password TEXT, role TEXT, email TEXT, city TEXT, age TEXT, about TEXT) """)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS lists(nick TEXT, title TEXT, description TEXT) """)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS chat(message TEXT, id TEXT) """)

    db.commit()
    