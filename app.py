"""
Resume Analyzer v3 — AI-Powered Career Assistant
Run: streamlit run app.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import time

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Analyzer — AI Career Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── reset ── */
*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

/* ── app background ── */
.stApp { background: #F4F4FB !important; }

/* ── hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #EBEBF5 !important;
    padding-top: 0 !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* ── sidebar nav items ── */
.nav-brand {
    display: flex; align-items: center; gap: 10px;
    padding: 22px 20px 18px 20px;
    border-bottom: 1px solid #F0F0F8;
}
.nav-brand-icon {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, #6C63FF, #9D95FF);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.nav-brand-text { font-size: 0.95rem; font-weight: 700; color: #1A1A2E; line-height: 1.2; }
.nav-brand-sub  { font-size: 0.72rem; color: #9B9BB0; font-weight: 400; }

.nav-section { padding: 16px 12px 4px 12px; }
.nav-label   { font-size: 0.68rem; font-weight: 600; color: #B0B0C8;
               text-transform: uppercase; letter-spacing: 0.08em;
               padding: 0 8px; margin-bottom: 4px; }

.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px; border-radius: 10px;
    font-size: 0.88rem; font-weight: 500; color: #5A5A7A;
    cursor: pointer; transition: all 0.15s; margin-bottom: 2px;
}
.nav-item:hover { background: #F4F4FB; color: #6C63FF; }
.nav-item.active { background: #EEF0FF; color: #6C63FF; font-weight: 600; }
.nav-item .nav-icon { font-size: 1rem; width: 20px; text-align: center; }

.nav-divider { height: 1px; background: #F0F0F8; margin: 10px 12px; }

/* ── user row ── */
.user-row {
    display: flex; align-items: center; gap: 10px;
    padding: 14px 20px; border-top: 1px solid #F0F0F8;
    position: absolute; bottom: 0; left: 0; right: 0;
    background: white;
}
.user-avatar {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, #6C63FF, #9D95FF);
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 0.9rem; flex-shrink: 0;
}
.user-name  { font-size: 0.85rem; font-weight: 600; color: #1A1A2E; }
.user-email { font-size: 0.72rem; color: #9B9BB0; }

/* ── JD input in sidebar ── */
.jd-section {
    padding: 16px 16px;
    border-top: 1px solid #F0F0F8;
    margin-top: 8px;
}
.jd-label {
    font-size: 0.78rem; font-weight: 600; color: #5A5A7A;
    text-transform: uppercase; letter-spacing: 0.06em;
    margin-bottom: 8px;
}

/* ══════════════════════════════════════
   TOPBAR
══════════════════════════════════════ */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 32px 12px 32px;
    background: white; border-bottom: 1px solid #EBEBF5;
    margin: -1rem -1rem 0 -1rem;
}
.topbar-title { font-size: 1.1rem; font-weight: 700; color: #1A1A2E; }
.topbar-right { display: flex; align-items: center; gap: 14px; }
.topbar-avatar {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, #6C63FF, #9D95FF);
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 0.9rem;
}

/* ══════════════════════════════════════
   MAIN CONTENT
══════════════════════════════════════ */
.main-content { padding: 28px 32px; }

/* ── hero text ── */
.hero-title {
    font-size: 2.2rem; font-weight: 800; color: #1A1A2E;
    text-align: center; margin-bottom: 10px; line-height: 1.2;
}
.hero-title span { color: #6C63FF; }
.hero-sub {
    text-align: center; color: #7070A0;
    font-size: 0.97rem; margin-bottom: 28px; line-height: 1.6;
}

/* ── upload box ── */
.upload-card {
    background: white; border-radius: 20px;
    padding: 40px 32px; text-align: center;
    box-shadow: 0 2px 20px rgba(108,99,255,0.08);
    margin-bottom: 16px;
}
.upload-icon-wrap {
    width: 68px; height: 68px; border-radius: 18px;
    background: #F0EEFF; margin: 0 auto 18px auto;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
}
.upload-title { font-size: 1.15rem; font-weight: 700; color: #1A1A2E; margin-bottom: 6px; }
.upload-sub   { color: #9B9BB0; font-size: 0.88rem; margin-bottom: 8px; }
.upload-or    { color: #C0C0D8; font-size: 0.85rem; margin: 10px 0; }
.upload-hint  { color: #B0B0C8; font-size: 0.78rem; margin-top: 14px; }

/* ── browse button ── */
.stButton > button {
    border-radius: 12px !important; font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6C63FF 0%, #9D95FF 100%) !important;
    color: white !important; border: none !important;
    padding: 0.6rem 2rem !important; font-size: 0.92rem !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 22px rgba(108,99,255,0.5) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: white !important; color: #6C63FF !important;
    border: 1.5px solid #6C63FF !important;
}

/* ── security note ── */
.security-note {
    text-align: center; font-size: 0.8rem; color: #B0B0C8;
    margin-top: 10px;
}

/* ── feature cards row ── */
.feature-card {
    background: white; border-radius: 16px;
    padding: 1.4rem 1rem; text-align: center;
    box-shadow: 0 2px 12px rgba(108,99,255,0.06);
    height: 100%;
}
.feature-icon {
    width: 48px; height: 48px; border-radius: 14px;
    background: #F0EEFF; margin: 0 auto 12px auto;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
}
.feature-title { font-size: 0.88rem; font-weight: 700; color: #1A1A2E; margin-bottom: 5px; }
.feature-desc  { font-size: 0.78rem; color: #9B9BB0; line-height: 1.5; }

/* ── hint bar ── */
.hint-bar {
    background: white; border-radius: 12px;
    padding: 12px 20px; margin-top: 16px;
    display: flex; align-items: center; gap: 10px;
    font-size: 0.85rem; color: #7070A0;
    box-shadow: 0 2px 8px rgba(108,99,255,0.06);
    border: 1px solid #EBEBF5;
}

/* ══════════════════════════════════════
   METRIC CARDS
══════════════════════════════════════ */
.kpi-row { display: flex; gap: 14px; margin-bottom: 20px; }
.kpi-card {
    flex: 1; background: white; border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 2px 12px rgba(108,99,255,0.06);
    border-left: 4px solid;
}
.kpi-card.purple { border-color: #6C63FF; }
.kpi-card.green  { border-color: #22C55E; }
.kpi-card.red    { border-color: #EF4444; }
.kpi-card.amber  { border-color: #F59E0B; }
.kpi-label { font-size: 0.72rem; font-weight: 600; color: #9B9BB0;
             text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.kpi-value { font-size: 1.9rem; font-weight: 800; line-height: 1; }
.kpi-card.purple .kpi-value { color: #6C63FF; }
.kpi-card.green  .kpi-value { color: #22C55E; }
.kpi-card.red    .kpi-value { color: #EF4444; }
.kpi-card.amber  .kpi-value { color: #F59E0B; }
.kpi-sub { font-size: 0.75rem; color: #B0B0C8; margin-top: 4px; }

/* ══════════════════════════════════════
   SECTION PANELS
══════════════════════════════════════ */
.panel {
    background: white; border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 12px rgba(108,99,255,0.06);
    margin-bottom: 16px;
}
.panel-title {
    font-size: 0.92rem; font-weight: 700; color: #1A1A2E;
    margin-bottom: 14px; padding-bottom: 10px;
    border-bottom: 1px solid #F0F0F8;
    display: flex; align-items: center; gap: 7px;
}

/* ── skill chips ── */
.chip-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.chip {
    display: inline-block; padding: 5px 13px;
    border-radius: 999px; font-size: 0.79rem; font-weight: 500;
}
.chip-match { background: #DCFCE7; color: #166534; border: 1px solid #86EFAC; }
.chip-miss  { background: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
.chip-all   { background: #EEF0FF; color: #4338CA; border: 1px solid #C7D2FE; }

/* ── suggestion card ── */
.sug-card {
    background: #FAFAFA; border-radius: 12px;
    padding: 12px 16px; margin-bottom: 10px;
    border-left: 4px solid; display: flex;
    gap: 12px; align-items: flex-start;
}
.sug-card.high   { border-color: #EF4444; }
.sug-card.medium { border-color: #F59E0B; }
.sug-card.low    { border-color: #22C55E; }
.sug-type { font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.07em; color: #9B9BB0; margin-bottom: 3px; }
.sug-msg  { font-size: 0.86rem; color: #3A3A5C; line-height: 1.5; }

/* ── roadmap ── */
.rm-item {
    display: flex; gap: 14px; align-items: flex-start;
    padding: 10px 0; border-bottom: 1px solid #F4F4FB;
}
.rm-item:last-child { border: none; }
.rm-week {
    background: #6C63FF; color: white; border-radius: 8px;
    padding: 3px 11px; font-size: 0.73rem; font-weight: 600;
    white-space: nowrap; flex-shrink: 0;
}
.rm-week.gap { background: #F59E0B; }
.rm-topic { font-size: 0.87rem; color: #3A3A5C; line-height: 1.5; padding-top: 2px; }

/* ── section checklist ── */
.sec-item {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 0; font-size: 0.86rem; color: #3A3A5C;
    border-bottom: 1px solid #F4F4FB;
}
.sec-item:last-child { border: none; }
.dot-ok  { width: 10px; height: 10px; border-radius: 50%;
            background: #22C55E; flex-shrink: 0; }
.dot-no  { width: 10px; height: 10px; border-radius: 50%;
            background: #EF4444; flex-shrink: 0; }

/* ── score pill ── */
.score-pill {
    display: inline-block; padding: 3px 12px;
    border-radius: 999px; font-size: 0.78rem; font-weight: 600;
}
.score-pill.good   { background: #DCFCE7; color: #166534; }
.score-pill.ok     { background: #FEF3C7; color: #92400E; }
.score-pill.bad    { background: #FEE2E2; color: #991B1B; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: white !important; border-radius: 14px !important;
    padding: 4px !important; gap: 2px !important;
    box-shadow: 0 2px 8px rgba(108,99,255,0.06) !important;
    border: 1px solid #EBEBF5 !important;
    margin-bottom: 16px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; padding: 8px 18px !important;
    font-size: 0.86rem !important; font-weight: 500 !important;
    color: #7070A0 !important; border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#6C63FF,#9D95FF) !important;
    color: white !important; font-weight: 600 !important;
}

/* ── progress bars ── */
.stProgress > div > div { background: #6C63FF !important; border-radius: 999px !important; }

/* ── file uploader override ── */
[data-testid="stFileUploadDropzone"] {
    background: #F8F7FF !important;
    border: 2px dashed #C4BFFF !important;
    border-radius: 14px !important; padding: 12px !important;
}
[data-testid="stFileUploadDropzone"] p { color: #9B9BB0 !important; font-size: 0.85rem !important; }

/* ── text area ── */
.stTextArea textarea {
    border-radius: 12px !important; border: 1.5px solid #E8E8F5 !important;
    font-size: 0.85rem !important; background: #FAFAFF !important;
}
.stTextArea textarea:focus { border-color: #6C63FF !important; box-shadow: 0 0 0 3px rgba(108,99,255,0.12) !important; }

/* ── selectbox ── */
[data-testid="stSelectbox"] > div > div {
    border-radius: 12px !important; border: 1.5px solid #E8E8F5 !important;
    background: #FAFAFF !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
from resumes.resume_parser import extract_text_from_pdf
from resumes.skill_extractor import extract_skills, extract_skills_by_category
from ats_calculator import calculate_ats_score
from resume_classifier import predict_roles
from utils.suggestions import generate_suggestions
from utils.roadmap_generator import generate_learning_roadmap
from utils.charts import (
    create_ats_gauge, create_breakdown_radar,
    create_skill_bar_chart, create_role_confidence_chart,
)
from utils.wordcloud_generator import generate_wordcloud

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"
if "dark" not in st.session_state:
    st.session_state["dark"] = False

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="nav-brand">
        <div class="nav-brand-icon">📄</div>
        <div>
            <div class="nav-brand-text">Resume Analyzer</div>
            <div class="nav-brand-sub">AI-Powered Career Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # Navigation
    pages = [
        ("📊", "Dashboard"),
        ("🕐", "History"),
        ("🔖", "Saved Reports"),
        ("⚙️", "Settings"),
        ("❓", "Help & Support"),
    ]
    for icon, page in pages:
        active = "active" if st.session_state["page"] == page else ""
        if st.button(
            f"{icon}  {page}",
            key=f"nav_{page}",
            use_container_width=True,
            type="secondary" if active else "secondary",
        ):
            st.session_state["page"] = page

    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

    # JD + Settings inside sidebar
    st.markdown("""
    <div class="jd-label" style="padding:0 8px;margin-top:8px">
        📋 Job Description
    </div>""", unsafe_allow_html=True)

    job_description = st.text_area(
        "jd",
        height=140,
        label_visibility="collapsed",
        placeholder="Paste job description here for accurate ATS scoring...\n\nExample: Looking for Python developer with ML, Django, PostgreSQL, Docker...",
        key="jd_input",
    )

    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    st.markdown("""<div class="jd-label" style="padding:0 8px;margin-top:4px">
        🎯 Target Role (for roadmap)
    </div>""", unsafe_allow_html=True)
    target_role = st.selectbox(
        "role",
        ["ML Engineer", "Data Scientist", "Frontend Developer",
         "Backend Developer", "Full Stack Developer",
         "AI / GenAI Engineer", "DevOps / Cloud Engineer"],
        label_visibility="collapsed",
    )

    # User row at bottom
    st.markdown("""
    <div style="height: 20px"></div>
    <div class="user-row">
        <div class="user-avatar">R</div>
        <div>
            <div class="user-name">Rimjhim</div>
            <div class="user-email">rimjhim27@gmail.com</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE ROUTER
