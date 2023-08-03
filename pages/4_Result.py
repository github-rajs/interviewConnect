import streamlit as st
import random
import json
from streamlit_extras.switch_page_button import switch_page
import time
import psycopg2 as pg
import pandas.io.sql as psql
from config import DBCONN
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import  streamlit_toggle as tog
from pathlib import Path
import pandas as pd
import numpy as np
from streamlit.source_util import _on_pages_changed, get_pages
from datetime import datetime

#database related variables
host=DBCONN.host
ip=DBCONN.ip
port=DBCONN.port
user_name=DBCONN.user_name
passwd=DBCONN.passwd
database=DBCONN.database
info_table=DBCONN.table1

def store_data(SQL):
    try:      
      connection = pg.connect(user=user_name,
                              password=passwd,
                              host=host,
                              port=port,
                              database=database)
      
      cursor = connection.cursor()
      cursor.execute(SQL)
      connection.commit()
      cursor.close()
      connection.close()
      dbstatus='success'

    except Exception as err:
      dbstatus=err
    return dbstatus

def fetch_data(SQL):
    try:      
      connection = pg.connect(user=user_name,
                              password=passwd,
                              host=host,
                              port=port,
                              database=database)
      
      cursor = connection.cursor()
      cursor.execute(SQL)
      fetched_data=cursor.fetchall()
      cursor.close()
      connection.close()
      fetch_status='success'

    except Exception as err:
      fetch_status=err
      fetched_data='null'
    return fetched_data,fetch_status



#####################################################################################################################################################################
st.set_page_config(page_title='InterviewConnect Demo', page_icon="💻", layout="wide", initial_sidebar_state="expanded", menu_items=None) 
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """         
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://i.ibb.co/txPQ2Yp/logo-new.png');
                background-repeat: no-repeat;
                padding-top: 0px;
                background-position: 0px 0px;
                background-size: 335px 115px;
                top: 13px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_logo()
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)


styl = """
    <style>
        div[data-testid="css-5rimss"] stTextInput > div[data-baseweb="input"] {width: 400px;}
    </style>
    """
st.markdown(styl, unsafe_allow_html=True)
#####################################################################################################################################################################

try:
    code = st.experimental_get_query_params()['code'][0]
    st.session_state.email=code
except:
   print('error')

if 'email' not in st.session_state:
   st.session_state.email='null'
if 'counter' not in st.session_state:
   st.session_state.counter=0
elif 'counter' in st.session_state:
   st.session_state.counter=0



def show_result():
  mcq_res_sql=f"select count(case when correct_option = entered_option then 0 end) as real_count \
  from cand_int_data  where qns_type='mcq' and email_id='{st.session_state.email}' and qid in(select distinct qid from cand_int_data)"

  coding_res_sql=f"select count(case when correct_option = 'correct' then 0 end) as real_count \
  from cand_int_data  where qns_type='coding' and email_id='{st.session_state.email}' and qid in(select distinct qid from cand_int_data)"

  mr,mt=fetch_data(mcq_res_sql)
  cr,ct=fetch_data(coding_res_sql)

  c1,c2,c3=st.columns([1,5,1])
  c2.header('Multiple Choice Questions')
  c2.subheader(f":red[{mr[0][0]}] answered correctly out of :red[20] questions")
  c2.text('')
  c2.text('')
  c2.header('Coding Problems')
  c2.subheader(f":red[{cr[0][0]}] answered correctly out of :red[10] questions")
  c2.text('')
  c2.text('')
  s1=mr[0][0]*2
  s2=cr[0][0]*5
  c2.header(f"Your Score : :red[{int(s1+s2/90*(100))}]")

  store_scoresql=f"update candidate_info set exam_result='{str(int(s1+s2/90*(100)))}' and logoff_time=now() where email_id='{st.session_state.email}';commit;"

  store_data(store_scoresql)

  close_btn=c2.button('Finish Exam & Log Out')
  if close_btn:
     st.cache_data.clear()
     switch_page('Candidate Login')
     


if st.session_state.email != 'null':
    try:
        fetch_status_sql=f"select coding_status from cand_qn_status where email_id='{st.session_state.email}';"
        fss,fsst=fetch_data(fetch_status_sql)

        if fss[0][0] == 'closed':
           show_result()

        else:
            st.text(f"Email is inavalid or not exist:{st.session_state.email}")    
    except Exception as someerr:
       st.image('src/locked_page.png',width=200)
       st.subheader('This Page is Locked')       
else:
   st.image('src/locked_page.png',width=200)  
   st.subheader('This Page is Locked')


#####################################################################################################################################################################


ft = """
<style>
a:link , a:visited{
color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

#page-container {
  position: relative;
  min-height: 10vh;
}

footer{
    visibility:hidden;
}

.footer {
position: relative;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #808080; /* theme's text color hex code at 50 percent brightness*/
text-align: center; /* you can replace 'left' with 'center' or 'right' if you want*/
}
</style>

<div id="page-container">

<div class="footer">
<p style='font-size: 0.875em;'>© 2023. Ahana Systems and Solutions Private Limited </p>
</div>

</div>
"""
st.write(ft, unsafe_allow_html=True)