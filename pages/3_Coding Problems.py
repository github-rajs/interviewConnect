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

def select_random_qns(input_list, num_items=20):
    num_items = min(num_items, len(input_list))
    return random.sample(input_list, num_items)


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


if 'stage4' not in st.session_state:
    st.session_state.stage4 = 0
if 'stage5' not in st.session_state:
    st.session_state.stage5 = 0
def set_stage4(stage):
    st.session_state.stage4 = stage
def set_stage5(stage):
    st.session_state.stage5 = stage

if 'counter' not in st.session_state: st.session_state.counter = 0
def next(): st.session_state.counter += 1
def prev(): st.session_state.counter -= 1

connection = pg.connect(user=user_name,
                        password=passwd,
                        host=host,
                        port=port,
                        database=database)

def get_current_time():
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    return current_time

def time_difference_in_minutes(time1_str, time2_str):
    time1 = datetime.strptime(time1_str, '%H:%M')
    time2 = datetime.strptime(time2_str, '%H:%M')
    time_diff = time2 - time1
    time_diff_minutes = time_diff.total_seconds() / 60
    return time_diff_minutes

def fetch_prev_time():
    fn=st.session_state.email+'_time.txt'
    with open("cand_data/time_track/"+fn, "r") as file:
        time_track=json.load(file)
        tm=time_track['cur_time']
    file.close()
    return tm


def update_cand_data(updated_data):
       with open('cand_data/'+st.session_state.email+'_code.json', "w") as file:
        json.dump(updated_data,file)
       file.close()

def update_mcq_count(answered):
    c3.metric(label="Total Questions", value=len(random_code_qns))
    c3.metric(label="Answered", value=answered)

def save_final_result(tab_tab):
   connection = pg.connect(user=user_name,
                           password=passwd,
                           host=host,
                           port=port,
                           database=database)
   cursor = connection.cursor()

   if tab_tab == 'secondary':
    with open('cand_data/'+st.session_state.email+'_code.json', "r") as file:
     coding_problems = json.load(file)
    for inf in coding_problems:
     emailID=st.session_state.email
     qns_type='coding'
     qid=inf['qid']
     corr_op=inf['cand_ans']
     qns_status='ans'
     qns_type_status='closed'
     SQL=f"insert into cand_int_data(email_id,qns_type,qid,correct_option,qns_status,qns_type_status) values('{emailID}','coding','{qid}','{corr_op}','ans','closed');commit"
     cursor.execute(SQL)
     connection.commit()
   elif tab_tab == 'primary':
      SQL=f"update candidate_info set logoff_time = now(),session_state='closed' where email_id='{st.session_state.email}';commit"
      cursor.execute(SQL)
      connection.commit()     
   connection.close()


c1,c2,c3=st.columns([3,5,1],gap='medium')
e1=st.columns(7)
d1,d2=c1.columns(2)


Employees={'column':['emp_id','emp_name','emp_age','emp_salary','dept_id','proj_id'],'datatype':['INT PRIMARY KEY','VARCHAR(50)','INT','DECIMAL(10, 2)','INT','INT']}
Departments={'column':['dept_id','dept_name','location'],'datatype':['NT PRIMARY KEY','VARCHAR(50)','VARCHAR(100)']}
Projects={'column':['proj_id','proj_name','start_date','end_date'],'datatype':['INT PRIMARY KEY','VARCHAR(50)','DATE','DATE']}




def CODE_PROBLEMS(random_code_qns):
    cur_time=get_current_time()
    prev_time=fetch_prev_time()
    diff_time=time_difference_in_minutes(prev_time,cur_time)

    if st.session_state.counter >-1 and st.session_state.counter <10:
        update_mcq_count(st.session_state.counter+1)
        c3.subheader(f"Time  {int(diff_time)}")
        c3.caption('(minutes)')
        with e1[1]: st.button("Next ➡️", on_click=next, use_container_width=True)
        with e1[0]: st.button("⬅️ Previous", on_click=prev, use_container_width=True)

        c1.markdown(f"**:black[Question: {random_code_qns[st.session_state.counter]['question']}]**")
        
        c1.caption("Tables to be used:{}".format(random_code_qns[st.session_state.counter]['tbl_structure']))
        with c1:
           with st.expander('View Table Structure',expanded=False):
            st.text('Employees')
            st.table(Employees)
            st.text('Departments')
            st.table(Departments)
            st.text('Projects')
            st.table(Projects)
        c2.text('')
        c2.markdown(f"**:black[SQL Query Editor]**")
        with c2:
            content = st_ace(
            placeholder="--write your sql query here",
            language= LANGUAGES[109],
            theme= THEMES[3],
            keybinding=KEYBINDINGS[3],
            font_size=15,
            min_lines=5,
            key="run_query",)

        c1.markdown(f"**:black[Expected Output]**")
        exp_data=psql.read_sql(random_code_qns[st.session_state.counter]['answer'], connection)
        c1.dataframe(exp_data.set_index(exp_data.columns[0]))

        try:
            if content:
               dataframe = psql.read_sql(content, connection)
               c2.dataframe(dataframe.set_index(dataframe.columns[0]))
               submit_answer=c2.button('Submit Answer',use_container_width=True)
               if submit_answer:
                  try:
                    comparison_column = np.where(dataframe == exp_data, True, False)
                    np_count=np.count_nonzero(~comparison_column)
                    if np_count==0:
                       c2.success('Answer Submitted!. You can proceed with next question')
                       random_code_qns[st.session_state.counter]['cand_ans']='correct'
                       update_cand_data(random_code_qns)
                    else:
                       c2.warning('Answer Submitted. You can proceed with next question')
                  except Exception as erc:
                     random_code_qns[st.session_state.counter]['cand_ans']='incorrect'
                     update_cand_data(random_code_qns)
                     c2.warning('Answer Submitted!. You can proceed with next question')

        except Exception as err:
            c2.caption(f"*:red[{err}]*")

        c1.text('')
        c1.text('')
        c1.text('')
    elif st.session_state.counter <0:
       st.session_state.counter=0 
    elif st.session_state.counter >9:
       st.info('You have completed all the sql coding questions. Please click below to finish')
       complete_coding_qns_btn=st.button('Finish Coding Session!',use_container_width=True)
       if complete_coding_qns_btn:
          save_final_result('secondary')
          save_final_result('primary')
          SQL=f"update cand_qn_status set coding_status='closed' where email_id='{st.session_state.email}';commit;"
          store_data(SQL)
          switch_page('Result')


try:
    code = st.experimental_get_query_params()['code'][0]
    st.session_state.email=code
except:
   print('error')

if 'email' not in st.session_state:
   st.session_state.email='null'

if st.session_state.email != 'null':
    try:
        fetch_status_sql=f"select mcq_status from cand_qn_status where email_id='{st.session_state.email}';"
        fss,fsst=fetch_data(fetch_status_sql)

        if fss[0][0] == 'closed':
            with open('cand_data/'+st.session_state.email+'_code.json', "r") as file:
                random_code_qns = json.load(file)
                CODE_PROBLEMS(random_code_qns)
        else:
            st.image('src/locked_page.png',width=200)  
            st.subheader('This Page is Locked')  
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