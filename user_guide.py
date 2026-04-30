import streamlit as st

st.set_page_config(page_title="PromptScanner – User Guide", layout="wide")

# ── GLOBAL STYLES ──
st.markdown("""
<style>
:root {
  --navy: #1a2340;
  --amber: #e8941a;
  --bg: #f5f0e8;
  --border: #e0d8cc;
}

body {
  background-color: var(--bg);
}

.section-header {
  border-bottom: 2px solid var(--navy);
  margin-top: 40px;
  margin-bottom: 20px;
}

.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.safe {background:#d4f5ee;}
.warn {background:#fef3dc;}
.flag {background:#fde8e8;}
.crit {background:#ede8fc;}

.card {
  background: white;
  padding: 18px;
  border-radius: 10px;
  border: 1px solid var(--border);
  margin-bottom: 10px;
}

.cover {
  background: var(--navy);
  color: white;
  padding: 50px;
  border-radius: 12px;
}

.cover span {
  color: var(--amber);
}

.step {
  background: white;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid var(--border);
  margin-bottom: 15px;
}

.footer {
  text-align:center;
  background: var(--navy);
  color: white;
  padding: 20px;
  margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# ── COVER ──
st.markdown("""
<div class="cover">
<h1>Prompt<span>Scanner</span></h1>
<p><b>Arabic AI Safety Tool</b></p>
<h3>User Guide</h3>
<p>Detect PII and toxic content in Arabic prompts before sending them to AI chatbots.</p>
</div>
""", unsafe_allow_html=True)

# ── SECTION 1 ──
st.markdown('<div class="section-header"><h2>1. What is PromptScanner?</h2></div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
PromptScanner analyses Arabic prompts before sending them to AI tools like ChatGPT.
<br><br>
✔ Detects personal information (PII)<br>
✔ Detects toxic / harmful content<br><br>
This helps protect your privacy and improves safe communication.
</div>
""", unsafe_allow_html=True)

# ── FLOW ──
st.markdown("### How it works")
col1, col2, col3, col4 = st.columns(4)
col1.markdown("📝 Type prompt")
col2.markdown("➡️ Press Scan")
col3.markdown("⚙️ Models run")
col4.markdown("📊 Results appear")

# ── COMPONENTS ──
st.markdown("### Components")

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="card">
    <b>AraBERT NER</b><br>
    Detects names, organisations, addresses, dates
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <b>Regex Engine</b><br>
    Detects phone, email, IP, financial info
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    <b>XLM-RoBERTa</b><br>
    Detects IDs and credentials
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <b>AraBERT Toxicity</b><br>
    Classifies harmful content
    </div>
    """, unsafe_allow_html=True)

# ── SECTION 2 ──
st.markdown('<div class="section-header"><h2>2. Interface Overview</h2></div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
<b>Main Parts:</b><br><br>
A — Model status panel<br>
B — Example prompts<br>
C — Text input area<br>
D — Scan / Clear buttons
</div>
""", unsafe_allow_html=True)

# ── SECTION 3 ──
st.markdown('<div class="section-header"><h2>3. How to Use</h2></div>', unsafe_allow_html=True)

st.markdown("""
<div class="step">
<b>1. Enter your Arabic prompt</b><br>
Type or paste your text into the input field.
</div>

<div class="step">
<b>2. Press فحص (Scan)</b><br>
The system analyzes your text instantly.
</div>

<div class="step">
<b>3. Review PII results</b><br>
<span class="badge safe">CLEAN</span> or detected entities shown.
</div>

<div class="step">
<b>4. Review toxicity result</b><br>
Shows category and confidence score.
</div>

<div class="step">
<b>5. Check keyword attention</b><br>
Highlighted words show influence on classification.
</div>

<div class="step">
<b>6. Use Rewrite feature</b><br>
Get a safer version of your prompt.
</div>
""", unsafe_allow_html=True)

# ── SECTION 4 ──
st.markdown('<div class="section-header"><h2>4. Understanding Results</h2></div>', unsafe_allow_html=True)

st.markdown("""
### Toxicity Levels

- SAFE → No harmful content  
- WARNING → Mild issues  
- FLAGGED → Harmful  
- CRITICAL → Sensitive / mental health  
""")

# ── SECTION 5 ──
st.markdown('<div class="section-header"><h2>5. Tips</h2></div>', unsafe_allow_html=True)

st.markdown("""
<div class="step">✔ Always scan before sending</div>
<div class="step">✔ Use masked text</div>
<div class="step">✔ Use full sentences</div>
<div class="step">✔ Check confidence score</div>
<div class="step">⚠ Tool assists but isn’t perfect</div>
""", unsafe_allow_html=True)

# ── SECTION 6 ──
st.markdown('<div class="section-header"><h2>6. Quick Reference</h2></div>', unsafe_allow_html=True)

st.markdown("""
- Scan → Press فحص  
- Clear → Press مسح  
- Try examples → Sidebar  
- Dark mode → 🌙  
- Language → EN / AR  
""")

# ── FOOTER ──
st.markdown("""
<div class="footer">
PromptScanner — User Guide · Final Year Project
</div>
""", unsafe_allow_html=True)
