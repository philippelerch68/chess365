-- create view of games where player is "white"
CREATE OR REPLACE VIEW datascientest.cnt_games_white AS 
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
	FROM datascientest.player p
	LEFT JOIN datascientest.game gw 
		ON p.id = gw.white_player_id
	LEFT JOIN datascientest.dim_result dr
		ON gw.result_id = dr.id
	) a
;

-- create view of games where player is "black"
CREATE OR REPLACE VIEW datascientest.cnt_games_black AS 
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
	FROM datascientest.player p
	LEFT JOIN datascientest.game gb 
		ON p.id = gb.black_player_id
	LEFT JOIN datascientest.dim_result dr
		ON gb.result_id = dr.id
	) a
;

-- create view, where data is merged
CREATE OR REPLACE VIEW datascientest.cnt_game AS 
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
	FROM datascientest.player p
    LEFT JOIN datascientest.game g
		ON (p.id = g.white_player_id OR p.id = g.black_player_id)
) p
LEFT JOIN datascientest.cnt_games_white cgw
	ON p.playerid = cgw.player_id AND p.game_year = cgw.game_year
LEFT JOIN datascientest.cnt_games_black cgb
	ON p.playerid = cgb.player_id AND p.game_year = cgb.game_year
;

CREATE TABLE datascientest.app_cnt_games
SELECT * 
FROM datascientest.cnt_game
ORDER BY cnt_games DESC
LIMIT 10;

select * from datascientest.app_cnt_games;
