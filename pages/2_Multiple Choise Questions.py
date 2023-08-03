import streamlit as st
import random
import json
from streamlit_extras.switch_page_button import switch_page
import psycopg2
from config import DBCONN
import os
from streamlit.source_util import _on_pages_changed, get_pages
from pathlib import Path
from datetime import datetime

all_sessions=os.listdir('cand_data/')


#database related variables
host=DBCONN.host
ip=DBCONN.ip
port=DBCONN.port
user_name=DBCONN.user_name
passwd=DBCONN.passwd
database=DBCONN.database
progress_table=DBCONN.table2

def store_data(SQL):
    try:      
      connection = psycopg2.connect(user=user_name,
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
      connection = psycopg2.connect(user=user_name,
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
st.set_page_config(page_title='InterviewConnect Demo', page_icon="💻", layout="wide", initial_sidebar_state='auto', menu_items=None) 
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


st.markdown(
    """<style>
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 32px;
}
    </style>
    """, unsafe_allow_html=True)

#####################################################################################################################################################################

if 'counter' not in st.session_state: st.session_state.counter = 0
def next(): st.session_state.counter += 1
def prev(): st.session_state.counter -= 1

if 'page' not in st.session_state:
    st.session_state.page = 'page'

if 'stage1' not in st.session_state:
    st.session_state.stage1 = 0
if 'stage2' not in st.session_state:
    st.session_state.stage2 = 0
if 'stage3' not in st.session_state:
    st.session_state.stage3 = 0
def set_stage1(stage):
    st.session_state.stage1 = stage
def set_stage2(stage):
    st.session_state.stage2 = stage

if 'result_store' not in st.session_state: 
    st.session_state.result_store = 0 
def result_store(): st.session_state.result_store += 1

q1,q2,q3=st.columns([0.5,4,1])
w1,w2,w3=st.columns([0.5,4,1])
e1=st.columns(3)

q2=q2.empty()
w2=w2.empty()

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

def update_mcq_count(answered):
    q3.metric(label="Total Questions", value=len(random_mcq_qns))
    q3.metric(label="Answered", value=answered)

def update_cand_data(updated_data):
       with open('cand_data/'+str(st.session_state.email)+'_.json', "w") as file:
        json.dump(updated_data,file)
       file.close()

def fetch_prev_time():
    fn=st.session_state.email+'_time.txt'
    with open("cand_data/time_track/"+fn, "r") as file:
        time_track=json.load(file)
        tm=time_track['cur_time']
    file.close()
    return tm


@st.cache_data
def load_coding_problems():
    with open('D:/REV_ST/src/coding_problems.txt', "r") as file:
        coding_problems_json = json.load(file)
    coding_problems=select_random_qns(coding_problems_json,10)
    with open('cand_data/'+st.session_state.email+'_code.json', 'w') as f:
        json.dump(coding_problems,f)
    f.close()

def save_final_result():
   connection = psycopg2.connect(user=user_name,
                           password=passwd,
                           host=host,
                           port=port,
                           database=database)
   cursor = connection.cursor()
   with open('cand_data/'+str(st.session_state.email)+'_.json', "r") as file:
    random_mcq_qns = json.load(file)
   for inf in random_mcq_qns:
    emailID=st.session_state.email
    qns_type='mcq'
    qid=inf['qid']
    corr_op=inf['correct_ans_index_pos']
    entered_op=inf['sel_op_index_pos']
    qns_status='ans'
    qns_type_status='closed'
    SQL=f"insert into cand_int_data(email_id,qns_type,qid,entered_option,correct_option,qns_status,qns_type_status) values('{emailID}','mcq','{qid}','{entered_op}','{corr_op}','ans','closed');commit"
    cursor.execute(SQL)
    connection.commit()
   connection.close()

def MCQ(random_mcq_qns):
    if st.session_state.counter >=0 and st.session_state.counter <=19:
        with e1[1]: st.button("Next ➡️", on_click=next, use_container_width=True)
        with e1[0]: st.button("⬅️ Previous", on_click=prev, use_container_width=True)  

        cur_time=get_current_time()
        prev_time=fetch_prev_time()
        diff_time=time_difference_in_minutes(prev_time,cur_time)


        q2.text('')
        mcq_ansr=q2.radio(
        label=random_mcq_qns[st.session_state.counter]['question'], 
        options=(random_mcq_qns[st.session_state.counter]['options']),
        index=random_mcq_qns[st.session_state.counter]['sel_op_index_pos']
        )
        w1.text('')
        w1.text('')
        w1.text('')
        w1.text('')
        w1.text('')
        w1.text('')
        w1.text('')
        w2.markdown(f'Your Answer : **:red[{mcq_ansr}]**')

        update_mcq_count(st.session_state.counter+1)
        q3.subheader(f"Time : {int(diff_time)}")
        q3.caption('(minutes)')
        sel_index_pos=random_mcq_qns[st.session_state.counter]['options'].index(mcq_ansr)
        random_mcq_qns[st.session_state.counter]['sel_op_index_pos']=sel_index_pos
        update_cand_data(random_mcq_qns)

    elif st.session_state.counter >19:
        st.success('You have answered all multiple choice questions!')
        mcq_submit=e1[0].button('Submit Answers',use_container_width=True)
        cancel_button=e1[1].button('Start Again!',use_container_width=True)
        if mcq_submit:
           save_final_result()
           st.success('Result stored in database')
           load_coding_problems()
           SQL=f"update cand_qn_status set mcq_status='closed' where email_id='{st.session_state.email}';commit;"
           store_data(SQL)
           switch_page('Coding Problems')
        elif cancel_button :
           st.session_state.counter=0


    

###################################

try:
    code = st.experimental_get_query_params()['code'][0]
    st.session_state.email=code
    #st.caption(st.session_state.email)
except Exception as err:
   print(err)

if 'email' not in st.session_state:
   st.session_state.email='null'

if st.session_state.email != 'null':
    try:
        fetch_status_sql=f"select login_status from cand_qn_status where email_id='{st.session_state.email}';"
        fss,fsst=fetch_data(fetch_status_sql)

        if fss[0][0] == 'closed':
            with open('cand_data/'+st.session_state.email+'_.json', "r") as file:
                random_mcq_qns = json.load(file)
                MCQ(random_mcq_qns)
        else:
            st.text(f"Email is inavalid or not exist:{st.session_state.email}")    
    except Exception as someerr:
       st.image('src/locked_page.png',width=200)
       st.subheader('This Page is Locked') 
       st.caption(someerr)      
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