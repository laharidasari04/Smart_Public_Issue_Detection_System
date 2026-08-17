"""Smart Public Issue Detection System - Main Streamlit Application."""

import os
from datetime import datetime

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

import ai_service
import database as db
from utils import (
    format_date,
    generate_complaint_id,
    get_severity_emoji,
    get_status_emoji,
    save_uploaded_image,
    validate_image,
)

load_dotenv()

# ---------------------------------------------------------------------------
# Page config & Custom Design System
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Smart Public Issue Detection System",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --sidebar-bg: #0F172A;
        --main-bg: #F8FAFC;
        --card-bg: #FFFFFF;
        --card-border: #E2E8F0;
        --primary: #2563EB;
        --primary-hover: #1D4ED8;
        --primary-light: #EFF6FF;
        --text-main: #0F172A;
        --text-muted: #64748B;
        --border-color: #E2E8F0;
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
        --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.04);
        --shadow-md: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        --shadow-hover: 0 20px 30px -10px rgba(37, 99, 235, 0.12), 0 10px 15px -5px rgba(0, 0, 0, 0.04);
    }

    /* Global typography & layout */
    html, body, .stApp {
        background: var(--main-bg) !important;
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
        color: var(--text-main) !important;
    }

    [data-testid="stAppViewContainer"], .main .block-container {
        background: var(--main-bg) !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        max-width: 100% !important;
    }

    header[data-testid="stHeader"] { background: transparent !important; }

    /* Hide standard Streamlit header/footer noise */
    footer, #MainMenu, header[data-testid="stHeader"] > div:first-child {
        visibility: hidden;
    }

    /* ── SIDEBAR STYLING & HIGH CONTRAST FIX ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
        padding-top: 1.5rem !important;
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stCaption {
        color: #F8FAFC !important;
        -webkit-text-fill-color: #F8FAFC !important;
        opacity: 1 !important;
    }

    /* Sidebar Radio Navigation Buttons */
    [data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] [data-testid="stRadioButton"] label,
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.55rem !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] [data-testid="stRadioButton"] label p,
    [data-testid="stSidebar"] [data-testid="stRadioButton"] label span,
    [data-testid="stSidebar"] div[role="radiogroup"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] label span {
        color: #F1F5F9 !important;
        -webkit-text-fill-color: #F1F5F9 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover,
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.16) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateX(4px);
    }
    [data-testid="stSidebar"] .stRadio label:hover p,
    [data-testid="stSidebar"] .stRadio label:hover span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Active / Checked Navigation item */
    [data-testid="stSidebar"] .stRadio label[data-checked="true"],
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
    [data-testid="stSidebar"] div[role="radiogroup"] div[aria-checked="true"] label {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        border: 1px solid #60A5FA !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45) !important;
        transform: translateX(4px);
    }
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] p,
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] span,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] span,
    [data-testid="stSidebar"] div[role="radiogroup"] div[aria-checked="true"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] div[aria-checked="true"] label span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* ── MAIN CONTENT TEXT CONTRAST (EXCLUDING DARK CARDS) ── */
    [data-testid="stMain"] .stMarkdown p:not(.hero-header *):not(.ai-hud-card *),
    [data-testid="stMain"] .stMarkdown label:not(.hero-header *):not(.ai-hud-card *),
    [data-testid="stMain"] [data-testid="stWidgetLabel"] p,
    [data-testid="stMain"] [data-testid="stWidgetLabel"] label,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] p:not(.hero-header *):not(.ai-hud-card *),
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] label:not(.hero-header *):not(.ai-hud-card *),
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] span:not(.hero-header *):not(.ai-hud-card *) {
        color: var(--text-main) !important;
        -webkit-text-fill-color: var(--text-main) !important;
        opacity: 1 !important;
    }

    /* ── FORM INPUTS & SELECTBOXES ── */
    .stTextInput input, .stTextArea textarea {
        background: #FFFFFF !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-main) !important;
        -webkit-text-fill-color: var(--text-main) !important;
        padding: 0.65rem 0.9rem !important;
        font-size: 0.95rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15) !important;
    }

    [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-main) !important;
    }
    [data-testid="stMain"] .stSelectbox [data-baseweb="select"] span {
        color: var(--text-main) !important;
        -webkit-text-fill-color: var(--text-main) !important;
        font-weight: 500 !important;
    }

    /* Dropdown popover list items */
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li,
    ul[role="listbox"] li {
        background-color: #FFFFFF !important;
        color: var(--text-main) !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="menu"] li:hover {
        background-color: var(--primary-light) !important;
        color: var(--primary) !important;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        border-radius: var(--radius-md) !important;
        font-weight: 700 !important;
        font-size: 0.93rem !important;
        border: 1px solid var(--border-color) !important;
        background: #FFFFFF !important;
        color: var(--text-main) !important;
        -webkit-text-fill-color: var(--text-main) !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md) !important;
        border-color: #CBD5E1 !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"],
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.45) !important;
        transform: translateY(-2px);
    }

    /* Streamlit Bordered Container Styling */
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--card-bg) !important;
        border-radius: var(--radius-lg) !important;
        border: 1px solid var(--card-border) !important;
        padding: 1.4rem 1.6rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #F1F5F9;
        padding: 0.35rem;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-muted) !important;
        -webkit-text-fill-color: var(--text-muted) !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.2rem !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        -webkit-text-fill-color: var(--primary) !important;
        background: #FFFFFF !important;
        box-shadow: var(--shadow-sm) !important;
        font-weight: 700 !important;
    }

    /* ── CUSTOM HERO / HEADER CARD (HIGH CONTRAST FIX) ── */
    .hero-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%) !important;
        border-radius: var(--radius-lg);
        padding: 2.2rem 2.6rem;
        margin-bottom: 1.8rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 12px 32px rgba(15, 23, 42, 0.18);
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(37, 99, 235, 0.25) 0%, rgba(0, 0, 0, 0) 70%);
        pointer-events: none;
    }
    .hero-header .hero-badge,
    .hero-header .hero-badge *,
    [data-testid="stMain"] .hero-header .hero-badge,
    section.main .hero-header .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(56, 189, 248, 0.15) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        color: #38BDF8 !important;
        -webkit-text-fill-color: #38BDF8 !important;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 0.3rem 0.85rem;
        border-radius: 20px;
        margin-bottom: 0.8rem;
    }
    .hero-header h1,
    .hero-header h1 *,
    [data-testid="stMain"] .hero-header h1,
    section.main .hero-header h1 {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        margin: 0 0 0.5rem 0 !important;
        line-height: 1.25 !important;
        opacity: 1 !important;
    }
    .hero-header p,
    .hero-header p *,
    [data-testid="stMain"] .hero-header p,
    section.main .hero-header p {
        color: #CBD5E1 !important;
        -webkit-text-fill-color: #CBD5E1 !important;
        margin: 0 !important;
        font-size: 1.05rem !important;
        max-width: 800px;
        opacity: 1 !important;
    }

    /* ── STAT METRIC CARDS ── */
    .stat-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.2rem;
        margin-bottom: 1.8rem;
    }
    .stat-card {
        background: #FFFFFF;
        border-radius: var(--radius-lg);
        padding: 1.3rem 1.5rem;
        border: 1px solid var(--card-border);
        box-shadow: var(--shadow-md);
        display: flex;
        align-items: center;
        gap: 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .stat-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--card-accent, var(--primary));
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-hover);
    }
    .stat-icon {
        width: 54px;
        height: 54px;
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        flex-shrink: 0;
        background: var(--icon-bg, #EFF6FF);
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-main) !important;
        -webkit-text-fill-color: var(--text-main) !important;
        line-height: 1;
        margin-bottom: 0.25rem;
    }
    .stat-label {
        font-size: 0.85rem;
        color: var(--text-muted) !important;
        -webkit-text-fill-color: var(--text-muted) !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    /* ── CIVIC HEALTH SUMMARY BAR ── */
    .survey-bar {
        background: #FFFFFF;
        border-radius: var(--radius-lg);
        padding: 1.25rem 1.8rem;
        margin-bottom: 1.8rem;
        border: 1px solid var(--card-border);
        box-shadow: var(--shadow-md);
        display: flex;
        flex-wrap: wrap;
        gap: 2rem;
        align-items: center;
        justify-content: space-between;
    }
    .survey-title-group {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .survey-title {
        font-weight: 800;
        color: var(--text-main) !important;
        font-size: 1.1rem;
    }
    .survey-metrics {
        display: flex;
        gap: 2.2rem;
        align-items: center;
    }
    .survey-item {
        text-align: center;
    }
    .survey-item .s-val {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--primary) !important;
        line-height: 1.2;
    }
    .survey-item .s-lbl {
        font-size: 0.78rem;
        color: var(--text-muted) !important;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* ── AI VISION SCANNED CARD (HIGH CONTRAST FIX) ── */
    .ai-hud-card,
    [data-testid="stMain"] .ai-hud-card,
    section.main .ai-hud-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        border: 1px solid #3B82F6 !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25) !important;
        margin-top: 0.8rem !important;
        position: relative !important;
    }

    .ai-hud-card *,
    [data-testid="stMain"] .ai-hud-card *,
    section.main .ai-hud-card *,
    [data-testid="stMain"] .ai-hud-card p,
    section.main .ai-hud-card p,
    [data-testid="stMain"] .ai-hud-card span,
    section.main .ai-hud-card span {
        color: #F8FAFC !important;
        -webkit-text-fill-color: #F8FAFC !important;
        opacity: 1 !important;
    }

    [data-testid="stMain"] .ai-hud-card p b,
    section.main .ai-hud-card p b {
        color: #93C5FD !important;
        -webkit-text-fill-color: #93C5FD !important;
        font-weight: 700 !important;
    }

    .ai-hud-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding-bottom: 0.75rem !important;
    }

    .ai-hud-tag,
    [data-testid="stMain"] .ai-hud-tag,
    section.main .ai-hud-tag {
        background: #2563EB !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        padding: 0.35rem 1rem !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        font-weight: 800 !important;
        display: inline-block !important;
    }

    .ai-live-pulse,
    [data-testid="stMain"] .ai-live-pulse,
    section.main .ai-live-pulse {
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.4rem !important;
        font-size: 0.82rem !important;
        color: #34D399 !important;
        -webkit-text-fill-color: #34D399 !important;
        font-weight: 700 !important;
    }

    .ai-hud-body p,
    [data-testid="stMain"] .ai-hud-body p,
    section.main .ai-hud-body p {
        margin: 0.6rem 0 !important;
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
    }

    /* ── WORKFLOW STEP CARDS ── */
    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 0.8rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .workflow-step-card {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem 0.8rem;
        text-align: center;
        transition: all 0.25s ease;
        box-shadow: var(--shadow-sm);
    }
    .workflow-step-card:hover {
        transform: translateY(-3px);
        border-color: var(--primary);
        box-shadow: var(--shadow-md);
    }
    .step-badge {
        width: 30px;
        height: 30px;
        background: var(--primary-light);
        color: var(--primary) !important;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    .step-icon {
        font-size: 1.75rem;
        margin-bottom: 0.3rem;
    }
    .step-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--text-main) !important;
    }

    /* ── SIDEBAR BRANDING CARD ── */
    .sidebar-brand-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-lg);
        padding: 1.3rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .sidebar-brand-card .brand-icon {
        font-size: 2.4rem;
        margin-bottom: 0.3rem;
    }
    .sidebar-brand-card h2 {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }
    .sidebar-brand-card .brand-sub {
        color: #94A3B8 !important;
        font-size: 0.75rem !important;
        margin-top: 0.25rem !important;
    }

    .sidebar-status-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-md);
        padding: 0.6rem 0.8rem;
        text-align: center;
        margin-top: 1rem;
    }

    /* Category progress bars */
    .cat-progress-item {
        margin-bottom: 1rem;
    }
    .cat-progress-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    .cat-progress-track {
        background: #E2E8F0;
        height: 10px;
        border-radius: 6px;
        overflow: hidden;
    }
    .cat-progress-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# Plotly theme matching our visual identity
