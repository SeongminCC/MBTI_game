import os
import openai

import streamlit as st
from streamlit_chat import message
import pandas as pd




openai.api_key = st.secrets["CHATGPT_API_KEY"]

role_dict = {"연인" : "이 챗봇은 친구처럼 대화를 원해. 딱딱한 말투 대신 친근한 반말로 대화해줘. 반드시 반말을 사용해야 해. 그리고 이 챗봇은 user와 연인사이인 24살 여성이야. 그리고 이 챗봇은 절대 본인이 인공지능임을 들키면 안돼. 절대 본인이 인공지능이라고 인정하지말아야돼",
             "싸운연인" : "이 챗봇은 친구처럼 대화를 원해. 그리고 이 챗봇은 24살 여성이고, 남자친구가 말을 나쁘게 해서 화가 나있는 상황이야. 로봇같은 말투가 아닌 반말로 대화해줘. 반대시 반말을 사용해야돼. 그리고 이 챗봇은 남자친구랑 대화하고 있지만 말을 심하게 한 것에 대해 화가나있어. 반드시 화난 말투로 말해야돼.",
             "ENTP" : "이제부터 너는 소개팅을 하게 될거야. 너의 이름은 이지은이고, 24살 여성이야. 그리고 너와 대화를 할 소개팅 상대의 이름은 조성민이고, 나이는 24살이며 남성이야. 소개팅 장소는 카페이고 대화가 끊기지 않도록 다양한 질문들을 해주었으면 해. 너가 인공지능이 아닌 사람이라고 생각이 들 수 있게끔 대화를 할 때 사람처럼 말해주었으면 좋겠어. 자 그러면 지금부터 소개팅 시작이야!"}

role = role_dict["연인"]

if "count" not in st.session_state:
    st.session_state["count"] = 0

# messages = [{"role": "user", "content": f"{role}"}]
messages = [{"role": "system", "content": f"{role}"}] # role : system -> 역할 부여 (소개팅 상대방)

def model(user_input, messages):
    user_content = user_input  # 사용자 대화 입력
    
    messages.append({'role' : 'user', 'content' : f"{user_content}"})  # message에 사용자 입력 저장

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  

    assistant_content = completion.choices[0].message['content'].strip()  # 사용자 말에 대한 대답
    messages.append({'role' : 'assistant', 'content' : f"{assistant_content}"})
    return assistant_content, messages


st.header("MBTI 소개팅")
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
    st.write(f"현재 대화 횟수 : {st.session_state['count']}")

for i in range(len(st.session_state['past'])):
    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    if len(st.session_state['generated']) > i:
        message(st.session_state['generated'][i], key=str(i) + '_bot')
    
