import mysql.connector
from mysql.connector import Error
from config import *


#create database
try:
    connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password
    )

    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_database}")
    cursor.execute(f"CREATE DATABASE {db_database}")
    print(f"Database {db_database} created successfully")

except Error as error:
    print(f"Failed to create database in MySQL: {error}")
finally:
    if connection.is_connected():
        print("The following databases are available:")
        cursor.execute("SHOW DATABASES")
        for x in cursor:
            print(x) 
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
