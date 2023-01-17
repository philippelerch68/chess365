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

def import_dim_eco():
    sql = "SELECT Distinct(ECO) FROM Datascientest.chess order by ECO ASC;"
    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        txt = raw[0]
        print(f"{c}, {txt}")
        sql = f"INSERT INTO dim_eco (id,txt) VALUES ({c},'{txt}')"
        result = insert_data(sql)
        print(sql,result)
        
#import_dim_eco()


def import_dim_result():
    sql = "SELECT Distinct(Result) FROM Datascientest.chess order by Result ASC;"
    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        txt = raw[0]
        print(f"{c}, {txt}")
        sql = f"INSERT INTO dim_result (id,txt) VALUES ({c},'{txt}')"
        result = insert_data(sql)
        print(sql,result)
        
#import_dim_result()

def import_dim_location():
    sql = "SELECT Distinct(Site) FROM Datascientest.chess order by Site ASC;"
    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        txt = ''
        txt1 = ''
        txt0 =raw[0]
        sites = raw[0].split(' ')
        l = len(sites)
        text1 = ''
        for i in range(l):
            pays = ""
            if((len(sites[i]))==3) and i>0 and sites[i]!='les':
                pays = " (pays) "
                txt1 = sites[i]
            else:
                txt = txt + ' ' + str(sites[i])
        
        print(f" {txt} -> {txt1}")
        sql = f"INSERT INTO dim_location (id,txt,txt1,txt0) VALUES ({c},'{txt}','{txt1}','{txt0}')"
        result = insert_data(sql)
        print(sql,result)
        

#import_dim_location()


def import_event():
    sql = "SELECT DISTINCT(Event), dim_location.id  FROM Datascientest.chess inner join dim_location on dim_location.txt0 = chess.Site order by Event"
    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        event = raw[0]
        location_id = raw[1]
        
        print(f"{c}, {event}, {location_id}")
        sql = f"INSERT INTO event (id,name,location_id) VALUES ({c},'{event}',{location_id})"
        result = insert_data(sql)
        print(sql,result)
        
# import_event()


def import_game():
    sql='''
    SELECT t3.id as event_id, t4.id as result_id, t5.id as eco_id, Date, Round, WhiteElo, BlackELO,t0.id,t1.id, t2.id  from chess as t0
    inner join player as t1 on t1.lastname = SUBSTRING_INDEX(t0.White,',',1) AND t1.firstname = SUBSTRING_INDEX(t0.White,', ',-1)
    inner join player as t2 on t2.lastname = SUBSTRING_INDEX(t0.Black,',',1) AND t2.firstname = SUBSTRING_INDEX(t0.Black,', ',-1) 
    inner join event as t3 on t3.name = t0.Event
    inner join dim_result as t4 on t4.txt = t0.Result
    inner join dim_eco as t5 on t5.txt = t0.ECO
    order by t0.id
    '''

    result= select_data(sql)
    c = 0
    for raw in result:
        c+=1
        event_id = raw[0]
        result_id = raw[1]
        eco_id = raw[2]
        gamedate = raw[3]
        gamedate =gamedate.replace(".","-")
        stage = raw[4]
        whiteelo = raw[5]
        blackelo = raw[6]       
        chess_id = raw[7]
        white_player_id =raw[8]
        black_player_id =raw[9]
        print(f"{c}, {event_id},{result_id},{eco_id},{gamedate},{stage},{whiteelo},{blackelo},{chess_id},{white_player_id},{black_player_id}")
        sql = f"INSERT INTO game (id,event_id,result_id,eco_id,gamedate,stage,whiteelo,blackelo,chess_id,white_player_id,black_player_id) VALUES ({c}, {event_id},{result_id},{eco_id},'{gamedate}','{stage}',{whiteelo},{blackelo},{chess_id},{white_player_id},{black_player_id})"
        result = insert_data(sql)
        print(sql,result)

import_game()