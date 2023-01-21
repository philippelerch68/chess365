tables = {
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
        page VARCHAR(2000) NULL
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
    
    "player": """(
        id INTEGER NOT NULL PRIMARY KEY,
        firstname VARCHAR(100) NULL,
        lastname VARCHAR(100) NULL,
        birthyear INTEGER UNSIGNED NULL,
        fideid INTEGER UNSIGNED NULL
        )
    """,
    
    "playerdetails": """(
        id INTEGER NOT NULL PRIMARY KEY,
        player_id INTEGER NOT NULL,
        title_id INTEGER NOT NULL,
        federation_id INTEGER NOT NULL,
        ranking INTEGER UNSIGNED NULL,
        elo INTEGER UNSIGNED NULL,
        games INTEGER UNSIGNED NULL,
        page VARCHAR(200)
        )
    """,
    
    "dim_title": """(
        id INTEGER NOT NULL PRIMARY KEY,
        txt VARCHAR(10)
        )
    """,
    
    "dim_federation": """(
        id INTEGER NOT NULL PRIMARY KEY,
        txt VARCHAR(10)
        )
    """,
    
    "event": """(
        id INTEGER NOT NULL PRIMARY KEY,
        name VARCHAR(100),
        location_id INTEGER UNSIGNED NOT NULL
        )
    """,
    
    "dim_location": """(
        id INTEGER NOT NULL PRIMARY KEY,
        txt VARCHAR(10),
        txt1 VARCHAR(10)
        )
    """,
    
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
        id INTEGER NOT NULL PRIMARY KEY,
        txt VARCHAR(100)
        )
    """,
    
    "dim_eco": """(
        id INTEGER NOT NULL PRIMARY KEY,
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