NEO_CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#0F172A", size=13),
    title_font=dict(size=16, color="#0F172A", family="Plus Jakarta Sans"),
    margin=dict(t=50, b=40, l=40, r=20),
)


def switch_page(page_name):
    """Switch active navigation page and synchronize sidebar radio widget state."""
    st.session_state.navigation_page = page_name
    st.session_state.nav_override = page_name
    st.rerun()



def dash_header(title, subtitle, badge="⚡ GENERATIVE AI · CIVIC INTELLIGENCE"):
    """Render high-impact hero header banner."""
    st.markdown(
        f'<div class="hero-header">'
        f'<div class="hero-badge">{badge}</div>'
        f'<h1>{title}</h1>'
        f'<p>{subtitle}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def stat_card_html(icon, value, label, accent_color="#2563EB", icon_bg="#EFF6FF"):
    """Return HTML for a styled KPI metric stat card."""
    return (
        f'<div class="stat-card" style="--card-accent: {accent_color};">'
        f'<div class="stat-icon" style="--icon-bg: {icon_bg};">{icon}</div>'
        f'<div>'
        f'<div class="stat-value">{value}</div>'
        f'<div class="stat-label">{label}</div>'
        f'</div></div>'
    )


def survey_summary_html(stats):
    """Render survey summary header bar."""
    total = stats.get("total", 0)
    pending = stats.get("pending", 0)
    resolved = stats.get("resolved", 0)
    status_text = "Action Required" if pending > 0 else "System Clear"
    status_color = "#F59E0B" if pending > 0 else "#10B981"

    return (
        f'<div class="survey-bar">'
        f'<div class="survey-title-group">'
        f'<span style="font-size:1.6rem;">📊</span>'
        f'<div class="survey-title">Public Issue Analytics</div>'
        f'</div>'
        f'<div class="survey-metrics">'
        f'<div class="survey-item"><div class="s-val">{total}</div><div class="s-lbl">Total Reports</div></div>'
        f'<div class="survey-item"><div class="s-val" style="color:#F59E0B!important;">{pending}</div><div class="s-lbl">Pending</div></div>'
        f'<div class="survey-item"><div class="s-val" style="color:#10B981!important;">{resolved}</div><div class="s-lbl">Resolved</div></div>'
        f'<div class="survey-item"><div class="s-val" style="color:{status_color}!important;font-size:1.15rem;">{status_text}</div><div class="s-lbl">Civic Health</div></div>'
        f'</div>'
        f'</div>'
    )


def category_progress_html(stats):
    """Render styled progress bars for category breakdown."""
    total = max(stats.get("total", 0), 1)
    palette = ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#0EA5E9", "#6366F1", "#EF4444"]

    html = '<div style="background:#FFF; padding:1.5rem; border-radius:16px; border:1px solid #E2E8F0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);">'
    html += '<p style="font-size:1.1rem; font-weight:800; color:#0F172A; margin:0 0 1.2rem 0;">Issue Category Breakdown</p>'

    for i, item in enumerate(stats.get("by_category", [])):
        pct = round(item["count"] / total * 100, 1)
        color = palette[i % len(palette)]
        html += (
            f'<div class="cat-progress-item">'
            f'<div class="cat-progress-header">'
            f'<span>{item["category"]}</span>'
            f'<span style="color:#64748B;">{item["count"]} ({pct}%)</span>'
            f'</div>'
            f'<div class="cat-progress-track">'
            f'<div class="cat-progress-fill" style="width:{pct}%; background:{color};"></div>'
            f'</div></div>'
        )
    html += '</div>'
    return html


def style_chart(fig):
    """Apply unified styling to Plotly charts."""
    fig.update_layout(**NEO_CHART_LAYOUT)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(226, 232, 240, 0.6)", zeroline=False)
    return fig


def init_session_state():
    """Initialize Streamlit session state variables."""
    defaults = {
        "ai_result": None,
        "saved_image_path": None,
        "uploaded_file_name": None,
        "admin_logged_in": False,
        "nav_override": None,
        "navigation_page": "🏠 Home",
        "last_submitted_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_report_state():
    """Clear report session state after successful submission."""
    st.session_state.ai_result = None
    st.session_state.saved_image_path = None
    st.session_state.uploaded_file_name = None


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------


def page_home():
    """Render modern Home Page."""
    dash_header(
        "Smart Public Issue Detection System",
        "Empowering citizens and municipal authorities with AI-driven infrastructure monitoring.",
    )

    try:
        stats = db.get_statistics()
    except Exception:
        stats = {"total": 0, "pending": 0, "under_review": 0, "in_progress": 0, "resolved": 0}

    st.markdown(survey_summary_html(stats), unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("📋", stats.get("total", 0), "Total Reports", "#2563EB", "#EFF6FF"),
        ("⏳", stats.get("pending", 0), "Pending Review", "#F59E0B", "#FEF3C7"),
        ("🔧", stats.get("in_progress", 0), "In Dispatch", "#8B5CF6", "#F3E8FF"),
        ("✅", stats.get("resolved", 0), "Resolved Issues", "#10B981", "#D1FAE5"),
    ]
    for col, (icon, val, label, accent, bg) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(stat_card_html(icon, val, label, accent, bg), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            '<p style="font-size:1.25rem; font-weight:800; color:#0F172A; margin-bottom:0.2rem;">'
            '🚀 System Workflow & AI Pipeline</p>'
            '<p style="color:#64748B; font-size:0.95rem; margin-bottom:1rem;">'
            'How complaints travel from citizen detection to municipal resolution.</p>',
            unsafe_allow_html=True,
        )

        steps = [
            ("1", "📸", "Upload Photo"),
            ("2", "🤖", "AI Vision Scan"),
            ("3", "🏷️", "Category ID"),
            ("4", "⚠️", "Severity Assessment"),
            ("5", "📝", "DB Registration"),
            ("6", "👨‍💼", "Admin Action"),
            ("7", "✅", "Verified Resolution"),
        ]

        steps_html = '<div class="workflow-grid">'
        for num, icon, text in steps:
            steps_html += (
                f'<div class="workflow-step-card">'
                f'<div class="step-badge">{num}</div>'
                f'<div class="step-icon">{icon}</div>'
                f'<div class="step-title">{text}</div>'
                f'</div>'
            )
        steps_html += '</div>'
        st.markdown(steps_html, unsafe_allow_html=True)

    col_cta1, col_cta2 = st.columns([2, 1])
    with col_cta1:
        if st.button("📝 Report an Infrastructure Issue Now", type="primary", use_container_width=True):
            switch_page("📝 Report Issue")
    with col_cta2:
        if st.button("📋 Track Existing Complaint", use_container_width=True):
            switch_page("📋 My Complaints")

    st.info(
        "💡 **Notice:** The AI analysis provides an initial automated assessment to assist municipal workers. "
        "All issues undergo final verification prior to ground repair."
    )


def page_report_issue():
    """Render Report Issue Page."""
    dash_header(
        "Visual Issue Analysis & Reporting",
        "Upload a photo of a public problem — our Generative AI model will analyze and categorize the issue.",
        badge="🤖 COMPUTER VISION SCANNER",
    )

    if st.session_state.get("last_submitted_id"):
        cid = st.session_state.last_submitted_id
        st.success(f"🎉 **Complaint #{cid} successfully submitted to authorities!**")
        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            if st.button("📋 Track My Complaint Now", type="primary", use_container_width=True):
                st.session_state.last_submitted_id = None
                switch_page("📋 My Complaints")
        with col_s2:
            if st.button("📝 Report Another Infrastructure Issue", use_container_width=True):
                st.session_state.last_submitted_id = None
                reset_report_state()
                st.rerun()
        st.markdown("---")

    col_form, col_upload = st.columns([1, 1])

    with col_form:
        with st.container(border=True):
            st.markdown(
                '<p style="font-size:1.15rem; font-weight:800; color:#0F172A; border-bottom:2px solid #F1F5F9; padding-bottom:0.5rem; margin-bottom:1rem;">'
                '👤 Citizen Details</p>',
                unsafe_allow_html=True,
            )
            citizen_name = st.text_input(
                "Full Name *",
                placeholder="e.g. Rahul Sharma",
                key="rep_name",
            )
            phone = st.text_input(
                "Mobile Number *",
                placeholder="10-digit mobile number (e.g. 9876543210)",
                key="rep_phone",
            )
            location = st.text_input(
                "Location / Landmark / Area *",
                placeholder="e.g. Main Road, Ward 4, Amalapuram",
                key="rep_loc",
            )
            additional_description = st.text_area(
                "Additional Details (Optional)",
                placeholder="Extra details about the defect...",
                key="rep_desc",
            )

    with col_upload:
        with st.container(border=True):
            st.markdown(
                '<p style="font-size:1.15rem; font-weight:800; color:#0F172A; border-bottom:2px solid #F1F5F9; padding-bottom:0.5rem; margin-bottom:1rem;">'
                '📷 Upload Issue Evidence Photo *</p>',
                unsafe_allow_html=True,
            )
            uploaded_file = st.file_uploader(
                "Upload Image File",
                type=["jpg", "jpeg", "png"],
                key="rep_file",
                label_visibility="collapsed",
            )

            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Evidence Photo Preview", use_container_width=True)
            else:
                st.info("💡 Upload a photo of the pothole, garbage dump, drainage leak, or damaged street light.")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 🤖 Generative AI Analysis & Complaint Dispatch")

        analyze_clicked = st.button("🔍 Run AI Vision Scan on Uploaded Image", type="primary", use_container_width=True)

        if analyze_clicked:
            if not citizen_name.strip():
                st.error("Please enter your full name.")
                return
            if not phone.strip() or len(phone.strip()) < 10:
                st.error("Please enter a valid 10-digit mobile number.")
                return
            if not location.strip():
                st.error("Please enter the issue location.")
                return
            if uploaded_file is None:
                st.error("Please upload an issue evidence photo.")
                return

            is_valid, error_msg = validate_image(uploaded_file)
            if not is_valid:
                st.error(error_msg)
                return

            with st.spinner("AI Vision is inspecting the image..."):
                try:
                    image = Image.open(uploaded_file)
                    result = ai_service.analyze_issue(image)
                    saved_path = save_uploaded_image(uploaded_file)

                    st.session_state.ai_result = result
                    st.session_state.saved_image_path = saved_path
                    st.session_state.form_data = {
                        "citizen_name": citizen_name.strip(),
                        "phone": phone.strip(),
                        "location": location.strip(),
                        "additional_description": additional_description.strip(),
                    }
                except Exception as e:
                    st.error(f"Error during AI analysis: {e}")
                    return

        if st.session_state.ai_result and "form_data" in st.session_state:
            result = st.session_state.ai_result
            if result.get("demo_mode"):
                st.warning("🟡 **Demo AI Mode Active** — using computer vision pretrained analysis.")

            col_res1, col_res2 = st.columns([1, 1])
            with col_res1:
                st.markdown("**Evidence Photo:**")
                if st.session_state.saved_image_path and os.path.exists(st.session_state.saved_image_path):
                    st.image(st.session_state.saved_image_path, use_container_width=True)
                elif uploaded_file:
                    st.image(uploaded_file, use_container_width=True)

            with col_res2:
                st.markdown(
                    f'<div class="ai-hud-card">'
                    f'<div class="ai-hud-header">'
                    f'<span class="ai-hud-tag">{result["category"]}</span>'
                    f'<span class="ai-live-pulse">🟢 Vision Inspection Complete</span>'
                    f'</div>'
                    f'<div class="ai-hud-body">'
                    f'<p><b>Severity Level:</b> {get_severity_emoji(result["severity"])}</p>'
                    f'<p><b>Detected Defect:</b> {result["description"]}</p>'
                    f'<p><b>Suggested Action:</b> {result["suggested_action"]}</p>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Confirm & Submit Complaint to Municipal Database", type="primary", use_container_width=True):
                try:
                    data = {
                        **st.session_state.form_data,
                        "image_path": st.session_state.saved_image_path,
                        "ai_category": result["category"],
                        "ai_description": result["description"],
                        "severity": result["severity"],
                        "suggested_action": result["suggested_action"],
                        "status": "Pending",
                    }
                    complaint_id = db.add_complaint(data)
                    st.session_state.last_submitted_id = complaint_id
                    reset_report_state()
                    if "form_data" in st.session_state:
                        del st.session_state.form_data
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to record complaint: {e}")


def page_my_complaints():
    """Render My Complaints Lookup Page."""
    dash_header(
        "Track Submitted Complaints",
        "View status and AI assessment of your reported public issues.",
        badge="📋 CITIZEN PORTAL",
    )

    with st.container(border=True):
        st.markdown(
            '<p style="font-size:1.1rem; font-weight:800; color:#0F172A; margin-bottom:0.5rem;">'
            '🔎 Lookup Complaints by Mobile Number</p>',
            unsafe_allow_html=True,
        )

        st.caption("Click a sample phone number to test lookup:")
        sample_cols = st.columns(4)
        sample_phones = ["9876543210", "9123456780", "9988776655", "9012345678"]
        for scol, sphone in zip(sample_cols, sample_phones):
            with scol:
                if st.button(f"📞 {sphone}", use_container_width=True):
                    st.session_state.search_phone_input = sphone
                    complaints = db.get_complaints_by_phone(sphone)
                    st.session_state.search_results = complaints
                    st.session_state.searched_phone = sphone
                    st.rerun()

        col_in, col_btn = st.columns([3, 1])
        with col_in:
            phone_val = st.text_input(
                "Mobile Number",
                value=st.session_state.get("search_phone_input", ""),
                placeholder="Enter mobile number (e.g. 9876543210)",
                key="my_comp_phone_input",
            )
        with col_btn:
            search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)

        if search_clicked:
            if not phone_val.strip():
                st.warning("Please enter a mobile number to search.")
            else:
                complaints = db.get_complaints_by_phone(phone_val.strip())
                st.session_state.search_results = complaints
                st.session_state.searched_phone = phone_val.strip()
                st.session_state.search_phone_input = phone_val.strip()

    if "search_results" in st.session_state:
        complaints = st.session_state.search_results
        phone_num = st.session_state.get("searched_phone", "")

        if not complaints:
            st.info(f"No complaint records found for mobile number **{phone_num}**.")
        else:
            st.markdown(
                f'<div style="background:#FFF; padding:1rem 1.5rem; border-radius:12px; border:1px solid #E2E8F0; margin-bottom:1.2rem;">'
                f'<span style="font-weight:700; font-size:1rem; color:#0F172A;">Found {len(complaints)} Complaint(s) registered under {phone_num}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            for c in complaints:
                with st.container(border=True):
                    head_col1, head_col2 = st.columns([3, 1])
                    with head_col1:
                        st.markdown(f"### Complaint ID {generate_complaint_id(c['id'])}")
                    with head_col2:
                        st.markdown(f"**Status:** {get_status_emoji(c['status'])}")

                    col_img, col_info = st.columns([1, 2])
                    with col_img:
                        if c["image_path"] and os.path.exists(c["image_path"]):
                            st.image(c["image_path"], caption="Uploaded Evidence Photo", use_container_width=True)
                        else:
                            st.info("📸 Photo not available")

                    with col_info:
                        st.write(f"**Issue Category:** {c['ai_category']}")
                        st.write(f"**Location:** 📍 {c['location']}")
                        st.write(f"**Severity Level:** {get_severity_emoji(c['severity'])}")
                        st.write(f"**Submitted Date:** {format_date(c['created_at'])}")
                        st.write(f"**AI Vision Assessment:** {c['ai_description']}")
                        st.write(f"**Suggested Action:** {c['suggested_action']}")


def page_admin_dashboard():
    """Render Admin Dashboard Page."""
    dash_header(
        "Administrator Command Dashboard",
        "Comprehensive analytics, complaint management, and authority action portal.",
        badge="📊 MUNICIPAL MONITORING TERMINAL",
    )

    if not st.session_state.admin_logged_in:
        with st.container(border=True):
            st.markdown(
                '<p style="font-size:1.2rem; font-weight:800; color:#0F172A; margin-bottom:0.5rem;">'
                '🔒 Administrator Authentication Required</p>',
                unsafe_allow_html=True,
            )
            password = st.text_input("Enter Admin Password", type="password", key="admin_pwd_input")
            if st.button("Unlock Admin Terminal", type="primary", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")
        return

    # Top Admin Control Toolbar
    top_col1, top_col2, top_col3 = st.columns([3, 1.5, 1])
    with top_col1:
        st.success("Authenticated as **Municipal Administrator**")
    with top_col2:
        if st.button("📥 Insert Sample Data"):
            count = db.insert_sample_data()
            if count > 0:
                st.success(f"Inserted {count} sample complaints!")
                st.rerun()
            else:
                st.info("Sample complaints already present.")
    with top_col3:
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

    try:
        stats = db.get_statistics()
        all_complaints = db.get_all_complaints()
    except Exception as e:
        st.error(f"Database read error: {e}")
        return

    st.markdown(survey_summary_html(stats), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 KPI Overview", "📈 Visual Analytics", "📋 All Records", "⚙️ Dispatch & Manage"
    ])

    with tab1:
        c1, c2, c3, c4, c5 = st.columns(5)
        kpis = [
            ("📋", stats.get("total", 0), "Total", "#2563EB", "#EFF6FF"),
            ("⏳", stats.get("pending", 0), "Pending", "#F59E0B", "#FEF3C7"),
            ("🔍", stats.get("under_review", 0), "Under Review", "#0EA5E9", "#E0F2FE"),
            ("🔧", stats.get("in_progress", 0), "In Progress", "#8B5CF6", "#F3E8FF"),
            ("✅", stats.get("resolved", 0), "Resolved", "#10B981", "#D1FAE5"),
        ]
        for col, (icon, val, label, accent, bg) in zip([c1, c2, c3, c4, c5], kpis):
            with col:
                st.markdown(stat_card_html(icon, val, label, accent, bg), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⏱️ Latest Submitted Complaints")
        recent = all_complaints[:8]
        if recent:
            st.dataframe(
                [
                    {
                        "ID": f"#{c['id']}",
                        "Citizen": c["citizen_name"],
                        "Category": c["ai_category"],
                        "Location": c["location"],
                        "Severity": c["severity"],
                        "Status": c["status"],
                        "Date": format_date(c["created_at"]),
                    }
                    for c in recent
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No complaints found in database.")

    with tab2:
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            if stats["by_category"]:
                fig_cat = px.bar(
                    x=[i["category"] for i in stats["by_category"]],
                    y=[i["count"] for i in stats["by_category"]],
                    labels={"x": "Issue Category", "y": "Complaint Count"},
                    title="Complaints by Category",
                    color=[i["count"] for i in stats["by_category"]],
                    color_continuous_scale=["#3B82F6", "#1D4ED8"],
                )
                fig_cat.update_layout(showlegend=False, xaxis_tickangle=-35)
                st.plotly_chart(style_chart(fig_cat), use_container_width=True)

        with col_chart2:
            if stats["by_status"]:
                fig_pie = px.pie(
                    names=[i["status"] for i in stats["by_status"]],
                    values=[i["count"] for i in stats["by_status"]],
                    title="Status Breakdown",
                    hole=0.45,
                    color_discrete_sequence=["#F59E0B", "#0EA5E9", "#8B5CF6", "#10B981"],
                )
                st.plotly_chart(style_chart(fig_pie), use_container_width=True)

        st.markdown(category_progress_html(stats), unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🔎 Filter & Search Complaints")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            filter_cat = st.selectbox("Category", ["All"] + db.CATEGORIES, key="f_cat")
        with f2:
            filter_sev = st.selectbox("Severity", ["All", "Low", "Medium", "High"], key="f_sev")
        with f3:
            filter_stat = st.selectbox("Status", ["All"] + db.VALID_STATUSES, key="f_stat")
        with f4:
            search_loc = st.text_input("Location Search", placeholder="e.g. Main Road", key="f_loc")

        filtered = all_complaints
        if filter_cat != "All":
            filtered = [c for c in filtered if c["ai_category"] == filter_cat]
        if filter_sev != "All":
            filtered = [c for c in filtered if c["severity"] == filter_sev]
        if filter_stat != "All":
            filtered = [c for c in filtered if c["status"] == filter_stat]
        if search_loc.strip():
            loc_lower = search_loc.strip().lower()
            filtered = [c for c in filtered if loc_lower in c["location"].lower()]

        if filtered:
            st.dataframe(
                [
                    {
                        "ID": f"#{c['id']}",
                        "Citizen": c["citizen_name"],
                        "Phone": c["phone"],
                        "Category": c["ai_category"],
                        "Location": c["location"],
                        "Severity": c["severity"],
                        "Status": c["status"],
                        "Date": format_date(c["created_at"]),
                    }
                    for c in filtered
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No complaints match the specified filter criteria.")

    with tab4:
        if not all_complaints:
            st.info("No complaints to manage.")
            return

        selected_id = st.selectbox(
            "Select Complaint Record ID to Modify",
            [c["id"] for c in all_complaints],
            format_func=lambda x: f"Complaint #{x}",
            key="admin_select_cid",
        )
        complaint = db.get_complaint_by_id(selected_id)
        if not complaint:
            st.error("Selected complaint not found.")
            return

        with st.container(border=True):
            c_det1, c_det2 = st.columns([1, 2])
            with c_det1:
                if complaint["image_path"] and os.path.exists(complaint["image_path"]):
                    st.image(complaint["image_path"], caption="Evidence Image", use_container_width=True)
                else:
                    st.info("📸 Photo not available on disk")

            with c_det2:
                st.markdown(f"### Complaint #{complaint['id']}")
                st.write(f"**Citizen:** {complaint['citizen_name']} ({complaint['phone']})")
                st.write(f"**Location:** 📍 {complaint['location']}")
                st.write(f"**Category:** {complaint['ai_category']}")
                st.write(f"**Severity:** {get_severity_emoji(complaint['severity'])}")
                st.write(f"**Current Status:** {get_status_emoji(complaint['status'])}")
                st.write(f"**AI Description:** {complaint['ai_description']}")
                st.write(f"**Suggested Action:** {complaint['suggested_action']}")
                st.write(f"**Registered On:** {format_date(complaint['created_at'])}")

        st.markdown("#### Update Status & Dispatch Workflow")
        col_stat, col_stat_btn = st.columns([3, 1])
        with col_stat:
            new_status = st.selectbox(
                "New Status",
                db.VALID_STATUSES,
                index=db.VALID_STATUSES.index(complaint["status"]),
                label_visibility="collapsed",
                key="admin_update_status_select",
            )
        with col_stat_btn:
            if st.button("Update Status", type="primary", use_container_width=True):
                if db.update_status(selected_id, new_status):
                    st.success("Complaint status updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update status.")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🗑️ Delete Complaint Record"):
            st.warning("⚠️ Deleting a complaint permanently erases the record and associated uploaded files.")
            confirm_del = st.checkbox(f"Confirm deletion of Complaint #{selected_id}", key="admin_del_confirm")
            if st.button("Delete Complaint", type="primary"):
                if not confirm_del:
                    st.error("Please check the confirmation box first.")
                elif db.delete_complaint(selected_id):
                    st.success("Complaint record deleted!")
                    st.rerun()
                else:
                    st.error("Deletion failed.")


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------


def main():
    """Main Streamlit application entry point."""
    db.init_db()
    init_session_state()

    # Sidebar branding
    st.sidebar.markdown(
        """
        <div class="sidebar-brand-card">
            <div class="brand-icon">🏙️</div>
            <h2>Smart Issue System</h2>
            <div class="brand-sub">Civic AI &amp; Infrastructure Portal</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = ["🏠 Home", "📝 Report Issue", "📋 My Complaints", "📊 Admin Dashboard"]

    # Initialize navigation page state
    if "navigation_page" not in st.session_state or st.session_state.navigation_page not in pages:
        st.session_state.navigation_page = "🏠 Home"

    # Synchronize sidebar radio widget key if needed
    if "app_sidebar_nav_radio" not in st.session_state or st.session_state.app_sidebar_nav_radio not in pages:
        st.session_state.app_sidebar_nav_radio = st.session_state.navigation_page

    # Handle nav_override if set by external links
    if st.session_state.nav_override and st.session_state.nav_override in pages:
        st.session_state.navigation_page = st.session_state.nav_override
        st.session_state.app_sidebar_nav_radio = st.session_state.nav_override
        st.session_state.nav_override = None

    # Persistent navigation radio button
    selected_page = st.sidebar.radio(
        "Navigation Menu",
        pages,
        index=pages.index(st.session_state.navigation_page),
        key="app_sidebar_nav_radio",
    )

    st.session_state.navigation_page = selected_page

    # Sidebar system status footer
    mode_str = "🟡 Demo AI Engine" if ai_service.is_demo_mode() else "🟢 Live Gemini AI"
    st.sidebar.markdown(
        f'<div class="sidebar-status-box"><span style="font-size:0.82rem; font-weight:700;">{mode_str}</span></div>',
        unsafe_allow_html=True,
    )
    st.sidebar.caption("Smart Civic Tech System · v2.0")

    # Render selected page
    if selected_page == "🏠 Home":
        page_home()
    elif selected_page == "📝 Report Issue":
        page_report_issue()
    elif selected_page == "📋 My Complaints":
        page_my_complaints()
    elif selected_page == "📊 Admin Dashboard":
        page_admin_dashboard()


if __name__ == "__main__":
    main()
