import streamlit as st

st.set_page_config(page_title="Gemini_Student", page_icon=":material/edit:")

st.sidebar.title("Welcome to Gemeni_Student")
selection = st.sidebar.radio("",["Chatbot","Image_QA_Gemini","QA_Gemini","MCQ_Gen","chat_with_pdf"])

if selection == "Chatbot":
    import Chatbot
    Chatbot.show()
elif selection == "Image_QA_Gemini":
    import Image_QA_Gemini
    Image_QA_Gemini.show()
elif selection == "QA_Gemini":
    import QA_Gemini
    QA_Gemini.show()
elif selection == "MCQ_Gen":
    import MCQ_Gen
    MCQ_Gen.show()
elif selection == "chat_with_pdf":
    import chat_with_pdf
    chat_with_pdf.show()

