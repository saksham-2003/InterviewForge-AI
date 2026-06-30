import streamlit as st

from modules.interview_engine import InterviewEngine
from ui.theme import render_metric_card, render_page_header


def _push_activity(message):
    history = list(st.session_state.activity_log)
    history.insert(0, message)
    st.session_state.activity_log = history[:5]


def render_interview():
    render_page_header(
        "AI Interview Studio",
        "Practice technical conversations with adaptive questions tailored to your background.",
        eyebrow="INTERVIEW",
    )

    if not st.session_state.resume_text:
        st.info("Upload a resume first so the interview engine can tailor questions to your experience.")
        return

    level = st.selectbox(
        "Interview level",
        ["Graduate", "Professional", "Expert"],
        key="interview_level",
    )

    if st.button("Start Interview", use_container_width=True):
        with st.spinner("Preparing your interview..."):
            engine = InterviewEngine()
            engine.start_interview(st.session_state.resume_text, level)
            st.session_state.engine = engine
            st.session_state.current_question = engine.get_current_question()
            st.session_state.interview_started = True
            st.session_state.question_number = 1
            st.session_state.evaluation = ""
            _push_activity("Started a new interview session")
        st.success("Interview session ready")

    if st.session_state.interview_started and st.session_state.current_question:
        progress_value = min(st.session_state.question_number / 10, 1.0)
        st.progress(progress_value)

        top_left, top_right = st.columns([1.1, 0.9])
        with top_left:
            render_metric_card("Question", f"{st.session_state.question_number} / 10", icon="🎯", subtitle="Current progress")
        with top_right:
            render_metric_card("Timer", "00:00", icon="⏱️", subtitle="Session timer placeholder")

        st.markdown(
            """
            <div class="section-card">
                <h4>💬 Question</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='insight-card'><p style='margin: 0; font-size: 1.03rem;'>{st.session_state.current_question['question']}</p></div>",
            unsafe_allow_html=True,
        )

        user_answer = st.text_area(
            "Your answer",
            height=190,
            key="user_answer",
            placeholder="Share your approach, trade-offs, and reasoning.",
        )

        actions = st.columns([1, 1])
        with actions[0]:
            if st.button("Submit Answer", use_container_width=True, disabled=(user_answer.strip() == "")):
                with st.spinner("Evaluating your response..."):
                    evaluation = st.session_state.engine.submit_answer(user_answer)
                    st.session_state.evaluation = evaluation
                    _push_activity("Submitted an answer for evaluation")
                st.success("Evaluation generated")

        with actions[1]:
            if st.button("Next Question", use_container_width=True, disabled=not st.session_state.evaluation):
                next_question = st.session_state.engine.next_question()
                if next_question is None:
                    st.session_state.interview_started = False
                    st.session_state.report = st.session_state.engine.get_report()
                    st.session_state.interviews_completed += 1
                    st.session_state.evaluation = ""
                    _push_activity("Interview completed successfully")
                    st.success("Interview completed. Your report is ready.")
                else:
                    st.session_state.current_question = next_question
                    st.session_state.question_number += 1
                    st.session_state.evaluation = ""
                    st.rerun()

        if st.session_state.evaluation:
            evaluation = st.session_state.evaluation
            st.markdown(
                """
                <div class="section-card">
                    <h4>🧠 Evaluation</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            score_col, summary_col = st.columns([0.4, 1.0])
            with score_col:
                render_metric_card("Score", f"{evaluation.get('overall_score', 0)}/10", icon="⭐", subtitle="Overall performance")
            with summary_col:
                st.info(evaluation.get("summary", "No summary available yet."))

            strengths = evaluation.get("strengths", []) or []
            weaknesses = evaluation.get("weaknesses", []) or []
            improvements = evaluation.get("improvements", []) or []

            if strengths:
                st.markdown("""
                <div class="section-card">
                    <h5>Highlights</h5>
                </div>
                """, unsafe_allow_html=True)
                for item in strengths:
                    st.success(f"• {item}")

            if weaknesses:
                st.markdown("""
                <div class="section-card">
                    <h5>Watch-outs</h5>
                </div>
                """, unsafe_allow_html=True)
                for item in weaknesses:
                    st.warning(f"• {item}")

            if improvements:
                st.markdown("""
                <div class="section-card">
                    <h5>Suggested improvements</h5>
                </div>
                """, unsafe_allow_html=True)
                for item in improvements:
                    st.info(f"• {item}")
