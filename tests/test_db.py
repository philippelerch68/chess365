import pytest
import mysql.connector
from mysql.connector import Error
from helpers import read_yaml
from db.create_db import create_database
from db.create_tables import create_tables
from db.db_ddl import tables


#database params
@pytest.fixture
def define_database_params():
    """Reads in the project config file and returns a list of parameters to create a test database
    
    Args:
        yaml_file: yaml file that contains the project config parameters
    
    Returns:
        list: list of database parameters
    """
    config = read_yaml("config.yaml")
    db_host=config.get('DATABASE').get('db_host')
    db_database='pytest_db'
    db_user=config.get('DATABASE').get('db_user')
    db_password=config.get('DATABASE').get('db_password')
    db=[db_host, db_database, db_user, db_password]

    return db


#database tables
@pytest.fixture
def define_tables():
    """Reads the database table definitions from the project

    Returns:
        dict: dictionary with project table definitions
    """
    return tables


def test_mysql(define_database_params):
    """Test connection to mysql instance

    Args:
        define_database_params: pytest.fixture function that returns a list with connection parameters
    """
    #connect to mysql instance
    db = define_database_params
    try:
        connection = mysql.connector.connect(host=db[0], user=db[2], password=db[3])
        test_connection = connection.is_connected()
        connection.close()      
    except mysql.connector.Error as error:
        test_connection = False
    finally:
        if connection.is_connected():
            connection.close()

    assert test_connection == True


def test_create_database(define_database_params):
    """Test to create a database pytest_db on the mysql instance

    Args:
        define_database_params: pytest.fixture function that returns a list with connection parameters
    """
    db = define_database_params
    #create database
    create_database(host=db[0], database=db[1], user=db[2], password=db[3])
    
    #connect to created test database
    try:
        connection = mysql.connector.connect(host=db[0], database=db[1], user=db[2], password=db[3])
        test_connection = connection.is_connected()
        connection.close()      
    except mysql.connector.Error as error:
        test_connection = False
    finally:
        if connection.is_connected():
            connection.close()

    assert test_connection == True


def test_create_tables(define_database_params, define_tables):
    """Test to create tables in a database pytest_db on the mysql instance

    Args:
        define_database_params: pytest.fixture function that returns a list with connection parameters
        define_tables: pytest.fixture function that returns a dictionary wit table definitions
    """
    db = define_database_params
    tables_dict = define_tables
    
    #create database
    create_database(host=db[0], database=db[1], user=db[2], password=db[3])
    
    #create tables
    create_tables(tables_dict, host=db[0], database=db[1], user=db[2], password=db[3])
    
    #test if tables are created
    try:
        connection = mysql.connector.connect(host=db[0], database=db[1], user=db[2], password=db[3])
        cursor = connection.cursor()
        cursor.execute("Show tables;")
        db_tables = cursor.fetchall()
        cursor.close()
        connection.close()      
    except mysql.connector.Error as error:
        db_tables = []
    finally:
        if connection.is_connected():
            connection.close()

    assert (('dim_eco',) in db_tables) == True
    assert (('dim_federation',) in db_tables) == True
    assert (('dim_location',) in db_tables) == True
    assert (('dim_result',) in db_tables) == True
    assert (('dim_title',) in db_tables) == True
    assert (('event',) in db_tables) == True
    assert (('game',) in db_tables) == True
    assert (('games_raw',) in db_tables) == True
    assert (('moves',) in db_tables) == True
    assert (('player',) in db_tables) == True
    assert (('playerdetails',) in db_tables) == True
    assert (('players_raw',) in db_tables) == True


def test_rm_db(define_database_params):
    """Remove database after running the tests

    Args:
        define_database_params: pytest.fixture function that returns a list with connection parameters
    """
    db = define_database_params

    connection = mysql.connector.connect(host=db[0], database=db[1], user=db[2], password=db[3])
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db[1]}")
    cursor.close()
    connection.close()