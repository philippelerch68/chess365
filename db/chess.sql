CREATE TABLE player 
(
	id INTEGER NOT NULL, 
	firstname VARCHAR(100), --name[0] 
	lastname VARCHAR(100), --name[1]
	birthyear INTEGER, 
	fideid INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE playerdetails 
(
	id INTEGER NOT NULL, 
	player_id INTEGER NOT NULL,
	title_id INTEGER NOT NULL,
	federation_id INTEGER NOT NULL,
	rank INTEGER,  
	elo INTEGER, 
	games INTEGER,
	page VARCHAR(200),
	PRIMARY KEY (id),
	FOREIGN KEY (player_id) REFERENCES player (id),
	FOREIGN KEY (title_id) REFERENCES dim_title (id),
	FOREIGN KEY (federation_id) REFERENCES dim_federation (id)
);

CREATE TABLE dim_title 
(
	id INTEGER NOT NULL,
	txt VARCHAR(10),
	PRIMARY KEY (id)
);

CREATE TABLE dim_federation 
(
	id INTEGER NOT NULL,
	 txt VARCHAR(100),
	 PRIMARY KEY (id)
);

CREATE TABLE event 
(
	id INTEGER NOT NULL, 
	name VARCHAR(100), --event
	location_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (location_id) REFERENCES dim_location (id)
);
				   
CREATE TABLE dim_location 
(
	id INTEGER NOT NULL,
	txt VARCHAR(100), --site[0]
	txt1 VARCHAR(10), --site[1]
	PRIMARY KEY (id)
);

CREATE TABLE game 
(
	id INTEGER NOT NULL, 
	event_id INTEGER NOT NULL,
	white_player_id INTEGER NOT NULL,
	black_player_id INTEGER NOT NULL,
	result_id INTEGER NOT NULL,
	eco_id INTEGER NOT NULL,
	gamedate DATE,
	stage VARCHAR(10), --round
	whiteelo INTEGER,
	blackelo INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY (event_id) REFERENCES event (id),
	FOREIGN KEY (white_player_id) REFERENCES player (id),
	FOREIGN KEY (black_player_id) REFERENCES player (id),
	FOREIGN KEY (result_id) REFERENCES dim_result (id),
	FOREIGN KEY (eco_id) REFERENCES dim_eco (id)
);

CREATE TABLE dim_result 
(
	id INTEGER NOT NULL,
	txt VARCHAR(100),
	PRIMARY KEY (id)
);
						
CREATE TABLE dim_eco 
(
	id INTEGER NOT NULL,
	txt VARCHAR(100),
	PRIMARY KEY (id)
);
                            
CREATE TABLE moves 
(
	id INTEGER NOT NULL,
	game_id INTEGER NOT NULL,
	movenr INTEGER,
	white VARCHAR(10),
	black VARCHAR(10),
	PRIMARY KEY (id),
	FOREIGN KEY (game_id) REFERENCES game (id)
);
