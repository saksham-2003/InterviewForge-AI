import streamlit as st

from ui.theme import render_metric_card, render_page_header


def render_report():
    render_page_header(
        "Performance Reports",
        "Review interview outcomes, ATS performance, and your strongest areas for improvement.",
        eyebrow="REPORTS",
    )

    if not st.session_state.report and not st.session_state.ats_report:
        st.info("No reports yet. Complete an ATS review or interview session to unlock your insights.")
        return

    if st.session_state.ats_report:
        report = st.session_state.ats_report
        rule_scores = report.get("rule_based_scores", {})
        st.markdown("""
        <div class="section-card">
            <h4>📄 ATS Summary</h4>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            render_metric_card("Overall ATS", f"{rule_scores.get('overall_score', 0)}/100", icon="🎯", subtitle="Recruiter readiness")
        with cols[1]:
            render_metric_card("Skills", f"{rule_scores.get('skills_score', 0)}/100", icon="🛠️", subtitle="Skill coverage")
        with cols[2]:
            render_metric_card("Experience", f"{rule_scores.get('experience_score', 0)}/100", icon="💼", subtitle="Experience evidence")
        st.caption(report.get("summary", ""))

    if st.session_state.report:
        report = st.session_state.report
        st.markdown("""
        <div class="section-card">
            <h4>🎤 Interview Summary</h4>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        with cols[0]:
            render_metric_card("Questions Answered", f"{report.get('questions_answered', 0)} / {report.get('total_questions', 0)}", icon="📝", subtitle="Responses recorded")
        with cols[1]:
            render_metric_card("Average Score", f"{report.get('average_score', 0)}/10", icon="⭐", subtitle="Mean evaluation score")
        with cols[2]:
            render_metric_card("Practice Sessions", st.session_state.interviews_completed, icon="🔁", subtitle="Completed interviews")

        evaluations = report.get("evaluations", []) or []
        scores = [item.get("overall_score", 0) for item in evaluations if isinstance(item, dict)]
        if scores:
            st.markdown("""
            <div class="section-card">
                <h5>Score Trend</h5>
            </div>
            """, unsafe_allow_html=True)
            st.bar_chart({"score": scores})

        strengths = []
        weaknesses = []
        for evaluation in evaluations:
            strengths.extend(evaluation.get("strengths", []) or [])
            weaknesses.extend(evaluation.get("weaknesses", []) or [])

        if strengths:
            st.markdown("""
            <div class="section-card">
                <h5>Strengths</h5>
            </div>
            """, unsafe_allow_html=True)
            for item in sorted(set(strengths)):
                st.success(f"• {item}")

        if weaknesses:
            st.markdown("""
            <div class="section-card">
                <h5>Areas to Improve</h5>
            </div>
            """, unsafe_allow_html=True)
            for item in sorted(set(weaknesses)):
                st.warning(f"• {item}")
