import sqlite3
from flask import g
import traceback

DATABASE = 'C:\Users\30697\Desktop\Thesis\flask\lightining_app\Thesis_webapp\database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

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

def get_champion_country_info (country_name: str):
    '''Gets information regarding the selected country.
    Returns only champion country information.
    '''
    db = get_db()
    sql_query = "SELECT * FROM Data WHERE country == ? AND champion == 1"
    cursor = db.execute(sql_query, (country_name,))
    result = cursor.fetchone()
    print(result)
    return result

def set_not_champion (db, id: int):
    '''Set champion values to 0.'''
    try:
        sql_query = "UPDATE Data SET CHAMPION = 0 WHERE ID==(?)"
        cursor = db.execute(sql_query, (id,))
        db.commit()
    except :
        traceback.print_exc()

def check_if_user_allowed_to_add_data (db, username: str, password: str):
    '''Returns True/False based on whether the user and password match any admin pair in the db.'''

    sql_query = "SELECT * FROM USER_CREDENTIALS WHERE USERNAME == ? AND PASSWORD == ?"
    cursor = db.execute(sql_query, (username, password))
    result = cursor.fetchone()
    if result == None:
        return False
    else:
        return True
