import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
from PIL import Image
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def show():    
    st.header("Image QA")
    input=st.text_input("Input Prompt: ",key="input")
    file=st.file_uploader("Chose an image...",type=["jpg","jpeg","png"])
    image=""
    if file is not None:
        image=Image.open(file)
        st.image(image)

    submit=st.button("Submit")

    if submit:
        model=genai.GenerativeModel('gemini-pro-vision')
        st.subheader("The Response is")
        if input!="":
            response=model.generate_content([input,image])
            st.write(response.text)

        else:
            response=model.generate_content(image)
            st.write(response.text)