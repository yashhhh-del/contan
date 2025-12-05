"""
AI Sales Copy & Ad Content Agent
================================
A complete AI system with premium UI/UX and dynamic graphics
"""

import streamlit as st
from groq import Groq
import os
import json
import sqlite3
import re
import io
from datetime import datetime
from dotenv import load_dotenv
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docq.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd
import nltk
from collections import Counter
import time
import random
import base64
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

# =============================================================================
# PREMIUM CSS STYLES WITH DYNAMIC ELEMENTS
# =============================================================================

PREMIUM_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

/* Root Variables */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --dark-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    --card-shadow: 0 10px 40px rgba(0,0,0,0.1);
    --hover-shadow: 0 20px 60px rgba(0,0,0,0.15);
    --glow: 0 0 20px rgba(102, 126, 234, 0.5);
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Container */
.main .block-container {
    padding: 2rem 3rem;
    max-width: 1400px;
}

/* Premium Header with Animation */
.premium-header {
    background: var(--primary-gradient);
    padding: 3rem 2rem;
    border-radius: 24px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: var(--card-shadow);
    position: relative;
    overflow: hidden;
    animation: headerPulse 8s ease-in-out infinite;
}

@keyframes headerPulse {
    0%, 100% { box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3); }
    50% { box-shadow: 0 25px 60px rgba(102, 126, 234, 0.5); }
}

.premium-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 0.8; }
}

.premium-header h1 {
    color: white;
    font-family: 'Poppins', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
    text-shadow: 2px 4px 20px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
    animation: textGlow 3s ease-in-out infinite alternate;
}

@keyframes textGlow {
    from { text-shadow: 2px 4px 20px rgba(0,0,0,0.3); }
    to { text-shadow: 2px 4px 30px rgba(255,255,255,0.5); }
}

.premium-header p {
    color: rgba(255,255,255,0.95);
    font-size: 1.3rem;
    margin-top: 1rem;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

.premium-badge {
    display: inline-block;
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1.5rem;
    border-radius: 50px;
    color: white;
    font-weight: 600;
    font-size: 0.9rem;
    margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.3);
    animation: badgePulse 2s ease-in-out infinite;
}

@keyframes badgePulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Animated Background Elements */
.floating-element {
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(5px);
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

/* Feature Cards with Hover Effects */
.feature-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: var(--card-shadow);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid rgba(0,0,0,0.05);
    height: 100%;
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: var(--primary-gradient);
    transition: all 0.4s ease;
}

.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: var(--hover-shadow);
}

.feature-card:hover::before {
    height: 100%;
    opacity: 0.1;
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: iconGlow 2s ease-in-out infinite alternate;
}

@keyframes iconGlow {
    from { opacity: 0.8; }
    to { opacity: 1; text-shadow: var(--glow); }
}

.feature-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 0.8rem;
}

.feature-desc {
    color: #666;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Stats Cards with Gradient */
.stats-card {
    background: var(--primary-gradient);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    color: white;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.stats-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, transparent 50%, rgba(255,255,255,0.1) 50%);
    background-size: 200% 200%;
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

.stats-number {
    font-size: 2.5rem;
    font-weight: 800;
    font-family: 'Poppins', sans-serif;
    margin: 0;
    animation: countUp 1.5s ease-out forwards;
}

@keyframes countUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.stats-label {
    font-size: 0.9rem;
    opacity: 0.9;
    margin-top: 0.3rem;
}

/* Premium Buttons */
.stButton>button {
    background: var(--primary-gradient);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35);
    position: relative;
    overflow: hidden;
}

.stButton>button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, transparent 50%, rgba(255,255,255,0.2) 50%);
    background-size: 200% 200%;
    transition: all 0.3s ease;
    z-index: 0;
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.45);
}

.stButton>button:hover::before {
    background-position: 100% 100%;
}

.stButton>button:active {
    transform: translateY(-1px);
}

.stButton>button span {
    position: relative;
    z-index: 1;
}

/* Input Fields */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
    border-radius: 12px;
    border: 2px solid #e0e0e0;
    padding: 0.8rem 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(5px);
}

.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
    background: white;
}

/* Select Box */
.stSelectbox>div>div {
    border-radius: 12px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(5px);
}

/* Expander */
div[data-testid="stExpander"] {
    background: white;
    border-radius: 16px;
    border: none;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    overflow: hidden;
    transition: all 0.3s ease;
}

div[data-testid="stExpander"] div[role="button"] {
    padding: 1rem 1.5rem;
    transition: all 0.3s ease;
}

div[data-testid="stExpander"] div[role="button"]:hover {
    background: rgba(102, 126, 234, 0.05);
}

div[data-testid="stExpander"] div[role="button"] p {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1a1a2e !important;
}

