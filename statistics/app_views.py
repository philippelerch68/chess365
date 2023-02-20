import mysql.connector
from mysql.connector import Error


def create_app_views(app_vw_dict, host, database, user, password):
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

    except mysql.connector.Error as error:
        print(f"Failed to connect to database {database}: {error}")

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
            , Sum(a.lose) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_white_loose
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
                ON p.id = gw.white_player_id AND YEAR(gw.gamedate) >= '2019'
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
            , Sum(a.lose) OVER (PARTITION BY a.player_id, a.game_year) AS cnt_games_black_loose
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
                ON p.id = gb.black_player_id AND YEAR(gb.gamedate) >= '2019'
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
            , cgw.cnt_games_white_loose
            , cgw.cnt_games_white_draw
            , cgb.cnt_games_black
            , cgb.cnt_games_black_succeed
            , cgb.cnt_games_black_loose
            , cgb.cnt_games_black_draw
            , cgw.cnt_games_white + cgb.cnt_games_black AS cnt_games
            , cgw.cnt_games_white_succeed + cgb.cnt_games_black_succeed AS cnt_games_succeed
            , cgw.cnt_games_white_loose + cgb.cnt_games_black_loose AS cnt_games_loose
            , cgw.cnt_games_white_draw + cgb.cnt_games_black_draw AS cnt_games_draw
        FROM (
            SELECT DISTINCT p.id AS playerid
                , p.firstname
                , p.lastname
                , p.birthyear
                , YEAR(g.gamedate) AS game_year
            FROM player p
            INNER JOIN game g
                ON (p.id = g.white_player_id OR p.id = g.black_player_id)
                AND YEAR(g.gamedate) >= '2019'
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
                FROM game
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
                FROM game
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

        FROM player p
        LEFT JOIN playerdetails pd
            ON p.id = pd.player_id 
        LEFT JOIN elo_2021 e
            ON p.id = e.player_id
    """,
    "app_cnt_fgame": """
        select G.id, 
        DE.name as Event, 
        DS.name AS Site,
        DMTW.txt AS WTitle,
        concat(PLW.firstname, ' ',PLW.lastname) AS White_player,
        DMFW.txt AS WFederation,
        PDEW.ranking AS WRank,
        PDEW.elo AS WElo,
        PDEW.page AS WPage,
        DMTB.txt AS BTitle,
        concat(PLB.firstname, ' ',PLB.lastname) AS Black_player,
        DMFB.txt AS BFederation,
        PDEB.ranking as BRank,
        PDEB.elo as BElo,
        PDEB.page AS BPage,
        DR.txt AS Result,
        DME.txt AS Eco,
        G.gamedate as Game_date,
        G.stage as Stage,
        G.whiteelo as Whiteelo,
        G.blackelo as Blackelo,
        G.moves as Moves,
        AMN.nbr_move as Total_move
        from game AS G
        inner join dim_event AS DE on DE.id = G.event_id
        inner join dim_site AS DS on DS.id = G.site_id
        inner join player AS PLW on PLW.id = G.white_player_id
        inner join player AS PLB on PLB.id = G.black_player_id
        inner join dim_result AS DR on DR.id = G.result_id
        inner join dim_eco AS DME on DME.id = G.eco_id
        inner join app_move_nbr AS AMN on AMN.id = G.id
        inner join playerdetails AS PDEW on PDEW.id = G.white_player_id
        inner join playerdetails AS PDEB on PDEB.id = G.black_player_id
        left join dim_federation AS DMFW on DMFW.id = G.white_player_id
        left join dim_federation AS DMFB on DMFB.id = G.black_player_id
        left join dim_title AS DMTW on DMTW.id = PDEW.title_id
        left join dim_title AS DMTB on DMTB.id = PDEB.title_id
    
    """
    
}
        
