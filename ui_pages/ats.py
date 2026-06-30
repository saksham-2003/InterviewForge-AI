import streamlit as st

from modules.ats_checker import check_ats
from modules.resume_parser import extract_text_from_pdf
from ui.theme import render_metric_card, render_page_header, visible_items


def _push_activity(message):
    history = list(st.session_state.activity_log)
    history.insert(0, message)
    st.session_state.activity_log = history[:5]


def render_ats():
    render_page_header(
        "ATS Resume Intelligence",
        "Turn your resume into a recruiter-ready profile with clear section-level insights.",
        eyebrow="ATS",
    )

    left, right = st.columns([1.3, 0.7])

    with left:
        uploaded_file = st.file_uploader(
            "Upload a resume PDF",
            type=["pdf"],
            key="ats_upload",
        )
        if uploaded_file is not None:
            with st.spinner("Extracting resume content..."):
                st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
                st.session_state.ats_report = None
                _push_activity("Resume uploaded for ATS review")
            st.success("Resume ready for analysis")

    with right:
        st.markdown(
            """
            <div class="section-card">
                <h4>🧭 ATS Focus Areas</h4>
                <p>Contact details, education, skills, projects, and experience are all scored and explained.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.resume_text:
        st.markdown("""
        <div class="section-card">
            <h4>📝 Extracted Resume Text</h4>
        </div>
        """, unsafe_allow_html=True)
        st.text_area(
            "Preview",
            st.session_state.resume_text,
            height=220,
            disabled=True,
            key="resume_preview",
        )
    else:
        st.info("Upload a resume to reveal the extracted content and ATS analysis.")

    if st.button("Run ATS Analysis", use_container_width=True):
        if not st.session_state.resume_text:
            st.warning("Upload a resume before running ATS analysis.")
        else:
            with st.spinner("Checking ATS score..."):
                st.session_state.ats_report = check_ats(st.session_state.resume_text)
                _push_activity("ATS analysis completed")
            st.success("ATS analysis completed")

    if st.session_state.ats_report:
        report = st.session_state.ats_report
        rule_scores = report.get("rule_based_scores", {})

        st.markdown("<div style='height: 0.4rem'></div>", unsafe_allow_html=True)
        cols = st.columns(6)
        with cols[0]:
            render_metric_card("Overall", f"{rule_scores.get('overall_score', 0)}/100", icon="🎯", subtitle="Overall ATS score")
        with cols[1]:
            render_metric_card("Contact", f"{rule_scores.get('contact_score', 0)}/100", icon="📇", subtitle="Contact details")
        with cols[2]:
            render_metric_card("Education", f"{rule_scores.get('education_score', 0)}/100", icon="🎓", subtitle="Education section")
        with cols[3]:
            render_metric_card("Skills", f"{rule_scores.get('skills_score', 0)}/100", icon="🛠️", subtitle="Skill coverage")
        with cols[4]:
            render_metric_card("Projects", f"{rule_scores.get('projects_score', 0)}/100", icon="📦", subtitle="Project evidence")
        with cols[5]:
            render_metric_card("Experience", f"{rule_scores.get('experience_score', 0)}/100", icon="💼", subtitle="Work history")

        strengths = visible_items(report.get("strengths", []))
        weaknesses = visible_items(report.get("missing_skills", []))
        suggestions = visible_items(report.get("suggestions", []))
        summary = report.get("summary", "")

        if strengths:
            st.markdown("""
            <div class="section-card">
                <h4>✅ Strengths</h4>
            </div>
            """, unsafe_allow_html=True)
            for item in strengths:
                st.success(f"• {item}")

        if weaknesses:
            st.markdown("""
            <div class="section-card">
                <h4>⚠️ Missing Skills</h4>
            </div>
            """, unsafe_allow_html=True)
            for item in weaknesses:
                st.warning(f"• {item}")

        if suggestions:
            st.markdown("""
            <div class="section-card">
                <h4>💡 Suggestions</h4>
            </div>
            """, unsafe_allow_html=True)
            for item in suggestions:
                st.info(f"• {item}")

        if summary:
            st.markdown("""
            <div class="section-card">
                <h4>📝 Summary</h4>
            </div>
            """, unsafe_allow_html=True)
            st.caption(summary)
