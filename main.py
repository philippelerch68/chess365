from config import *
from db.create_db import create_database
from db.create_tables import create_tables
from download.importdata import download, extract
from download.gamesparser_to_db import games_parsing
from download.playersparser_to_db import players_parsing
from db.db_ddl import tables
from helpers import read_yaml


config = read_yaml("config.yaml")

db_host=config.get('DATABASE').get('db_host')
db_database=config.get('DATABASE').get('db_database')
db_user=config.get('DATABASE').get('db_user')
db_password=config.get('DATABASE').get('db_password')


if __name__=='__main__':
    
    print("Starting process        ", end='\r')
    print("----------------------------")
    
    print("Creating database       ", end='\r')
    create_database(host=db_host, database=db_database, user=db_user, password=db_password)
    print("Database created        ", end='\r')
    
    print("Creating tables         ", end='\r')
    create_tables(tables_dict=tables, host=db_host, database=db_database, user=db_user, password=db_password)
    print("Tables created          ", end='\r')
    print("--------END OF DDL --------")
    
    print("Loading compressed file ", end='\r')
    #download()
    print("File downloaded         ", end='\r')
    
    print("Extracting data         ", end='\r')
    #extract()
    print("Data extracted          ", end='\r')
    print("--------END OF EXTRACT --------")
    
    print("IMPORTING folder games files to db")
    #games_parsing()
    print("Games import done")

    print("----------------------------")
    print("IMPORTING folder players files to db")
    #players_parsing()
    print("Players import done")
    print("--------END OF LOAD --------")