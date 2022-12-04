
import re
import array
import os
import numpy as np
import pandas as pd
from config import *


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
       
    count = 0
    flog = open("log.txt", "a")
    flog.write(f"\-------------------------------\n")
    flog.write(f"file: {f}\n")
    for line in lines:
        count+=1
        #print("->" +str(line))
        if line.startswith('[') and line.rstrip('\n').endswith(']'):
            line = line.replace('[','')
            line = line.replace(']','')
            line = line.replace(' "',';"')
            arr = line.split(';')
            exist =","
            key = arr[0]
            keys.append(key)
            value = arr[1]
            flog.write(f"key: {key}\n")
            flog.write(f"value: {value}\n")
           
        if line.startswith('1.') and line.endswith('\n'):
            key = 'game'
            keys.append(key)
            value = '"'+line+'"'
            flog.write(f"key: {key}\n")
            flog.write(f"value: {value}\n")
            #print(value)
        
    flog.write(f"\-------------------------------\n")                          
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
        
        
   
   