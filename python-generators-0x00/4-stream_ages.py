#!/usr/bin/python3
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


def calculate_average_age():
    """Calculate average age using generator in a memory-efficient way"""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age 
        count += 1

    if count > 0:
        average_age = total_age / count
    else:
        average_age = 0

    print(f"Average age of users: {average_age}")


if __name__ == "__main__":
    calculate_average_age()