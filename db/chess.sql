CREATE TABLE player (id INTEGER NOT NULL, 
                     firstname VARCHAR(100), --name[0] 
                     lastname VARCHAR(100), --name[1]
                     birthyear INTEGER, 
                     fideid INTEGER, 
                     PRIMARY KEY (id)
                    );

CREATE TABLE playerdetails (id INTEGER NOT NULL, 
                            player_id INTEGER NOT NULL,
                            title INTEGER, -- DIM
                            rank INTEGER,  
                            elo INTEGER, 
                            federation VARCHAR(100), -- DIM
                            games INTEGER,
                            page VARCHAR(200),
                            PRIMARY KEY (id),
                            FOREIGN KEY (player_id) REFERENCES player (id)
                           );
                           
CREATE TABLE event (id INTEGER NOT NULL, 
                    name VARCHAR(100), --event
                    city VARCHAR(100), --site[0] -- DIM
                    country  VARCHAR(3), --site[1] -- DIM
                    PRIMARY KEY (id)
                   );
                   
CREATE TABLE game (id INTEGER NOT NULL, 
                   event_id INTEGER NOT NULL,
                   white_player_id INTEGER NOT NULL,
				   black_player_id INTEGER NOT NULL,
                   year INTEGER, --date
                   month INTEGER, --date
                   day INTEGER, --date
                   round VARCHAR(10),
                   result VARCHAR(10),
                   whiteelo INTEGER,
                   blackelo INTEGER,
                   eco VARCHAR(10),
                   PRIMARY KEY (id),
                   FOREIGN KEY (event_id) REFERENCES event (id),
                   FOREIGN KEY (white_player_id) REFERENCES player (id),
                   FOREIGN KEY (black_player_id) REFERENCES player (id)
                   );
                              
