import streamlit as st

from auth_service import AuthService
from ui.auth_views import render_login_page, render_signup_page
from ui_pages.home import render_home
from ui_pages.ats import render_ats
from ui_pages.interview import render_interview
from ui_pages.report import render_report
from ui.theme import load_css


def initialize_state():
    defaults = {
        "resume_text": "",
        "analysis": "",
        "interview_started": False,
        "engine": None,
        "current_question": None,
        "evaluation": "",
        "user_answer": "",
        "question_number": 1,
        "report": None,
        "ats_report": None,
        "current_page": "Dashboard",
        "interviews_completed": 0,
        "activity_log": [],
        "auth_mode": "login",
        "auth_user": None,
        "auth_guest": False,
        "auth_message": "",
        "auth_message_type": "",
        "auth_remember_me": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def push_activity(message):
    history = list(st.session_state.activity_log)
    history.insert(0, message)
    st.session_state.activity_log = history[:5]


def is_authenticated():
    return st.session_state.get("auth_user") is not None


def is_guest_mode():
    return st.session_state.get("auth_guest", False)


def navigate_to(page_name):
    """Navigation callback: safely update the current page."""
    st.session_state.current_page = page_name
    st.rerun()


def logout():
    st.session_state.auth_user = None
    st.session_state.auth_guest = False
    st.session_state.auth_message = "You have been logged out."
    st.session_state.auth_message_type = "info"
    st.session_state.auth_mode = "login"
    st.session_state.current_page = "Dashboard"
    st.rerun()


initialize_state()
auth_service = AuthService()

st.set_page_config(
    page_title="InterviewForge AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(load_css(), unsafe_allow_html=True)


if not is_authenticated() and not is_guest_mode():
    #if st.session_state.auth_message:
        #if st.session_state.auth_message_type == "success":
            #st.success(st.session_state.auth_message)
        #elif st.session_state.auth_message_type == "error":
            #st.error(st.session_state.auth_message)
        #else:
            #st.info(st.session_state.auth_message)

    if st.session_state.auth_mode == "signup":
        result = render_signup_page(auth_service)
        if result is not None:
            if result["success"]:
                st.session_state.auth_message = result["message"]
                st.session_state.auth_message_type = "success"
                st.session_state.auth_mode = "login"
                st.rerun()
            else:
                st.session_state.auth_message = result["message"]
                st.session_state.auth_message_type = "error"
                st.rerun()
    else:
        result = render_login_page(auth_service)
        if result is not None:
            if result.get("guest"):
                st.session_state.auth_guest = True
                st.session_state.auth_user = None
                st.session_state.auth_message = "Continuing as a guest."
                st.session_state.auth_message_type = "success"
                st.session_state.current_page = "Dashboard"
                st.rerun()
            elif result["success"]:
                st.session_state.auth_user = result["user"]
                st.session_state.auth_guest = False
                st.session_state.auth_message = result["message"]
                st.session_state.auth_message_type = "success"
                st.session_state.current_page = "Dashboard"
                st.session_state.auth_remember_me = result.get("remember_me", False)
                st.rerun()
            else:
                st.session_state.auth_message = result["message"]
                st.session_state.auth_message_type = "error"
                st.rerun()

    if st.session_state.auth_mode == "login":
        if st.button("Create an account", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.session_state.auth_message = ""
            st.session_state.auth_message_type = ""
            st.rerun()

        if st.button("Forgot Password", use_container_width=True):
            st.info("Password reset is coming soon. Contact support for account recovery.")
    else:
        if st.button("Already have an account? Login", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.session_state.auth_message = ""
            st.session_state.auth_message_type = ""
            st.rerun()

    st.stop()


with st.sidebar:
    st.markdown(
        """
        <div class="hero-card" style="padding: 1rem; margin-bottom: 0.8rem;">
            <div class="eyebrow">AI CAREER OS</div>
            <h3 style="margin: 0.2rem 0;">InterviewForge AI</h3>
            <p style="margin: 0; color: #94a3b8;">Premium interview prep workspace</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if is_authenticated():
        user = st.session_state.auth_user or {}
        st.markdown(
            f"""
            <div class="section-card" style="padding: 0.8rem 0.9rem; margin-bottom: 0.8rem;">
                <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.14em; color: #8b5cf6;">Signed in</div>
                <div style="font-weight: 700; margin-top: 0.25rem;">{user.get('full_name', 'User')}</div>
                <div style="color: #94a3b8; font-size: 0.9rem;">{user.get('email', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    pages = ["Dashboard", "ATS Resume", "AI Interview", "Reports", "Settings (future)"]

    for page in pages:
        icon_map = {
            "Dashboard": "🏠",
            "ATS Resume": "📄",
            "AI Interview": "🎤",
            "Reports": "📊",
            "Settings (future)": "⚙️",
        }
        icon = icon_map.get(page, "•")

        if page == "Settings (future)":
            st.button(f"{icon} {page}", use_container_width=True, disabled=True)
        elif st.button(f"{icon} {page}", use_container_width=True):
            navigate_to(page)

    if is_authenticated():
        st.divider()
        if st.button("Logout", use_container_width=True):
            logout()
    else:
        st.divider()
        st.caption("Guest mode • Secure workspace")


if st.session_state.current_page == "Dashboard":
    render_home()
elif st.session_state.current_page == "ATS Resume":
    render_ats()
elif st.session_state.current_page == "AI Interview":
    render_interview()
else:
    render_report()

st.markdown(
    """
    <div class="section-card" style="margin-top: 1.2rem; text-align: center;">
        <p style="margin: 0; color: #94a3b8;">InterviewForge AI • Designed for modern AI-native hiring workflows</p>
    </div>
    """,
    unsafe_allow_html=True,
)
