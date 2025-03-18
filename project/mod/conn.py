import pymysql, pandas as pd, streamlit as st

def get_conn():
    return pymysql.connect(host = "localhost", user = "root", password = "Mayank3@", database = "my_database", cursorclass = pymysql.cursors.DictCursor)


def run_query(query):
    conn = get_conn()

    with conn.cursor() as cursor:
        cursor.execute(query)

        result = cursor.fetchall()

    

    conn.close()

    return pd.DataFrame(result)

