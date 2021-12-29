import sqlite3
from flask import g

DATABASE = 'C:/Users/30697/Desktop/Thesis/flask/lightning_app/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#app.teardown_appcontext
def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()