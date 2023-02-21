import chess
import chess.svg
import chess.pgn
import sys
import os
import io
import mysql.connector
import streamlit as st
from PIL import Image
import base64
import textwrap

#@st.cache_resource
def init_connection():
    """_summary_
        BD initialisation
    Returns:
        _type_: Connection
    """
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

#arguments = sys.argv  ! Check if need for your os
#pgnfilename = str(arguments[1])

def max_width():
    max_width_str = "max-width:600px;"
    st.markdown(
        f"""
    <style>
    .block-container {{
        {max_width_str}
        }}
    <style>
    """,
        unsafe_allow_html=True,
    )
    

max_width()

st.sidebar.markdown('''
                    This is an example who load a game board and display result.
                    ''')

tab1, tab2 = st.tabs(["Players", "Game"])

def run_query(query):
    """_summary_

    Args:
        query (_type_): Run sql query

    Returns:
        _type_: return result of query
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def render_svg(svg):
    """Renders the given svg string to PNG"""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    with st.container():
        st.write(html, unsafe_allow_html=True)
        
        

def render_svg_example(image):
    """_summary_

    Args:
        image (_type_): Generate SVG file
    """
    svg = image
    render_svg(svg)
    
    

def export_svg(id):
    """_summary_

    Args:
        id (INT): Id from game table

    Returns:
        INT: return number of moves
    """
    
    sql =f"SELECT game.id, game.moves FROM game where id ={id}"
    result=run_query(sql)
    for raw in result:
            #Load data from query and generate chess game boards for each move
            a = 0
            game_id = raw[0]
            game_value = raw[1]
            pgn = io.StringIO(game_value)
            game = chess.pgn.read_game(pgn)
            path_data = f"./images/game/{game_id}"
            isExist = os.path.exists(path_data)
            if isExist == False :
                
                try:
                    oldmask = os.umask(000)
                    mode = 0o777
                    os.mkdir(path_data, mode)
                    os.umask(oldmask)
                except OSError as error:
                    print(f" Please check right to create image ! {error}")
                    exit()
            
            try:
                # game.mainline()  
                board = game.board()
                for move in game.mainline_moves():
                    a+=1
                    board.push(move)                     
                    boardsvg = chess.svg.board(board=board)
                    f = open(f"./images/game/{game_id}/chess_id_{game_id}_{a}.SVG", "w")
                    f.write(boardsvg)
                    f.close()
        
            except:
                print("error")
    return a


def display_game(id):
    """_summary_

    Args:
        id (int): id passed to DB
        
    """
    sql =f'''SELECT * FROM app_cnt_fgame where id = {id}
    ''' 
    result= run_query(sql)
    text = ''
    for raw in result:
        st.sidebar.text("--- GAME INFORMATION ---")
        st.sidebar.text(f"Event : {raw[1]}")
        st.sidebar.text(f"Location : {raw[2]}")
        st.sidebar.text(f"Date : {raw[17]}")
        st.sidebar.text(f"Stage : {raw[18]}")
        st.sidebar.text(f" Nbr moves : {raw[22]}")
        st.sidebar.text(f"Result : {raw[15]}")
        
        st.subheader(f"WHITE")
        st.text(f"Name : {raw[3]}  {raw[4]}")
        st.text(f"Federation : {raw[5]}")
        st.text(f"Rank : {raw[6]} Elo : {raw[7]} Elo2 : {raw[19]}")
        st.markdown(f"More info : {raw[8]}")
        st.write("--------------------------")
        st.subheader(f"BLACK")
        st.text(f"Name : {raw[9]}  {raw[10]}")
        st.text(f"Federation : {raw[11]}")
        st.text(f"Rank : {raw[12]} Elo : {raw[13]} Elo2 : {raw[20]}")
        st.markdown(f"More info : {raw[14]}")
        
        game_value = raw[21]
        pgn = io.StringIO(game_value)
        game = chess.pgn.read_game(pgn)
        game.mainline()  
        board = game.board()
        
        for move in game.mainline():
            
            comment = move.comment
            if(comment != ''):
                text = text + str(comment)+str(" ")
        
        st.write("---------------")
                
        with tab1:
            if(text):
                expander = st.expander("See Comments")
                expander.write(f"{text}")
                
input_id = st.sidebar.text_input("Enter an ID from game.",1)

if input_id :
    
    with tab1:
        a=export_svg(id=input_id)
        display_game(input_id)
    

if a:
    with tab2:
        move_id = st.slider('move', 1, 1, a)    
  
if move_id :
    f = open(f"./images/game/{input_id}/chess_id_{input_id}_{move_id}.SVG", "r")
    image = f.read()
    with tab2:
        render_svg_example(image)

