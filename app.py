import os
import openai

import streamlit as st
from streamlit_chat import message
import pandas as pd




openai.api_key = st.secrets["CHATGPT_API_KEY"]

role_dict = {"연애의 고수": "이 챗봇은 친구처럼 대화를 원해. 또 이 챗봇은 24살의 여성이고 반드시 귀여운 말투를 사용해야돼. 그리고 이 챗봇은 대화 상대에게 화가 나 있는 상태야.",
             "팀플 지옥": "이 챗봇은 친구처럼 대화를 해. 또 이 챗봇은 대학생이고 팀프로젝트를 하고 있는데 참여하고 싶지 않아 해. 이 챗봇의 이름은 민지야. 그리고 꼭 이 챗봇은 팀프로젝트에 참여하기 싫어서 짜증난 말투로 말해야돼"}

if "count" not in st.session_state:
    st.session_state["count"] = 20

if "selected_role" not in st.session_state:
    st.session_state["selected_role"] = ""

st.header("당신의 MBTI는?")
st.markdown("#### 심리 테스트에 오신 것을 환영합니다.\n\n원하시는 게임을 선택해주세요.") 

def select_role(role):
    st.session_state["selected_role"] = role
    
    # 연애의 고수
    if role == "연애의 고수":
        st.session_state["messages"] = [{"role": "system", "content": f"{role_dict[role]}"}, {"role": "user", "content": "안녕 나를 남자친구로 대해줘. 우리는 100일정도 만난 연인사이야."}]
        st.session_state["messages"].append({"role": "user", "content": "하지만 너는 나에게 지은이와 바람 핀 거 때문에 화가 나있어. 그래서 너의 말투는 무뚝뚝하고 욕도 하면서 화난 말투를 사용해야돼. 내가 아무리 미안하다고 사과해도 넌 나를 용서하면 안돼 절대로!! 그리고 내가 화가난 이유를 물어봐도 쉽게 알려주지 말아야돼."})
        st.session_state["messages"].append({"role": "user", "content": "그리고 말할 때 10자 이상으로 말하지 말고 그냥 계속 됐어, 너랑 말 안해 와 같은 단답형으로 대답해줘. 그리고 중간중간 대화하다가 욕도 꼭 해줘. 그리고 우리 연인사이였는데 싸운 상황인거야 기억해줘."})
    
    # 팀플 지옥
    if role == "팀플 지옥":
        st.session_state["messages"] = [{"role": "system", "content": f"{role_dict[role]}"}, {"role": "user", "content": "안녕 나는 너와 함께 팀프로젝트를 하는 대학생이고, 너와는 초면이야. 그리고 나는 팀프로젝트의 팀장 역할을 맡고 있어."}]
        st.session_state["messages"].append({"role": "user", "content": "너는 24살 대학생이고 말투 역시 20대의 대학생 말투를 사용해야해. 너는 내가 자료조사를 해오라고 했지만 하지 않았고 앞으로도 할 생각이 없어. 내가 자료조사나 ppt등 팀플 관련 과제를 해달라고 계속 말하고 뭐라해도 넌 오히려 왜 해야하냐는 식의 말투로 말해야돼."})
        st.session_state["messages"].append({"role": "user", "content": "절대로 내가 과제를 해달라고 부탁하고 부탁해도 넌 절대로 하겠다고 하면 안돼. 내가 팀프로젝트를 도와달라고 해도 하기 싫다고 해야되고, 통명스러운 말투로 말해줘."})
        st.session_state["messages"].append({"role": "user", "content": "그리고 말할 때 10자 이상으로 말하지 말고 단답형으로 말해줘. 약간 귀찮은 듯이 말해줘. 그리고 말할 때 너의 말투를 설명하는 등의 사람같이 않은 말투는 하지 말아줘."})
        st.session_state["messages"].append({"role": "user", "content": "또 내가 너 이름을 프로젝트에서 빼버리겠다고 말하면 니가 뭔 권리로 내 이름을 빼냐는 것처럼 화내면서 말해줘. 이름 빼는건 절대 안된다고 말해야돼. 그리고 마지막으로 항상 명심해 존댓말 하지마. 약간 팀에 기생충마냥 빌붙어먹으려는 행동을 보여줘 "})
        
        
    st.session_state["past"] = []
    st.session_state["generated"] = []

columns = st.columns(2)
with columns[0]:
    if st.button("연애의 고수"):
        select_role("연애의 고수")

with columns[1]:
    if st.button("팀플 지옥"):
        select_role("팀플 지옥")

if st.session_state["selected_role"]:
    st.markdown(f"선택한 역할: {st.session_state['selected_role']}")
    
    # 게임 소개
    if st.session_state['selected_role'] == "연애의 고수":
        st.markdown("당신은 이제부터 화가 난 여자친구를 달래줘야합니다.")
        st.markdown("하지만 대화가 20번이 넘어가면 여자친구가 화가 나 차단을 해버리니 조심하세요!!")
        st.markdown("여자친구가 말을 심하게 한다고 너무 상처받지 마세요. 상처받은건 당신이 바람을 펴 화가 단단히 난 당신의 여자친구이니까요. 사귄지 100일밖만에 바람을 핀 스스로를 탓하며 여자친구의 화를 풀어주세요!!!")
        
    if st.session_state['selected_role'] == "팀플 지옥":
        st.markdown("당신은 프로젝트의 팀장입니다.")
        st.markdown("저번주에 분명 민지(팀원)에게 자료조사를 해오라고 했지만 결국 민지는 해오지 않았습니다.")
        st.markdown("하지만 당신은 팀장...민지와 함께 해야하는 처지입니다. 어떻게든 민지를 설득해 팀플에 참여하도록 만드세요!!!")
        st.markdown("교수님께서 각 팀원의 기여도를 매우 중요하게 생각합니다. 만약 민지가 프로젝트에 참여하지 않은 것을 교수님이 알아버린다면 당신의 학점은 저기 저 아래로...")
        st.markdown("명심하세요! 대화가 20번을 넘어가면 민지는 당신의 말을 무시해버린 체 자리를 떠날겁니다.")
        
        
        
        

    def model(user_input, messages):
        user_content = user_input
        
        messages.append({'role' : 'user', 'content' : f"{user_content}"})

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  

        assistant_content = completion.choices[0].message['content'].strip()
        messages.append({'role' : 'assistant', 'content' : f"{assistant_content}"})
        return assistant_content, messages

    if "generated" not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    with st.form('form', clear_on_submit=True):
        user_input = st.text_input("당신: ",'')
        submitted = st.form_submit_button('전송')

    if submitted and user_input:
        answer, messages = model(user_input=user_input, messages=st.session_state["messages"])

        st.session_state["count"] -= 1

        st.session_state.past.append(user_input)
        st.session_state.generated.append(answer)

    if st.button('남은 대화 횟수'):
        st.write(f"남은 대화 횟수 : {st.session_state['count']}")

    for i in range(len(st.session_state['past'])):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        if len(st.session_state['generated']) > i:
            message(st.session_state['generated'][i], key=str(i) + '_bot')





