# Philippe LERCH

'''
philippe@DDev:/Projects/Datascientest/Examens/chess365/chess_4/chess365/streamlit$ streamlit run streamlit_app.py 
Network URL: http://192.168.0.35:8501
'''

import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
        page_title="Chess",
        layout="centered",
    )


# Side bar

st.markdown("# Welcome ")
st.sidebar.markdown("# Main page ")

# Main container

# Default
text = '''
This part is an analytics application base on a dataengineering pipeline, which loads chess data of 200 Players and their Gamehistory. 
\n
More info at : https://github.com/philippelerch68/chess365


IMPORTATION STATUS


|                                            |  NBRS  |   %    |
| ------------------------------------------ | -----  | ------ |  
| Nbrs game files (png)                      |    200 | 100    |
| Nbrs player files (json)                   |    200 | 100    |
| ------------------------------------------ | -----  | ------ |
| GAME    RAWS   TOTAL                       | 279209 | 100    |
| PLAYERS RAWS   TOTAL                       |    200 | 100    |
| ------------------------------------------ | -----  | ------ |
| GAME RAW DEGRADATION IMPORT                |        |        |
| Total raw                                  | 279623 | 100    |
| Total raw imported to game_raw             | 279209 |  99.85 |
| Total raw imported in game                 | 226134 |  80.99 |
|                                            |        |        |
| **Total lost**                                 |  **53489** |  **19.15** |
|                                            |        |        |
| Cause of lost data :                       |        |        |
|     - PNG parser                           |    414 |   0.14 |
|     - Date format (??)                     |  24234 |   8.66 |
|     - Incompatible import                  |  29225 |  10.04 |
|     - SQL import error :                   |     11 |  0.003 |
| ------------------------------------------ | -----  | ------ |
| PLAYERS RAWS TOTAL (players + game parsing)|  19846 |  98.99*| 
----------------------------------------------------------------
* Only 1.01 is comming from player files (json)







'''

st.subheader("General info")
st.markdown(text)



# Pie chart, where the slices will be ordered and plotted counter-clockwise:
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct      

title_string = "CAUSE OF LOST DATA"
labels = 'PNG parser', 'Date', 'SQL'
values = [30, 34, 11]


fig = plt.figure(2, figsize=(0.5,0.5))
ax = fig.add_subplot(111)
ax.axis('equal')
plt.suptitle(title_string,fontsize = 4)
ax.pie(values,  labels=labels, autopct=make_autopct(values), shadow=False, startangle=90, textprops={'fontsize': 4})
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)
        
 

