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
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()
input_id = 1
move_id =1
game_id = None
#arguments = sys.argv
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
tabs_font_css = """
<style>
div[class*="stText"] label {
  font-size: 26px;
  color: red;
}

div[class*="stTextInput"] label {
  size: 26px;
  color: red;
}

div[class*="stNumberInput"] label {
  font-size: 26px;
  color: green;
}

div[class*="stWriteExpander"] label {
  font-size: 26px;
  color: green;
}

 .streamlit-expanderHeader.st-ae.st-dj.st-ag.st-ah.st-ai.st-aj.st-bv.st-dk.st-bw.st-dl.st-dm.st-dn.st-do.st-ar.st-as.st-dp.st-dq.st-b3.st-cj.st-c5.st-dr.st-b4.st-ds.st-c3.st-c4.st-c2.st-c1{
                           font-size:30px;
                           text-align:center;     
                           color:blue;
                           background-color :red;
                    }



</style>
"""

st.write(tabs_font_css, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Players", "Game"])

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    with st.container():
        st.write(html, unsafe_allow_html=True)

def render_svg_example(image):
    svg = image
    render_svg(svg)

def export_svg(id):
    
    sql =f"SELECT game.id, game.moves FROM game where id ={id}"
    result=run_query(sql)
    

    for raw in result:
            a = 0
            game_id = raw[0]
            game_value = raw[1]
            pgn = io.StringIO(game_value)
            game = chess.pgn.read_game(pgn)
            path_data = f"./images/game/{game_id}"
            isExist = os.path.exists(path_data)
            if isExist == False :
                try:
                    mode = 0o755
                    os.mkdir(f"./images/game/{game_id}", mode)
                except:
                    print("Not able to create directory !")
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
        
        0 G.id 
        1 Event 
        2 Site
        ------ White info
        3 WTitle
        4 White_player
        5 WFederation
        6 WRank
        7 WElo
        8 WPage
        
        -----  Black info         
        9 BTitle
        10 Black_player
        11 BFederation
        12 BRank
        13 BElo
        14 BPage
        
        ----- Game info 
        15 Result
        16 Eco
        17 Game_date
        18 Stage
        19 Whiteelo
        20 Blackelo
        21 Moves
        22 Total_move
    """
   
    sql =f'''SELECT * FROM datascientest.cnt_Fgame where id = {id}
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

        st.header(" GAME INFORMATION ")
        st.write("--------------------------")
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
                
        
        
            


input_id = st.sidebar.text_input("game id",1)


if input_id :
    #display_move(id=input_id)
    with tab1:
        a=export_svg(id=input_id)
        display_game(input_id)
    #image = f"./images/game/{input_id}/chess_id_{input_id}_1.SVG"

if a:
    with tab2:
        move_id = st.slider('move', 1, 1, a)    
  
if move_id :
    f = open(f"./images/game/{input_id}/chess_id_{input_id}_{move_id}.SVG", "r")
    image = f.read()
    with tab2:
        render_svg_example(image)
   
    
