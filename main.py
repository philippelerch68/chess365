

import re
import array
import numpy as np 
from config import *
from importdata import *
from gamesparser import *


'''
if __name__=='__main__':
    print(" starting")
    download()
    print(" done ")
    print("extract data")
    extract()
    print("end extraction")


'''
flog = open("players.csv", "w")
flog.write("Event,Site,Date,Round,White,Black,Result,WhiteElo,BlackElo,ECO")
flog.write("\n")                          
flog.close()
parsing()
