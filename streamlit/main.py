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

# Main container

# Default
text = '''
This part is an analytics application base on a dataengineering pipeline, which loads chess data of 200 Players and their Gamehistory. 
\n
More info at : https://github.com/philippelerch68/chess365


IMPORTATION STATUS


'''

st.subheader("General info")
st.markdown(text)

     
 

