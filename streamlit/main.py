# Philippe LERCH

'''
philippe@DDev:/Projects/Datascientest/Examens/chess365/chess_4/chess365/streamlit$ streamlit run main.py 
Network URL: http://192.168.0.35:8501
'''
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


# Side bar


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


df, result = get_data(sql ="SELECT title, data1 FROM app_stat", issue='')
     

# Default
text = f'''
<h1> CHESS</h1>
<i>Analytics Engineering Project </i><br><br>
<b>The aim of this project is to build a data engineering pipeline in the form of an ELT process that loads chess data for 200 players and their game histories. The data is loaded, fitted, and integrated into a data model built on a SQL database schema (MySQL).
<br><i>More details can be found at  <a href="https://github.com/philippelerch68/chess365" target="_blank">Chess Project</a></i>
<br><br><b>The last part of project is to create an analytics application. <i>(Done with Streamlit)</i>.</b>
<br><br>
<h3> Streamlit content</h3>
    <li> game    : Display an example of complete chess board. </li>
    <li> insight : Somes statistics about chess Games data.</li>

<br>
<h4> Importation information</h4>

Of {result[6][1]} records, {result[5][1]} are successfully integrated on dedicated tables.
Less than <b  style="color:Green;">1%</b> are lost ! ({result[0][1]}).<br><br>
<B>Below additional information</B><br><i>(Table record, games & players informations)<i>

'''

st.markdown(text,unsafe_allow_html=True)
st.dataframe(df)


st.markdown(''' --------------------------------- 
            Christophe P. & Philppe L. | Analytics Engineering Project | @Datascientest 2023 
            ''')