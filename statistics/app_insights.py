import mysql.connector
from mysql.connector import Error


def select_insights(insights_dict, host, database, user, password):
    """APP step; executes app views to persist insights for displaying in app later on

    Args:
        insights_dict (dict): definition of retreiving insights.
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
        
        for tab in insights_dict.keys():
            try: 
                cursor = connection.cursor()
                cursor.execute(f"DROP TABLE IF EXISTS {tab}")
                cursor.execute(f"CREATE TABLE {tab} AS {insights_dict.get(tab)}")
                connection.commit()
                print(f"App insights table created successfully {tab}, {cursor.rowcount} rows inserted")
                
            except mysql.connector.Error as error:
                print(f"Failed to create insights table {tab}: {error}")

    except mysql.connector.Error as error:
        print(f"Failed to connect to database {database}: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print(f"Connection to database {database} is closed")    




app_insights = {
    #"Who played the most games by year?"
    "app_cnt_games": """
        SELECT a.* FROM (
            SELECT game_year, firstname, lastname, cnt_games
                , ROW_NUMBER() OVER (PARTITION BY game_year ORDER BY cnt_games DESC) AS rn
            FROM app_cnt_game
            WHERE game_year >= '2019' AND cnt_games <>''
        ) a
        WHERE a.rn <= 10
    """,
    
    #"Who was the most successful player by year?"
    "app_pct_success": """
        SELECT a.* FROM (
            SELECT b.*
                , ROW_NUMBER() OVER (PARTITION BY b.game_year ORDER BY b.pct_success DESC) AS rn
            FROM (
                SELECT game_year, firstname, lastname, cnt_games
                    , ROUND(cnt_games_succeed / cnt_games * 100, 1) AS pct_success
                FROM app_cnt_game
                WHERE game_year >= '2019' AND cnt_games <>''
            ) b
        ) a
        WHERE a.rn <= 10
    """,
    
    #"Who was the least successful player by year?"
    "app_pct_loose": """
        SELECT a.* FROM (
            SELECT b.*
                , ROW_NUMBER() OVER (PARTITION BY b.game_year ORDER BY b.pct_loose DESC) AS rn
            FROM (
                SELECT game_year, firstname, lastname, cnt_games
                    , ROUND(cnt_games_loose / cnt_games * 100, 1) AS pct_loose
                FROM app_cnt_game
                WHERE game_year >= '2019' AND cnt_games <>''
            ) b
        ) a
        WHERE a.rn <= 10
    """,    
    
    #"Who was the most successful player playing white by year?"
    "app_pct_white_success": """
        SELECT a.* FROM (
            SELECT b.*
                , ROW_NUMBER() OVER (PARTITION BY b.game_year ORDER BY b.pct_white_success DESC, b.cnt_games_white DESC) AS rn
            FROM (
                SELECT game_year, firstname, lastname, cnt_games_white
                    , ROUND(cnt_games_white_succeed / cnt_games_white * 100, 1) AS pct_white_success
                FROM app_cnt_game
                WHERE game_year >= '2019' AND cnt_games <>''
            ) b
        ) a
        WHERE a.rn <= 10
    """,
    
    #"Who was the most successful player playing black by year?"
    "app_pct_black_success": """
        SELECT a.* FROM (
            SELECT b.*
                , ROW_NUMBER() OVER (PARTITION BY b.game_year ORDER BY b.pct_black_success DESC, b.cnt_games_black DESC) AS rn
            FROM (
                SELECT game_year, firstname, lastname, cnt_games_black
                    , ROUND(cnt_games_black_succeed / cnt_games_black * 100, 1) AS pct_black_success
                FROM app_cnt_game
                WHERE game_year >= '2019' AND cnt_games <>''
            ) b
        ) a
        WHERE a.rn <= 10
    """,

    #"Which player improved in skill level in 2022?"
    "app_elo_increase": """
        SELECT firstname, lastname, elo_current, elo_2021, elo_increase
        FROM app_elo
        ORDER BY elo_increase DESC
        LIMIT 10
    """,
    
    #"Graph: white vs black"
    "app_white_black": """
        SELECT cg.playerid
            , ROUND(cnt_games_white_succeed / cnt_games_white, 2) AS PCT_SUCCEED_WHITE
            , ROUND(cnt_games_black_succeed / cnt_games_black, 2) AS PCT_SUCCEED_BLACK
            , coalesce(cnt_games_white, 'NULL VALUE') + coalesce(cnt_games_black, 'NULL VALUE') AS cnt_games
        FROM app_cnt_game cg 
        ORDER BY cnt_games DESC
    """
}
        
