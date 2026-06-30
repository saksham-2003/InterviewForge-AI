import streamlit as st

from modules.resume_parser import extract_text_from_pdf
from ui.theme import render_metric_card, render_page_header, visible_items


def _push_activity(message):
    history = list(st.session_state.activity_log)
    history.insert(0, message)
    st.session_state.activity_log = history[:5]


def _navigate_to(page_name):
    """Update current_page and trigger rerun."""
    st.session_state.current_page = page_name
    st.rerun()


def render_home():
    render_page_header(
        "InterviewForge AI",
        "A premium workspace for ATS optimization, AI-led interview prep, and performance insights.",
        eyebrow="DASHBOARD",
    )

    if st.session_state.resume_text:
        status_text = "Resume ready for analysis"
    else:
        status_text = "Upload a PDF to begin"

    col1, col2 = st.columns([1.35, 0.65])

    with col1:
        st.markdown(
            f"""
            <div class="glass-card" style="padding: 1rem 1.05rem; margin-bottom: 1rem;">
                <div class="eyebrow">READY TO BEGIN</div>
                <h3 style="margin: 0.2rem 0;">{status_text}</h3>
                <p style="margin: 0.2rem 0 0; color: #94a3b8;">Upload your resume, run ATS scoring, and launch a tailored interview session in one flow.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Upload your resume PDF",
            type=["pdf"],
            key="home_upload",
        )

        if uploaded_file is not None:
            with st.spinner("Extracting your resume text..."):
                st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
                st.session_state.analysis = ""
                st.session_state.ats_report = None
                _push_activity("Resume uploaded successfully")
            st.success("Resume extracted successfully")

    with col2:
        st.markdown(
            """
            <div class="insight-card">
                <div class="title">⚡ Quick Actions</div>
                <p style="margin: 0; color: #94a3b8;">Launch the next step in your prep flow.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Analyze Resume", use_container_width=True):
            if st.session_state.resume_text:
                _navigate_to("ATS Resume")
                _push_activity("Opened ATS analysis workspace")
            else:
                st.warning("Upload a resume first to unlock ATS insights.")

        if st.button("ATS Resume Score", use_container_width=True):
            if st.session_state.resume_text:
                _navigate_to("ATS Resume")
                _push_activity("Opened ATS score workspace")
            else:
                st.warning("Upload a resume first to inspect your score.")

        if st.button("Start Interview", use_container_width=True):
            if st.session_state.resume_text:
                _navigate_to("AI Interview")
                _push_activity("Started a new interview session")
            else:
                st.warning("Upload a resume first to generate tailored questions.")

    st.markdown("<div style='height: 0.35rem'></div>", unsafe_allow_html=True)

    metrics = [
        ("ATS Score", st.session_state.ats_report.get("rule_based_scores", {}).get("overall_score", "—") if st.session_state.ats_report else "—", "🎯", "Recruiter readiness"),
        ("Interview Score", f"{st.session_state.report['average_score']}/10" if st.session_state.report else "—", "🎤", "Recent interview performance"),
        ("Interviews Completed", st.session_state.interviews_completed, "🧠", "Practice sessions"),
        ("Improvement", "+12%" if st.session_state.ats_report else "—", "📈", "From your latest review"),
    ]

    cols = st.columns(4)
    for idx, (title, value, icon, subtitle) in enumerate(metrics):
        with cols[idx]:
            render_metric_card(title, value, icon=icon, subtitle=subtitle)

    st.markdown("<div style='height: 0.7rem'></div>", unsafe_allow_html=True)

    activity_col, preview_col = st.columns([1.1, 0.9])
    with activity_col:
        st.markdown("""
        <div class="section-card">
            <h4>🗂️ Recent Activity</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.activity_log:
            for item in st.session_state.activity_log:
                st.info(f"• {item}")
        else:
            st.info("Your prep history will appear here after each action.")

    with preview_col:
        st.markdown("""
        <div class="section-card">
            <h4>🧩 What you can do next</h4>
            <ul>
                <li>Run an ATS review on your latest resume.</li>
                <li>Practice with adaptive difficulty levels.</li>
                <li>Track your interview performance over time.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.8rem'></div>", unsafe_allow_html=True)
    st.caption("InterviewForge AI • Premium AI interview preparation")
