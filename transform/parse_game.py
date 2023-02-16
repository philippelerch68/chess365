# MOve info
# pip install mysql-connector-python
import io
import chess.pgn
import mysql.connector
from mysql.connector import Error

if __name__=='__main__':
    
    host = "192.168.0.35"
    port = 3306
    database = "datascientest"
    user = "philippe"
    password = "philippe"

    connection = mysql.connector.connect(host=host,
                                                database=database,
                                                user=user,
                                                password=password)
    cursor = connection.cursor()


    sql="TRUNCATE TABLE app_move_nbr"
    cursor.execute(sql)
    connection.commit()

    sql ="SELECT game.id, game.moves FROM game"
    cursor.execute(sql)
    result = cursor.fetchall()
    list_value=[]
    a=0

    for raw in result:
            a = 0
            game_id = raw[0]
            game_value = raw[1]
            pgn = io.StringIO(game_value)
            game = chess.pgn.read_game(pgn)
            try:
                # game.mainline()  
                board = game.board()
                array=[]
                for move in game.mainline_moves():
                    a+=1

                #list_value.append([game_id,a])
                
            except:
                error = raw[0]
                a=0
                #list_value.append([game_id,0])
                #print(error)
            
            sql =f"insert into app_move_nbr (id,nbr_move) values ({game_id},{a})"
            cursor.execute(sql)
            connection.commit()