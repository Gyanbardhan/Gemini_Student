import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import Pinecone as PC
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
os.getenv("PINECONE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")


def Pine():
    from pinecone import Pinecone, ServerlessSpec

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "testing"

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
    return index_name


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    index_name = Pine()
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    docsearch = PC.from_texts([t for t in text_chunks], embedding, index_name=index_name)
    return docsearch


def showman(pdf_docs):
    st.header("Chat with PDF")

    user_question = st.text_input("Ask a Question from the PDF Files", key="user_question")
    ask_another_question = st.button("Ask Another Question",on_click=clear_text)

    if user_question and not ask_another_question:
        llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.9)
        from langchain.chains import RetrievalQA
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=st.session_state["docsearch"].as_retriever())
        response = qa(user_question)
        st.session_state["response"] = response["result"]
        st.write("Answer:", st.session_state["response"])


def clear_text():
    st.session_state["user_question"] = ""
    st.session_state["response"] = ""

def show():
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        st.session_state["pdf_docs"] = pdf_docs if pdf_docs is not None else st.session_state.get("pdf_docs", [])
        processed = st.session_state.get("processed", False)

        if not processed and pdf_docs:
            if st.button("Submit & Process"):
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    docsearch = get_vector_store(text_chunks)
                    st.session_state["docsearch"] = docsearch
                    st.session_state["processed"] = True
                st.success("Done!")
    
    showman(st.session_state["pdf_docs"])