

import re
import array
import numpy as np 
from config import *
from importdata import *
from gamesparser_to_db import *
from playersparser_to_db import *
import pathlib


if __name__=='__main__':
    
    print("Starting                ", end='\r')
    print("Loading compressed file ", end='\r')
    download()
    print("File downloaded         ", end='\r')
    print("Extracting data         ", end='\r')
    extract()
    print("End extraction          ", end='\r')
          
    print("----------------------------")
    print("IMPORTING folder games files to db")
    games_parsing()
    print("Games import done")

    print("----------------------------")
    print("IMPORTING folder players files to db")
    players_parsing()
    print("Players import done")
    print("--------END OF IMPORTATION --------")