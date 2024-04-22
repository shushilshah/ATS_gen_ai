import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = pdf.PdfReader(uploaded_file)
        text = ""

        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text
    else:
        raise FileNotFoundError("no file uploaded")


# Building APP
st.set_page_config(page_title='ATS System')
st.header("ATS System")
input_text = st.text_area('Job description', key='input')
uploaded_file = st.file_uploader("uploade resume", type=['pdf'])

if uploaded_file is not None:
    st.write("PDF uploaded succesfully")

submit1 = st.button('Tell me about resume')
# submit2 = st.button("How can I improved my skills")
submit2 = st.button("Percentage matched")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of data science, Full stack data science
data engineering and data analyst, your task is to review the provided resume against the job 
description for these profiles. Please share your professional evaluation on whether the
candidate profile aligns with description or not. Also highlight the strangth and weaknesses
 of the applicant in relation to the specified job description
"""

input_prompt2 = """
You are an skilled ATS(Application Tracking System) scanner with a deep understanding of data science, data analysis,
big data engineering, full stack data science. Your task is to evaluate the resume against the provided job description.
Give me the percentage matched the resume with job description. First, the output should come as percentage and then
keywords missing in the resume 
"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
