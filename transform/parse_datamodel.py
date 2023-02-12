import mysql.connector
from mysql.connector import Error
from helpers import select_data, insert_data


def parse_datamodel(erd_dict, host, database, user, password):
    """DDL step; creates defined tables in database

    Args:
        erd_dict (dict): definition of transformations in order to fit in the entity relationship diagram.
        host (str): ip_address
        database (str): name of the database
        user (str): database user for connection
        password (str): password of the user
    """

    try:
        connection = mysql.connector.connect(host=host,
                                            database=database,
                                            user=user,
                                            password=password)

        
        print(f"Connection to database {database} established successfully")
        
        for tab in erd_dict.keys():
            try: 
                cursor = connection.cursor()
                cursor.execute(f"TRUNCATE TABLE {tab}")
                cursor.execute(f"INSERT INTO {tab} {erd_dict.get(tab)}")
                connection.commit()
                print(f"Data inserted successfully into table {tab}, {cursor.rowcount} rows inserted")
                
            except mysql.connector.Error as error:
                print(f"Failed to insert data into table {tab}: {error}")

    except mysql.connector.Error as error:
        print(f"Failed to connect to database {database}: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print(f"Connection to database {database} is closed")    




erd = {
    #player_data
    "player": """
        (firstname, lastname, birthyear, fideid,complet_name)
        SELECT gr1.firstname, gr1.lastname, pr.birthyear, pr.fideid,player_name
        FROM (
            SELECT DISTINCT
                player_name
                , SUBSTRING_INDEX(player_name,',',-1) AS firstname
                , SUBSTRING_INDEX(player_name,',',1) AS lastname
            FROM (
                SELECT DISTINCT white AS player_name FROM games_raw
                UNION ALL 
                SELECT DISTINCT black AS player_name FROM games_raw
            ) gr
        ) gr1
        LEFT JOIN players_raw pr
            ON REPLACE(pr.name, "`", "'") = TRIM(CONCAT_WS(' ', gr1.firstname, gr1.lastname))
    """,
    
    ##insert empty
    "dim_title": """
        (txt) 
        SELECT null AS txt 
            UNION ALL
        SELECT DISTINCT (title) AS txt
        FROM players_raw
    """,
    
    "dim_federation": """
        (txt) 
        SELECT null AS txt 
            UNION ALL
        SELECT DISTINCT (federation) AS txt
        FROM players_raw
    """,
    
    "playerdetails": """
        (player_id, title_id, federation_id, ranking, elo, games, page)
        SELECT
            p.id AS player_id
            , dt.id AS title_id
            , df.id AS federation_id
            , pr.ranking
            , pr.elo
            , pr.games
            , pr.page

        FROM player p
        LEFT JOIN players_raw pr
            ON REPLACE(pr.name, "`", "'") = TRIM(CONCAT_WS(' ', p.firstname, p.lastname))
        LEFT JOIN dim_title dt ON pr.title=dt.txt
        LEFT JOIN dim_federation df ON pr.federation=df.txt
    """,    
    
    #games_data
    "dim_result": """
        (txt) 
        SELECT DISTINCT (result) AS txt
        FROM games_raw
    """,
    
    "dim_eco": """
        (txt) 
        SELECT DISTINCT (eco) AS txt
        FROM games_raw
    """,
 
    "dim_event": """
        (name)
        select distinct(gr.event) as name
        FROM games_raw gr
        order by name
    """,
    
     "dim_site": """
        (name)
        select distinct(gr.site) as name
        FROM games_raw gr
        order by name
    """,
     "game": """
        (event_id, site_id, white_player_id, black_player_id, result_id, eco_id, gamedate, stage, whiteelo, blackelo, moves)
        SELECT DISTINCT 
            e.id AS event_id
            , s.id AS site_id
            , p1.id AS white_player_id
            , p2.id AS black_player_id
            , dr.id AS result_id
            , de.id AS eco_id
            , CASE 
                WHEN SUBSTRING(gr.date, 6,2) = '02' AND SUBSTRING(gr.date, 9,2) > '28' 
                    THEN STR_TO_DATE(CONCAT(SUBSTRING(REPLACE(gr.date, '-', '.'), 1,8), '28'),'%Y.%m.%d')
                WHEN SUBSTRING(gr.date, 6,2) IN ('04', '06', '09', '11') AND SUBSTRING(gr.date, 9,2) >= '31' 
                    THEN STR_TO_DATE(CONCAT(SUBSTRING(REPLACE(gr.date, '-', '.'), 1,8), '30'),'%Y.%m.%d')
                WHEN SUBSTRING(gr.date, 6,2) > '12'
                    THEN STR_TO_DATE(CONCAT(SUBSTRING(REPLACE(gr.date, '-', '.'), 1,5), '12.31'),'%Y.%m.%d')
                ELSE STR_TO_DATE(REPLACE(REPLACE(gr.date, '-', '.'), "??", "01"),'%Y.%m.%d')
                END AS gamedate
            , gr.round AS stage
            , gr.whiteelo
            , gr.blackelo
            , gr.game AS moves
        FROM games_raw gr
        inner JOIN dim_event e
            ON gr.event=e.name
        inner JOIN dim_site s
            ON gr.site=s.name
        inner JOIN player p1
            ON gr.white =p1.complet_name
        inner JOIN player p2
            ON gr.black =p2.complet_name
        inner JOIN dim_result dr
            ON gr.result=dr.txt
        inner JOIN dim_eco de
            ON gr.eco=de.txt
        
    """
}

def import_dim_location(db,db_log,error_log):
    '''
    import_dim_location
    '''
    sql = "SELECT Distinct(Site) FROM games_raw order by Site ASC;"
    result= select_data(db,sql)
    for raw in result:
        c = ''
        txt = ''
        txt0 = ''
        txt1 = ''
        
        txt = raw[0].replace("'", "`")
        txt0 = txt
        
        sites = txt0.split(' ')
        
        l = len(sites)-1
        c = sites[l]
        if c.isupper():
            txt = txt0.replace(c, '')
            txt = txt.rstrip()
            txt1 = c
            
        sql_i = f"INSERT INTO dim_location (txt,txt1,txt0) VALUES ('{txt}','{txt1}','{txt0}')"
        result = insert_data(db, sql_i,db_log,error_log)
        #print(sql_i,result)
        print(f"{c}, {txt} -> {txt1} | {result}                                                              ", end="\r")
        

def import_game_data(host, database, user, password):
    
    sql = {
        "game": """
        (event_id, site_id, white_player_id, black_player_id, result_id, eco_id, gamedate, stage, whiteelo, blackelo, moves)
        SELECT DISTINCT 
            e.id AS event_id
            , s.id AS site_id
            , p1.id AS white_player_id
            , p2.id AS black_player_id
            , dr.id AS result_id
            , de.id AS eco_id
            , CASE 
                WHEN SUBSTRING(gr.date, 6,2) = '02' AND SUBSTRING(gr.date, 9,2) > '28' 
                    THEN STR_TO_DATE(CONCAT(SUBSTRING(REPLACE(gr.date, '-', '.'), 1,8), '28'),'%Y.%m.%d')
                WHEN SUBSTRING(gr.date, 6,2) IN ('04', '06', '09', '11') AND SUBSTRING(gr.date, 9,2) >= '31' 
                    THEN STR_TO_DATE(CONCAT(SUBSTRING(REPLACE(gr.date, '-', '.'), 1,8), '30'),'%Y.%m.%d')
                WHEN SUBSTRING(gr.date, 6,2) > '12'
                    THEN STR_TO_DATE(CONCAT(SUBSTRING(REPLACE(gr.date, '-', '.'), 1,5), '12.31'),'%Y.%m.%d')
                ELSE STR_TO_DATE(REPLACE(REPLACE(gr.date, '-', '.'), "??", "01"),'%Y.%m.%d')
                END AS gamedate
            , gr.round AS stage
            , gr.whiteelo
            , gr.blackelo
            , gr.game AS moves
        FROM games_raw gr
        inner JOIN dim_event e
            ON gr.event=e.name
        inner JOIN dim_site s
            ON gr.site=s.name
        inner JOIN player p1
            ON gr.white =p1.complet_name
        inner JOIN player p2
            ON gr.black =p2.complet_name
        inner JOIN dim_result dr
            ON gr.result=dr.txt
        inner JOIN dim_eco de
            ON gr.eco=de.txt
        
    """
    }
    
    parse_datamodel(sql, host, database, user, password)
    
    
    