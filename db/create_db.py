import mysql.connector
from mysql.connector import Error
#from config import db_host, db_database, db_user, db_password

def create_database(host, database, user, password):
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
        cursor.execute(f"DROP DATABASE IF EXISTS {database}")
        cursor.execute(f"CREATE DATABASE {database}")
        print(f"Database {database} created successfully")

    except Error as error:
        print(f"Failed to create database {database}: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
