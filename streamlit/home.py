import streamlit as st
import matplotlib.pyplot as plt
import mysql.connector
import io
import chess.pgn
import pandas as pd
import numpy as np

st.set_page_config(
        page_title="Chess",
        layout="centered",
    )


# Initialize connection.
# @st.cache_resource
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
    return df, result

# statistic info
df, result = get_data(sql ="SELECT title, data1 FROM app_stat", issue='')
     
st.image("./images/chess-banner.png")
# Default
text = f'''
<b>The aim of this project is to build a data engineering pipeline in the form of an ELT process that loads chess data for 200 players and their game histories. The data is loaded, fitted, and integrated into a data model built on a SQL database schema (MySQL).
<br><i>More details can be found at  <a href="https://github.com/philippelerch68/chess365" target="_blank">Chess Project</a></i>
<br><br><b>The last part of project is to create an analytics application. <i>(Done with Streamlit)</i>.</b>
<br><br>
<h3> Streamlit content</h3>
    <li> main    : General information about project,data and tables. </li>
    <li> game    : Display an example of complete chess board. </li>
    <li> insight : Somes statistics about chess Games data.</li>

<br>
<h4> Importation information</h4>

Of {result[6][1]} records, {result[5][1]} are successfully integrated on dedicated tables.
Less than <b  style="color:Yellow;">1%</b> are lost ! ({result[0][1]}).<br><br>

'''

st.markdown(text,unsafe_allow_html=True)

# Samples data from Game tables
st.write("All data are from Game table and displayed via Views tables.")
st.write("Game table sample:")
result = run_query("SELECT id, event_id, site_id, white_player_id, black_player_id, result_id, eco_id, gamedate, stage, whiteelo, blackelo, moves FROM game limit 10;")
dfr = pd.DataFrame(result, columns=['id', 'event_id', 'site_id', 'white_player_id', 'black_player_id', 'result_id', 'eco_id', 'gamedate', 'stage', 'whiteelo', 'blackelo', 'moves'])
st.dataframe(dfr)

# Tables views list
st.write("Tables views list:")
result = run_query("Show tables like 'app%';")
dfr = pd.DataFrame(result, columns=['Tables'])
st.dataframe(dfr)

# Additionnal information coming from statistic (get_data)
st.write("Below additional information")
st.dataframe(df)


# FOOTER

st.markdown(''' --------------------------------- 
            Christophe P. & Philppe L. | Analytics Engineering Project | @Datascientest 2023 
            ''')
