import os
import pathlib
import sys
sys.path.append('../')
from config import *
from db_chess import *



def create_tables():
    
    # Raw table players
    sql0 ='''
    CREATE TABLE `players` (
    `id` int NOT NULL,
    `rank` varchar(45) DEFAULT NULL,
    `name` varchar(45) DEFAULT NULL,
    `elo` varchar(45) DEFAULT NULL,
    `title` varchar(45) DEFAULT NULL,
    `fideid` varchar(45) DEFAULT NULL,
    `federation` varchar(45) DEFAULT NULL,
    `games` varchar(45) DEFAULT NULL,
    `birthyear` varchar(45) DEFAULT NULL,
    `page` tinytext,
    PRIMARY KEY (`id`)) '''
    
    
    sql ='''
            CREATE TABLE player 
        (
            id INTEGER NOT NULL, 
            firstname VARCHAR(100), 
            lastname VARCHAR(100),
            birthyear INTEGER, 
            fideid INTEGER, 
            PRIMARY KEY (id)
        );

    '''
    
    
    
    
    #sql = "CREATE TABLE player (id INTEGER NOT NULL, firstname VARCHAR(100), lastname VARCHAR(100),	birthyear INTEGER,fideid INTEGER,PRIMARY KEY (id));"
    #sql= 'CREATE TABLE playerdetails (id INTEGER NOT NULL, player_id INTEGER NOT NULL,title_id INTEGER NOT NULL, federation_id INTEGER NOT NULL, rank INTEGER, elo INTEGER, games INTEGER,	page VARCHAR(200),	PRIMARY KEY (id), FOREIGN KEY (player_id) REFERENCES player (id),FOREIGN KEY (title_id) REFERENCES dim_title (id), FOREIGN KEY (federation_id) REFERENCES dim_federation (id));'
    print(sql)
    status=insert_data(sql)
    print(status)
    
create_tables()

