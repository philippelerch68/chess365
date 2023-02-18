import os
import json
import chess.pgn as pgn
from helpers import insert_data


def parse_directory(dir_path, db, table,db_log,error_log):
    """Analyse files of a given directory; calls function read_load_file_data()

    Args:
        dir_path (str): Path to directory, where raw data files are stored
        db (str): Database, where data should be inserted
        table (str): Database table, where data should be inserted
    """
    files = sorted(os.listdir(dir_path), reverse=False)
    len(files)
    #print(files)

    for file in files:
        print(f"Process File {files.index(file)+1}/{len(files)}: {file}", end="\r")
        read_load_file_data(dir_path, file, db, table,db_log,error_log)
        

def read_load_file_data(dir_path, file, db, table,db_log,error_log):
    """Opens all files of a given directory, and inserts the content of the file in a given database table. 
    Players and Games are processed according to their file extension. In case of Games, a function content_cleaner()
    is called.

    Args:
        dir_path (str): Path to directory, where raw data files are stored
        file (str): File to be processed
        db (str): Database, where data should be inserted
        table (str): Database table, where data should be inserted
    """
    #process games
    result=''
    if file.endswith('.pgn'):
        try:
            with open(dir_path.joinpath(file),encoding='utf-8', errors='ignore') as f:
                games = []
                while True:
                    try:
                        game = pgn.read_game(f)
                    except:
                        game = str(game)
                        print(f"!------READING Problem with file: {file} ------!")
                        flog = open(f"{error_log}", "a")
                        flog.write(f"!------READING Problem with file: {file} ------!")
                        flog.write(f"{game} ")
                        flog.write("-----------------------------------------------------------")
                        flog.write("\n")
                        
                    if game is not None:
                        games.append(game)
                    else:
                        break
                        
            for game in games:
                move = str(game.mainline_moves())
                move = move.replace('"','`')
                sql = f"""INSERT INTO {table} (
                    event, site, date, round, white, black, result, whiteelo, blackelo, eco, game) 
                    VALUES ("{game.headers["Event"]}",
                            "{game.headers["Site"]}",
                            "{game.headers["Date"]}",
                            "{game.headers["Round"]}",
                            "{game.headers["White"]}",
                            "{game.headers["Black"]}",
                            "{game.headers["Result"]}",
                            "{game.headers["WhiteElo"]}",
                            "{game.headers["BlackElo"]}",
                            "{game.headers["ECO"]}",
                            "{move}"
                    )
                    """          
                #print(sql)
                result = insert_data(db, sql,db_log,error_log)
                '''
                #print(f"!------log from  file: {file} ------!")
                flog = open (f"{db_log}", "a")
                flog.write(f"{result}{sql} --")
                flog.write("\n")
                '''
        
        except:
            print(f"!------Problem with file: {file} ------!")
            flog = open(f"{error_log}", "a")
            flog.write(f"error : {file} --")
            flog.write(f"{result} --")
            flog.write("\n")
    
    #process players
    elif file.endswith('.json'):
        try:
            with open(dir_path.joinpath(file),encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
            
            sql = f"""INSERT INTO {table} (
                ranking,name,elo,title,fideid,federation,games,birthyear,page) 
                VALUES ("{data.get('Rank')}",
                        "{data.get('Name').replace("'","`")}",
                        "{data.get('ELO')}",
                        "{data.get('Title')}",
                        "{data.get('FIDEId')}",
                        "{data.get('Federation')}",
                        "{data.get('Games')}",
                        "{data.get('BirthYear')}",
                        "{data.get('Page').replace("'","`")}"
                )
                """
            #print(sql)
            result = insert_data(db, sql,db_log,error_log)
            #print(f"!------log from  file: {file} ------!")
            flog = open(f"{db_log}", "a")
            flog.write(f"{result}{sql} --")
            flog.write("\n")
        
        except:
            print(f"!------Player reading Problem with file: {file} ------!")
            flog = open(f"{error_log}", "a")
            flog.write(f"{file} --")
            flog.write(f"{result} --")
            flog.write("\n")
            