# ═════════════════════════════════════════════════════════════════════════════
page = st.session_state["page"]

# ── stub pages ───────────────────────────────────────────────────────────────
if page in ("History", "Saved Reports", "Settings", "Help & Support"):
    st.markdown(f"""
    <div style="padding:60px 32px;text-align:center">
        <div style="font-size:3rem;margin-bottom:12px">
            {"🕐" if page=="History" else "🔖" if page=="Saved Reports" else "⚙️" if page=="Settings" else "❓"}
        </div>
        <div style="font-size:1.4rem;font-weight:700;color:#1A1A2E;margin-bottom:8px">{page}</div>
        <div style="color:#9B9BB0;font-size:0.92rem">This section is coming soon.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ═════════════════════════════════════════════════════════════════════════════

# ── topbar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-title">Dashboard</div>
    <div class="topbar-right">
        <span style="font-size:1.1rem;cursor:pointer">🌙</span>
        <div class="topbar-avatar">R</div>
        <span style="font-size:0.85rem;font-weight:600;color:#1A1A2E">Rimjhim ▾</span>
    </div>
</div>
<div style="height:24px"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# LANDING — no results yet
# ─────────────────────────────────────────────────────────────────────────────
def show_landing():
    # Hero
    st.markdown("""
    <div style="text-align:center;padding:0 0 20px 0">
        <div class="hero-title">Analyze. Improve. <span>Succeed.</span></div>
        <div class="hero-sub">
            Get AI-powered insights to optimize your resume,<br>
            match jobs better and accelerate your career.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload card — centered
    _, mid, _ = st.columns([0.5, 2, 0.5])
    with mid:
        st.markdown("""
        <div class="upload-card">
            <div class="upload-icon-wrap">📤</div>
            <div class="upload-title">Upload Your Resume</div>
            <div class="upload-sub">Drag & drop your PDF resume here</div>
            <div class="upload-or">or</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "upload",
            type=["pdf"],
            label_visibility="collapsed",
            key="main_upload",
        )

        if uploaded:
            st.success(f"✅ **{uploaded.name}** ready to analyze!")
            st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
            if st.button("🔍  Analyze My Resume", type="primary", use_container_width=True):
                return uploaded
        else:
            st.markdown("""
            <div class="upload-hint">PDF format only &nbsp;•&nbsp; Max size: 20MB</div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="security-note">
            🔒 &nbsp;Your data is secure and private. We never share your information.
        </div>
        """, unsafe_allow_html=True)

    # Feature cards
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("📊", "ATS Score",          "See how well your resume passes ATS systems"),
        ("🎯", "Skill Gaps",          "Identify missing skills and keywords"),
        ("👥", "Role Match",          "Get role suitability prediction"),
        ("🗺️", "Personalized Roadmap","Actionable steps to improve your profile"),
    ]
    for col, (icon, title, desc) in zip([c1,c2,c3,c4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Hint bar
    st.markdown("""
    <div class="hint-bar">
        ✨ &nbsp; Paste a job description in the left panel to get started with a more accurate analysis.
    </div>
    """, unsafe_allow_html=True)

    return None


# ─────────────────────────────────────────────────────────────────────────────
# RESULTS DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
def show_results(r):
    ats_score       = r["ats_score"]
    resume_strength = r["resume_strength"]
    matched_skills  = r["matched_skills"]
    missing_skills  = r["missing_skills"]
    skills          = r["skills"]
    skills_by_cat   = r["skills_by_cat"]
    breakdown       = r["breakdown"]
    found_sections  = r["found_sections"]
    missing_sections = r["missing_sections"]
    roles           = r["roles"]
    suggestions     = r["suggestions"]
    roadmap         = r["roadmap"]
    resume_text     = r["resume_text"]

    # ── KPI row ──────────────────────────────────────────────────────────────
    ats_col   = "purple"
    str_col   = "green" if resume_strength >= 70 else "amber" if resume_strength >= 45 else "red"
    match_col = "green"
    miss_col  = "red" if missing_skills else "green"

    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, "purple",   f"{ats_score}%",          "ATS Score",       "Weighted across 7 dimensions"),
        (c2, str_col,    f"{resume_strength}%",     "Resume Strength", "How well you match the JD"),
        (c3, match_col,  str(len(matched_skills)),  "Skills Matched",  "Found in job description"),
        (c4, miss_col,   str(len(missing_skills)),  "Skills Missing",  "Not found in your resume"),
    ]
    for col, color, val, label, sub in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card {color}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊  Overview",
        "🎯  Skills",
        "💡  Suggestions",
        "🗺️  Roadmap",
        "📝  Resume Text",
    ])

    # ── TAB 1: OVERVIEW ──────────────────────────────────────────────────────
    with tab1:
        col_l, col_r = st.columns([1, 1.5], gap="large")

        with col_l:
            # Gauge
            st.markdown('<div class="panel"><div class="panel-title">📊 ATS Score Gauge</div>', unsafe_allow_html=True)
            st.pyplot(create_ats_gauge(ats_score))
            st.markdown('</div>', unsafe_allow_html=True)

            # Section checklist
            st.markdown('<div class="panel"><div class="panel-title">📋 Resume Sections</div>', unsafe_allow_html=True)
            for s in found_sections:
                st.markdown(f'<div class="sec-item"><div class="dot-ok"></div>{s}</div>', unsafe_allow_html=True)
            for s in missing_sections:
                st.markdown(f'<div class="sec-item"><div class="dot-no"></div><span style="color:#9B9BB0">{s} (missing)</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            # Radar
            st.markdown('<div class="panel"><div class="panel-title">🎯 Score Breakdown (7 Dimensions)</div>', unsafe_allow_html=True)
            st.pyplot(create_breakdown_radar(breakdown))
            st.markdown('</div>', unsafe_allow_html=True)

            # Role predictions
            st.markdown('<div class="panel"><div class="panel-title">👥 Predicted Role Fit</div>', unsafe_allow_html=True)
            fig_role = create_role_confidence_chart(roles)
            if fig_role:
                st.pyplot(fig_role)
            st.markdown('</div>', unsafe_allow_html=True)

        # Dimension detail row
        st.markdown('<div class="panel"><div class="panel-title">📈 Dimension Scores</div>', unsafe_allow_html=True)
        dcols = st.columns(len(breakdown))
        for i, (dim, score) in enumerate(breakdown.items()):
            with dcols[i]:
                color = "#22C55E" if score >= 70 else "#F59E0B" if score >= 45 else "#EF4444"
                pill_cls = "good" if score >= 70 else "ok" if score >= 45 else "bad"
                st.markdown(f"""
                <div style="text-align:center;padding:10px 4px">
                    <div style="font-size:1.5rem;font-weight:800;color:{color}">{score}</div>
                    <div style="font-size:0.67rem;color:#9B9BB0;font-weight:600;
                    text-transform:uppercase;letter-spacing:0.05em;margin:4px 0">{dim}</div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(score)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: SKILLS ────────────────────────────────────────────────────────
    with tab2:
        fig_bar = create_skill_bar_chart(matched_skills, missing_skills)

        col_chart, col_chips = st.columns([1.3, 1], gap="large")

        with col_chart:
            if fig_bar:
                st.markdown('<div class="panel"><div class="panel-title">📊 Matched vs Missing</div>', unsafe_allow_html=True)
                st.pyplot(fig_bar)
                st.markdown('</div>', unsafe_allow_html=True)

            # Word cloud
            wc = generate_wordcloud(skills)
            if wc:
                st.markdown('<div class="panel"><div class="panel-title">☁️ Skills Word Cloud</div>', unsafe_allow_html=True)
                st.pyplot(wc)
                st.markdown('</div>', unsafe_allow_html=True)

        with col_chips:
            st.markdown('<div class="panel"><div class="panel-title">✅ Matched Skills</div>', unsafe_allow_html=True)
            if matched_skills:
                chips = "".join(f'<span class="chip chip-match">{s}</span>' for s in matched_skills)
                st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
            else:
                st.caption("No matched skills found for this JD.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="panel"><div class="panel-title">❌ Missing Skills</div>', unsafe_allow_html=True)
            if missing_skills:
                chips = "".join(f'<span class="chip chip-miss">{s}</span>' for s in missing_skills)
                st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
            else:
                st.success("🎉 Your resume covers all required skills!")
            st.markdown('</div>', unsafe_allow_html=True)

        # Skills by category
        st.markdown('<div class="panel"><div class="panel-title">🗂️ All Skills by Category</div>', unsafe_allow_html=True)
        if skills_by_cat:
            for cat, cat_skills in skills_by_cat.items():
                with st.expander(f"**{cat}** — {len(cat_skills)} skill(s)"):
                    chips = "".join(f'<span class="chip chip-all">{s}</span>' for s in cat_skills)
                    st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
        else:
            st.caption("No categorized skills found.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 3: SUGGESTIONS ───────────────────────────────────────────────────
    with tab3:
        grouped = {"high": [], "medium": [], "low": []}
        for s in suggestions:
            grouped[s["priority"]].append(s)

        priority_labels = {
            "high":   ("🔴", "High Priority"),
            "medium": ("🟡", "Medium Priority"),
            "low":    ("🟢", "Low Priority"),
        }

        for prio, (dot, label) in priority_labels.items():
            group = grouped[prio]
            if not group:
                continue
            st.markdown(f"""
            <div style="font-size:0.82rem;font-weight:700;color:#9B9BB0;
            text-transform:uppercase;letter-spacing:0.07em;
            margin:16px 0 8px 0">{dot} {label}</div>
            """, unsafe_allow_html=True)
            for s in group:
                st.markdown(f"""
                <div class="sug-card {prio}">
                    <div style="font-size:1.35rem;flex-shrink:0;margin-top:1px">{s['icon']}</div>
                    <div>
                        <div class="sug-type">{s['type']}</div>
                        <div class="sug-msg">{s['message']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 4: ROADMAP ────────────────────────────────────────────────────────
    with tab4:
        col_rm, col_role = st.columns([1.5, 1], gap="large")

        with col_rm:
            st.markdown(f'<div class="panel"><div class="panel-title">🗺️ {target_role} — 8-Week Roadmap</div>', unsafe_allow_html=True)

            if missing_skills:
                chips = "".join(f'<span class="chip chip-miss">{s}</span>' for s in missing_skills[:6])
                st.markdown(f'<div style="margin-bottom:12px"><div style="font-size:0.78rem;font-weight:600;color:#9B9BB0;margin-bottom:6px">YOUR SKILL GAPS</div><div class="chip-wrap">{chips}</div></div>', unsafe_allow_html=True)

            for item in roadmap:
                wc_cls = "gap" if item["is_skill_gap"] else ""
                st.markdown(f"""
                <div class="rm-item">
                    <span class="rm-week {wc_cls}">{item['week']}</span>
                    <span class="rm-topic">{item['topic']}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_role:
            st.markdown('<div class="panel"><div class="panel-title">👥 Role Confidence</div>', unsafe_allow_html=True)
            for role_name, conf in roles:
                color = "#22C55E" if conf >= 60 else "#F59E0B" if conf >= 30 else "#9B9BB0"
                pill_cls = "good" if conf >= 60 else "ok" if conf >= 30 else "bad"
                st.markdown(f"""
                <div style="margin-bottom:14px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px">
                        <span style="font-size:0.86rem;font-weight:600;color:#3A3A5C">{role_name}</span>
                        <span class="score-pill {pill_cls}">{conf}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(int(conf))
            st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 5: RESUME TEXT ────────────────────────────────────────────────────
    with tab5:
        wcount = len(resume_text.split())
        st.markdown(f'<div class="panel"><div class="panel-title">📝 Extracted Resume Text &nbsp;<span style="font-size:0.78rem;color:#9B9BB0;font-weight:400">{wcount} words · {len(resume_text)} chars</span></div>', unsafe_allow_html=True)
        if wcount < 100:
            st.warning("⚠️ Very little text extracted. The PDF may be image-based or scanned.")
        elif wcount < 250:
            st.info("ℹ️ Short extraction. Ensure your PDF is not scanned/image-based.")
        st.text_area("text", value=resume_text, height=420, label_visibility="collapsed", disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Re-analyze button
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    if st.button("🔄  Analyze Another Resume", type="secondary"):
        del st.session_state["results"]
        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# MAIN FLOW
# ═════════════════════════════════════════════════════════════════════════════
if "results" in st.session_state:
    show_results(st.session_state["results"])
else:
    uploaded_file = show_landing()

    if uploaded_file is not None:
        with st.spinner(""):
            prog = st.progress(0, text="📄 Extracting text from PDF...")
            resume_text = extract_text_from_pdf(uploaded_file)
            time.sleep(0.2)

            if not resume_text or len(resume_text.strip()) < 30:
                st.error("⚠️ Couldn't extract text. Please use a text-based (non-scanned) PDF.")
                st.stop()

            prog.progress(25, "🔍 Identifying skills...")
            skills = extract_skills(resume_text)
            skills_by_cat = extract_skills_by_category(resume_text)

            prog.progress(50, "🧮 Calculating ATS score...")
            jd = job_description.strip() if job_description.strip() else " ".join(skills)
            (
                ats_score, matched_skills, missing_skills,
                resume_strength, breakdown, found_sections, missing_sections
            ) = calculate_ats_score(skills, jd, resume_text)

            prog.progress(75, "🤖 Predicting roles & generating insights...")
            roles       = predict_roles(resume_text)
            suggestions = generate_suggestions(ats_score, missing_skills, resume_text, missing_sections, matched_skills)
            roadmap     = generate_learning_roadmap(target_role, missing_skills)

            prog.progress(100, "✅ Analysis complete!")
            time.sleep(0.3)
            prog.empty()

            st.session_state["results"] = dict(
                ats_score=ats_score, resume_strength=resume_strength,
                matched_skills=matched_skills, missing_skills=missing_skills,
                skills=skills, skills_by_cat=skills_by_cat,
                breakdown=breakdown, found_sections=found_sections,
                missing_sections=missing_sections, roles=roles,
                suggestions=suggestions, roadmap=roadmap,
                resume_text=resume_text,
            )
            st.rerun()
