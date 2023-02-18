import streamlit as st
import mysql.connector
import io
import chess.pgn
import pandas as pd
import numpy as np






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
    df = pd.DataFrame(result, columns=['title','value'])
    df = df.set_index(['title'])
    pd.set_option('display.max_columns', True)

    st.dataframe(df)

    
get_data(sql ="SELECT title, data1 FROM app_stat order by title")
