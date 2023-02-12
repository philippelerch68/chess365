import streamlit as st
import mysql.connector
import io
import chess.pgn
import pandas as pd
import numpy as np

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()


def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
def  get_data(sql):
    game_moves = []
    
    result = run_query(sql)

    for raw in result:
        game_id = raw[0]
        total_game_moves = raw[1]
        game_moves.append(total_game_moves)

    df = pd.DataFrame(game_moves)
    return df
    

def move_describe(sql):
    df = get_data(sql)
    describe = df.describe().apply(lambda s: s.apply('{0:.0f}'.format))
    min = df.min().astype(int) 
    mean = df.mean().astype(int) 
    max = df.max().astype(int)
    count = df.count().astype(int)
    
    return min,max,mean,count


def histogram(df):
    a=0
     


def duplicate_move(sql):
    df = get_data(sql)
    return df

    
    


# GET Describe
def display_describe():
    st.subheader("MOVES STATISTICS")
    min,max,mean,count = move_describe(sql ="SELECT game_id, total_game_moves FROM move_count")
    count = count[0]
    st.write(f"Count : {count}")
    st.write(f"Min : {min[0]}")
    st.write(f"Max : {max[0]}")
    st.write(f"Mean : {mean[0]}")



def display_duplicate_move():
    sql = '''
    SELECT moves, count(id)
    FROM   game
    GROUP  BY moves
    HAVING COUNT(moves) > 1;
    '''
    # st.dataframe(describe)  
    data = duplicate_move(sql)
    count = int((int(data.count()[0])- (1235+130+55)))
    st.write(f" Identical moves : {count} ")

             
display_describe()             
display_duplicate_move()        

    