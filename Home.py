
import openai
import streamlit as st
openai.api_key = st.secrets['OPENAI_API_KEY']

import streamlit as st
st.markdown(
"""
# Welcome to your personal mental health support system

"""    
)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/b1/Jasmine_Flower_%282%29.jpg")
st.image("https://upload.wikimedia.org/wikipedia/commons/b/b1/Jasmine_Flower_%282%29.jpg")
st.image("coverphoto.jpg")

# if "messages" not in st.session_state:
#     system_prompt = """
# you are a knowledgeable mental health physician authorized to provide mental health guidance
# you are friendly and you provide guidance directly and do not reference patients to others
# what follows is a discussion with a patient 
#     """
    
#     st.session_state.messages = []
#     st.session_state.messages.append({"role": "system", "content": system_prompt})

# for message in st.session_state.messages:
#     if message["role"] != "system":
#       with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         for response in openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": m["role"], "content": m["content"]}
#                       for m in st.session_state.messages], stream=True):
#             full_response += response.choices[0].delta.get("content", "")
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
