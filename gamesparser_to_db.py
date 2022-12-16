
import re
import array
import os
from tqdm import tqdm
import pathlib
import numpy as np
from config import *
from db_chess import *
import time
#, 'game'
list_keys = ['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'WhiteElo', 'BlackElo', 'ECO','Game']
file_error = []

def file_count(games_dir):
    
    initial_count = 0
    for path in pathlib.Path(games_dir).iterdir():
        if path.is_file():
            initial_count += 1
    return initial_count


def parsing_file_data(f,nbr_files,id_icrement,nbr_total_file):
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
    count_lines = len(lines)
    
    #print(count_lines)
    dot = ''
    a=0
    for line in lines:
        key=[]
        keys=[]
        value=''
        a+=1
        percent = int(round((a/count_lines)*100,0))
        print(f" {nbr_files}/{nbr_total_file} ->  FILE : {f}  |  {percent} %          ", end="\r")
       
        # Parsing, cleaning
        if line.startswith('[') and line.rstrip('\n').endswith('"]'):
            line = line.replace('[','')
            line = line.replace(' "]','"]')
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
            #replace " in game data because making insert error
            line=line.replace('"',"`")  
            value = '"'+line+'"'
            db_data = db_data + value
            
            
            
        if line.startswith('0') and line.endswith('\n'):
            key = 'Game'
            line=line.replace('"',"`")  
            value = '"'+line+'"'
            db_data = db_data + value
            
        if line.startswith('{') and line.endswith('\n'):
            key = 'Game'
            line=line.replace('"',"`")  
            value = '"'+line+'"'
            db_data = db_data + value   
        
        if line.startswith('*') and line.endswith('\n'):
            key = 'Game'
            line=line.replace('"',"`")  
            value = '"'+line+'"'
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
                    flog = open('insert_error.txt', "a")
                    flog.write(f"{file} {sql} --")
                    flog.write("\n")
                    
                '''
                Log for  all successfull insert
                if(status =='ok'):
                    flog = open('insesrt_ok,txt', "a")
                    flog.write(f"{file} {sql} --")
                    flog.write("\n")
                '''
                
    
   
    #print("------END OF FILE  ----------")
    #print(f"file read = {f},nbr_files = {nbr_files}, id_icrement={id_icrement}")
    a=0
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
        if (nbr_files<nbr_total_file+1):
            f,nbr_files,id_icrement= parsing_file_data(f,nbr_files,id_icrement,nbr_total_file)
           
        
   
   