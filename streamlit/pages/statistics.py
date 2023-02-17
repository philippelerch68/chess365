import streamlit as st
import mysql.connector
import io
import chess.pgn
import pandas as pd
import numpy as np


'''
0	1	total_files_games	200
1	3	dim_eco	501
2	4	dim_event	7257
3	5	dim_federation	45
4	6	dim_result	5
5	7	dim_site	2179
6	8	dim_title	2
7	9	game	279209
8	11	player	19846
9	14	moves_min	4
10	15	moves_mean	86
11	16	moves_max	471
12	17	total_error_import	403
13	18	total_begin	279612
14	19	lost_import_percent	0.14


'''



# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()


def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
def  get_data(sql, issue):
    st.subheader(issue)
    result = run_query(sql)
    for raw in result:
        st.text(raw)

st.header(" Insights of chess data ")    
get_data(sql = "SELECT * FROM app_cnt_games ORDER BY game_year, cnt_games DESC", issue = "Who played the most games by year?")

st.write("--------------------------")
get_data(sql = "SELECT * FROM app_cnt_games ORDER BY game_year, cnt_games_succeed DESC", issue = "Who was the most successful player by year (success percentage)?")

st.write("--------------------------")
get_data(sql = "SELECT * FROM app_cnt_games ORDER BY game_year, cnt_games_lose DESC", issue = "Who was the least successful player by year (loose percentage)?")

st.write("--------------------------")
get_data(sql = "SELECT * FROM app_cnt_games ORDER BY game_year, cnt_games_succeed ASC", issue = "Who was the most successful player, playing white, by year (success percentage)?")

st.write("--------------------------")
get_data(sql = "SELECT * FROM app_cnt_games ORDER BY game_year, cnt_games_succeed ASC", issue = "Who was the most successful player, playing black, by year (success percentage)?")

st.write("--------------------------")
get_data(sql = "SELECT * FROM app_cnt_games ORDER BY game_year, cnt_games_succeed ASC", issue = "Which player improved in skill level in 2022?")



