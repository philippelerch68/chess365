import pytest
import mysql.connector
from mysql.connector import Error
from helpers import read_yaml
from db.create_db import create_database


#database params
@pytest.fixture
def define_database_params():
    """Returns parameters to create a test database"""
    config = read_yaml("config.yaml")
    db_host=config.get('DATABASE').get('db_host')
    db_database='pytest_db'
    db_user=config.get('DATABASE').get('db_user')
    db_password=config.get('DATABASE').get('db_password')
    db=[db_host, db_database, db_user, db_password]

    return db


def test_mysql(define_database_params):
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