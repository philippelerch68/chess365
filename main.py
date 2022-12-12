

import re
import array
import numpy as np 
from config import *
from importdata import *
from gamesparser_to_db import *



if __name__=='__main__':
    '''
    print("Starting                ", end='\r')
    print("Loading compressed file ", end='\r')
    download()
    print("File downloaded         ", end='\r')
    print("Extracting data         ", end='\r')
    extract()
    print("End extraction          ", end='\r')
    '''
    print("----------------------------")
    print("IMPORTING folder games files to db")
    parsing()
    print("Parsing, cleaning saving  done")
