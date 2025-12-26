import sqlite3

DB_PATH = "order_app.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
