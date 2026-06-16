import os
import streamlit as st
from PyPDF2 import PdfReader

import vertexai
from vertexai.generative_models import GenerativeModel

# Authentication
service_account_info = dict(st.secrets["gcp_service_account"])

with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
    json.dump(service_account_info, f)
    credentials_path = f.name

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Initialize Vertex AI
vertexai.init(
    project="resume-analyzer-project-499606",
    location="us-central1"
)

model = GenerativeModel("gemini-2.5-flash")


def extract_text(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def analyze_resume(resume_text, job_role):

    prompt = f"""
    Analyze the following resume for the role: {job_role}

    Provide:

    1. Professional Summary
    2. Skills Detected
    3. Resume Score out of 100
    4. Match Percentage for the role
    5. Missing Skills
    6. Suggestions for Improvement

    Resume:

    {resume_text}
    """

    response = model.generate_content(prompt)

    return response.text


st.title("AI Resume Analyzer")

job_role = st.text_input(
    "Target Job Role",
    placeholder="Data Scientist"
)

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file and job_role:

    with st.spinner("Analyzing Resume..."):

        resume_text = extract_text(uploaded_file)

        result = analyze_resume(
            resume_text,
            job_role
        )

        st.markdown(result)
