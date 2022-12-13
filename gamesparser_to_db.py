
import re
import array
import os
from tqdm import tqdm
import pathlib
import numpy as np
from config import *
from db_chess import *

#, 'game'
list_keys=['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'WhiteElo', 'BlackElo', 'ECO','Game']
file_error = []

def file_count(games_dir):
    
    initial_count = 0
    for path in pathlib.Path(games_dir).iterdir():
        if path.is_file():
            initial_count += 1
    return initial_count


def parsing_file_data(f,nbr_files,id_icrement):
    file = open(games_dir+f,encoding='utf-8', errors='ignore')
    line =''
    lines = ''
    try:
        lines = file.readlines()
        file.close()
    except:
        print(f"!------Problem with file: {file} ------!")
        file_error.append(file)
        
    key = []
    count = 0
    db_data =''
   
    for line in lines:
        key=[]
        keys=[]
        value=''
        
          
        # Parsing, cleaning
        if line.startswith('[') and line.rstrip('\n').endswith(']'):
            line = line.replace('[','')
            line = line.replace(', "]','"')
            line = line.replace(']','')
            line = line.replace(' "',';"')
            line = line.replace(', "',',""')
            arr = line.split(';')
            key = arr[0]
            value = arr[1]
            value = value.replace('\n',"")
            db_data = db_data + value +","
            
                      
                
        # FOR GAME Value.   
        if line.startswith('1') and line.endswith('\n'):
            key = 'Game'
            value = '"'+line+'"'
            #if((key in list_keys) and key!='ECO'):
            db_data = db_data + value
            
        if line.startswith('0') and line.endswith('\n'):
            key = 'Game'
            value = '"'+line+'"'
            #if((key in list_keys) and key!='ECO'):
            db_data = db_data + value
            
            
            
        if(value!=''):
            count+=1
            #print(f"{count} key: {key} ; value: {value}")
            if(key=='Game'):
                count=0
                id_icrement+=1
                db_data = db_data.replace('\n',"")   
                sql = f"INSERT INTO chess(id,Event, Site, Date, Round, White, Black, Result, WhiteElo, BlackElo, ECO, Game) VALUES ({id_icrement},{db_data})"
                #print(f"sql : {sql}")
                #print("----------------")
                db_data=''
                # INSERT DATA IN DB
                status=insert_data(sql)
                if(status =='error'):
                    flog = open('insert_error,txt', "a")
                    flog.write(f"{file} {sql} --")
                    flog.write("\n")
                
                if(status =='ok'):
                    flog = open('insert_ok,txt', "a")
                    flog.write(f"{file} {sql} --")
                    flog.write("\n")
    
   
    #print("------END OF FILE  ----------")
    #print(f"file read = {f},nbr_files = {nbr_files}, id_icrement={id_icrement}")
    return f,nbr_files,id_icrement
    

#Read each file in folder and parsing data (parsing_file_data(f))
def parsing():
    id_icrement=0
    nbr_files = 0
    error_count = 0
    keys_unique = []
    files = sorted(os.listdir(games_dir), reverse=False)
    nbr_total_file=file_count(games_dir)
    for f in files:
        nbr_files+=1
        if (nbr_files<200):
            #print(f" FILE : {f}")
            for i in tqdm(range(100) ,ascii=" *",desc =f"{nbr_files}/{nbr_total_file}  {f}"):
                f,nbr_files,id_icrement= parsing_file_data(f,nbr_files,id_icrement)
           
        
   
   