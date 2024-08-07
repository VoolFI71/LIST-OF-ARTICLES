from sqlalchemy import *
import sqlite3

with sqlite3.connect("db/database.db") as db:
    cursor = db.cursor()
    cursor.execute(""" DROP TABLE logins """)
    cursor.execute(""" DROP TABLE lists """)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS logins(nick TEXT PRIMARY KEY, password TEXT, role TEXT, token TEXT, email TEXT, city TEXT, age TEXT, about TEXT) """)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS lists(nick TEXT, title TEXT, description TEXT) """)
    db.commit()