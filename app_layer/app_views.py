import mysql.connector
from mysql.connector import Error


def create_app_views(app_vw_dict, host, database, user, password,db_log,error_log):
    """APP step; creates views needed for streamlit app

    Args:
        app_vw_dict (dict): definition of views
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
        
        for tab in app_vw_dict.keys():
            try: 
                cursor = connection.cursor()
                cursor.execute(f"CREATE OR REPLACE VIEW {tab} AS {app_vw_dict.get(tab)}")
                connection.commit()
                print(f"App view created successfully {tab}")
                
            except mysql.connector.Error as error:
                print(f"Failed to create view {tab}: {error}")
                flog = open(f"{error_log}", "a")
                flog.write(f"error : {error} --")
                flog.write("\n")

    except mysql.connector.Error as error:
        print(f"Failed to connect to database {database}: {error}")
        flog = open(f"{error_log}", "a")
        flog.write(f"error : {error} --")
        flog.write("\n")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print(f"Connection to database {database} is closed")    




app_views = {
    "app_cnt_games_white": """
        SELECT DISTINCT
            a.player_id
            , a.game_year
            , Count(a.game_id) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_white
            , Sum(a.succeed) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_white_succeed
            , Sum(a.lose) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_white_lose
            , Sum(a.draw) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_white_draw
        FROM (
            SELECT
                p.id AS player_id
                , gw.id AS game_id
                , YEAR(gw.gamedate) AS game_year
                , dr.txt
                , CASE WHEN dr.txt = '1-0' THEN 1
                    ELSE 0 END AS succeed
                , CASE WHEN dr.txt = '0-1' THEN 1
                    ELSE 0 END AS lose
                , CASE WHEN dr.txt = '1/2-1/2' THEN 1
                    ELSE 0 END AS draw
            FROM player p
            LEFT JOIN game gw 
                ON p.id = gw.white_player_id
            LEFT JOIN dim_result dr
                ON gw.result_id = dr.id
            ) a
    """,
    
    "app_cnt_games_black": """
        SELECT DISTINCT
            a.player_id
            , a.game_year
            , Count(a.game_id) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_black
            , Sum(a.succeed) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_black_succeed
            , Sum(a.lose) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_black_lose
            , Sum(a.draw) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_black_draw
        FROM (
            SELECT
                p.id AS player_id
                , gb.id AS game_id
                , YEAR(gb.gamedate) AS game_year
                , dr.txt
                , CASE WHEN dr.txt = '1-0' THEN 1
                    ELSE 0 END AS succeed
                , CASE WHEN dr.txt = '0-1' THEN 1
                    ELSE 0 END AS lose
                , CASE WHEN dr.txt = '1/2-1/2' THEN 1
                    ELSE 0 END AS draw
            FROM player p
            LEFT JOIN game gb 
                ON p.id = gb.black_player_id
            LEFT JOIN dim_result dr
                ON gb.result_id = dr.id
            ) a
    """,
    
    "app_cnt_game": """
        SELECT DISTINCT
            p.playerid
            , p.firstname
            , p.lastname
            , p.birthyear
            , p.game_year
            , cgw.cnt_games_white
            , cgw.cnt_games_white_succeed
            , cgw.cnt_games_white_lose
            , cgw.cnt_games_white_draw
            , cgb.cnt_games_black
            , cgb.cnt_games_black_succeed
            , cgb.cnt_games_black_lose
            , cgb.cnt_games_black_draw
            , cgw.cnt_games_white + cgb.cnt_games_black AS cnt_games
            , cgw.cnt_games_white_succeed + cgb.cnt_games_black_succeed AS cnt_games_succeed
            , cgw.cnt_games_white_lose + cgb.cnt_games_black_lose AS cnt_games_lose
            , cgw.cnt_games_white_draw + cgb.cnt_games_black_draw AS cnt_games_draw
        FROM (
            SELECT DISTINCT p.id AS playerid
                , p.firstname
                , p.lastname
                , p.birthyear
                , YEAR(g.gamedate) AS game_year
            FROM player p
            LEFT JOIN game g
                ON (p.id = g.white_player_id OR p.id = g.black_player_id)
        ) p
        LEFT JOIN app_cnt_games_white cgw
            ON p.playerid = cgw.player_id AND p.game_year = cgw.game_year
        LEFT JOIN app_cnt_games_black cgb
            ON p.playerid = cgb.player_id AND p.game_year = cgb.game_year
    """,
    
    "app_elo": """
        WITH white_elo AS (
            SELECT white_player_id AS player_id, whiteelo, max_gamedate
            FROM (
                SELECT DISTINCT white_player_id
                    , MAX(gamedate) OVER (PARTITION BY white_player_id) AS max_gamedate
                    , gamedate
                    , whiteelo
                FROM datascientest.game
                WHERE YEAR(gamedate) = 2021
            ) a
            WHERE max_gamedate=gamedate
        )
        , black_elo AS (
            SELECT black_player_id AS player_id, blackelo, max_gamedate
            FROM (
                SELECT DISTINCT black_player_id
                    , MAX(gamedate) OVER (PARTITION BY black_player_id) AS max_gamedate
                    , gamedate
                    , blackelo
                FROM datascientest.game
                WHERE YEAR(gamedate) = 2021
            ) a
            WHERE max_gamedate=gamedate
        )
        , elo_2021 AS (
            SELECT COALESCE(w.player_id, b.player_id) AS player_id
                , CASE WHEN w.max_gamedate >= b.max_gamedate THEN w.whiteelo
                    ELSE b.blackelo END AS elo_2021
            FROM white_elo w
            LEFT OUTER JOIN black_elo b
                ON w.player_id = b.player_id
        )

        SELECT
            p.id AS player_id
            , p.firstname
            , p.lastname
            , pd.elo as elo_current
            , e.elo_2021
            , CASE WHEN pd.elo <>'' AND e.elo_2021 <>'' AND pd.elo > e.elo_2021
                THEN (pd.elo - e.elo_2021) END AS elo_increase
            , CASE WHEN pd.elo <>'' AND e.elo_2021 <>'' AND pd.elo < e.elo_2021
                THEN (e.elo_2021 - pd.elo) END AS elo_decrease

        FROM datascientest.player p
        LEFT JOIN datascientest.playerdetails pd
            ON p.id = pd.player_id 
        LEFT JOIN elo_2021 e
            ON p.id = e.player_id
    """,
}
        
