# Gemini_Student

This repository contains the source code for Gemini_Student, a versatile educational application powered by the Gemini large language model. It offers five interactive components designed to enhance student learning:

[Gemini_Student_Demo Video](https://drive.google.com/file/d/1M1WT-L419ML_j43dQIyABCy8Ni79NyIq/view?usp=sharing)

[Gemini_Student Website](https://huggingface.co/spaces/gyanbardhan123/Gemeni_Student)

## Components:

### 1. Chatbot (chatbot.py):

- Employs API calls to interact with the Gemini model, providing real-time responses.
- Stores conversation history for a seamless user experience.
### 2.Image_QA_Gemini (image_qa_gemini.py):

- Accepts image input and a user prompt.
- Leverages Gemini's capabilities to generate informative answers.
### 3.QA_Gemini (qa_gemini.py):

- Functions as a straightforward question-answering platform for students.
- Interacts with Gemini to offer insightful responses to various queries.
### 4.MCQ_GEN (mcq_gen.py):

- Takes user-provided text, topic, number of MCQs, and difficulty level (easy, medium, hard) as inputs.
- Generates a PDF containing multiple-choice questions along with Gemini-verified answers, ensuring accuracy.
### 5.Chat_with_PDF (chat_with_pdf.py):

- Enables users to upload multiple PDFs.
- Utilizes the Pinecone Vector Database for efficient document retrieval.
- Allows students to ask questions directly related to the uploaded PDFs, facilitating deeper comprehension.

## Project Structure:

- The repository is organized with one Python file for each component (chatbot.py, image_qa_gemini.py, qa_gemini.py, mcq_gen.py, and chat_with_pdf.py).
- An additional Python file (app.py) serves as the main application entry point, orchestrating the overall functionality.

## Installation
To use Gemini_Student locally, clone this repository and install the required dependencies:

- git clone https://github.com/Gyanbardhan/Gemini_Student.git
- cd Gemini_Student
- pip install -r requirements.txt

## Usage
- Install streamlit using pip install streamlit 

- streamlit run app.py

## Join Us
Join us in our quest to improve the experience of students efficiently. Together, we can help users to access the application quickly, enhancing their overall experience on the platform.
