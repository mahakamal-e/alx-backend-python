#!/usr/bin/python3

import mysql.connector


def stream_users_in_batches(batch_size):
    """ fetchs users in batches form database """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'    
    )
    try:
        cursor = connection.cursor(dictionary=True, buffered = True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    
    finally:
        cursor.close()
        connection.close()
    

def batch_processing(batch_size):
    """ Process each batch and fillter it based on age"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)