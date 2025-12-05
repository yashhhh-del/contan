import streamlit as st
from groq import Groq
import os
import json
import sqlite3
import re
import io
import time
from datetime import datetime
from dotenv import load_dotenv
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import nltk
from collections import Counter

# Load env
load_dotenv()

# Download NLTK data once
def download_nltk():
    for name in ['punkt', 'stopwords', 'averaged_perceptron_tagger']:
        try:
            nltk.data.find(f'tokenizers/{name}')
        except:
            nltk.download(name, quiet=True)
download_nltk()

# =============================================================================
# ULTIMATE PREMIUM UI + ANIMATIONS
# =============================================================================

ULTIMATE_UI = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

:root {
    --primary: #6366f1;
    --secondary: #ec4899;
    --success: #10b981;
    --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --glass: rgba(255, 255, 255, 0.15);
    --shadow: 0 20px 50px rgba(0,0,0,0.15);
}

#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

.animated-bg {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
    background-size: 400% 400%;
    animation: gradient 20s ease infinite;
    opacity: 0.1; z-index: -1;
}
@keyframes gradient {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}

.main .block-container {padding: 2rem; max-width: 1600px;}

.hero-header {
    background: var(--gradient-1);
    padding: 4rem 2rem; border-radius: 32px; margin: 2rem 0; text-align: center;
    box-shadow: var(--shadow); position: relative; overflow: hidden;
    transform: perspective(1000px) rotateX(5deg);
    transition: all 0.5s;
}
.hero-header:hover {transform: perspective(1000px) rotateX(0) translateY(-10px);}
.hero-header h1 {
    font-family: 'Space Grotesk', sans-serif; font-size: 4.5rem; font-weight: 900;
    background: linear-gradient(90deg, #fff, #e0e7ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-header p {font-size: 1.5rem; color: rgba(255,255,255,0.95);}

.glass-card {
    background: var(--glass); backdrop-filter: blur(20px);
    border-radius: 24px; padding: 2rem; border: 1px solid rgba(255,255,255,0.2);
    box-shadow: var(--shadow); transition: all 0.4s;
}
.glass-card:hover {transform: translateY(-15px);}

.preview-card {
    background: white; border-radius: 20px; padding: 1.5rem; margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-left: 5px solid var(--primary);
    animation: slideIn 0.8s ease-out;
}
@keyframes slideIn {from {opacity: 0; transform: translateY(30px);} to {opacity: 1;}}

.fab {
    position: fixed; bottom: 30px; right: 30px;
    background: var(--gradient-1); color: white; width: 70px; height: 70px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 2.5rem; box-shadow: 0 10px 30px rgba(102,126,234,0.4);
    cursor: pointer; z-index: 1000; animation: float 3s ease-in-out infinite;
}
@keyframes float {0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}

.progress-bar {height: 12px; background: var(--gradient-2); border-radius: 50px;}
</style>

<div class="animated-bg"></div>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
"""

# =============================================================================
# DATABASE & NLP
# =============================================================================

def init_db():
    conn = sqlite3.connect('sales_agent.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY, user_id INTEGER, business TEXT, inputs TEXT, outputs TEXT, created_at TEXT
    )''')
    conn.commit(); conn.close()

def save_history(inputs, outputs):
    conn = sqlite3.connect('sales_agent.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, business, inputs, outputs, created_at) VALUES (?,?,?,?,?)",
              (1, inputs.get('business_name',''), json.dumps(inputs), json.dumps(outputs), datetime.now().isoformat()))
    conn.commit(); conn.close()

def extract_keywords(text):
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    stop = set(stopwords.words('english') + ['will','get','new','one','like','use','make'])
    words = [w.lower() for w in word_tokenize(text) if w.isalpha() and w.lower() not in stop and len(w)>2]
    return [w for w,c in Counter(words).most_common(15)]

# =============================================================================
# PROMPT TEMPLATES (Same as your original — excellent!)
# =============================================================================

class Prompts:
    @staticmethod
    def all_platforms(inputs):
        return f"""
You are a world-class marketing expert. Generate HIGH-CONVERTING content for ALL platforms.

Business: {inputs['business_name']}
Product/Service: {inputs['product_service']}
Audience: {inputs['target_audience']}
Offer: {inputs['offer']}
Tone: {inputs['tone']}

Return ONLY valid JSON:
{{
    "google_ads": {{"headlines": ["15 headlines ≤30 chars"], "descriptions": ["5 desc ≤90 chars"]}},
    "facebook": {{"primary_texts": ["3 scroll-stopping texts"], "headlines": ["5 headlines"]}},
    "instagram": {{"captions": ["3 viral captions"], "hashtags": ["20 hashtags"]}},
    "seo": {{"titles": ["5 SEO titles"], "meta_descriptions": ["5 meta desc"]}},
    "landing_page": {{"hero_headline": "...", "cta": "..."}},
    "email": {{"subjects": ["5 subject lines"]}}
}}
"""

# =============================================================================
# CONTENT GENERATOR
# =============================================================================

class Generator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
    
    def generate(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=4000
            )
            text = response.choices[0].message.content.strip()
            text = re.sub(r'^```json?\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
            return json.loads(text)
        except Exception as e:
            st.error(f"Error: {e}")
            return None

# =============================================================================
# UI COMPONENTS
# =============================================================================

def lottie_welcome():
    st.markdown("""
    <div style="text-align:center; margin:2rem 0;">
        <lottie-player src="https://assets8.lottiefiles.com/packages/lf20_kkflmtur.json"
            background="transparent" speed="1" style="width:350px;height:350px;" loop autoplay></lottie-player>
    </div>
    """, unsafe_allow_html=True)

def trigger_confetti():
    st.markdown("""
    <script>
    confetti({particleCount:300, spread:100, origin:{y:0.6},
        colors:['#6366f1','#ec4899','#10b981','#f59e0b']});
    </script>
    """, unsafe_allow_html=True)

def live_previews(results):
    if not results: return

    headline = results.get("google_ads",{}).get("headlines",[""])[0]
    desc = results.get("google_ads",{}).get("descriptions",[""])[0]
    caption = results.get("instagram",{}).get("captions",[""])[0]
    hashtags = " ".join(results.get("instagram",{}).get("hashtags",[])[:12])

    st.markdown(f"""
    <div class="glass-card">
        <h3>Live Google Ads Preview</h3>
        <div style="background:#f8f9ff; padding:1.5rem; border-radius:16px; border:2px dashed #6366f1;">
            <h2 style="color:#1a73e8; font-size:1.4rem;">{headline}</h2>
            <p>{desc}</p>
            <p style="color:#0f9d58; font-weight:bold;">YourBrand.com → <span style="background:#1a73e8;color:white;padding:0.4rem 1rem;border-radius:20px;">Shop Now</span></p>
        </div>
    </div>

    <div class="glass-card" style="margin-top:1rem;">
        <h3>Instagram Post Preview</h3>
        <div style="background:white; border-radius:20px; overflow:hidden; box-shadow:0 15px 35px rgba(0,0,0,0.2);">
            <div style="background:var(--gradient-2); height:350px; display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">
                Image
            </div>
            <div style="padding:1.5rem;">
                <p><strong>YourBrand</strong> {caption[:120]}...</p>
                <p style="color:#888; font-size:0.9rem;">{hashtags}</p>
                <button style="background:var(--gradient-1); color:white; border:none; padding:0.8rem 2rem; border-radius:50px; font-weight:bold;">Get Offer</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    st.set_page_config(page_title="AI Sales Copy Agent 4.0", page_icon="✨", layout="wide")
    st.markdown(ULTIMATE_UI, unsafe_allow_html=True)
    init_db()

    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv("GROQ_API_KEY", "")

    with st.sidebar:
        st.markdown("<h1 style='color:#6366f1;'>AI Sales Agent</h1>", unsafe_allow_html=True)
        st.markdown("### Navigation")
        page = st.radio("Go to", ["Home", "Generate Content", "History"], label_visibility="collapsed")

        st.markdown("### Groq API Key (FREE)")
        key = st.text_input("Enter key", type="password", value=st.session_state.api_key)
        if key:
            st.session_state.api_key = key
            st.success("Connected!")

        st.markdown("[Get FREE Key](https://console.groq.com)")

    if page == "Home":
        lottie_welcome()
        st.markdown("""
        <div class="hero-header">
            <h1>Generate 10X Better Ads</h1>
            <p>Google • Facebook • Instagram • SEO • Landing Pages • Email</p>
            <p>100% FREE • Powered by Groq + Llama 3.3 70B</p>
        </div>
        """, unsafe_allow_html=True)

    elif page == "Generate Content":
        st.markdown("<h1 style='text-align:center; color:#6366f1;'>Generate Marketing Content</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            business_name = st.text_input("Business Name", placeholder="e.g. FitPulse Gym")
            product_service = st.text_area("Product/Service", height=100)
        with col2:
            target_audience = st.text_area("Target Audience", height=100)
            offer = st.text_input("Special Offer", placeholder="e.g. 70% OFF First Month")

        tone = st.selectbox("Tone", ["Exciting", "Professional", "Urgent", "Friendly", "Luxury"])

        if st.button("Generate Magic ✨", type="primary", use_container_width=True):
            if not st.session_state.api_key:
                st.error("Please add your Groq API key in sidebar")
            else:
                with st.spinner(""):
                    progress = st.progress(0)
                    status = st.empty()
                    for i in range(100):
                        time.sleep(0.02)
                        progress.progress(i+1)
                        status.text(["Analyzing...", "Writing headlines...", "Crafting copy...", "Adding magic..."][i//25])
                    
                    gen = Generator(st.session_state.api_key)
                    result = gen.generate(Prompts.all_platforms({
                        'business_name': business_name,
                        'product_service': product_service,
                        'target_audience': target_audience,
                        'offer': offer,
                        'tone': tone
                    }))

                    if result:
                        st.session_state.last_result = result
                        save_history({
                            'business_name': business_name,
                            'product_service': product_service,
                            'target_audience': target_audience,
                            'offer': offer,
                            'tone': tone
                        }, result)
                        trigger_confetti()
                        st.success("Generated Successfully!")
                        live_previews(result)

                        with st.expander("View Full JSON Output"):
                            st.json(result, expanded=False)

    elif page == "History":
        st.markdown("<h2>Generation History</h2>", unsafe_allow_html=True)
        conn = sqlite3.connect('sales_agent.db')
        df = pd.read_sql("SELECT * FROM history ORDER BY created_at DESC LIMIT 20", conn)
        if not df.empty:
            for _, row in df.iterrows():
                with st.expander(f"{row['business']} • {row['created_at'][:10]}"):
                    st.json(json.loads(row['outputs']))
        else:
            st.info("No history yet. Generate your first content!")

    # Floating Action Button
    st.markdown('<div class="fab" onclick="window.scrollTo(0,0)">Top</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()






