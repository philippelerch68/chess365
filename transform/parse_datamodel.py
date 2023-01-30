import mysql.connector
from mysql.connector import Error


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
        (firstname, lastname, birthyear, fideid)
        SELECT gr1.firstname, gr1.lastname, pr.birthyear, pr.fideid
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
    
    "dim_location": """
        (txt, txt1)
        SELECT DISTINCT (site) AS txt, '' as txt1
        FROM games_raw
    """,
    
    "event": """
        (name, location_id)
        SELECT DISTINCT (gr.event) AS name
            , dl.id AS location_id
        FROM games_raw gr
        LEFT JOIN dim_location dl
            ON gr.site=dl.txt
    """,
    
    "game": """
        (event_id, white_player_id, black_player_id, result_id, eco_id, gamedate, stage, whiteelo, blackelo, moves)
        SELECT e.id AS event_id
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
        LEFT JOIN event e
            ON gr.event=e.name
        LEFT JOIN player p1
            ON SUBSTRING_INDEX(gr.white,',',-1) = p1.firstname
            AND SUBSTRING_INDEX(gr.white,',',1) = p1.lastname
        LEFT JOIN player p2
            ON SUBSTRING_INDEX(gr.black,',',-1) = p2.firstname
            AND SUBSTRING_INDEX(gr.black,',',1) = p2.lastname
        LEFT JOIN dim_result dr
            ON gr.result=dr.txt
        LEFT JOIN dim_eco de
            ON gr.eco=de.txt
    """,
    #moves is not needed since    
    #"moves": """(
    #    (game_id, movenr, white, black)
    #"""
}
