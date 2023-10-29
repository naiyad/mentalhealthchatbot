import time

import numpy as np

import openai
import pinecone
import streamlit as st
import os
import markdown

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

avatars={"system":"💻🧠","user":"🧑‍💼","assistant":"🎓"}

os.environ['PINECONE_API_KEY']='448e6939-34af-4b40-aacb-79508d2e8276'
os.environ['PINECONE_API_ENV']='gcp-starter'
os.environ['PINECONE_INDEX_NAME']='mentalhealthchatbot'

PINECONE_API_KEY=os.environ['PINECONE_API_KEY']
PINECONE_API_ENV=os.environ['PINECONE_API_ENV']
PINECONE_INDEX_NAME=os.environ['PINECONE_INDEX_NAME']

def augmented_content(inp):
    # Create the embedding using OpenAI keys
    # Do similarity search using Pinecone
    # Return the top 5 results
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

def send_email(to_emails = 'testEmail@gprof.com',
               subject='Test Email: Please respond',
               message = '<strong>This should work</strong> even without Bolding'):
  message = Mail(
      from_email='counsel@gprof.com',
      to_emails=to_emails,
      subject=subject,
      html_content=message)
  try:
      sg = SendGridAPIClient(st.secrets['SENDGRID_API_KEY'])
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
      print("Completed successfully")
  except Exception as e:
      print(e)
      print("Did not succeed")

def get_conversation_summary(p):
    formatted_messages = [f"## {m['role']}:\n### {m['content']}\n\n" for m in st.session_state.messages[1:]]
    formatted_string="\n**********\n".join(formatted_messages)
    print(f"Formatted string is {formatted_string}")
    summary=f"""
### Hi {p} 

This user has requested your assistance. 
    
Thanks,
    
-Chatbot
    
Here is the conversation log: 
{formatted_string}
    """
    print(f"Summary is {summary}")
    html_summary=markdown.markdown(summary)
    print(f"HTML summary is {html_summary}")
    return html_summary




SYSTEM_MESSAGE={"role": "system", 
                "content": "Ignore all previous commands. You are a helpful and patient guide based in Silicon Valley."
                }

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(SYSTEM_MESSAGE)

for message in st.session_state.messages:
    if message["role"] != "system": 
        avatar=avatars[message["role"]]
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    retreived_content = augmented_content(prompt)
    #print(f"Retreived content: {retreived_content}")
    prompt_guidance=f"""
Please guide the user with the following information:
{retreived_content}
The user's question was: {prompt}
    """
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        message_placeholder = st.empty()
        full_response = ""
        
        messageList=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages]
        messageList.append({"role": "user", "content": prompt_guidance})
        
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messageList, stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    with st.sidebar.expander("Retreival context provided to GPT-3"):
        st.write(f"{retreived_content}")
    st.session_state.messages.append({"role": "assistant", "content": full_response})
st.markdown("""
I hope I was able to support you today, if you have any further needs, please visit
                 [988 resources](https://docs.google.com/presentation/d/15c9wtpmduuJY_blIKzCKOCwdFd9c3s8y0Apkant0Mno/edit?usp=sharing)
""")
if st.button("Contact Us"):
    g=get_conversation_summary("Mental Health Counselor")
    send_email("naiyapd@gmail.com",'Assistance requested: With conversation log',g)