from modules.interview_engine import InterviewEngine
from modules.resume_analyzer import analyze_resume
from modules.skill_extractor import extract_skills
from modules.resume_parser import extract_text_from_pdf
import streamlit as st

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = ""

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "engine" not in st.session_state:
    st.session_state.engine = None

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "evaluation" not in st.session_state:
    st.session_state.evaluation = ""

if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

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

st.subheader("Choose Your Interview Level")

level = st.selectbox(
    "Interview Level",
    [
        "Graduate",
        "Professional",
        "Expert"
    ]
)

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    st.session_state.resume_text = extract_text_from_pdf(
    uploaded_file
)

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

        analysis = analyze_resume(
          st.session_state.resume_text
       )

        st.session_state.analysis = analysis

        st.subheader("AI Resume Analysis")

        st.write(analysis)

if st.button("Start Interview"):

    with st.spinner("Preparing your interview..."):

        engine = InterviewEngine()

        engine.start_interview(
            st.session_state.resume_text
        )

        st.session_state.engine = engine

        st.session_state.current_question = (
            engine.get_current_question()
        )

        st.session_state.interview_started = True
        st.session_state.question_number = 1

if st.session_state.interview_started:

    st.progress(st.session_state.question_number / 10)

    st.markdown(
        f"### Question {st.session_state.question_number} of 10"
    )
    st.subheader("🎤 Interview Question")

    st.write(
        st.session_state.current_question["question"]
    )

    user_answer = st.text_area(
        "Your Answer",
        height=200
    )

    if st.button(
        "Submit Answer",
        disabled=(user_answer.strip() == "")
    ):

        evaluation = (
            st.session_state.engine.submit_answer(
                user_answer
            )
        )

        st.session_state.evaluation = evaluation

    if st.session_state.evaluation:

        st.subheader("AI Evaluation")

        st.write(
            st.session_state.evaluation
        )

        if st.button("Next Question"):

            next_question = (
                st.session_state.engine.next_question()
            )

            if next_question is None:

                st.session_state.interview_started = False

                st.success("🎉 Interview Completed!")

                st.balloons()

            else:

                st.session_state.current_question = next_question

                st.session_state.question_number += 1

                st.session_state.evaluation = ""

                st.rerun()