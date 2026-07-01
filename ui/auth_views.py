import re

import streamlit as st

from auth_service import AuthService


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

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


def _render_auth_message():
    """Single source of truth for session-state-driven auth feedback.

    Renders the message written by app.py (login success, logout
    confirmation, signup redirect, etc.) exactly once, then clears it so
    it is never shown on a subsequent rerun.  Field-level validation errors
    are handled separately via inline st.empty() slots and never pass
    through this function.
    """
    if st.session_state.get("auth_message"):
        message_type = st.session_state.get("auth_message_type")

        if message_type == "success":
            st.success(st.session_state.auth_message)
        elif message_type == "error":
            st.error(st.session_state.auth_message)
        else:
            st.info(st.session_state.auth_message)

        st.session_state.auth_message = ""
        st.session_state.auth_message_type = ""


def _valid_email(email: str) -> bool:
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.match(pattern, email))


# ---------------------------------------------------------------------------
# Login page
# ---------------------------------------------------------------------------

def render_login_page(auth_service: AuthService):
    """Render the login form and return a result dict or None.

    Return contracts (consumed by app.py):
      None                              — form not submitted, or field
                                          validation failed (inline errors
                                          already displayed; no rerun needed)
      {"success": True,  "guest": True} — guest login requested
      {"success": True,  "user": ..., "message": ..., "remember_me": ...}
                                        — authenticated successfully
      {"success": False, "message": ...}— authentication failed (app.py will
                                          write auth_message and rerun so
                                          _render_auth_message() shows it)
    """
    _render_auth_card(
        "Welcome back",
        "Sign in to continue your interview preparation workspace.",
    )

    # ------------------------------------------------------------------
    # Form — all inputs and submit buttons live here.
    # st.empty() slots declared immediately after each input act as
    # reserved DOM positions for field-level error messages.  They can
    # be written to after the `with` block closes because they are Python
    # objects referencing already-committed DOM slots; Streamlit updates
    # them in-place within the same rerun without a rerun being needed.
    # ------------------------------------------------------------------
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        email_err = st.empty()

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )
        password_err = st.empty()

        remember_me = st.checkbox("Remember me", key="login_remember_me")

        col1, col2 = st.columns(2)
        with col1:
            login = st.form_submit_button("Login", use_container_width=True)
        with col2:
            guest = st.form_submit_button(
                "Continue as Guest", use_container_width=True
            )

    # ------------------------------------------------------------------
    # Post-form area: one slot for below-button errors (authentication
    # failures that are not field-level), then the session-state message
    # renderer for messages written by app.py on a previous rerun.
    # ------------------------------------------------------------------
    auth_err = st.empty()
    _render_auth_message()

    # ------------------------------------------------------------------
    # Guest path — no validation required.
    # ------------------------------------------------------------------
    if guest:
        return {"success": True, "guest": True}

    # ------------------------------------------------------------------
    # Login path — field validation first, then DB authentication.
    # ------------------------------------------------------------------
    if login:
        has_error = False

        if email.strip() == "":
            email_err.error("❌ Email is required.")
            has_error = True
        elif not _valid_email(email):
            email_err.error("❌ Invalid email format.")
            has_error = True

        if password.strip() == "":
            password_err.error("❌ Password is required.")
            has_error = True

        if has_error:
            # Inline errors already written; return None so app.py does
            # not trigger a rerun (the errors are visible this pass).
            return None

        result = auth_service.authenticate_user(email, password)

        if result.get("success"):
            return {
                "success": True,
                "message": result["message"],
                "user": result["user"],
                "guest": False,
                "remember_me": remember_me,
            }

        # Authentication failed.  Write the error to the below-button
        # slot immediately (visible this rerun) AND return the failure
        # dict so app.py persists it in session_state for the rerun that
        # follows — _render_auth_message() will show it on that pass.
        # The two-pass approach ensures the message survives regardless
        # of rerun timing.
        auth_err.error("❌ Invalid email or password.")
        return {"success": False, "message": "Invalid email or password."}

    return None


# ---------------------------------------------------------------------------
# Signup page
# ---------------------------------------------------------------------------

def render_signup_page(auth_service: AuthService):
    """Render the signup form and return a result dict or None.

    Return contracts (consumed by app.py):
      None                              — form not submitted, or field
                                          validation failed (inline errors
                                          already displayed; no rerun needed)
      {"success": True,  "user": ..., "message": ..., "guest": False}
                                        — account created; app.py redirects
                                          to login with a success banner
      {"success": False, "message": ...}— unexpected DB error (app.py will
                                          write auth_message and rerun)
    """
    _render_auth_card(
        "Create your account",
        "Join InterviewForge AI and unlock personalized prep flows.",
    )

    with st.form("signup_form"):
        full_name = st.text_input("Full name", key="signup_full_name")
        full_name_err = st.empty()

        email = st.text_input("Email", key="signup_email")
        email_err = st.empty()

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password",
        )
        password_err = st.empty()

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm_password",
        )
        confirm_err = st.empty()

        submit = st.form_submit_button(
            "Create Account", use_container_width=True
        )

    # Below-button slot for unexpected DB errors; session-state renderer
    # for messages written by app.py (e.g. "logged out", redirects).
    db_err = st.empty()
    _render_auth_message()

    if not submit:
        return None

    # ------------------------------------------------------------------
    # Field-level validation — all fields checked before any DB call.
    # Multiple errors can be shown simultaneously.
    # ------------------------------------------------------------------
    has_error = False

    if full_name.strip() == "":
        full_name_err.error("❌ Full name is required.")
        has_error = True

    if email.strip() == "":
        email_err.error("❌ Email is required.")
        has_error = True
    elif not _valid_email(email):
        email_err.error("❌ Invalid email format.")
        has_error = True

    if password.strip() == "":
        password_err.error("❌ Password is required.")
        has_error = True
    else:
        if len(password) < 8:
            password_err.error("❌ Password must be at least 8 characters.")
            has_error = True
        elif not re.search(r"[A-Z]", password):
            password_err.error(
                "❌ Password must contain at least one uppercase letter."
            )
            has_error = True
        elif not re.search(r"[a-z]", password):
            password_err.error(
                "❌ Password must contain at least one lowercase letter."
            )
            has_error = True
        elif not re.search(r"\d", password):
            password_err.error("❌ Password must contain at least one digit.")
            has_error = True

    if password != confirm_password:
        confirm_err.error("❌ Passwords do not match.")
        has_error = True

    if has_error:
        return None

    # ------------------------------------------------------------------
    # DB registration — field validation passed.
    # ------------------------------------------------------------------
    try:
        result = auth_service.register_user(
            full_name, email, password, confirm_password
        )
    except Exception:
        db_err.error("❌ Database error. Please try again later.")
        return {"success": False, "message": "Database error. Please try again later."}

    if result.get("success"):
        return {
            "success": True,
            "message": result["message"],
            "user": result.get("user"),
            "guest": False,
        }

    msg = result.get("message", "An error occurred.")

    # Duplicate email — show inline under the Email field, no rerun needed.
    if "already exists" in msg.lower():
        email_err.error(f"❌ {msg}")
        return None

    # Any other service-level error — pass up to app.py for session-state
    # handling so it persists across the rerun.
    db_err.error(f"❌ {msg}")
    return {"success": False, "message": msg}