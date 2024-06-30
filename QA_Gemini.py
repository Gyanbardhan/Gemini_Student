import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def show():    
    st.header("QA Gemeni")
    input=st.text_input("Input Prompt: ",key="input")

    submit=st.button("Submit")

    if submit:
        model=genai.GenerativeModel('gemini-1.0-pro-latest')
        st.subheader("The Response is")
        if input!="":
            response=model.generate_content(input)
            st.write(response.text)

        else:
            st.write("Ask a Question First!!")