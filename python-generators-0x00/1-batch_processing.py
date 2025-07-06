#!/usr/bin/python3

import mysql.connector


def stream_users_in_batches(batch_size):
    """Fetch users in batches from database"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )
    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            for user in batch:
                yield user
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """Process each user and filter based on age"""
    results = []
    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            results.append(user)
            print(user)
    return results