/* Content Results Card */
.result-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: var(--card-shadow);
    border-left: 5px solid #667eea;
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.result-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: var(--dark-gradient);
    padding: 1rem;
    border-radius: 0 20px 20px 0;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

section[data-testid="stSidebar"] .stMarkdown {
    color: white;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

section[data-testid="stSidebar"] .stRadio label {
    color: rgba(255,255,255,0.9) !important;
}

section[data-testid="stSidebar"] .stTextInput label {
    color: rgba(255,255,255,0.9) !important;
}

/* Download Buttons */
.stDownloadButton>button {
    background: var(--success-gradient);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1.5rem;
    font-weight: 600;
    box-shadow: 0 8px 25px rgba(17, 153, 142, 0.3);
    transition: all 0.3s ease;
}

.stDownloadButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(17, 153, 142, 0.4);
}

/* Platform tags */
.platform-tag {
    display: inline-block;
    padding: 0.4rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.3rem;
    transition: all 0.3s ease;
    animation: tagPop 0.5s ease-out;
}

@keyframes tagPop {
    0% { transform: scale(0.8); opacity: 0; }
    80% { transform: scale(1.05); }
    100% { transform: scale(1); opacity: 1; }
}

.tag-google { background: linear-gradient(135deg, #4285f4, #34a853); color: white; }
.tag-facebook { background: linear-gradient(135deg, #1877f2, #3b5998); color: white; }
.tag-instagram { background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white; }
.tag-seo { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; }
.tag-landing { background: var(--primary-gradient); color: white; }
.tag-all { background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3); color: white; }

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary-gradient);
    border-radius: 10px;
}

/* Loading Animation */
.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(102, 126, 234, 0.2);
    border-radius: 50%;
    border-top-color: #667eea;
    animation: spin 1s ease-in-out infinite;
    margin: 0 auto;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Content Card Animations */
.content-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: var(--card-shadow);
    transition: all 0.3s ease;
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out forwards;
}

.content-card:nth-child(1) { animation-delay: 0.1s; }
.content-card:nth-child(2) { animation-delay: 0.2s; }
.content-card:nth-child(3) { animation-delay: 0.3s; }
.content-card:nth-child(4) { animation-delay: 0.4s; }

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .premium-header h1 {
        font-size: 2rem;
    }
    .premium-header p {
        font-size: 1rem;
    }
    .main .block-container {
        padding: 1rem;
    }
    .feature-card {
        padding: 1.5rem;
    }
}

/* Gradient Text */
.gradient-text {
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

/* Animated Border */
.animated-border {
    position: relative;
    padding: 2px;
    border-radius: 18px;
    background: var(--primary-gradient);
    animation: borderPulse 3s linear infinite;
}

@keyframes borderPulse {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}

.animated-border-content {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
}

/* 3D Effect */
.three-d-card {
    transform: perspective(1000px) rotateX(5deg);
    transition: all 0.3s ease;
}

.three-d-card:hover {
    transform: perspective(1000px) rotateX(0deg) translateY(-10px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.2);
}
</style>
"""

# =============================================================================
# DYNAMIC GRAPHICS AND ANIMATIONS
# =============================================================================

def create_animated_background():
    """Create animated background elements"""
    st.markdown("""
    <div class="floating-element" style="width: 100px; height: 100px; top: 10%; left: 10%; animation-delay: 0s;"></div>
    <div class="floating-element" style="width: 60px; height: 60px; top: 20%; right: 15%; animation-delay: 1s;"></div>
    <div class="floating-element" style="width: 80px; height: 80px; bottom: 30%; left: 20%; animation-delay: 2s;"></div>
    <div class="floating-element" style="width: 40px; height: 40px; top: 60%; right: 10%; animation-delay: 0.5s;"></div>
    """, unsafe_allow_html=True)

def create_loading_animation():
    """Create a custom loading animation"""
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
        <div class="loading-spinner"></div>
        <div style="margin-left: 1rem; font-size: 1.2rem; color: #667eea; font-weight: 600;">
            Generating your high-converting content...
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_success_animation():
    """Create success animation"""
    st.balloons()
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="font-size: 3rem; color: #4CAF50; margin-bottom: 1rem;">✅</div>
        <h3 style="color: #1a1a2e; margin: 0;">Content Generated Successfully!</h3>
        <p style="color: #666; margin-top: 0.5rem;">Your high-converting marketing content is ready</p>
    </div>
    """, unsafe_allow_html=True)

