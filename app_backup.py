from modules.rag_retriever import retrieve_questions
from modules.resume_analyzer import analyze_resume
from modules.skill_extractor import extract_skills
from modules.question_generator import generate_questions
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

else:
    resume_text = ""
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

if st.button("Generate Interview Questions"):

    with st.spinner("Generating Questions..."):

        skills = extract_skills(resume_text)

        # Handle both string and list outputs
        if isinstance(skills, str):
            query = skills
        else:
            query = " ".join(skills)

        retrieved_questions = retrieve_questions(
            query
        )

        st.subheader(
            "Retrieved Questions from Knowledge Base"
        )

        st.write(
            retrieved_questions
        )

        questions = generate_questions(
            skills,
            retrieved_questions
        )

        st.subheader(
            "RAG Powered Personalized Interview Questions"
        )

        st.write(
            questions
        )