import os

import yaml
import streamlit as st
import streamlit_authenticator as stauth
from langchain.memory import ConversationBufferMemory
from yaml.loader import SafeLoader
from dotenv import load_dotenv

from utils import generator_picture

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login(fields={'Form name': '登陆', 'Username': '用户名', 'Password': '密码',
                            'Login': '确认'})

load_dotenv()

if st.session_state["authentication_status"]:
    title, logout_button = st.columns([6, 1])
    with logout_button:
        authenticator.logout(button_name="退出", location="main")
    with title:
        st.write(f'欢迎 *{st.session_state["name"]}*')
  
    st.title("💬 克隆ChatGPT")
    # with st.sidebar:
    #     # openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    #     st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(return_memory=True)
        st.session_state["messages"] = [{"role": "ai",
                                         "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]
    
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])
    
    prompt = st.chat_input()
    
    if prompt:
        if not openai_api_key:
            st.info("请输入你的OpenAI API Key")
            st.stop()
        st.session_state["messages"].append({"role": "human", "content": prompt})
        st.chat_message("human").write(prompt)
    
        with st.spinner("AI正在思考中，请稍等..."):
            response = get_chat_response(prompt, st.session_state["memory"], openai_api_key)
        msg = {"role": "ai", "content": response}
        st.session_state["messages"].append(msg)
        st.chat_message("ai").write(response)
