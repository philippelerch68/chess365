import os
import pathlib
import sys
sys.path.append('../')
from config import *
from db_chess import *



def import_players():
    
    # select table players name and import in table player
    sql = "SELECT distinct (name),birthyear,fideid from players"
    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        log =''
        birthyear = raw[1]
        fideid = raw[2]
        first_last_name = raw[0]
        lfs = first_last_name.split(' ')
        firstname = lfs[0]
        try :
            lastname = lfs[1]
        
        except :
           log = ("no lastname found")
            
        try :
            lastname = lfs[2]
            firstname =f"{lfs[0]} {lfs[1]}"
            log = ("firstname not single")
        
        except :
            log = ("firstname single")
        
            
        print(f"{c}, {firstname},{lastname},{birthyear},{fideid},{log}")
        sql = f"INSERT INTO player (id,firstname, lastname,birthyear,fideid) VALUES ({c},'{firstname}','{lastname}',{birthyear},{fideid})"
        result = insert_data(sql)
        print(sql,result)
    
    
        
    
       
       
import_players()

'''
for names in result:
        c +=1
        lf = names[0]
        lfs = lf.split(' ')
        firstname = lfs[0]
        try :
            lastname = lfs[1]
        
        except :
            lastname ='--'
        print(f" {firstname}  {lastname} {birthyear}")
        sql = f"INSERT INTO player (id,firstname, lastname) VALUES ({c},'{firstname}','{lastname}')"
        #result = insert_data(sql)
        #print(sql,result)
'''