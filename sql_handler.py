import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        curr = conn.cursor()
        curr.execute(create_table_sql)

    except Error as e:
        print(e)

def insert_data(conn, insert_data_sql, values):
    try:
        curr = conn.cursor()
        curr.execute(insert_data_sql, values)
        conn.commit()

    except Error as e:
        print(e)

def update_data(conn, update_data_sql):
    try:
        curr = conn.cursor()
        curr.execute(update_data_sql)
        conn.commit()

    except Error as e:
        print(e)

def retrieve_data(conn, retrieve_data_sql):
    try:
        curr = conn.cursor()
        curr.execute(retrieve_data_sql)
        return curr.fetchall()

    except Error as e:
        print(e)
        return None