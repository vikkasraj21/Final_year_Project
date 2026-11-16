import mysql.connector
from mysql.connector import Error
import os

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ["MYSQL_PASSWORD"],
            database="college_timetable",
            port=3306
        )

        if connection.is_connected():
            print("MySQL Database Connected Successfully!")
            return connection

    except (Error, KeyError) as e:
        print(f"Database Connection Error: {e}")
        return None