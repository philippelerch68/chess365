from helpers import read_yaml, files_count, insert_data
import json

def parse_directory(dir_path, db, table):
    """Analyse files of a given directory; calls function read_load_file_data()

    Args:
        dir_path (str): Path to directory, where raw data files are stored
        db (str): Database, where data should be inserted
        table (str): Database table, where data should be inserted
    """
    files = sorted(os.listdir(dir_path), reverse=False)
    len(files)
    print(files)

    for file in files:
        print(f"Process File {files.index(file)+1}/{len(files)}: {file}", end="\r")
        read_load_file_data(dir_path, file, db, table)
        

def read_load_file_data(dir_path, file, db, table):
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
    if file.endswith('.pgn'):
        try:
            with open(dir_path+file,encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        
            for line in lines:
                #process_lines_pct = int(round((lines.index(line)+1/len(lines))*100,0))
                arr = content_cleaner(line)
                #for each game,create a row to be inserted
                db_data = []
                if arr:
                    db_data.append(arr[1])
                #if the line contains 'game', then insert into table    
                    if arr[0] == 'Move':
                        sql = f"""INSERT INTO {table} (
                            event, site, date, round, white, black, result, whiteelo, blackelo, eco, game) 
                            VALUES ({db_data})
                            """
                        #print(sql)
                        insert_data(db, sql)
        
        except:
            print(f"!------Problem with file: {file} ------!")
            flog = open('file-error.txt', "a")
            flog.write(f"{file} --")
            flog.write("\n")
    
    #process players
    elif file.endswith('.json'):
        try:
            with open(dir_path+file,encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
            
            sql = f"""INSERT INTO {table} (
                ranking,name,elo,title,fideid,federation,games,birthyear,page) 
                VALUES ({data.get('Rank')},
                        {data.get('Name').replace("'","`")},
                        {data.get('ELO')},
                        {data.get('Title')},
                        {data.get('FIDEId')},
                        {data.get('Federation')},
                        {data.get('Games')},
                        {data.get('BirthYear')},
                        {data.get('Page').replace("'","`")}
                )
                """
            #print(sql)
            insert_data(db, sql)
        
        except:
            print(f"!------Problem with file: {file} ------!")
            flog = open('file-error.txt', "a")
            flog.write(f"{file} --")
            flog.write("\n")
            

def content_cleaner(line):
    """Applies some cleaning to individual lines of Games data files

    Args:
        line (str): Individual line of a Games data file
    """
    arr=[]
    if line.startswith('[') and line.rstrip('\n').endswith('"]'):
        line = line.replace('[','')
        line = line.replace(' "]','"]')
        line = line.replace(', "]','"')
        line = line.replace(']','')
        line = line.replace(' "',';"')
        line = line.replace(', "',',""')
        line = line.replace('\n',"")
        arr = line.split(';')
        
    # FOR GAME Value.   
    elif any(line.startswith(x) for x in ["1", "0", "{", "*"]) and line.endswith('\n'):
            arr.append('Move')
            line=line.replace('"',"`")
            line = line.replace('\n',"") 
            arr.append('"'+line+'"')
    return arr