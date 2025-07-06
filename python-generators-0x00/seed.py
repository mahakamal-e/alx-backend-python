#!/usr/bin/python3
import mysql.connector
import csv
from uuid import uuid4


def connect_db():
    "Connect to MySQL server database "
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = ''
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """ Create database ALX_prodev if doesn't exist."""
    curser = connection.cursor()
    curser.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    curser.close()


def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print("Error: {err}")
        return None

 
def create_table(connection):
    """Create table inside database if not exists"""
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email varchar(255) NOT NULL,
        age DECIMAL NOT NULL
    );
    """
    cursor.execute(query)
    cursor.close()


def insert_data(connection, data):
    """Insert data from CSV file INTO table user_data """
    cursor = connection.cursor()
    with open(data, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (row['user_id'],))
            if cursor.fetchone():
                continue
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (str(uuid4()), row['name'], row['email'], row['age'])
            )
    connection.commit()
    cursor.close()