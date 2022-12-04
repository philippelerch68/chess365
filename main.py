

import re
import array
import numpy as np 
from config import *
from importdata import *
from gamesparser import *



if __name__=='__main__':
    print("Starting                ", end='\r')
    print("Loading compressed file ", end='\r')
    download()
    print("File downloaded         ", end='\r')
    print("Extracting data         ", end='\r')
    extract()
    print("End extraction          ", end='\r')
    print("Creating games csv", end='\r')
    flog = open(games_to_csv, "w")
    flog.write("Event,Site,Date,Round,White,Black,Result,WhiteElo,BlackElo,ECO")
    flog.write("\n")                          
    flog.close()
    print("Parsing, cleaning saving in games.csv", end='\r')
    parsing()
    print("Parsing, cleaning saving in games.csv done", end='\r')
