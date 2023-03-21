import os
import openai

import streamlit as st
from streamlit_chat import message
import pandas as pd




openai.api_key = st.secrets["CHATGPT_API_KEY"]

role_dict = {"연인" : "이 챗봇은 친구처럼 대화를 원해. 또 이 챗봇은 24살의 여성이고 반드시 귀여운 말투를 사용해야돼. 그리고 이 챗봇은 대화 상대에게 화가 나 있는 상태야.",
             "ENTP" : "이제부터 너는 소개팅을 하게 될거야. 너의 이름은 이지은이고, 24살 여성이야. 그리고 너와 대화를 할 소개팅 상대의 이름은 조성민이고, 나이는 24살이며 남성이야"}

role = role_dict["연인"]

if "count" not in st.session_state:
    st.session_state["count"] = 0

# messages = [{"role": "user", "content": f"{role}"}]
messages = [{"role": "system", "content": f"{role}"}, {"role": "user", "content": "안녕 나를 남자친구로 대해줘. 우리는 100일정도 만난 연인사이야."}] 
messages.append({"role": "user", "content": "하지만 너는 나에게 지은이와 바람 핀 거 때문에 화가 나있어. 그래서 너의 말투는 무뚝뚝하고 욕도 하면서 화난 말투를 사용해야돼. 내가 아무리 미안하다고 사과해도 넌 나를 용서하면 안돼 절대로!! 그리고 내가 화가난 이유를 물어봐도 쉽게 알려주지 말아야돼."})
messages.append({"role": "user", "content": "그리고 말할 때 10자 이상으로 말하지 말고 그냥 계속 됐어, 너랑 말 안해 와 같은 단답형으로 대답해줘. 그리고 중간중간 대화하다가 욕도 꼭 해줘. 그리고 우리 연인사이였는데 싸운 상황인거야 기억해줘."})
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
    
