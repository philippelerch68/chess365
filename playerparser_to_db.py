
import re
import array
import os
import json
import numpy as np
import pathlib
from config import *
file_error = []
key=[]
list_keys = ['Rank', 'Name', 'ELO', 'Title', 'FIDEId', 'Federation', 'Games', 'BirthYear', 'Page']

def file_count(games_dir):
    
    initial_count = 0
    for path in pathlib.Path(players_dir).iterdir():
        if path.is_file():
            initial_count += 1
    return initial_count

def parsing_file_data(f):
    file = open(players_dir+f)
    data = json.load(file)
    return data
    

def parsing():
    db_data =''
    a = 0
    nbr_files = 0
    datas = []
    id_icrement=0
    nbr_files = 0
    error_count = 0
    players_files = sorted(os.listdir(players_dir), reverse=False)
    nbr_total_file=file_count(players_files)
    count_lines = len(players_files)
    for f in players_files:
        db_data = ''
        id_icrement+=1
        nbr_files+=1
        a+=1
        percent = int(round((a/count_lines)*100,0))
        #print(f" {nbr_files}/{nbr_total_file} ->  FILE : {f}  |  {percent} %          ", end="\r")
       
        data = parsing_file_data(f)
        
        for key, value in data.items():
            #print (key, value)
            db_data = db_data + value
        
        db_data = db_data + value
        print(db_data)
        print("-----------")
        '''
         #print(data)
        key = data.keys()
        value = data.values()
        db_data = str(value) 
        print(f"{key:}{value}")
        #sql = f"INSERT INTO players(id,Event, Site, Date, Round, White, Black, Result, WhiteElo, BlackElo, ECO, Game) VALUES ({id_icrement},{db_data})"
        #print(sql)  
        
        '''    
            
        
    

if __name__=='__main__':
    print(" starting")
    parsing()
    print(" done ")
 