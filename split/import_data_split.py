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
    
       
# import_players()


def import_dim_title():
    sql = "SELECT distinct (title)from players"
    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        title = raw[0]
        print(f"{c}, {title}")
        sql = f"INSERT INTO dim_title (id,txt) VALUES ({c},'{title}')"
        result = insert_data(sql)
        print(sql,result)
        
#import_dim_title()


def import_federation():
    sql = "SELECT distinct(federation)  FROM Datascientest.players order by federation asc;"
    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        title = raw[0]
        print(f"{c}, {title}")
        sql = f"INSERT INTO dim_federation (id,txt) VALUES ({c},'{title}')"
        result = insert_data(sql)
        print(sql,result)
        
#import_federation()
        
        
def import_playerdetails():        
    sql= '''SELECT  player.id as player_id,dim_title.id as title_id,dim_federation.id as federation_id,players.rank as ranks ,elo,games, page FROM Datascientest.players
    inner join dim_title on dim_title.txt = players.title
    inner join dim_federation on dim_federation.txt = players.federation
    inner join player on players.name = concat(player.firstname, ' ', player.lastname)'''

    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        player_id = raw[0]
        title_id = raw[1]
        federation_id = raw[2]
        rank = raw[3]
        elo = raw[4]
        games = raw[5]
        page = raw[6]
        
        
        
        print(f"{c},{player_id},{title_id},{federation_id},{rank},{elo},{games},{page}")
        sql = f"INSERT INTO playerdetails (id,player_id,title_id,federation_id,´rank´,elo,games,page) VALUES ({c},{player_id},{title_id},{federation_id},{rank},{elo},{games},'{page}')"
        result = insert_data(sql)
        print(sql, result)

# import_playerdetails()