def create_content_card(title, content, icon="📄", color="#667eea", delay=0):
    """Create a styled content card with animation"""
    st.markdown(f"""
    <div class="content-card" style="animation-delay: {delay}s; border-left: 4px solid {color};">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <h4 style="color: {color}; margin: 0; font-family: 'Poppins', sans-serif;">{title}</h4>
        </div>
        <div style="color: #1a1a2e; line-height: 1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def create_animated_counter(target, label, color="#667eea"):
    """Create an animated counter"""
    st.markdown(f"""
    <div class="stats-card" style="background: linear-gradient(135deg, {color} 0%, {color} 100%);">
        <div class="stats-number" id="counter-{label.replace(' ', '-')}">{target}</div>
        <div class="stats-label">{label}</div>
    </div>
    <script>
    function animateCounter(elementId, target) {{
        const element = document.getElementById(elementId);
        const start = 0;
        const duration = 1500;
        const startTime = performance.now();

        function updateCounter(currentTime) {{
            const elapsedTime = currentTime - startTime;
            const progress = Math.min(elapsedTime / duration, 1);
            const value = Math.floor(progress * target);

            element.textContent = value;

            if (progress < 1) {{
                requestAnimationFrame(updateCounter);
            }} else {{
                element.textContent = target;
            }}
        }}

        requestAnimationFrame(updateCounter);
    }}

    setTimeout(() => {{
        animateCounter('counter-{label.replace(' ', '-')}', {target});
    }}, 500);
    </script>
    """, unsafe_allow_html=True)

def create_interactive_chart(data, title, type="bar"):
    """Create an interactive chart using Plotly"""
    if type == "bar":
        fig = px.bar(
            data,
            x=data.index,
            y=data.values,
            title=title,
            color=data.index,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
    elif type == "pie":
        fig = px.pie(
            data,
            names=data.index,
            values=data.values,
            title=title,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
    elif type == "line":
        fig = px.line(
            data,
            x=data.index,
            y=data.values,
            title=title,
            line_shape="spline",
            color_discrete_sequence=["#667eea"]
        )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1a1a2e"),
        margin=dict(l=20, r=20, t=50, b=20),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

def create_3d_card(content, title, icon="📊"):
    """Create a 3D effect card"""
    st.markdown(f"""
    <div class="three-d-card" style="background: white; border-radius: 16px; padding: 2rem; margin: 2rem 0; box-shadow: var(--card-shadow);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <h3 style="color: #1a1a2e; margin: 0; font-family: 'Poppins', sans-serif;">{title}</h3>
        </div>
        <div style="color: #666; line-height: 1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def create_gradient_button(text, color1="#667eea", color2="#764ba2"):
    """Create a gradient button"""
    st.markdown(f"""
    <button style="
        background: linear-gradient(135deg, {color1}, {color2});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35);
        transition: all 0.3s ease;
        margin: 1rem 0;
    ">
        {text}
    </button>
    """, unsafe_allow_html=True)

# =============================================================================
# DATABASE SETUP (Enhanced)
# =============================================================================

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('sales_content.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            business_name TEXT,
            business_type TEXT,
            product_service TEXT,
            target_audience TEXT,
            offer TEXT,
            tone TEXT,
            platform TEXT,
            headlines TEXT,
            descriptions TEXT,
            hashtags TEXT,
            keywords TEXT,
            cta TEXT,
            seo_title TEXT,
            meta_description TEXT,
            landing_page_content TEXT,
            full_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            performance_score REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATE,
            content_generated INTEGER DEFAULT 0,
            platforms_used TEXT,
            tones_used TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

def save_to_history(user_id, inputs, outputs):
    """Save generated content to database history"""
    conn = sqlite3.connect('sales_content.db')
    cursor = conn.cursor()

    # Update analytics
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        INSERT OR IGNORE INTO analytics (user_id, date)
        VALUES (?, ?)
    ''', (user_id, today))

    cursor.execute('''
        UPDATE analytics
        SET content_generated = content_generated + 1,
            platforms_used = CASE
                WHEN platforms_used IS NULL OR platforms_used = '' THEN ?
                ELSE platforms_used || ',' || ?
            END,
            tones_used = CASE
                WHEN tones_used IS NULL OR tones_used = '' THEN ?
                ELSE tones_used || ',' || ?
            END
        WHERE user_id = ? AND date = ?
    ''', (
        inputs.get('platform', ''),
        inputs.get('platform', ''),
        inputs.get('tone', ''),
        inputs.get('tone', ''),
        user_id,
        today
    ))

    cursor.execute('''
        INSERT INTO content_history
        (user_id, business_name, business_type, product_service, target_audience,
         offer, tone, platform, headlines, descriptions, hashtags, keywords,
         cta, seo_title, meta_description, landing_page_content, full_response)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        inputs.get('business_name', ''),
        inputs.get('business_type', ''),
        inputs.get('product_service', ''),
        inputs.get('target_audience', ''),
        inputs.get('offer', ''),
        inputs.get('tone', ''),
        ', '.join(inputs.get('platform', [])) if isinstance(inputs.get('platform'), list) else inputs.get('platform', ''),
        outputs.get('headlines', ''),
        outputs.get('descriptions', ''),
        outputs.get('hashtags', ''),
        outputs.get('keywords', ''),
        outputs.get('cta', ''),
        outputs.get('seo_title', ''),
        outputs.get('meta_description', ''),
        outputs.get('landing_page_content', ''),
        json.dumps(outputs)
    ))

    conn.commit()
    conn.close()

