
import re
import array
import os
import sys
sys.path.append('../')

import json
import numpy as np
import pathlib
from config import *
from db_chess import *



file_error = []
key=[]
list_keys = ['Rank', 'Name', 'ELO', 'Title', 'FIDEId', 'Federation', 'Games', 'BirthYear', 'Page']

def file_count(games_dir):
    
    initial_count = 0
    for path in pathlib.Path(players_dir).iterdir():
        if path.is_file():
            initial_count += 1
    return initial_count

def pparsing_file_data(f):
    file = open(players_dir+f)
    data = json.load(file)
    return data
    

def players_parsing():
    id_icrement=0
    players_files = sorted(os.listdir(players_dir), reverse=False)
    count_lines = len(players_files)
    for f in players_files:
        id_icrement+=1 
        data = pparsing_file_data(f)
        rank = data['Rank']
        name = data['Name'].replace("'","`")
        elo = data['ELO']
        title = data['Title']
        fideid = data['FIDEId']
        federation = data['Federation']
        games = data['Games']
        birthyear = data['BirthYear'] 
        page = data['Page'].replace("'","`")
        sql = f"INSERT INTO players(`id`,`rank`,`name`,`elo`,`title`,`fideid`,`federation`,`games`,`birthyear`,`page`) VALUES ({id_icrement},'{rank}','{name}','{elo}','{title}','{fideid}','{federation}','{games}','{birthyear}','{page}')"
        #print(sql)
        print(f" {id_icrement}/{count_lines} ->  FILE : {f}            ", end="\r")
        status=insert_data(sql)
        if(status =='error'):
            flog = open('players_insert_error.txt', "a")
            flog.write(f"{sql} --")
            flog.write("\n")
        
    print(f" Done                                    ", end="\r")

if __name__=='__main__':
    players_parsing()