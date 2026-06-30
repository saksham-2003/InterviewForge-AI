def load_css():

    return """
<style>

/* Hide Streamlit default menu */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: visible !important;
}

/* Main background */

.stApp{

    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );

    color:white;
}

/* Buttons */

.stButton > button{

    width:100%;

    border-radius:12px;

    border:none;

    padding:12px;

    font-size:16px;

    font-weight:bold;

    background:#2563eb;

    color:white;

    transition:0.3s;
}

.stButton > button:hover{

    background:#1d4ed8;

    transform:scale(1.02);
}

/* Upload Box */

section[data-testid="stFileUploader"]{

    border:2px dashed #3b82f6;

    border-radius:15px;

    padding:20px;

    background:#1e293b;
}

/* Text Area */

textarea{

    border-radius:12px !important;
}

/* Metrics */

div[data-testid="metric-container"]{

    background:#1e293b;

    padding:15px;

    border-radius:15px;

    border:1px solid #334155;
}

/* Sidebar */

section[data-testid="stSidebar"]{

    background:#0f172a;
}

</style>
"""