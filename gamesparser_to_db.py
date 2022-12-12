
import re
import array
import os
import numpy as np
from config import *
from db_chess import *
#, 'game'
list_keys=['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'WhiteElo', 'BlackElo', 'ECO','Game']
file_error = []

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
        if line.startswith('1.') and line.endswith('\n'):
            key = 'Game'
            value = '"'+line+'"'
            #if((key in list_keys) and key!='ECO'):
            db_data = db_data + value
            
            
        if(value!=''):
            count+=1
            print(f"{count} key: {key} ; value: {value}")
            if(key=='Game'):
                count=0
                id_icrement+=1
                db_data = db_data.replace('\n',"")   
                sql = f"INSERT INTO chess(id,Event, Site, Date, Round, White, Black, Result, WhiteElo, BlackElo, ECO, Game) VALUES ({id_icrement},{db_data})"
                print(f"sql : {sql}")
                print("----------------")
                db_data=''
                insert_data(sql)
    '''
    flog = open('insert_log,txt', "w")
    flog.write(f"{sql}")
    flog.write("-------------")
    flog.write("\n")
    '''
    
    
    #insert_data(sql)
    print("------END OF FILE  ----------")
    print(f"file read = {f},nbr_files = {nbr_files}, id_icrement={id_icrement}")
    return f,nbr_files,id_icrement
    

#Read each file in folder and parsing data (parsing_file_data(f))
def parsing():
    id_icrement=0
    nbr_files = 0
    error_count = 0
    keys_unique = []
    files = sorted(os.listdir(games_dir), reverse=False)
    for f in files:
        nbr_files+=1
        if (nbr_files<200):
            print(f" FILE : {f}")
            f,nbr_files,id_icrement= parsing_file_data(f,nbr_files,id_icrement)
           
        
   
   