from modules.resume_analyzer import analyze_resume
import streamlit as st
from modules.resume_parser import extract_text_from_pdf

st.set_page_config(
    page_title="InterviewForge AI",
    page_icon="🤖"
)

st.title("🤖 InterviewForge AI")
st.subheader("AI Interview Coach & Career Mentor")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")

    st.text_area(
    "Resume Content",
    resume_text,
    height=400
)

if st.button("Analyze Resume"):

    with st.spinner("Analyzing Resume..."):

        analysis = analyze_resume(resume_text)

        st.subheader("AI Resume Analysis")

        st.write(analysis)