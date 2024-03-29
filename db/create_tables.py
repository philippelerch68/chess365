import mysql.connector
from mysql.connector import Error


def create_tables(tables_dict, host, database, user, password):
    """DDL step; creates defined tables in database

    Args:
        tables_dict (dict): definition of tables
        host (str): ip_address
        database (str): name of the database
        user (str): database user for connection
        password (str): password of the user
    """

    try:
        connection = mysql.connector.connect(host=host,
                                            database=database,
                                            user=user,
                                            password=password)

        cursor = connection.cursor()
        print(f"Connection to database {database} established successfully")
        
        for tab in tables_dict.keys():
            try: 
                result0 = cursor.execute(f"DROP TABLE IF EXISTS {tab}")
                result = cursor.execute(f"CREATE TABLE {tab} {tables_dict.get(tab)}")
                print(f"Table {tab} created successfully ")
                
            except mysql.connector.Error as error:
                print(f"Failed to create table {tab}: {error}")

    except mysql.connector.Error as error:
        print(f"Failed to connect to database {database}: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print(f"Connection to database {database} is closed")