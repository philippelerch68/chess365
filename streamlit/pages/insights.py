import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


# Initialize connection.
# Uses st.experimental_singleton to only run once.
#@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()


#create plot
st.header("Success percentage of players playing white vs black")
df = pd.read_sql("SELECT * FROM app_white_black",conn)
fig, ax = plt.subplots()
ax = df.plot(kind='scatter', x='cnt_games', y='PCT_SUCCEED_WHITE', color='grey', legend=True)    
ax2 = df.plot(kind='scatter', x='cnt_games', y='PCT_SUCCEED_BLACK', color='black', ax=ax)    

plt.legend(['white', 'black'])
plt.xlabel('Number of games played')
plt.ylabel('Success percentage')
st.pyplot()

st.write()
st.write()
st.write()
st.write()



#query data to df
df_app_cnt_games = pd.read_sql("SELECT * FROM app_cnt_games",conn)
year = df_app_cnt_games['game_year'].drop_duplicates()
year_choice = st.sidebar.selectbox('Select year:', year)

years_df_app_cnt_games = df_app_cnt_games.loc[df_app_cnt_games["game_year"] == year_choice]


st.header("Insights on Games played since 2019")

st.subheader("Who played the most games by year?")
st.write(years_df_app_cnt_games)

st.subheader("Who was the most successful player by year?")
df_app_pct_success = pd.read_sql("SELECT * FROM app_pct_success",conn)
years_df_app_pct_success = df_app_pct_success.loc[df_app_pct_success["game_year"] == year_choice]
st.write(years_df_app_pct_success)
    
st.subheader("Who was the least successful player by year?")
df_app_pct_loose = pd.read_sql("SELECT * FROM app_pct_loose",conn)
years_df_app_pct_loose = df_app_pct_loose.loc[df_app_pct_loose["game_year"] == year_choice]
st.write(years_df_app_pct_loose)

st.subheader("Who was the most successful player playing white by year?")
df_app_pct_white_success = pd.read_sql("SELECT * FROM app_pct_white_success",conn)
years_df_app_pct_white_success = df_app_pct_white_success.loc[df_app_pct_white_success["game_year"] == year_choice]
st.write(years_df_app_pct_white_success)

st.subheader("Who was the most successful player playing black by year?")
df_app_pct_black_success = pd.read_sql("SELECT * FROM app_pct_black_success",conn)
years_df_app_pct_black_success = df_app_pct_black_success.loc[df_app_pct_black_success["game_year"] == year_choice]
st.write(years_df_app_pct_black_success)

st.subheader("Which player improved in skill level in 2022?")
df_app_elo_increase = pd.read_sql("SELECT * FROM app_elo_increase",conn)
st.write(df_app_elo_increase)
