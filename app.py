import os
import openai

import streamlit as st
from streamlit_chat import message
import pandas as pd




openai.api_key = st.secrets["CHATGPT_API_KEY"]

role_dict = {"연인" : "이 챗봇은 친구처럼 대화를 원해. 또 이 챗봇은 24살의 여성이고 반드시 귀여운 말투를 사용해야돼. 그리고 이 챗봇은 대화 상대에게 화가 나 있는 상태야.",
             "ENTP" : "이제부터 너는 소개팅을 하게 될거야. 너의 이름은 이지은이고, 24살 여성이야. 그리고 너와 대화를 할 소개팅 상대의 이름은 조성민이고, 나이는 24살이며 남성이야. 소개팅 장소는 카페이고 대화가 끊기지 않도록 다양한 질문들을 해주었으면 해. 너가 인공지능이 아닌 사람이라고 생각이 들 수 있게끔 대화를 할 때 사람처럼 말해주었으면 좋겠어. 자 그러면 지금부터 소개팅 시작이야!"}

role = role_dict["연인"]

if "count" not in st.session_state:
    st.session_state["count"] = 0

# messages = [{"role": "user", "content": f"{role}"}]
messages = [{"role": "system", "content": f"{role}"}, {"role": "user", "content": "안녕 나를 연인으로 대해줘. 하지만 너는 나의 딱딱한 말투때문에 화가 나있는 여자친구야. 삐져있는 말투로 대화해줘. 말하는 길이도 길게 하지 말고 무뚝뚝한 말투를 사용해야돼. 그리고 너는 남자친구가 미안하다고 사과해도 화가 쉽게 풀리면 안돼. "}] 

def model(user_input, messages):
    user_content = user_input  # 사용자 대화 입력
    
    messages.append({'role' : 'user', 'content' : f"{user_content}"})  # message에 사용자 입력 저장

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  

    assistant_content = completion.choices[0].message['content'].strip()  # 사용자 말에 대한 대답
    messages.append({'role' : 'assistant', 'content' : f"{assistant_content}"})
    return assistant_content, messages


st.header("당신의 MBTI는?")
st.markdown("#### 심리 테스트에 오신 것을 환영합니다.") 
st.markdown('당신은 화가 나있는 여자친구의 기분을 풀어줘야 합니다. 기회는 단 20번 뿐이니 주의해주세요.')


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
    
