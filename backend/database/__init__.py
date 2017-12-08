import re
import sqlite3

from twisted.enterprise import adbapi

from backend.database.schema import create_tables_query


def cp_openfun(conn):
    conn.create_function('regexp', 2, lambda p, i: 1 if re.search(p, i) else 0)
    print(conn)


data_db = 'data.db'
data_db_conn = adbapi.ConnectionPool('sqlite3', data_db, cp_openfun=cp_openfun, check_same_thread=False)


def create_data_db():
    conn = sqlite3.connect(data_db)
    cursor = conn.cursor()
    for key, value in create_tables_query.items():
        cursor.execute(value)
    conn.commit()
    conn.close()


def close_data_db():
    data_db_conn.close()


create_data_db()
