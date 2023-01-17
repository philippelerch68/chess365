from config import *
from db.create_db import create_database
from db.create_tables import create_tables
from download.importdata import download, extract
from download.gamesparser_to_db import games_parsing
from download.playersparser_to_db import players_parsing



if __name__=='__main__':
    
    print("Starting process        ", end='\r')
    print("----------------------------")
    
    print("Creating database       ", end='\r')
    download()
    print("Database created        ", end='\r')
    
    print("Creating tables         ", end='\r')
    download()
    print("Tables created          ", end='\r')
    print("--------END OF DDL --------")
    
    print("Loading compressed file ", end='\r')
    download()
    print("File downloaded         ", end='\r')
    
    print("Extracting data         ", end='\r')
    extract()
    print("Data extracted          ", end='\r')
    print("--------END OF EXTRACT --------")
    
    print("IMPORTING folder games files to db")
    games_parsing()
    print("Games import done")

    print("----------------------------")
    print("IMPORTING folder players files to db")
    players_parsing()
    print("Players import done")
    print("--------END OF LOAD --------")