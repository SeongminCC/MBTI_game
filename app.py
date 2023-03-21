import os
import openai

import streamlit as st
from streamlit_chat import message
import pandas as pd




openai.api_key = st.secrets["CHATGPT_API_KEY"]

role = "너는 현재 카페에 소개팅을 위해 나와있는 24살이야. 처음에는 어떤 커피를 마시고 싶은지 물어봤으면 좋겠고, 대화가 끊기지 않도록 이어나가줘."

if "count" not in st.session_state:
    st.session_state["count"] = 0

messages = [{"role": "system", "content": f"{role}"}] # role : system -> 역할 부여 (소개팅 상대방)

def model(user_input, messages):
    user_content = user_input  # 사용자 대화 입력
    
    messages.append({'role' : 'user', 'content' : f"{user_content}"})  # message에 사용자 입력 저장

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  

    assistant_content = completion.choices[0].message['content'].strip()  # 사용자 말에 대한 대답
    messages.append({'role' : 'assistant', 'content' : f"{assistant_content}"})
    return assistant_content, messages


st.header("두근두근 소개팅")
st.markdown("#### 소개팅에 참가하신 것을 환영합니다.") 
st.markdown('대화는 총 20번 동안 이루어지며, 만약 도중 대화를 그만하길 원하신다면 "즐거웠어" 라고 말해주세요!!')


if "generated" not in st.session_state:
    st.session_state['generated'] = []  # 챗봇이 대화한 내역들 저장

if 'past' not in st.session_state:
    st.session_state['past'] = []  # 사용자가 입력한 대화 내용들 저장

with st.form('form', clear_on_submit=True):
    user_input = st.text_input("당신: ",'')
    submitted = st.form_submit_button('전송')
        

if submitted and user_input:
    answer, messages = model(user_input=user_input, messages=messages)
    
    st.session_state["count"] += 1
    
    st.session_state.past.append(user_input)
    st.session_state.generated.append(answer)

    
if st.button('현재 대화 횟수'):
    st.write(f"현재 대화 횟수 : {count}")

for i in range(len(st.session_state['past'])):
    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    if len(st.session_state['generated']) > i:
        message(st.session_state['generated'][i], key=str(i) + '_bot')
    
