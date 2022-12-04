
import re
import array
import os
import numpy as np
from config import *
#, 'game'
list_keys=['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'WhiteElo', 'BlackElo', 'ECO']
file_error = []
def parsing_file_data(f):
    
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
    keys = []
    a = 0
    count = 0
    flog = open("players.csv", "a")
    
    #flog.write(f"'file_name': '{f}',")
    for line in lines:
        count+=1
        a+=1
        #print("->" +str(line))
        if line.startswith('[') and line.rstrip('\n').endswith(']'):
            line = line.replace('[','')
            line = line.replace(', "]','"')
            line = line.replace(']','')
            line = line.replace(' "',';"')
            line = line.replace(', "',',""')
            
            
            
            arr = line.split(';')
            exist =","
            key = arr[0]
            keys.append(key)
            value = arr[1]
            
            if(key in list_keys):
                flog.write(value.rstrip())
            if((key in list_keys) and key!='ECO'):
                flog.write(",")
            if (key == 'ECO'):
                flog.write("\n") 
                a = 0
           
        if line.startswith('1.') and line.endswith('\n'):
            key = 'game'
            keys.append(key)
            value = '"'+line+'"'
           # flog.write(f"'key': '{key}',")
           # flog.write(f"'value': '{value}'\n")
            #print(value)
        
    flog.write("\n")                          
    flog.close()
  
    
    return f,keys, value,
    

def parsing():
    nbr_files = 0
    error_count = 0
    keys_unique = []
    files = sorted(os.listdir(games_dir), reverse=False)
    for f in files:
        nbr_files+=1
        print(f" {nbr_files} {f}")
        f,keys, value = parsing_file_data(f)
        for key in keys:
            if(key not in keys_unique):
                keys_unique.append(key)
    
    print(keys_unique)
        
        
   
   