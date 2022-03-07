import sqlite3
from flask import g
import traceback

DATABASE = '/home/xhino/Desktop/marg_thesis/Thesis_webapp/database.db'

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



def get_champion_id (db, country_name: str):
    '''If there is a champion country return the id, otherwise return NULL.'''
    sql_query = "SELECT * FROM Data WHERE COUNTRY==(?)"
    cursor = db.execute(sql_query, (country_name,))
    results = cursor.fetchall()
    #print(results)
    for result in results:
        if result[12] == 1:
            return result[13]
    return -1

def set_not_champion (db, id: int):
    '''Set champion values to 0.'''
    try:
        sql_query = "UPDATE Data SET CHAMPION = 0 WHERE ID==(?)"
        cursor = db.execute(sql_query, (id,))
        db.commit()
    except :
        traceback.print_exc()