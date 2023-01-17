import mysql.connector
from mysql.connector import Error
from config import host, database, user, password


def create_database(host=host, database=database, user=user, password=password):
    """DDL step; creates the database

    Args:
        host (str): ip_address. Defaults to host defined in config.
        database (str): name of the database. Defaults to database defined in config.
        user (str): database user for connection. Defaults to user defined in config.
        password (str): password of the user. Defaults to password defined in config.
    """

    try:
        connection = mysql.connector.connect(host=host,
                                            user=user,
                                            password=password)

        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {db_database}")
        cursor.execute(f"CREATE DATABASE {db_database}")
        print(f"Database {db_database} created successfully")

    except Error as error:
        print(f"Failed to create database {db_database}: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
