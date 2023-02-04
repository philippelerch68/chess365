import streamlit as st
import mysql.connector
import io
import chess.pgn

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()
input_id = None
game_id = None


def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
def select_game():
    """_summary_

    Returns:
        _type_: _description_
    """
    sql ='''
    SELECT game.id, event_id, event.name, dim_location.txt as location,dim_location.txt1 as country, gamedate, plw.lastname as wlastname,plw.firstname as wfirstname ,plb.lastname as plastname,plb.firstname as pfirstname, stage,whiteelo,blackelo, dim_result.txt as result, moves FROM game
        inner join player as plw on plw.id = white_player_id
        inner join player as plb on plb.id = black_player_id
        inner join event on event.id = game.event_id
        inner join dim_result on dim_result.id = game.result_id
        inner join dim_location on dim_location.id = event.location_id
        where moves like "%{%" and  dim_location.txt like "%Paris%"
        order by game.id
        '''
    result= run_query(sql)
    list_value = [(row[0], row[6]+ "  <--> " + row[8]) for row in result]
    
    return list_value
    
    
def display_chess_game(id):
    """_summary_

    Args:
        id (id): id passed to DB for game.id
    """
    
    input_id = id
    game_id = id
    sql =f"SELECT game.id, game FROM Datascientest.game where id = {id} "
    result= run_query(sql)
    line=''
    comment = False
    a=0
    
    for raw in result:
        game_id = raw[0]
        game_value = raw[1]
        pgn = io.StringIO(game_value)
        game = chess.pgn.read_game(pgn)
        game.mainline()  
        board = game.board()
        array=[]
        # print(game.mainline())  see original data
        col1, col2 = st.columns([3, 2])
        
        with col1:
            display_move(id=id)
        
        for move in game.mainline():
            
            comment = move.comment
            if(comment != ''):
                with col1:
                    st.subheader("Comment from game ")
                    st.write(f" {comment}")
        a=0
        for move in game.mainline_moves():
            board.push(move) 
            array.append(board.unicode())
            a+=1
        with col1:
            st.subheader(f"Total numbers of battle : {a}")
        b =0
        with col2:
            st.subheader("Moves")
            for move in array:
                b+=1
                st.write(f"battle : {b}") 
                st.text(move)
        

def display_move(id):
    """_summary_

    Args:
        id (int): id passed to DB
    """
    
    sql =f'''
    SELECT game.id,event_id, event.name, dim_location.txt as location,dim_location.txt1 as country, gamedate, plw.lastname as wlastname,plw.firstname as wfirstname ,plb.lastname as plastname,plb.firstname as pfirstname, stage,whiteelo,blackelo, dim_result.txt as result, moves FROM game
    inner join player as plw on plw.id = white_player_id
    inner join player as plb on plb.id = black_player_id
    inner join event on event.id = game.event_id
    inner join dim_result on dim_result.id = game.result_id
    inner join dim_location on dim_location.id = event.location_id
    where game.id = {id}
    ''' 
    result= run_query(sql)
    for raw in result:
        st.subheader(f"Event")
        st.write(f"{raw[5]}  {raw[2]}  at: {raw[3]} {raw[4]}")
        st.subheader(f"Players")
        st.markdown(f" White : **{raw[6]}** {raw[7]}  ")
        st.write(f" Black : **{raw[8]}**  {raw[9]}  ")
        st.subheader(f"Result ")
        st.write(f" {raw[13]}")


list_value = select_game()

st.sidebar.subheader(f" Global ")   
input_id = st.sidebar.text_input("game id (6483)")
if input_id:
    #st.write(f" {input_id}")
    display_chess_game(id=input_id)  #6483


st.sidebar.subheader("Game in Paris ")  
game_id = st.sidebar.selectbox(label='Select players',options=list_value,format_func=lambda x: x[1])
if game_id:
    input_id = game_id[0]
    display_chess_game(id=game_id[0])  #6483




