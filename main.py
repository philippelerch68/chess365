from db.create_db import create_database
from db.create_tables import create_tables
from extract_load.extract import download, extract
from extract_load.parse_load import parse_directory
from db.db_ddl import tables
from helpers import read_yaml




if __name__=='__main__':
    
    config = read_yaml("config.yaml")

    print("Read config        ", end='\r')    
    db_host=config.get('DATABASE').get('db_host')
    db_database=config.get('DATABASE').get('db_database')
    db_user=config.get('DATABASE').get('db_user')
    db_password=config.get('DATABASE').get('db_password')
    db=[db_host, db_database, db_user, db_password]

    url=config.get('DATA').get('url')
    data_dir=config.get('DATA').get('data_dir')
    save_as=config.get('DATA').get('save_as')
    games_dir=config.get('DATA').get('games_dir')
    players_dir=config.get('DATA').get('players_dir')
    
    
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
    download(url, save_as)
    print("File downloaded         ", end='\r')
    
    print("Extracting data         ", end='\r')
    extract(save_as, data_dir)
    print("Data extracted          ", end='\r')
    print("--------END OF EXTRACT --------")
    
    print("IMPORTING folder games files to db")
    parse_directory(games_dir, db, 'games_raw')
    print("Games import done")

    print("----------------------------")
    print("IMPORTING folder players files to db")
    parse_directory(players_dir, db, 'players_raw')
    print("Players import done")
    print("--------END OF LOAD --------")
    
    
    
