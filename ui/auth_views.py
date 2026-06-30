import re
import streamlit as st

from auth_service import AuthService


def _render_auth_card(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="auth-card">
            <div class="eyebrow">SECURE ACCESS</div>
            <h2 style="margin:0.2rem 0;">{title}</h2>
            <p style="color:#94a3b8;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email)


# ---------------- LOGIN ---------------- #

def render_login_page(auth_service: AuthService):

    _render_auth_card(
        "Welcome back",
        "Sign in to continue your interview preparation workspace."
    )

    st.write("Outside form")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    remember_me = st.checkbox("Remember me")

    col1, col2 = st.columns(2)

    with col1:
        login = st.button(
            "Login",
            use_container_width=True
            )

    with col2:
        guest = st.button(
            "Continue as Guest",
            use_container_width=True
        )
        message_placeholder = st.empty()
        if guest:
            return {
                "success": True,
                "guest": True
            }

        if login:

            if email.strip() == "":
                message_placeholder.error("Email is required.")
                return None

            if not _valid_email(email):
                message_placeholder.error("Invalid email format.")
                return None

            if password.strip() == "":
                message_placeholder.error("Password is required.")
                return None

            result = auth_service.authenticate_user(
                email,
                password
            )

            if result["success"]:

                return {
                    "success": True,
                    "message": result["message"],
                    "user": result["user"],
                    "guest": False,
                    "remember_me": remember_me
                }

            else:

                message_placeholder.error(result["message"])

    return None


# ---------------- SIGNUP ---------------- #

def render_signup_page(auth_service: AuthService):

    _render_auth_card(
        "Create your account",
        "Join InterviewForge AI and unlock personalized prep flows."
    )

    with st.form("signup_form"):

        full_name = st.text_input("Full name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submit = st.button(
            "Create Account",
            use_container_width=True
        )
        message_placeholder = st.empty()
        if submit:

            if full_name.strip() == "":
                message_placeholder.error("Full name is required.")
                return None

            if email.strip() == "":
                message_placeholder.error("Email is required.")
                return None

            if not _valid_email(email):
                message_placeholder.error("Invalid email format.")
                return None

            if len(password) < 8:
                message_placeholder.error("Password must contain at least 8 characters.")
                return None

            if not re.search(r"[A-Z]", password):
                message_placeholder.error("Password must contain at least one uppercase letter.")
                return None

            if not re.search(r"[a-z]", password):
                message_placeholder.error("Password must contain at least one lowercase letter.")
                return None

            if not re.search(r"\d", password):
                message_placeholder.error("Password must contain at least one number.")
                return None

            if password != confirm_password:
                message_placeholder.error("Passwords do not match.")
                return None

            result = auth_service.register_user(
                full_name,
                email,
                password,
                confirm_password
            )

            if result["success"]:

                return {
                    "success": True,
                    "message": result["message"],
                    "user": result.get("user"),
                    "guest": False
                }

            else:

                message_placeholder.error(result["message"])

    return None