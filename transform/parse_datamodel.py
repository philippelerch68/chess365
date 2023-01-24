inserts_stmt = {
    "players_raw": """(
        id INT(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
        ranking VARCHAR(10) NULL,
        name VARCHAR(100) NULL,
        elo VARCHAR(10) NULL,
        title VARCHAR(10) NULL,
        fideid VARCHAR(10) NULL,
        federation VARCHAR(100) NULL,
        games VARCHAR(10) NULL,
        birthyear VARCHAR(10) NULL,
        page VARCHAR(5000) NULL
        )
    """,
    
	"games_raw": """(
        id INT(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
        event VARCHAR(40) NULL,
        site VARCHAR(30) NULL,
        date VARCHAR(12) NULL,
        round VARCHAR(6) NULL,
        white VARCHAR(35) NULL,
        black VARCHAR(35) NULL,
        result varchar(10) NULL,
        whiteelo VARCHAR(5) NULL,
        blackelo VARCHAR(5) NULL,
        eco VARCHAR(5) NULL,
        game VARCHAR(2000) NULL
        )
    """,
    #player_data
    #TODO
    "player": """
        (id, name, firstname, lastname, birthyear, fideid)
        SELECT id
            , name
            , name as firstname
            , name as lastname
            , birthyear, fideid
        FROM players_raw
    """,
    
    "dim_title": """
        (txt) 
        SELECT DISTINCT (title) 
        FROM players_raw
    """,
    
    "dim_federation": """
        (txt) 
        SELECT DISTINCT (federation) 
        FROM players_raw
    """,
    
    "playerdetails": """
        (id, player_id, title_id, federation_id, ranking, elo, games, page)
        SELECT pr.id
            , p.id AS player_id
            , dt.id AS title_id
            , df.id AS federation_id
            , ranking
            , elo
            , games
            , page
        
        FROM players_raw pr
        LEFT JOIN player p ON pr.name = p.name
        LEFT JOIN dim_title dt ON pr.title=dt.txt
        LEFT JOIN dim_federation df ON pr.federation=df.txt
    """,    
    
    #games_data
    #TODO
    "dim_location": """
        (txt, txt1)
        SELECT DISTINCT (txt, txt1)
        FROM (
            SELECT 
                site as txt
                , site as txt1
            FROM games_raw
        )
    """,
    
    "event": """
        (id, name, location_id)
    """,
    
################################
    
    "game": """(
        id INTEGER NOT NULL PRIMARY KEY,
        event_id INTEGER UNSIGNED NOT NULL,
        white_player_id INTEGER UNSIGNED NOT NULL,
        black_player_id INTEGER UNSIGNED NOT NULL,
        result_id INTEGER UNSIGNED NOT NULL,
        eco_id INTEGER UNSIGNED NOT NULL,
        gamedate DATE,
        stage VARCHAR(10),
        whiteelo INTEGER UNSIGNED,
        blackelo INTEGER UNSIGNED
        )
    """,
    
    "dim_result": """(
        id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
        txt VARCHAR(100)
        )
    """,
    
    "dim_eco": """(
        id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
        txt VARCHAR(100)
        )
    """,
    
    "moves": """(
        id INTEGER NOT NULL PRIMARY KEY,
        game_id INTEGER NOT NULL,
        movenr INTEGER UNSIGNED,
        white VARCHAR(10),
        black VARCHAR(10)
        )
    """
}