def get_user_history(user_id, limit=50):
    """Retrieve user's content generation history"""
    conn = sqlite3.connect('sales_content.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM content_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (user_id, limit))

    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    return [dict(zip(columns, row)) for row in rows]

def get_analytics_data(user_id):
    """Get analytics data for dashboard"""
    conn = sqlite3.connect('sales_content.db')
    cursor = conn.cursor()

    # Get total content generated
    cursor.execute('''
        SELECT COUNT(*) FROM content_history WHERE user_id = ?
    ''', (user_id,))
    total_content = cursor.fetchone()[0]

    # Get content by platform
    cursor.execute('''
        SELECT platform, COUNT(*) as count
        FROM content_history
        WHERE user_id = ?
        GROUP BY platform
        ORDER BY count DESC
    ''', (user_id,))
    platform_data = cursor.fetchall()

    # Get content by tone
    cursor.execute('''
        SELECT tone, COUNT(*) as count
        FROM content_history
        WHERE user_id = ?
        GROUP BY tone
        ORDER BY count DESC
    ''', (user_id,))
    tone_data = cursor.fetchall()

    # Get content over time
    cursor.execute('''
        SELECT date(created_at) as day, COUNT(*) as count
        FROM content_history
        WHERE user_id = ?
        GROUP BY day
        ORDER BY day
    ''', (user_id,))
    time_data = cursor.fetchall()

    conn.close()

    return {
        'total_content': total_content,
        'platform_data': platform_data,
        'tone_data': tone_data,
        'time_data': time_data
    }

# =============================================================================
# NLP KEYWORD EXTRACTION ENGINE (Enhanced)
# =============================================================================

def download_nltk_data():
    """Download required NLTK data"""
    nltk_packages = [
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('corpora/stopwords', 'stopwords'),
        ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
        ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng'),
    ]

    for path, package in nltk_packages:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, quiet=True)

def extract_keywords_nlp(text, num_keywords=15):
    """Extract keywords from text using NLTK"""
    download_nltk_data()

    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk import pos_tag

    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))

    marketing_stopwords = {
        'will', 'can', 'get', 'make', 'use', 'new', 'one', 'also',
        'like', 'just', 'know', 'take', 'come', 'see', 'want', 'look',
        'give', 'think', 'good', 'best', 'way', 'need', 'feel', 'try'
    }
    stop_words.update(marketing_stopwords)

    filtered_tokens = [
        token for token in tokens
        if token.isalnum() and token not in stop_words and len(token) > 2
    ]

    pos_tags = pos_tag(filtered_tokens)
    important_tags = {'NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBG', 'JJ', 'JJR', 'JJS'}

    important_words = [
        word for word, tag in pos_tags
        if tag in important_tags
    ]

    word_freq = Counter(important_words)
    keywords = [word for word, count in word_freq.most_common(num_keywords)]

    return keywords

def generate_hashtags(keywords, platform='instagram'):
    """Generate platform-appropriate hashtags from keywords"""
    hashtags = []

    for keyword in keywords[:10]:
        tag = keyword.replace(' ', '').replace('-', '').lower()
        if tag:
            hashtags.append(f"#{tag}")

    if platform.lower() in ['instagram', 'facebook']:
        common_tags = ['#marketing', '#business', '#entrepreneur', '#success', '#growth']
        hashtags.extend(common_tags[:3])

    return list(set(hashtags))[:15]

# =============================================================================
# PROMPT TEMPLATES ENGINE (Enhanced)
# =============================================================================

