# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

import numpy as np

import streamlit as st
from streamlit.hello.utils import show_code

import time

import numpy as np

import openai
import pinecone
import streamlit as st

PINECONE_API_KEY='448e6939-34af-4b40-aacb-79508d2e8276'
PINECONE_API_ENV='gcp-starter'
PINECONE_INDEX_NAME='mentalhealthchatbot'

def augmented_content(inp):
    # Create the embedding using OpenAI keys
    # Do similarity search using Pinecone
    # Return the top 5 results
    print(f"Starting augmented content with input {inp}")
    st.write(f"Starting augmented content with input {inp}")
    embedding=openai.Embedding.create(model="text-embedding-ada-002", input=inp)['data'][0]['embedding']
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    index = pinecone.Index(PINECONE_INDEX_NAME)
    results=index.query(embedding,top_k=3,include_metadata=True)
    #print(f"Results: {results}")
    #st.write(f"Results: {results}")
    rr=[ r['metadata']['text'] for r in results['matches']]
    #print(f"RR: {rr}")
    #st.write(f"RR: {rr}")
    return rr


SYSTEM_MESSAGE={"role": "system", 
                "content": "Ignore all previous commands. You are a helpful and patient guide based in Silicon Valley."
                }

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(SYSTEM_MESSAGE)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    retreived_content = augmented_content(prompt)
    prompt_guidance=f"""
please assist the user using the information below if possible
{retreived_content}
user request is {prompt}
    """
    st.session_state.messages.append({"role": "user", "content": prompt_guidance})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        #print(f"Retreived content: {retreived_content}")
        messageList=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages]
        ##for r in retreived_content:
            ##messageList.append({"role": "assistant", "content": r})
        
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messageList, stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.write(f"Saw response:\n{full_response} for full request:\n {messageList}\n*****\n")
    st.session_state.messages.append({"role": "assistant", "content": full_response})
