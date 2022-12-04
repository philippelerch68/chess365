
import re
import array
import os
import json
import numpy as np
from config import *


file_error = []
def parsing_file_data(f):
    
    file = open(players_dir+f)
    data = json.load(file)
    return data
    


def parsing():
    nbr_files = 0
    datas = []
    files = sorted(os.listdir(players_dir), reverse=False)
    for f in files:
        nbr_files+=1
        print(f" {nbr_files} {f}")
        data = parsing_file_data(f)
        #print(data)
        print(data.keys())
        
    

if __name__=='__main__':
    print(" starting")
    parsing()
    print(" done ")
 