CREATE OR REPLACE VIEW datascientest.cnt_Fgame AS 
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