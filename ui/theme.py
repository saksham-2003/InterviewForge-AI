import html
import streamlit as st


def load_css():
    return """
    <style>
    :root {
        --bg: #060816;
        --panel: rgba(15, 23, 42, 0.92);
        --panel-soft: rgba(30, 41, 59, 0.88);
        --border: rgba(148, 163, 184, 0.18);
        --text: #f8fafc;
        --muted: #94a3b8;
        --accent: #7c3aed;
        --accent-2: #38bdf8;
        --success: #34d399;
        --warning: #f59e0b;
        --danger: #fb7185;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(124, 58, 237, 0.22), transparent 28%),
            radial-gradient(circle at bottom right, rgba(56, 189, 248, 0.16), transparent 24%),
            var(--bg);
        color: var(--text);
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.96);
        border-right: 1px solid var(--border);
        display: block !important;
        visibility: visible !important;
    }

    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stFileUploader"] {
        border: 1px dashed rgba(56, 189, 248, 0.45);
        border-radius: 18px;
        padding: 0.8rem;
        background: rgba(15, 23, 42, 0.7);
    }

    .hero-card,
    .glass-card,
    .section-card,
    .metric-card,
    .insight-card,
    .auth-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.86));
        border: 1px solid var(--border);
        border-radius: 22px;
        box-shadow: 0 18px 50px rgba(2, 6, 23, 0.28);
        backdrop-filter: blur(18px);
    }

    .auth-card {
        padding: 1.2rem 1.2rem 1rem;
        margin-bottom: 1rem;
        max-width: 560px;
    }

    .hero-card {
        padding: 1.35rem 1.4rem;
        margin-bottom: 1rem;
    }

    .hero-card h1 {
        margin: 0.2rem 0 0.25rem;
        font-size: 2rem;
        line-height: 1.15;
    }

    .hero-card p {
        color: var(--muted);
        margin: 0;
        font-size: 0.97rem;
    }

    .eyebrow {
        display: inline-block;
        padding: 0.28rem 0.62rem;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(124, 58, 237, 0.2), rgba(56, 189, 248, 0.2));
        color: #d8b4fe;
        font-size: 0.75rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    .metric-card {
        padding: 1rem 1rem 0.95rem;
        height: 100%;
    }

    .metric-card .metric-icon {
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.28), rgba(56, 189, 248, 0.22));
        margin-bottom: 0.7rem;
        font-size: 1.1rem;
    }

    .metric-card .metric-title {
        color: var(--muted);
        font-size: 0.84rem;
        margin-bottom: 0.28rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-card .metric-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--text);
    }

    .metric-card .metric-subtitle {
        color: var(--muted);
        font-size: 0.9rem;
        margin-top: 0.28rem;
    }

    .section-card {
        padding: 1rem 1.05rem;
        margin-bottom: 0.8rem;
    }

    .section-card h4,
    .section-card h5 {
        margin: 0 0 0.4rem;
    }

    .section-card p,
    .section-card li {
        color: var(--muted);
        margin: 0.2rem 0;
    }

    .insight-card {
        padding: 1rem;
        margin-bottom: 0.85rem;
    }

    .insight-card .title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        margin-bottom: 0.45rem;
        color: var(--text);
    }

    .stButton > button {
        border: none;
        border-radius: 999px;
        padding: 0.72rem 1rem;
        font-weight: 600;
        background: linear-gradient(90deg, var(--accent), var(--accent-2));
        color: white;
        box-shadow: 0 12px 24px rgba(124, 58, 237, 0.16);
        transition: transform 160ms ease, box-shadow 160ms ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 15px 28px rgba(35, 104, 235, 0.18);
    }

    .stButton > button:disabled {
        opacity: 0.65;
        cursor: not-allowed;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div > div {
        border-radius: 14px !important;
        background: rgba(15, 23, 42, 0.88);
        color: var(--text);
        border: 1px solid var(--border);
    }

    .stAlert,
    .stSuccess,
    .stWarning,
    .stInfo {
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.06);
    }

    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.8rem 0.9rem;
    }

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: visible !important;
    }
    </style>
    """


def render_page_header(title, subtitle, eyebrow="AI PRODUCT"):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="eyebrow">{html.escape(eyebrow)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(title, value, icon="✦", subtitle="", accent=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{html.escape(icon)}</div>
            <div class="metric-title">{html.escape(title)}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-subtitle">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_card(title, content, icon="•"):
    st.markdown(
        f"""
        <div class="section-card">
            <h4>{html.escape(icon)} {html.escape(title)}</h4>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_list(items, kind="info"):
    if not items:
        return
    content = "<ul>"
    for item in items:
        if item and str(item).strip():
            content += f"<li>{html.escape(str(item))}</li>"
    content += "</ul>"
    render_section_card(kind.capitalize(), content, icon="•")


def visible_items(items):
    return [item for item in items or [] if item and str(item).strip()]
