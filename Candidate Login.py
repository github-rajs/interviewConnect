import streamlit as st
import random
import json
from streamlit_extras.switch_page_button import switch_page
import time
import psycopg2
from config import DBCONN
from streamlit.source_util import _on_pages_changed, get_pages
from pathlib import Path
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


if 'btn_key' not in st.session_state: st.session_state.btn_key = 0
def btn_key(val): st.session_state.btn_key=val


@st.cache_data
def get_mcq_data():
    with open('src/mcq_basic.txt', "r") as file:
        mcq_basic_json = json.load(file)
    with open('src/mcq_advance.txt', "r") as file1:
        mcq_advance_json = json.load(file1)
    all_mcq_qn=mcq_basic_json+mcq_advance_json
    random_mcq=select_random_qns(all_mcq_qn,20)
    for i in random_mcq:
        cor_ans=i['answer']
        correct_ans_index_pos=i['options'].index(cor_ans)
        i['sel_op_index_pos']=0
        i['correct_ans_index_pos']=correct_ans_index_pos
    with open('cand_data/'+st.session_state.email+'_.json', 'w') as f:
        json.dump(random_mcq,f)
    f.close()

def greetings_based_on_time():
    current_time = datetime.now().time()
    hour = current_time.hour
    if 5 <= hour < 12:
        greeting_msg="Good Morning!"
    elif 12 <= hour < 17:
        greeting_msg="Good Afternoon!"
    elif 17 <= hour < 21:
        greeting_msg="Good Evening!"
    else:
        greeting_msg="Good Night!"
    return greeting_msg

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


def create_track_time_file():
    ct=get_current_time()
    format_json={'prev_time':'','cur_time':ct}
    fn=st.session_state.email+'_time.txt'
    with open("cand_data/time_track/"+fn, "w") as file:
        json.dump(format_json,file)
    file.close()


q1,q2,q3=st.columns([2,4,2])
w1,w2,w3=st.columns([2,4,2])
e1,e2,e3=st.columns(3)
w2=w2.empty()
q2=q2.empty()
e2=e2.empty()
e1,e2,e3=st.columns([2,4,2]) #Question and Answer



with st.sidebar:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.caption(f"""
    Ahana Systems and Solutions pvt ltd.
     <br>
     App Version 1.0
     """, unsafe_allow_html=True)




greetig_msg=greetings_based_on_time()
q2.subheader(f"{greetig_msg} Please login to get started!")
candi_form = w2.form("Enter Details")
with candi_form:
    fname=st.text_input(label='Full Name')
    phnum=st.text_input(label='Contact Number',value="+91" )
    emailid=st.text_input(label='Email',key='email')
    sb_btn=st.form_submit_button("Login",on_click=btn_key,args=(1,))
e2.text('')
if st.session_state.btn_key >0:
    st.experimental_set_query_params(code=st.session_state.email)

    if len(fname) > 3 and len(phnum) >5 and len(emailid) > 3:
        SQL="insert into candidate_info(full_name,contact_no,email_id,login_time,session_state) values('{}','{}','{}',now(),'active')".format(fname,phnum,emailid)
        status=store_data(SQL)
        check_if_closed_sql="select count(1) from candidate_info where email_id='{}' and session_state='closed';".format(emailid)
        check_if_active_sql="select count(1) from candidate_info where email_id='{}' and session_state='active';".format(emailid)
        is_closed,cs=fetch_data(check_if_closed_sql)
        is_active,cs=fetch_data(check_if_active_sql)
        if str(is_active[0][0]) == '1':
            SQL=f"insert into cand_qn_status(email_id,login_status) values('{st.session_state.email}','active');commit;"
            store_data(SQL)
            q2.success(f'Hi, {fname}!. Please read below instructions carefully!')
            w2.markdown(
            """
            `Test Format:`
            1. The test consists of three sections: Multiple Choice Questions (MCQs), Coding Exercise, and Logical Reasoning.
            2. Each section will have a separate set of instructions.
            `Time Limit:`
            1. The total duration of the test is 60 minutes.
            2. Each section will have a specified time limit.
            `Navigational Instructions:`
            1. Use the "Next" and "Previous" buttons to navigate between questions.
            2. You can skip a question and come back to it later.
            `Multiple Choice Questions (MCQs):`
            1. Select the most appropriate answer by clicking on the radio button next to the option.
            2. You can select only one answer choice for each question.
            `Coding Exercise:`
            1. Write your code in the provided coding editor.
            2. The coding language allowed is Python.
            3. Click the "Submit Code" button when you are done.
            `Logical Reasoning:`
            1. Read each scenario carefully and choose the correct option.
            2. You can select multiple answers for each question.
            `Submission Guidelines:`
            1. Once you have completed all the sections, click the "Submit Test" button to submit your responses.
            2. Ensure you have attempted and submitted all questions before the time limit expires.
            `Honesty and Integrity:`
            1. Please do not use external resources or help from others during the test.
            2. Plagiarism or cheating will result in disqualification.
            `Breaks and Pauses:`
            1. No breaks are allowed during the test. Please plan accordingly.
            `Support Contact:`
            If you encounter any technical issues or have questions related to the test, contact your interviewer.
            `Confidentiality and Data Privacy:`
            1. Your personal information and test results will be handled with strict confidentiality.
            2. We comply with all data privacy regulations.
                """
            )
            btn_2=e2.button('Lets Get Started!.',on_click=btn_key,args=(2,))
            if st.session_state.btn_key > 1:
                btn_key(0)
                progress_text = "Preparing intervew questions..Good Luck!"
                my_bar = e2.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.001)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                get_mcq_data()
                SQL=f"update cand_qn_status set login_status='closed' where email_id='{st.session_state.email}';commit;"
                store_data(SQL)
                create_track_time_file()
                time.sleep(1)
                switch_page('Multiple Choise Questions')

        elif str(is_closed[0][0]) =='1':
            e2.error('Session is already closed by {}'.format(emailid))
            e2.error('Please contact your HR to reset session')
        else:
            e2.error(status)
            e2.error('Please contact your administrator')
    else:
         e2.warning('Invalid details provided!. Please verify.')

































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