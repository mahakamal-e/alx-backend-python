#!/usr/bin/python3

import mysql.connector


def stream_users():
    """Generator function that streams users row by row using yield from the database."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )

    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    finally:
        cursor.close()
        connection.close()
