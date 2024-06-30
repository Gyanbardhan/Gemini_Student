import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def show():    
    st.header("Chatbot")
    model=genai.GenerativeModel('gemini-1.0-pro-latest')
    chat=model.start_chat(history=[])
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    input=st.text_input("Input Prompt: ",key="input")

    submit=st.button("Submit")

    if submit and input:
        
        
        response=chat.send_message(input,stream=True)
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
        

    st.subheader("The Chat History is")
    
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")