class PromptTemplates:
    """Enhanced prompt templates for high-converting content"""

    @staticmethod
    def get_tone_modifier(tone):
        """Return tone-specific writing instructions"""
        tone_modifiers = {
            'Professional': "Use formal, business-appropriate language. Be authoritative and trustworthy. Focus on value propositions, data, and credibility. Use industry-specific terminology when appropriate.",
            'Emotional': "Connect emotionally with the reader. Use storytelling elements, personal anecdotes, and relatable scenarios. Appeal to feelings, desires, and aspirations. Use power words that trigger emotions like joy, fear, excitement, or curiosity.",
            'Exciting': "Use energetic, dynamic language. Create enthusiasm and anticipation. Use action words, exclamation points, and phrases that create urgency. Make the reader feel like they're missing out if they don't act now.",
            'Urgent': "Create a strong sense of urgency and scarcity. Use time-sensitive language and emphasize limited availability or time-bound offers. Use words like NOW, TODAY, LIMITED, HURRY, LAST CHANCE, DON'T MISS OUT.",
            'Friendly': "Use warm, conversational tone. Be approachable and relatable. Write as if talking to a friend. Use casual language, contractions, and personal pronouns. Make the reader feel like you're speaking directly to them.",
            'Luxury': "Use sophisticated, premium language. Emphasize exclusivity, quality, and prestige. Appeal to aspirational desires. Use words like EXCLUSIVE, PREMIUM, ELITE, LUXURY, HIGH-END, VIP, BESPOKE, CRAFTSMANSHIP."
        }
        return tone_modifiers.get(tone, tone_modifiers['Professional'])

    @staticmethod
    def google_ads_prompt(inputs):
        """Generate Google Ads content prompt with high-converting headlines"""
        return f"""
You are a world-class Google Ads copywriter who has generated over $100M in revenue. Create IRRESISTIBLE, HIGH-CONVERTING Google Ads content that stops scrolls and drives clicks.

BUSINESS DETAILS:
- Business Name: {inputs['business_name']}
- Business Type: {inputs['business_type']}
- Product/Service: {inputs['product_service']}
- Target Audience: {inputs['target_audience']}
- Offer: {inputs['offer']}
- Tone: {inputs['tone']}

TONE INSTRUCTIONS: {PromptTemplates.get_tone_modifier(inputs['tone'])}

HEADLINE POWER FORMULAS (Use these patterns - MUST be 30 characters or less):
1. [Number] + [Benefit] + [Timeframe] → "5X More Leads in 7 Days"
2. [Action Verb] + [Desire] + [Differentiator] → "Unlock Premium Results Fast"
3. [Question] that triggers curiosity → "Want 10X More Customers?"
4. [Pain Point] + [Solution] → "Tired of Low Sales? Fix It Now"
5. [Social Proof] + [Result] → "Join 10K+ Happy Customers"
6. [Urgency] + [Benefit] → "Limited: 50% Off Today Only"
7. [How to] + [Achieve Result] → "How to Double Sales in 30 Days"
8. [Secret] + [Benefit] → "The Secret to More Leads Revealed"
9. [Guarantee] + [Result] → "Guaranteed to Boost Sales or Money Back"
10. [Comparison] + [Benefit] → "Better Than [Competitor] - Try Free"

POWER WORDS TO USE: Free, New, Proven, Guaranteed, Instant, Exclusive, Secret, Easy, Fast, Save, Discover, Unlock, Transform, Boost, Skyrocket, Limited, Today, Now, Hurry, Don't Miss, Last Chance

STRICT CHARACTER LIMITS:
- Headlines: Maximum 30 characters each (including spaces)
- Descriptions: Maximum 90 characters each (including spaces)

Generate the following in JSON format:
{{
    "headlines": [
        // 15 IRRESISTIBLE headlines using power formulas
        // Each MUST be 30 characters or less - COUNT CAREFULLY
        // Mix different formulas for variety
        // Include numbers, power words, and emotional triggers
        // At least 5 should include urgency/scarcity
        // At least 3 should include social proof
    ],
    "descriptions": [
        // 5 compelling descriptions with clear value proposition and CTA
        // Max 90 chars each - COUNT CAREFULLY
        // Include benefit + CTA in each
        // Use power words and emotional triggers
    ],
    "display_urls": [
        // 3 keyword-rich display URL paths
        // Should be short and include primary keywords
    ],
    "keywords": [
        // 15 high-intent search keywords
        // Mix of short-tail and long-tail
        // Include buyer intent keywords
    ],
    "negative_keywords": [
        // 5 negative keywords to exclude
        // Words that would attract wrong audience
    ],
    "cta_suggestions": [
        // 5 action-oriented CTAs
        // Should create urgency and drive action
    ],
    "performance_tips": [
        // 3 tips to improve ad performance
        // Based on the business and audience
    ]
}}

IMPORTANT RULES:
1. Every headline must trigger curiosity, desire, or urgency
2. Use numbers and specifics (3X, 50%, 24hrs, 10K+)
3. Include at least 5 headlines with urgency/scarcity
4. Include at least 3 headlines with social proof
5. Count characters carefully - headlines over 30 chars will be rejected
6. Descriptions must include a clear CTA
7. Return ONLY valid JSON - no markdown, no explanations
8. Make every word count - no fluff
"""

    @staticmethod
    def facebook_instagram_prompt(inputs):
        """Generate Facebook/Instagram ad content prompt"""
        return f"""
You are a viral social media marketing expert with 10M+ followers and 1000+ successful campaigns. Create SCROLL-STOPPING content that gets high engagement and conversions.

BUSINESS DETAILS:
- Business Name: {inputs['business_name']}
- Business Type: {inputs['business_type']}
- Product/Service: {inputs['product_service']}
- Target Audience: {inputs['target_audience']}
- Offer: {inputs['offer']}
- Tone: {inputs['tone']}

TONE INSTRUCTIONS: {PromptTemplates.get_tone_modifier(inputs['tone'])}

VIRAL HOOKS FORMULAS (First line MUST stop the scroll):
1. "Stop scrolling if you..." + [pain point/desire]
2. "POV: You just discovered..." + [solution/secret]
3. "This is your sign to..." + [action]
4. "Nobody talks about this but..." + [unique insight]
5. "The secret to [desire] is..." + [solution]
6. "Here's why [common belief] is wrong..." + [contrarian view]
7. "I tried [solution] for 30 days..." + [result]
8. "Most people don't know this..." + [valuable insight]
9. "What if I told you..." + [surprising fact]
10. "This changed everything..." + [transformation]

EMOJI STRATEGY:
- Use emojis to break up text and draw attention
- 1 emoji per 2-3 lines of text
- Use relevant emojis that match the content
- Don't overuse - max 3-4 per post

Generate the following in JSON format:
{{
    "facebook_ad": {{
        "primary_text": [
            // 3 SCROLL-STOPPING primary texts with hooks (125-500 chars)
            // First line MUST be a hook that stops the scroll
            // Include social proof, urgency, and clear CTA
            // Use line breaks for readability
            // Include emojis strategically
        ],
        "headlines": [
            // 5 curiosity-driven headlines (max 40 characters)
            // Should make people want to click
        ],
        "descriptions": [
            // 3 benefit-focused link descriptions (max 30 characters)
            // Highlight key benefit or offer
        ],
        "cta_button": [
            "Shop Now", "Learn More", "Sign Up", "Get Offer", "Book Now", "Download", "Try Free"
        ],
        "image_suggestions": [
            // 3 image/video concepts that would work well
        ]
    }},
    "instagram_ad": {{
        "captions": [
            // 3 engaging captions with emojis, hooks, and story elements
            // Use line breaks for readability
            // First line MUST be a hook
            // Include call-to-action at end
            // Use relevant hashtags within text
        ],
        "story_text": [
            // 3 punchy story overlay texts (max 100 characters)
            // Should be attention-grabbing
            // Include CTA like "Swipe up" or "Link in bio"
        ],
        "hashtags": [
            // 25 strategic hashtags (mix of popular, niche, and branded)
            // Group by category: 5 popular, 10 niche, 5 branded, 5 trending
        ],
        "bio_link_cta": [
            // 3 compelling "Link in bio" CTAs
            // Should create urgency
        ],
        "reels_hooks": [
            // 5 viral reel opening hooks (first 3 seconds)
            // Should stop the scroll immediately
            // Use text overlays and visual hooks
        ],
        "content_calendar": [
            // 3 content ideas for the next week
            // Mix of educational, entertaining, and promotional
        ]
    }},
    "carousel_hooks": [
        // 5 carousel slide headline hooks that make people swipe
        // Each should create curiosity about next slide
    ],
    "engagement_questions": [
        // 3 questions to boost comments and engagement
        // Should be relevant to the audience
        // Encourage discussion
    ],
    "performance_tips": [
        // 3 tips to improve ad performance on these platforms
    ]
}}

IMPORTANT:
- First line MUST stop the scroll - make it irresistible
- Use emojis strategically (not excessively)
- Create FOMO and urgency
- Include clear CTAs
- Make it about THEM, not you
- Return ONLY valid JSON
"""

    @staticmethod
    def seo_content_prompt(inputs):
        """Generate SEO-optimized content prompt"""
        return f"""
You are an SEO expert who has ranked 1000+ pages on Google's first page. Create content that ranks well AND converts visitors into customers.

BUSINESS DETAILS:
- Business Name: {inputs['business_name']}
- Business Type: {inputs['business_type']}
- Product/Service: {inputs['product_service']}
- Target Audience: {inputs['target_audience']}
- Offer: {inputs['offer']}
- Tone: {inputs['tone']}

TONE INSTRUCTIONS: {PromptTemplates.get_tone_modifier(inputs['tone'])}

SEO TITLE FORMULAS (50-60 characters):
1. [Primary Keyword] - [Benefit] | [Brand]
2. [Number] Best [Keyword] for [Audience] in [Year]
3. How to [Achieve Result] with [Solution] [Year]
4. [Keyword]: The Ultimate Guide to [Benefit]
5. [Keyword] vs [Keyword]: Which is Better for [Audience]?
6. [Number] [Keyword] Tips to [Achieve Result]
7. The Complete [Year] Guide to [Keyword]
8. [Keyword] Made Simple: A Step-by-Step Guide
9. Why [Common Problem] Happens & How to Fix It
10. [Keyword] Examples: [Number] Ideas to Inspire You

META DESCRIPTION BEST PRACTICES:
- 150-160 characters
- Include primary keyword
- Clear value proposition
- Call-to-action
- Create curiosity
- Use power words

Generate the following in JSON format:
{{
    "seo_titles": [
        // 5 click-worthy SEO titles (50-60 characters) using formulas above
        // Include primary keyword in each
        // Create curiosity and desire
        // Use numbers when appropriate
    ],
    "meta_descriptions": [
        // 5 compelling meta descriptions with CTA (150-160 characters)
        // Include primary keyword
        // Highlight key benefit
        // Create urgency or curiosity
    ],
    "h1_headings": [
        // 3 powerful H1 headings with primary keyword
        // Should match or be similar to SEO title
    ],
    "h2_subheadings": [
        // 5 engaging H2 subheadings
        // Should include secondary keywords
        // Create logical content structure
    ],
    "content_outline": [
        // Detailed content outline with headings and subheadings
        // Should flow logically
        // Include FAQ section
        // Include CTA sections
    ],
    "keywords": {{
        "primary": [
            // 5 high-volume primary keywords
            // Should be included in titles and headings
        ],
        "secondary": [
            // 10 LSI/secondary keywords
            // Should be included in subheadings and content
        ],
        "long_tail": [
            // 10 long-tail keyword phrases with buyer intent
            // Should be used in content and FAQs
        ],
        "semantic": [
            // 10 semantic keywords related to the topic
        ]
    }},
    "url_slugs": [
        // 3 SEO-friendly URL slugs
        // Should be short and include primary keyword
        // Use hyphens to separate words
    ],
    "image_alt_texts": [
        // 5 descriptive image alt texts
        // Include keywords naturally
        // Describe the image accurately
    ],
    "schema_suggestions": {{
        "type": "suggested schema type (e.g., Product, Service, FAQPage, HowTo)",
        "key_properties": [
            // List of key schema properties to include
        ],
        "example": "JSON-LD schema markup example"
    }},
    "internal_linking": [
        // 5 internal linking opportunities
        // Related content that should be linked to
    ],
    "performance_tips": [
        // 3 tips to improve SEO performance
    ]
}}

Return ONLY valid JSON.
"""

    @staticmethod
    def landing_page_prompt(inputs):
        """Generate landing page content prompt"""
        return f"""
You are a conversion rate optimization expert with a track record of 40%+ conversion rates. Create a high-converting landing page that turns visitors into customers.

BUSINESS DETAILS:
- Business Name: {inputs['business_name']}
- Business Type: {inputs['business_type']}
- Product/Service: {inputs['product_service']}
- Target Audience: {inputs['target_audience']}
- Offer: {inputs['offer']}
- Tone: {inputs['tone']}

TONE INSTRUCTIONS: {PromptTemplates.get_tone_modifier(inputs['tone'])}

HEADLINE FORMULAS FOR HIGH CONVERSION:
1. "[Result] Without [Pain Point]"
2. "The [Adjective] Way to [Achieve Desire]"
3. "Get [Specific Result] in [Timeframe] or [Guarantee]"
4. "Finally, [Solution] That [Unique Benefit]"
5. "[Number]% of [Audience] Struggle With [Problem] - Here's Why"
6. "Stop [Pain Point] and Start [Desire]"
7. "The Secret to [Desire] That [Industry] Doesn't Want You to Know"
8. "[Product] vs [Competitor]: Which is Right For You?"
9. "How [Customer] Got [Result] in [Timeframe]"
10. "[Number] Reasons Why [Audience] Love [Product]"

Generate the following in JSON format:
{{
    "hero_section": {{
        "headline": "Powerful headline using formula above (max 10 words)",
        "subheadline": "Supporting text that expands the promise (max 20 words)",
        "cta_button_text": "Action-oriented CTA (e.g., 'Start Free Trial')",
        "cta_supporting_text": "Risk reducer (e.g., 'No credit card required • Cancel anytime')",
        "hero_image_suggestion": "Description of ideal hero image/video",
        "trust_indicators": [
            // 3 trust elements for hero section (e.g., "As seen in Forbes")
        ]
    }},
    "value_propositions": [
        {{
            "title": "Benefit-focused title (max 5 words)",
            "description": "2-3 sentence description with specific outcomes",
            "icon_suggestion": "relevant icon name or emoji",
            "supporting_stat": "Impressive statistic to support claim"
        }}
        // 4 total value propositions
    ],
    "features_benefits": [
        {{
            "feature": "Feature name (what it is)",
            "benefit": "What it means for the user (outcome-focused)",
            "how_it_works": "Brief explanation of how it works",
            "icon_suggestion": "relevant icon or emoji"
        }}
        // 6 feature-benefit pairs
    ],
    "social_proof": {{
        "testimonials": [
            {{
                "quote": "Customer testimonial quote",
                "name": "Customer name",
                "title": "Customer title/company",
                "photo_suggestion": "Description of ideal photo",
                "result": "Specific result achieved"
            }}
            // 3 testimonials
        ],
        "stats": [
            // 3 impressive stats to showcase (e.g., "10,000+ happy customers")
        ],
        "trust_badges": [
            // 5 trust elements (e.g., "30-day money-back guarantee")
        ],
        "media_mentions": [
            // 3 media mentions (e.g., "Featured in TechCrunch")
        ]
    }},
    "objection_handling": [
        {{
            "objection": "Common customer objection",
            "response": "Persuasive response that overcomes the objection",
            "supporting_stat": "Statistic or fact to support response"
        }}
        // 5 common objections
    ],
    "faq": [
        {{
            "question": "Common question that addresses an objection",
            "answer": "Clear, concise answer that builds trust",
            "cta_in_answer": "Subtle CTA within the answer"
        }}
        // 5 FAQ items
    ],
    "urgency_elements": [
        // 3 urgency/scarcity elements (e.g., "Only 3 spots left!")
    ],
    "final_cta": {{
        "headline": "Final push headline (should create urgency)",
        "subheadline": "Supporting text that reinforces the offer",
        "cta_text": "Strong final CTA (e.g., 'Get Instant Access Now')",
        "guarantee": "Risk reversal guarantee (e.g., '30-day money-back guarantee')",
        "trust_indicators": [
            // 3 final trust elements
        ]
    }},
    "email_capture": {{
        "headline": "Email capture headline",
        "subheadline": "Supporting text for email capture",
        "cta_text": "Email capture CTA",
        "incentive": "What they get for signing up (e.g., 'Free guide')"
    }},
    "performance_tips": [
        // 3 tips to improve landing page conversion rate
    ],
    "a_b_testing": [
        // 3 A/B testing suggestions
    ]
}}

Return ONLY valid JSON.
"""

    @staticmethod
    def multi_platform_prompt(inputs):
        """Generate content for all platforms at once"""
        return f"""
You are a multi-channel marketing genius who has scaled brands from 0 to millions. Create a cohesive, high-converting content strategy across all platforms.

BUSINESS DETAILS:
- Business Name: {inputs['business_name']}
- Business Type: {inputs['business_type']}
- Product/Service: {inputs['product_service']}
- Target Audience: {inputs['target_audience']}
- Offer: {inputs['offer']}
- Tone: {inputs['tone']}

TONE INSTRUCTIONS: {PromptTemplates.get_tone_modifier(inputs['tone'])}

CONTENT STRATEGY PRINCIPLES:
1. Consistency: Maintain consistent messaging across all platforms
2. Platform-Specific: Adapt content to each platform's best practices
3. Audience-Centric: Focus on the audience's needs and desires
4. Benefit-Driven: Highlight benefits, not features
5. Urgency: Create urgency and scarcity where appropriate
6. Social Proof: Include social proof and credibility
7. Clear CTA: Every piece of content should have a clear call-to-action

Generate IRRESISTIBLE, HIGH-CONVERTING content for ALL platforms in JSON format:
{{
    "brand": {{
        "tagline": "Memorable brand tagline (max 10 words)",
        "elevator_pitch": "30-second compelling pitch",
        "unique_selling_points": [
            // 3 clear USPs that differentiate from competitors
        ],
        "brand_voice": "Description of brand voice and personality",
        "brand_keywords": [
            // 10 keywords that define the brand
        ]
    }},
    "google_ads": {{
        "headlines": [
            // 15 POWER headlines using formulas
            // Max 30 chars each - COUNT CAREFULLY
            // Mix of urgency, social proof, and benefit-driven
        ],
        "descriptions": [
            // 5 compelling descriptions, max 90 chars each
            // Include benefit + CTA
        ],
        "keywords": [
            // 15 high-intent keywords
            // Mix of short-tail and long-tail
        ],
        "negative_keywords": [
            // 5 negative keywords
        ],
        "cta_buttons": [
            // 3 CTA button suggestions
        ]
    }},
    "facebook": {{
        "primary_texts": [
            // 3 scroll-stopping ad texts with hooks
            // First line MUST stop the scroll
            // Include social proof and urgency
        ],
        "headlines": [
            // 5 curiosity-driven headlines, max 40 chars
        ],
        "image_suggestions": 
