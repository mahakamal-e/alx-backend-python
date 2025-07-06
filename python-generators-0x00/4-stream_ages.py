#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """Generator to stream user ages one by one from the database"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )
    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row['age']
    finally:
        cursor.close()
        connection.close()