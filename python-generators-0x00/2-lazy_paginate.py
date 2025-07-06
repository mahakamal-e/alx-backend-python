#!/usr/bin/python3
import mysql.connector


def stream_user_ages():
    """ Generator that streams user ages """
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
        

def calculate_average_age():
    """ Calculate the average age using generator """
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age}")