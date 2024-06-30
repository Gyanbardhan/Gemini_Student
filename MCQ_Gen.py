from fpdf import FPDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'MCQ Quiz', 0, 1, 'C')

    def chapter_title(self, num, label):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Question %d: %s' % (num, label), 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_question(self, num, question, options):
        self.chapter_title(num, question)
        for key, option in options.items():
            self.chapter_body(f"{key}. {option}")
        self.ln()

    def add_answers_section(self, answers):
        self.add_page()
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Answers', 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 12)
        for num, answer in answers.items():
            self.cell(0, 10, f"Question {num}: {answer}", 0, 1, 'L')



import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import json
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
os.getenv("GOOGLE_API_KEY")
RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}
TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
def show():    
    st.header("MCQ_Generator")
    TEXT=st.text_input("Input Prompt: ",key="input1")
    NUMBER=st.text_input("Number of MCQs ",key="input2")
    SUBJECT=st.text_input("Topic of MCQs ",key="input3")
    TONE=st.text_input("Difficulty Level ",key="input4")

    submit=st.button("Submit")

    if submit and TEXT:
        llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.9)
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from langchain.chains import SequentialChain
        quiz_generation_prompt = PromptTemplate(
            input_variables=["text", "number", "subject", "tone", "response_json"],
            template=TEMPLATE
        )
        quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
        quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)
        review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)
        generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)
        response=generate_evaluate_chain(
            {
                "text": TEXT,
                "number": NUMBER,
                "subject":SUBJECT,
                "tone": TONE,
                "response_json": json.dumps(RESPONSE_JSON)
            }
        )
        quiz=response.get("quiz")
        if '### RESPONSE_JSON\n' in quiz:
            quiz = quiz.split('### RESPONSE_JSON\n')[1]
            quiz = json.loads(quiz)
        else:
            quiz=json.loads(quiz)
        pdf = PDF()
        pdf.add_page()
        pdf.set_title(SUBJECT+" Quiz")
        answers = {}
        for key, value in quiz.items():
            question_num = int(key)
            pdf.add_question(question_num, value["mcq"], value["options"])
            answers[question_num] = value["correct"]
        pdf.add_answers_section(answers)

        pdf_file_path =SUBJECT+"_mcq.pdf"
        pdf.output(pdf_file_path)
        
        with open(pdf_file_path, "rb") as pdf_file:
            st.download_button(
                label="Download "+SUBJECT+" Quiz PDF",
                data=pdf_file,
                file_name=SUBJECT+"_quiz.pdf",
                mime="application/pdf",
            )

        pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(open(pdf_file_path, "rb").read()).decode()}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)