from pathlib import Path
from db.create_db import create_database
from db.create_tables import create_tables
from extract_load.extract import download, extract
from extract_load.parse_load import parse_directory
from transform.parse_datamodel import parse_datamodel, erd, import_dim_location,import_game_data
from db.db_ddl import tables
from helpers import read_yaml, select_data, insert_data, delete_data




if __name__=='__main__':
    
    config = read_yaml("config.yaml")

    print("------------------ Read config -------------------", end='\r')    
    db_host=config.get('DATABASE').get('db_host')
    db_database=config.get('DATABASE').get('db_database')
    db_user=config.get('DATABASE').get('db_user')
    db_password=config.get('DATABASE').get('db_password')
    db=[db_host, db_database, db_user, db_password]

    url=config.get('DATA').get('url')
    data_dir=Path(config.get('DATA').get('data_dir'))
    save_as=Path(config.get('DATA').get('save_as'))
    games_dir=Path(config.get('DATA').get('games_dir'))
    players_dir=Path(config.get('DATA').get('players_dir'))
    db_log = Path(config.get('DATA').get('db_log')) 
    error_log = Path(config.get('DATA').get('db_error_log')) 
    

    print("------------------ Starting process --------------", end='\r')
    print("------------------------------------------------------------")
    
    print("Creating database ................................", end='\r')
    #create_database(host=db_host, database=db_database, user=db_user, password=db_password)

    print("Creating tables ..................................", end='\r')
    #create_tables(tables_dict=tables, host=db_host, database=db_database, user=db_user, password=db_password)
    
    print("Loading compressed file ..........................", end='\r')
    #download(url,data_dir, save_as)

    print("Extracting data ..................................", end='\r')
    #extract(save_as, data_dir)

    # -------- END OF DOWNLOAD AND EXTRACTING ----------------------------

    print("IMPORTING folder games files to db ...............", end='\r')
    parse_directory(games_dir, db, 'games_raw',db_log,error_log)
    
    
    
    
    print("IMPORTING folder players files to db .............                      ", end='\r')
    parse_directory(players_dir, db, 'players_raw',db_log,error_log)
    
    # ------------- END  PART OF  CHESS_RAW  AND PLAYERS_ RAW  -------------------------
    
    
    print("TRANSFORM import_dim_location ....", end='\r')
    import_dim_location(db,db_log,error_log)

    print("TRANSFORM data into entity relationship model ....", end='\r')
    parse_datamodel(erd_dict=erd, host=db_host, database=db_database, user=db_user, password=db_password)
    
    print("Cleaning event table ..........................", end='\r')
    sql = '''
        DELETE FROM event
            WHERE 
            id IN (
            SELECT id
            FROM (
                select id,ROW_NUMBER() 
                    OVER (PARTITION BY name ORDER BY name ) AS number
                from event
            ) t
            WHERE number > 1
            )
        '''
        
    delete_data(db, sql,db_log,error_log)
    
    print("IMPORT GAME  ..........................", end='\r')
    import_game_data(host=db_host, database=db_database, user=db_user, password=db_password)
    
    print("------------------------------------------------------------")
    print("------------------- END OF LOAD ----------------------------")
    
    
    
