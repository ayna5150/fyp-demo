import streamlit as st
from pathlib import Path
import base64

# ─────────────────────────────────────────────────────────────
# CSS — matches app.py brand exactly
# ─────────────────────────────────────────────────────────────
def get_guide_css():
    return """
    :root {
        --bg:      #EAE4D9; --card: #F3EDE3; --white: #FDFAF5;
        --navy:    #0F1C35; --ink:  #1A1714; --muted: #7A7068;
        --border:  rgba(0,0,0,0.08);
    }
    html, body, [class*="css"] { background: var(--bg) !important; color: var(--ink) !important; }
    """

GUIDE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 900px; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.stApp,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],
[data-testid="stHeader"],[data-testid="stBottomBlockContainer"],.main .block-container {
    background: var(--bg) !important; color: var(--ink) !important;
}

/* ── HEADER ── */
.guide-hero {
    background: var(--navy);
    color: #EAE4D9;
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 2rem;
    direction: rtl;
}
.guide-hero-logo { font-weight: 800; font-size: 1.9rem; letter-spacing: -1px; color: #EAE4D9; }
.guide-hero-logo span { color: #E8520A; }
.guide-hero-sub { font-family: 'JetBrains Mono', monospace !important; font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(234,228,217,0.5); margin-top: 3px; }
.guide-hero-title { font-size: 1.4rem; font-weight: 300; color: rgba(234,228,217,0.85); margin-top: 18px; margin-bottom: 8px; }
.guide-hero-desc { font-size: 0.9rem; color: rgba(234,228,217,0.6); line-height: 1.7; max-width: 560px; }
.guide-rule { height: 3px; background: linear-gradient(90deg, #E8520A, transparent 60%); margin-top: 20px; border-radius: 2px; }

/* ── SECTION HEADERS ── */
.sec-head {
    display: flex; align-items: center; gap: 12px;
    flex-direction: row-reverse;
    justify-content: flex-end;
    margin: 36px 0 18px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--navy);
    direction: rtl;
    text-align: right;
}
.sec-num {
    background: var(--navy); color: #EAE4D9;
    font-weight: 800; font-size: 0.88rem;
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; font-family: 'JetBrains Mono', monospace !important;
}
.sec-title { font-size: 1.15rem; font-weight: 700; color: var(--navy); }

/* ── CARDS ── */
.guide-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; padding: 18px 20px; margin-bottom: 12px;
}
.guide-card-orange { border-top: 3px solid #E8520A; }
.guide-card-blue   { border-top: 3px solid #2D5BE3; }
.guide-card-teal   { border-top: 3px solid #00C9A7; }
.guide-card-purple { border-top: 3px solid #6B4FBB; }
.guide-card-navy   { border-top: 3px solid #0F1C35; }

/* ── STEP ROWS ── */
.step-wrap { display: flex; flex-direction: row; gap: 0; margin-bottom: 0; direction: rtl; }
.step-left { display: flex; flex-direction: column; align-items: center; width: 44px; flex-shrink: 0; margin-right: 0; margin-left: 10px; }
.step-num {
    width: 30px; height: 30px; border-radius: 50%;
    background: var(--navy); color: #EAE4D9;
    font-weight: 800; font-size: 0.82rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; z-index: 1;
    font-family: 'JetBrains Mono', monospace !important;
}
.step-line { width: 2px; flex: 1; min-height: 16px; background: var(--border); margin-top: 4px; }
.step-body {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px 16px;
    margin-bottom: 10px; flex: 1; text-align: right;
}
.step-label { font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: var(--navy); }
.step-desc  { color: var(--muted); font-size: 0.86rem; line-height: 1.65; }

/* ── CALLOUTS ── */
.callout {
    border-radius: 10px; padding: 12px 16px; margin: 12px 0;
    font-size: 0.87rem; display: flex; gap: 10px; align-items: flex-start;
    direction: rtl; text-align: right;
}
.callout-tip  { background: rgba(45,91,227,0.06); border-right: 3px solid #2D5BE3; }
.callout-warn { background: rgba(232,82,10,0.06);  border-right: 3px solid #E8520A; }

/* ── FLOW DIAGRAM ── */
.flow { display: flex; justify-content: center; align-items: center; gap: 0; margin: 16px auto; flex-wrap: wrap; }
.flow-node {
    background: var(--navy); color: #EAE4D9;
    border-radius: 8px; padding: 8px 14px;
    font-size: 0.8rem; font-weight: 600; text-align: center;
    min-width: 110px; flex-shrink: 0; line-height: 1.4;
}
.flow-orange { background: #E8520A !important; }
.flow-teal   { background: #00C9A7 !important; color: #0F1C35 !important; }
.flow-arr    { font-size: 1rem; color: var(--muted); padding: 0 4px; flex-shrink: 0; }

/* ── MODEL PILLS ── */
.model-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0; }
.model-card { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; direction: rtl; text-align: right; }
.model-name { font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-bottom: 6px; }
.model-name-orange { background: #E8520A; color: #fff; }
.model-name-blue   { background: #2D5BE3; color: #fff; }
.model-desc { font-size: 0.82rem; color: var(--muted); line-height: 1.5; margin-bottom: 7px; }
.model-cats { display: flex; flex-wrap: wrap; gap: 4px; justify-content: flex-start; direction: rtl; }
.cat-pill   { font-size: 0.67rem; font-weight: 700; padding: 2px 7px; border-radius: 8px; letter-spacing: 0.02em; font-family: 'JetBrains Mono', monospace !important; }

/* ── PII TABLE ── */
.pii-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; margin: 12px 0; direction: rtl; text-align: right; }
.pii-table th { background: var(--navy); color: #EAE4D9; padding: 8px 12px; text-align: right; font-size: 0.73rem; letter-spacing: 0.06em; text-transform: uppercase; font-family: 'JetBrains Mono', monospace !important; }
.pii-table td { padding: 8px 12px; border-bottom: 1px solid var(--border); text-align: right; }
.pii-table tr:nth-child(even) td { background: var(--white); }
.pii-tag { display: inline-block; background: rgba(232,82,10,0.10); color: #E8520A; border: 1px solid rgba(232,82,10,0.3); border-radius: 4px; padding: 1px 6px; font-size: 0.68rem; font-family: 'JetBrains Mono', monospace !important; font-weight: 700; }

.qr-table { width: 100%; border-collapse: collapse; font-size: 0.86rem; margin: 12px 0; direction: rtl; text-align: right; }
.qr-table th { background: var(--navy); color: #EAE4D9; padding: 8px 12px; text-align: right; font-size: 0.73rem; text-transform: uppercase; font-family: 'JetBrains Mono', monospace !important; }
.qr-table td { padding: 9px 12px; border-bottom: 1px solid var(--border); text-align: right; }
.qr-table tr:nth-child(even) td { background: var(--white); }
.qr-table td:first-child { font-weight: 600; color: var(--navy); }

/* ── TOX BADGES ── */
.badge { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.04em; font-family: 'JetBrains Mono', monospace !important; }
.b-safe   { background: rgba(0,201,167,0.10); color: #00C9A7;  border: 1px solid rgba(0,201,167,0.3); }
.b-warn   { background: rgba(232,82,10,0.10); color: #E8520A;  border: 1px solid rgba(232,82,10,0.3); }
.b-flag   { background: rgba(217,48,37,0.10); color: #D93025;  border: 1px solid rgba(217,48,37,0.3); }
.b-crit   { background: rgba(107,79,187,0.10);color: #6B4FBB;  border: 1px solid rgba(107,79,187,0.3); }

/* ── EXT POPUP MOCKUP ── */
.ext-popup { background: #EAE4D9; border: 1px solid rgba(0,0,0,0.1); border-radius: 14px; overflow: hidden; width: 290px; box-shadow: 0 8px 32px rgba(15,28,53,0.15); }
.ext-hdr { background: #F3EDE3; padding: 10px 13px 8px; border-bottom: 1px solid rgba(0,0,0,0.08); display: flex; align-items: center; justify-content: space-between; }
.ext-logo-txt { font-weight: 800; font-size: 0.88rem; color: #0F1C35; }
.ext-logo-txt span { color: #E8520A; }
.ext-logo-sub { font-size: 0.58rem; color: #7A7068; font-family: 'JetBrains Mono', monospace !important; }
.ext-gear { width: 26px; height: 26px; background: rgba(0,0,0,0.06); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; color: #7A7068; }
.ext-elapsed { text-align: center; padding: 5px 13px 2px; font-size: 0.62rem; color: #7A7068; font-family: 'JetBrains Mono', monospace !important; }
.ext-sec { padding: 7px 12px 3px; }
.ext-sec-t { font-size: 0.72rem; font-weight: 700; color: #0F1C35; margin-bottom: 5px; }
.ext-tbox { background: #FDFAF5; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 8px 10px; font-size: 0.78rem; line-height: 1.7; direction: rtl; text-align: right; color: #1A1714; min-height: 44px; }
.ext-tox-card { background: #FDFAF5; border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; padding: 9px 11px; }
.ext-tox-name { font-size: 1rem; font-weight: 800; }
.ext-tox-cf { font-size: 0.68rem; color: #7A7068; margin: 2px 0 5px; }
.ext-bar { background: rgba(0,0,0,0.08); border-radius: 3px; height: 5px; overflow: hidden; }
.ext-bar-f { height: 100%; border-radius: 3px; }
.ext-hl { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 3px; padding: 5px 2px; direction: rtl; }
.ext-div { height: 1px; background: rgba(0,0,0,0.08); margin: 6px 12px; }
.ext-btn-navy { background: #0F1C35; color: #EAE4D9; border-radius: 9px; padding: 8px 10px; text-align: center; font-weight: 700; font-size: 0.76rem; margin: 3px 0; font-family: 'JetBrains Mono', monospace !important; }
.ext-btn-orange { background: #E8520A; color: #fff; border-radius: 9px; padding: 8px 10px; text-align: center; font-weight: 700; font-size: 0.76rem; margin: 3px 0; font-family: 'JetBrains Mono', monospace !important; }
.ext-btn-teal { background: #00C9A7; color: #0F1C35; border-radius: 9px; padding: 8px 10px; text-align: center; font-weight: 700; font-size: 0.76rem; margin: 3px 0; font-family: 'JetBrains Mono', monospace !important; }
.ext-btn-ghost { background: transparent; color: #7A7068; border: 1px solid rgba(0,0,0,0.1); border-radius: 9px; padding: 8px 10px; text-align: center; font-size: 0.76rem; margin: 3px 0; }
.ext-set-row { display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid rgba(0,0,0,0.06); }
.ext-set-row:last-child { border-bottom: none; }
.ext-set-lbl { font-weight: 700; font-size: 0.8rem; color: #0F1C35; }
.ext-set-sub { font-size: 0.67rem; color: #7A7068; margin-top: 1px; }
.ext-tog-on  { width: 36px; height: 20px; background: #E8520A; border-radius: 10px; position: relative; flex-shrink: 0; }
.ext-tog-off { width: 36px; height: 20px; background: rgba(0,0,0,0.15); border-radius: 10px; position: relative; flex-shrink: 0; }
.ext-tog-k-on  { width: 14px; height: 14px; background: #fff; border-radius: 50%; position: absolute; top: 3px; left: 19px; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
.ext-tog-k-off { width: 14px; height: 14px; background: #fff; border-radius: 50%; position: absolute; top: 3px; left: 3px; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
.ext-lang { display: flex; gap: 4px; }
.ext-lang-active { padding: 3px 9px; border-radius: 5px; font-size: 0.7rem; font-weight: 700; background: #E8520A; color: #fff; }
.ext-lang-off    { padding: 3px 9px; border-radius: 5px; font-size: 0.7rem; font-weight: 700; background: rgba(0,0,0,0.06); color: #7A7068; }

/* ── ANNOTATION PANEL ── */
.ann-panel { background: var(--white); border: 1px solid var(--border); border-radius: 12px; padding: 12px 16px; }
.ann-row { display: flex; gap: 10px; align-items: flex-start; padding: 7px 0; border-bottom: 1px solid var(--border); font-size: 0.85rem; direction: rtl; text-align: right; line-height: 1.6; }
.ann-row:last-child { border-bottom: none; }
.ann-dot { width: 20px; height: 20px; border-radius: 50%; background: #E8520A; color: #fff; font-weight: 800; font-size: 0.62rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-family: 'JetBrains Mono', monospace !important; }

/* ── BUTTONS ── */
div[data-testid="stButton"] button {
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important;
    font-size: .82rem !important; border: none !important; border-radius: 10px !important;
    padding: .5rem 1.4rem !important; transition: all .2s !important;
    cursor: pointer !important; white-space: nowrap !important;
}
div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }
div[data-testid="stButton"] button[kind="primary"] {
    background: #E8520A !important; color: #fff !important;
}
div[data-testid="stButton"] button[kind="secondary"] {
    background: var(--card) !important; color: var(--muted) !important;
    box-shadow: none !important; border: 1px solid var(--border) !important;
}

/* ── HIGHLIGHT WORDS ── */
.hl-h { display:inline-block;border-radius:4px;padding:2px 6px;margin:1px;font-size:.8rem;background:rgba(217,48,37,0.75);color:#fff;font-weight:700; }
.hl-m { display:inline-block;border-radius:4px;padding:2px 6px;margin:1px;font-size:.8rem;background:rgba(217,48,37,0.40);color:#c0392b;font-weight:600; }
.hl-l { display:inline-block;border-radius:4px;padding:2px 6px;margin:1px;font-size:.8rem;background:rgba(217,48,37,0.15);color:#c0392b; }
.hl-s { display:inline-block;border-radius:4px;padding:2px 6px;margin:1px;font-size:.8rem;background:rgba(0,0,0,0.05);color:#aaa; }

/* ── FOOTER ── */
.guide-footer { background: var(--navy); color: rgba(234,228,217,0.5); text-align: center; padding: 18px; font-size: 0.75rem; border-radius: 12px; margin-top: 3rem; }
.guide-footer span { color: #E8520A; }
"""

def inject_css():
    st.markdown(f"<style>{get_guide_css()}{GUIDE_CSS}</style>", unsafe_allow_html=True)

def img_b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

# ─────────────────────────────────────────────────────────────
# LANGUAGE STRINGS
# ─────────────────────────────────────────────────────────────
LANG = {
    "ar": {
        "lang_btn":   "EN",
        "hero_sub":   "حارس خصوصيتك في عالم الذكاء الاصطناعي",
        "hero_title": "دليل المستخدم",
        "hero_desc":  "تعليمات خطوة بخطوة لاستخدام PromptScanner للكشف عن المعلومات الشخصية والمحتوى الضار في مطالباتك العربية قبل إرسالها إلى روبوتات الدردشة.",
        "tab1":       "الجزء الأول — الموقع الإلكتروني",
        "tab2":       "الجزء الثاني — إضافة المتصفح",
        "footer_web": "دليل المستخدم · الجزء الأول: الموقع الإلكتروني",
        "footer_ext": "دليل المستخدم · الجزء الثاني: إضافة المتصفح",
    },
    "en": {
        "lang_btn":   "عربي",
        "hero_sub":   "Your Privacy Guardian in the AI World",
        "hero_title": "User Guide",
        "hero_desc":  "Step-by-step instructions for using PromptScanner to detect personal information and harmful content in your Arabic prompts before sending them to AI chatbots.",
        "tab1":       "Part 1 — Website",
        "tab2":       "Part 2 — Browser Extension",
        "footer_web": "User Guide · Part 1: Website",
        "footer_ext": "User Guide · Part 2: Browser Extension",
    },
}

# ─────────────────────────────────────────────────────────────
# HELPER RENDERERS
# ─────────────────────────────────────────────────────────────
def hero(logo_b64, lang="ar"):
    L = LANG[lang]
    rtl_style = "direction:rtl;text-align:right;" if lang == "ar" else "direction:ltr;text-align:left;"
    st.markdown(f"""
<div class="guide-hero" style="{rtl_style}">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;{'flex-direction:row-reverse;' if lang=='en' else ''}">
    <img src="data:image/png;base64,{logo_b64}"
         style="width:46px;height:46px;border-radius:10px;object-fit:contain;" />
    <div>
      <div class="guide-hero-logo">Prompt<span>Scanner</span></div>
      <div class="guide-hero-sub">{L["hero_sub"]}</div>
    </div>
  </div>
  <div class="guide-hero-title">{L["hero_title"]}</div>
  <p class="guide-hero-desc">{L["hero_desc"]}</p>
  <div class="guide-rule"></div>
</div>
""", unsafe_allow_html=True)


def sec(num, title):
    st.markdown(f"""
<div class="sec-head" style="direction:rtl;text-align:right;">
  <div class="sec-num">{num}</div>
  <div class="sec-title">{title}</div>
</div>""", unsafe_allow_html=True)


def step_item(num, label, desc, last=False):
    line = "" if last else '<div class="step-line"></div>'
    st.markdown(f"""
<div class="step-wrap">
  <div class="step-body">
    <div class="step-label">{label}</div>
    <div class="step-desc">{desc}</div>
  </div>
  <div class="step-left">
    <div class="step-num">{num}</div>
    {line}
  </div>
</div>""", unsafe_allow_html=True)


def tip(text, warn=False):
    kind = "warn" if warn else "tip"
    icon = "⚠" if warn else "💡"
    st.markdown(
        f'<div class="callout callout-{kind}"><span style="font-size:1rem">{icon}</span>'
        f'<div>{text}</div></div>',
        unsafe_allow_html=True
    )


def flow(*nodes):
    # Reverse order for RTL — rightmost node first visually
    reversed_nodes = list(reversed(nodes))
    parts = []
    for i, (label, cls) in enumerate(reversed_nodes):
        parts.append(f'<div class="flow-node {cls}">{label}</div>')
        if i < len(reversed_nodes) - 1:
            parts.append('<div class="flow-arr">←</div>')
    st.markdown(
        f'<div class="flow" style="direction:rtl;">{"".join(parts)}</div>',
        unsafe_allow_html=True
    )


def ann_panel(items):
    rows = "".join(
        f'<div class="ann-row"><div class="ann-dot">{label}</div><div>{text}</div></div>'
        for label, text in items
    )
    st.markdown(f'<div class="ann-panel">{rows}</div>', unsafe_allow_html=True)


def popup_with_ann(popup_html, items):
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown(popup_html, unsafe_allow_html=True)
    with c2:
        ann_panel(items)


# ─────────────────────────────────────────────────────────────
# POPUP MOCKUPS — using real Arabic strings from popup.js
# ─────────────────────────────────────────────────────────────
def popup_header(logo_b64, gear_active=False):
    gear_style = "background:#E8520A;color:#fff;" if gear_active else ""
    return f"""
  <div class="ext-hdr">
    <div style="display:flex;align-items:center;gap:8px;">
      <img src="data:image/png;base64,{logo_b64}"
           style="width:24px;height:24px;border-radius:6px;object-fit:contain;" />
      <div>
        <div class="ext-logo-txt">Prompt<span>Scanner</span></div>
        <div class="ext-logo-sub">فحص الخصوصية والسلامة</div>
      </div>
    </div>
    <div class="ext-gear" style="{gear_style}">{'✕' if gear_active else '⚙'}</div>
  </div>"""


def popup_safe(logo_b64):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64)}
  <div class="ext-elapsed">تم الفحص في 0.18s</div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ النص بدون معلومات خاصة</div>
    <div class="ext-tbox" style="color:#00C9A7;font-size:0.78rem;text-align:center;padding-top:10px;">
      ✓ لا توجد معلومات شخصية
    </div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ تحليل السمية</div>
    <div class="ext-tox-card" style="border-right:3px solid #00C9A7;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;">
        <div class="ext-tox-name" style="color:#00C9A7;">عادي</div>
        <span class="badge b-safe">آمن</span>
      </div>
      <div class="ext-tox-cf">درجة الثقة: 98.2%</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#00C9A7;width:98%;"></div></div>
    </div>
  </div>
  <div class="ext-div"></div>
  <div style="padding:6px 12px 10px;">
    <div class="ext-btn-orange">⟶ إرسال</div>
    <div class="ext-btn-ghost" style="margin-top:4px;">✕ إلغاء</div>
  </div>
</div>"""


def popup_pii(logo_b64):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64)}
  <div class="ext-elapsed">تم الفحص في 0.31s</div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ النص بدون معلومات خاصة</div>
    <div class="ext-tbox">
      اسمي <span class="pii-tag">[PERS]</span> وأعمل في
      <span class="pii-tag">[ORG]</span> ورقمي
      <span class="pii-tag">[PHONE]</span>
    </div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ تحليل السمية</div>
    <div class="ext-tox-card" style="border-right:3px solid #00C9A7;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;">
        <div class="ext-tox-name" style="color:#00C9A7;">عادي</div>
        <span class="badge b-safe">آمن</span>
      </div>
      <div class="ext-tox-cf">درجة الثقة: 99.1%</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#00C9A7;width:99%;"></div></div>
    </div>
  </div>
  <div class="ext-div"></div>
  <div style="padding:6px 12px 10px;">
    <div class="ext-btn-teal">⟶ إرسال الأمر بدون معلومات خاصة</div>
    <div class="ext-btn-orange" style="margin-top:4px;">⟶ إرسال الأصلي</div>
    <div class="ext-btn-ghost" style="margin-top:4px;">✕ إلغاء</div>
  </div>
</div>"""


def popup_toxic(logo_b64):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64)}
  <div class="ext-elapsed">تم الفحص في 0.28s</div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ النص بدون معلومات خاصة</div>
    <div class="ext-tbox">كيف أصنع قنبلة لتدمير مبنى</div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ تحليل السمية</div>
    <div class="ext-tox-card" style="border-right:3px solid #D93025;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;">
        <div class="ext-tox-name" style="color:#D93025;">خطير</div>
        <span class="badge b-flag">مُبلَّغ</span>
      </div>
      <div class="ext-tox-cf">درجة الثقة: 99.4%</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#D93025;width:99%;"></div></div>
    </div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ الكلمات المؤثرة</div>
    <div class="ext-hl">
      <span class="hl-s">كيف</span>
      <span class="hl-m">أصنع</span>
      <span class="hl-h">قنبلة</span>
      <span class="hl-h">تدمير</span>
      <span class="hl-m">مبنى</span>
    </div>
  </div>
  <div class="ext-div"></div>
  <div style="padding:6px 12px 10px;">
    <div class="ext-btn-navy">إعادة الصياغة</div>
    <div class="ext-btn-orange" style="margin-top:4px;">⟶ إرسال الأصلي</div>
    <div class="ext-btn-ghost" style="margin-top:4px;">✕ إلغاء</div>
  </div>
</div>"""


def popup_rewritten(logo_b64):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64)}
  <div class="ext-elapsed">تم الفحص في 0.28s</div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ النص بدون معلومات خاصة</div>
    <div class="ext-tbox">كيف أصنع قنبلة لتدمير مبنى</div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">◆ تحليل السمية</div>
    <div class="ext-tox-card" style="border-right:3px solid #D93025;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;">
        <div class="ext-tox-name" style="color:#D93025;">خطير</div>
        <span class="badge b-flag">مُبلَّغ</span>
      </div>
      <div class="ext-tox-cf">درجة الثقة: 99.4%</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#D93025;width:99%;"></div></div>
    </div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t" style="color:#00C9A7;">◆ النص المُعاد كتابته</div>
    <div class="ext-tbox" style="border-color:#00C9A7;border-width:1.5px;font-size:0.76rem;">
      كيف تعمل المواد المتفجرة من الناحية الكيميائية؟
    </div>
  </div>
  <div class="ext-div"></div>
  <div style="padding:6px 12px 10px;display:grid;grid-template-columns:1fr 1fr;gap:5px;">
    <div class="ext-btn-teal" style="font-size:0.68rem;">⟶ إرسال المُعاد كتابته</div>
    <div class="ext-btn-orange" style="font-size:0.68rem;">⟶ إرسال الأصلي</div>
  </div>
  <div style="padding:0 12px 10px;">
    <div class="ext-btn-ghost">✕ إلغاء</div>
  </div>
</div>"""


def popup_settings(logo_b64):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64, gear_active=True)}
  <div style="padding:10px 13px;">
    <div style="background:#FDFAF5;border:1px solid rgba(0,0,0,0.08);border-radius:10px;padding:8px 13px;margin-bottom:8px;">
      <div style="font-size:0.72rem;font-weight:700;color:#7A7068;text-transform:uppercase;letter-spacing:0.12em;padding:6px 0 8px;border-bottom:1px solid rgba(0,0,0,0.06);margin-bottom:4px;">◆ المظهر</div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">الوضع الداكن</div><div class="ext-set-sub">تفعيل المظهر الداكن</div></div>
        <div class="ext-tog-off"><div class="ext-tog-k-off"></div></div>
      </div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">اللغة</div><div class="ext-set-sub">لغة واجهة الإضافة</div></div>
        <div class="ext-lang"><div class="ext-lang-active">العربية</div><div class="ext-lang-off">English</div></div>
      </div>
    </div>
    <div style="background:#FDFAF5;border:1px solid rgba(0,0,0,0.08);border-radius:10px;padding:8px 13px;margin-bottom:8px;">
      <div style="font-size:0.72rem;font-weight:700;color:#7A7068;text-transform:uppercase;letter-spacing:0.12em;padding:6px 0 8px;border-bottom:1px solid rgba(0,0,0,0.06);margin-bottom:4px;">◆ السلوك</div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">عرض النافذة للمحتوى الآمن</div><div class="ext-set-sub">إذا كان آمناً اعرض النافذة، وإلا أرسل تلقائياً</div></div>
        <div class="ext-tog-on"><div class="ext-tog-k-on"></div></div>
      </div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">الفحص التلقائي</div><div class="ext-set-sub">فحص المحتوى عند الضغط على إرسال أو Enter</div></div>
        <div class="ext-tog-on"><div class="ext-tog-k-on"></div></div>
      </div>
    </div>
    <div style="background:#E8520A;color:#fff;border-radius:10px;padding:10px;text-align:center;font-weight:700;font-size:0.84rem;">✓ حفظ الإعدادات</div>
  </div>
</div>"""


# ─────────────────────────────────────────────────────────────
# WEBSITE GUIDE
# ─────────────────────────────────────────────────────────────
def render_website(logo_b64):

    # ── 1. ما هو PromptScanner ──────────────────────────────
    sec("1", "ما هو PromptScanner؟")
    st.markdown("""
<div style="background:#0F1C35;color:rgba(234,228,217,0.85);border-radius:12px;
            padding:18px 22px;margin:12px 0 18px;line-height:1.7;
            font-size:0.92rem;direction:rtl;text-align:right;">
يحلل <strong>PromptScanner</strong> نصوصك العربية <strong>قبل</strong> إرسالها إلى روبوت الدردشة.
يكتشف المعلومات الشخصية الحساسة ويفحص المحتوى الضار في وقت واحد،
لحماية خصوصيتك وتعزيز سلامة تفاعلاتك مع الذكاء الاصطناعي.
</div>""", unsafe_allow_html=True)

    flow(
        ("اكتب نصك", ""),
        ("اضغط فحص", "flow-orange"),
        ("4 نماذج تعمل معاً", "flow-teal"),
        ("تظهر النتائج", ""),
    )

    # ── 2. النماذج المستخدمة ─────────────────────────────────
    sec("2", "النماذج المستخدمة")
    st.markdown("""
<div class="model-grid">
  <div class="model-card">
    <div><span class="model-name model-name-orange">AraBERT NER</span></div>
    <div class="model-desc">يكتشف الأسماء والمؤسسات والعناوين والتواريخ باستخدام نموذج لغوي عربي مدرَّب خصيصاً.</div>
    <div class="model-cats">
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">PERS</span>
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">ORG</span>
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">ADDRESS</span>
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">DATETIME</span>
    </div>
  </div>
  <div class="model-card">
    <div><span class="model-name model-name-orange">XLM-RoBERTa</span></div>
    <div class="model-desc">يكتشف أرقام الهوية وبيانات الدخول، بما فيها القيم اللاتينية داخل الجمل العربية.</div>
    <div class="model-cats">
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">ID</span>
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">CREDENTIAL</span>
    </div>
  </div>
  <div class="model-card">
    <div><span class="model-name model-name-orange">Regex Engine</span></div>
    <div class="model-desc">كشف مبني على أنماط ثابتة للهاتف والبريد الإلكتروني وعناوين IP والروابط والمعلومات المالية.</div>
    <div class="model-cats">
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">PHONE</span>
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">EMAIL</span>
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">IP</span>
      <span class="cat-pill" style="background:rgba(232,82,10,0.1);color:#E8520A;">URL</span>
    </div>
  </div>
  <div class="model-card">
    <div><span class="model-name model-name-blue">AraBERT v2</span></div>
    <div class="model-desc">يصنّف النص إلى 7 فئات أمان مع إبراز الكلمات التي أثّرت في قرار التصنيف.</div>
    <div class="model-cats">
      <span class="cat-pill" style="background:rgba(45,91,227,0.1);color:#2D5BE3;">7 فئات</span>
      <span class="cat-pill" style="background:rgba(45,91,227,0.1);color:#2D5BE3;">تحليل الكلمات</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── 3. خطوة بخطوة ────────────────────────────────────────
    sec("3", "خطوة بخطوة")
    tip("يمكنك النقر على أي <strong>زر مثال</strong> في الشريط الأيسر لتحميل نص تجريبي جاهز دون الحاجة للكتابة.")

    step_item("1", "أدخل نصك العربي",
              "انقر في حقل الإدخال واكتب أو الصق النص العربي. يمكنك أيضاً الضغط على أحد أزرار الأمثلة في الشريط الأيسر.")
    step_item("2", "اضغط فحص",
              "تعمل جميع النماذج الأربعة في آنٍ واحد. تظهر النتائج خلال 1-2 ثانية. اضغط مسح للبدء من جديد.")
    step_item("3", "اقرأ نتيجة المعلومات الشخصية (البطاقة اليسرى)",
              "تُظهر إما «آمن» إذا لم تُكتشف معلومات شخصية، أو النص المُقنَّع مع بطاقات ملونة تُعدّد كل كيان ونوعه والنموذج الذي اكتشفه (RGX / NER / XLM).")
    step_item("4", "اقرأ نتيجة تحليل السمية (البطاقة اليمنى)",
              "تُظهر الفئة المتوقعة ودرجة الثقة وتفصيل كامل للفئات السبع مع شارة تُشير إلى مستوى الخطورة.")
    step_item("5", "اقرأ خريطة الكلمات المؤثرة",
              "كل كلمة مُلوَّنة بحسب مدى تأثيرها في قرار التصنيف. اللون الداكن يعني تأثيراً أعلى. حروف الوصل تظهر باللون الرمادي.")
    step_item("6", "استخدم إعادة الصياغة (عند الحاجة)",
              "عند اكتشاف محتوى ضار يظهر قسم إعادة الصياغة. يعرض نسخة آمنة بديلة مع الحفاظ على المعنى الأصلي قدر الإمكان.",
              last=True)

    tip("استخدم دائماً <strong>النص المُقنَّع</strong> بدلاً من النص الأصلي عند إرسال مطالبتك — روبوت الدردشة سيفهم طلبك دون استقبال بياناتك الشخصية.")

    # ── 4. أنواع المعلومات الشخصية ───────────────────────────
    sec("4", "أنواع المعلومات الشخصية المكتشفة")
    st.markdown("""
<table class="pii-table">
  <thead><tr>
    <th>البطاقة</th><th>النوع</th><th>مثال</th><th>يكتشفه</th>
  </tr></thead>
  <tbody>
    <tr><td><span class="pii-tag">[PERS]</span></td><td>اسم شخص</td><td>أحمد المقبالي</td><td>AraBERT NER</td></tr>
    <tr><td><span class="pii-tag">[ORG]</span></td><td>مؤسسة</td><td>بنك مسقط</td><td>AraBERT NER</td></tr>
    <tr><td><span class="pii-tag">[ADDRESS]</span></td><td>موقع / عنوان</td><td>مسقط، عُمان</td><td>AraBERT NER</td></tr>
    <tr><td><span class="pii-tag">[DATETIME]</span></td><td>تاريخ / وقت</td><td>الثلاثاء 5 مارس</td><td>AraBERT NER</td></tr>
    <tr><td><span class="pii-tag">[ID]</span></td><td>رقم هوية / جواز سفر</td><td>12345678</td><td>XLM-RoBERTa</td></tr>
    <tr><td><span class="pii-tag">[CREDENTIAL]</span></td><td>كلمة مرور / PIN</td><td>MyPass123!</td><td>XLM-RoBERTa</td></tr>
    <tr><td><span class="pii-tag">[PHONE]</span></td><td>رقم هاتف</td><td>+968 91234567</td><td>Regex</td></tr>
    <tr><td><span class="pii-tag">[EMAIL]</span></td><td>بريد إلكتروني</td><td>ahmed@squ.edu.om</td><td>Regex</td></tr>
    <tr><td><span class="pii-tag">[IP]</span></td><td>عنوان IP</td><td>192.168.1.1</td><td>Regex</td></tr>
    <tr><td><span class="pii-tag">[URL]</span></td><td>رابط إنترنت</td><td>https://example.com</td><td>Regex</td></tr>
    <tr><td><span class="pii-tag">[FINANCIAL_INFO]</span></td><td>رقم بطاقة / IBAN</td><td>OM21BMI…</td><td>Regex</td></tr>
  </tbody>
</table>""", unsafe_allow_html=True)

    # ── 5. فئات السمية ───────────────────────────────────────
    sec("5", "فئات تحليل السمية")
    st.markdown("""
<table class="pii-table">
  <thead><tr><th>الفئة</th><th>الشارة</th><th>المعنى</th></tr></thead>
  <tbody>
    <tr><td>عادي</td><td><span class="badge b-safe">آمن</span></td><td>لا يوجد محتوى ضار</td></tr>
    <tr><td>مسيء بشكل خفيف</td><td><span class="badge b-warn">تحذير</span></td><td>محتوى مسيء خفيف</td></tr>
    <tr><td>مسيء</td><td><span class="badge b-warn">تحذير</span></td><td>محتوى مسيء واضح</td></tr>
    <tr><td>انتهاك الخصوصية</td><td><span class="badge b-warn">تحذير</span></td><td>يتضمن طلباً ينتهك الخصوصية</td></tr>
    <tr><td>محتوى فاضح</td><td><span class="badge b-flag">مُبلَّغ</span></td><td>محتوى غير لائق</td></tr>
    <tr><td>خطير</td><td><span class="badge b-flag">مُبلَّغ</span></td><td>محتوى خطير يستدعي التنبيه</td></tr>
    <tr><td>محتوى نفسي</td><td><span class="badge b-crit">خطر</span></td><td>يتضمن مؤشرات تستدعي العناية</td></tr>
  </tbody>
</table>""", unsafe_allow_html=True)

    # ── 6. مرجع سريع ─────────────────────────────────────────
    sec("6", "مرجع سريع")
    st.markdown("""
<table class="qr-table">
  <thead><tr><th>الإجراء</th><th>الطريقة</th></tr></thead>
  <tbody>
    <tr><td>فحص نص</td><td>اكتب أو الصق النص ← اضغط فحص</td></tr>
    <tr><td>مسح حقل الإدخال</td><td>اضغط مسح (يظهر بعد الفحص)</td></tr>
    <tr><td>تجربة مثال جاهز</td><td>انقر أحد أزرار الأمثلة في الشريط الأيسر</td></tr>
    <tr><td>التبديل بين الوضع الليلي/النهاري</td><td>انقر 🌙 في أعلى يمين الصفحة</td></tr>
    <tr><td>تغيير لغة الواجهة</td><td>انقر EN / عربي في أعلى يمين الصفحة</td></tr>
    <tr><td>معرفة النموذج الذي اكتشف الكيان</td><td>تحقق من التسمية الصغيرة (RGX / NER / XLM) على كل بطاقة</td></tr>
    <tr><td>الحصول على إعادة صياغة آمنة</td><td>اضغط «إعادة الصياغة» في قسم النتائج</td></tr>
  </tbody>
</table>""", unsafe_allow_html=True)

    st.markdown("""
<div class="guide-footer">
  <span>PromptScanner</span> — دليل المستخدم · الجزء الأول: الموقع الإلكتروني
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# EXTENSION GUIDE
# ─────────────────────────────────────────────────────────────
def render_extension(logo_b64):

    # ── 1. ما تفعله الإضافة ──────────────────────────────────
    sec("1", "ما الذي تفعله الإضافة؟")
    st.markdown("""
<div style="background:#0F1C35;color:rgba(234,228,217,0.85);border-radius:12px;
            padding:18px 22px;margin:12px 0 18px;line-height:1.7;
            font-size:0.92rem;direction:rtl;text-align:right;">
تضيف إضافة <strong>PromptScanner</strong> طبقةً أمنية مباشرةً داخل مواقع روبوتات الدردشة مثل
<strong>ChatGPT</strong> و<strong>Gemini</strong>. عند الضغط على إرسال أو Enter،
تعترض الإضافة النص وتفحصه وتعرض النتائج في نافذة منبثقة
<strong>قبل</strong> وصول أي شيء إلى الذكاء الاصطناعي. ثم تختار أنت ما تريد إرساله.
</div>""", unsafe_allow_html=True)

    flow(
        ("اكتب في ChatGPT / Gemini", ""),
        ("اضغط إرسال / Enter",       "flow-orange"),
        ("الإضافة تفحص النص",         "flow-teal"),
        ("أنت تقرر",                   ""),
    )

    # ── 2. التثبيت ───────────────────────────────────────────
    sec("2", "تثبيت الإضافة")
    step_item("1", "افتح متجر Chrome الإلكتروني",
              "اذهب إلى <strong>chromewebstore.google.com</strong> وابحث عن PromptScanner، أو استخدم الرابط المباشر الموجود على موقعنا.")
    step_item("2", "انقر «إضافة إلى Chrome»",
              "اضغط على زر «Add to Chrome» ثم أكّد التثبيت عند ظهور نافذة التأكيد.")
    step_item("3", "ثبّت الإضافة في شريط الأدوات",
              "انقر على أيقونة قطعة الأحجية 🧩 في أعلى يمين المتصفح، ابحث عن PromptScanner، ثم انقر أيقونة الدبوس 📌 لإبقائها ظاهرة دائماً.")
    step_item("4", "ابدأ الاستخدام",
              "ادخل إلى ChatGPT أو Gemini، اكتب مطالبتك، واضغط إرسال — ستظهر نافذة PromptScanner تلقائياً.",
              last=True)

    tip("تأكد من أن الإضافة مُثبَّتة وتظهر في شريط الأدوات قبل البدء. يمكنك التحقق من ذلك بالنقر على أيقونة PromptScanner مباشرةً.")

    # ── 3. حالات النافذة المنبثقة ─────────────────────────────
    sec("3", "حالات النافذة المنبثقة")
    st.markdown("""
<p style="color:var(--muted);font-size:0.9rem;direction:rtl;text-align:right;margin-bottom:16px;">
عند الضغط على إرسال تظهر نافذة PromptScanner بإحدى الحالات الأربع التالية حسب نتيجة الفحص:
</p>""", unsafe_allow_html=True)

    # State A
    st.markdown('<div style="font-size:1rem;font-weight:700;color:var(--navy);direction:rtl;text-align:right;margin:16px 0 8px;">الحالة أ — محتوى آمن ✓</div>', unsafe_allow_html=True)
    popup_with_ann(popup_safe(logo_b64), [
        ("1", "النص المُقنَّع يؤكد عدم وجود معلومات شخصية."),
        ("2", "التصنيف الأخضر «عادي» بثقة عالية — المحتوى آمن تماماً."),
        ("3", "<strong>⟶ إرسال</strong> — يرسل المطالبة كما هي. نقرة واحدة وتنتهي."),
    ])

    # State B — PII
    st.markdown('<div style="font-size:1rem;font-weight:700;color:var(--navy);direction:rtl;text-align:right;margin:20px 0 8px;">الحالة ب — تم اكتشاف معلومات شخصية</div>', unsafe_allow_html=True)
    popup_with_ann(popup_pii(logo_b64), [
        ("1", "النص المُقنَّع يعرض المطالبة مع استبدال البيانات الشخصية بعلامات مثل <span class='pii-tag'>[PERS]</span>."),
        ("2", "<strong>⟶ إرسال الأمر بدون معلومات خاصة</strong> — يُرسل النسخة الآمنة دون بياناتك الشخصية."),
        ("3", "<strong>⟶ إرسال الأصلي</strong> — يُرسل النص كما كتبته. القرار لك دائماً."),
    ])

    # State C — Toxic
    st.markdown('<div style="font-size:1rem;font-weight:700;color:var(--navy);direction:rtl;text-align:right;margin:20px 0 8px;">الحالة ج — تم اكتشاف محتوى ضار</div>', unsafe_allow_html=True)
    popup_with_ann(popup_toxic(logo_b64), [
        ("1", "قسم «الكلمات المؤثرة» يُظهر الكلمات التي أثّرت في قرار التصنيف بألوان متدرجة."),
        ("2", "<strong>إعادة الصياغة</strong> — يُولِّد نسخة آمنة تحافظ على المعنى الأصلي قدر الإمكان."),
        ("3", "<strong>⟶ إرسال الأصلي</strong> — إرسال النص رغم التحذير. القرار النهائي لك."),
    ])

    # State D — Rewritten
    st.markdown('<div style="font-size:1rem;font-weight:700;color:var(--navy);direction:rtl;text-align:right;margin:20px 0 8px;">الحالة د — بعد إعادة الصياغة</div>', unsafe_allow_html=True)
    popup_with_ann(popup_rewritten(logo_b64), [
        ("1", "قسم «النص المُعاد كتابته» بحد أخضر يعرض البديل الآمن."),
        ("2", "<strong>⟶ إرسال المُعاد كتابته</strong> — يُرسل النسخة الآمنة مباشرةً."),
        ("3", "<strong>⟶ إرسال الأصلي</strong> — يُرسل النص الأصلي رغم التحذير."),
        ("4", "<strong>✕ إلغاء</strong> — يغلق النافذة دون إرسال لتتمكن من التعديل يدوياً."),
    ])

    # ── 4. الإعدادات ─────────────────────────────────────────
    sec("4", "الإعدادات")
    st.markdown("""
<p style="color:var(--muted);font-size:0.9rem;direction:rtl;text-align:right;margin-bottom:14px;">
انقر أيقونة ⚙ في رأس النافذة المنبثقة للوصول إلى الإعدادات.
</p>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.markdown(popup_settings(logo_b64), unsafe_allow_html=True)
    with c2:
        st.markdown("""
<table class="pii-table">
  <thead><tr><th>الإعداد</th><th>الوظيفة</th></tr></thead>
  <tbody>
    <tr><td><strong>الوضع الداكن</strong></td><td>يُبدِّل النافذة إلى سمة ألوان داكنة.</td></tr>
    <tr><td><strong>اللغة</strong></td><td>اختر العربية أو الإنجليزية لجميع نصوص الإضافة.</td></tr>
    <tr><td><strong>عرض النافذة للمحتوى الآمن</strong></td><td>مفعَّل: تظهر النافذة حتى للمطالبات الآمنة. معطَّل: تُرسَل تلقائياً دون توقف.</td></tr>
    <tr><td><strong>الفحص التلقائي</strong></td><td>مفعَّل: الفحص يبدأ تلقائياً عند ضغط إرسال أو Enter. معطَّل: لا فحص تلقائي.</td></tr>
  </tbody>
</table>""", unsafe_allow_html=True)

    tip("اضغط دائماً <strong>حفظ الإعدادات</strong> بعد أي تغيير. لن تُطبَّق التغييرات حتى يتم الحفظ.", warn=True)

    # ── 5. مواقع مدعومة ──────────────────────────────────────
    sec("5", "المواقع المدعومة")
    st.markdown("""
<table class="pii-table">
  <thead><tr><th>الموقع</th><th>الرابط</th></tr></thead>
  <tbody>
    <tr><td>ChatGPT</td><td>chatgpt.com</td></tr>
    <tr><td>Gemini</td><td>gemini.google.com</td></tr>
    <tr><td>Claude</td><td>claude.ai</td></tr>
    <tr><td>Microsoft Copilot</td><td>copilot.microsoft.com</td></tr>
    <tr><td>Perplexity</td><td>perplexity.ai</td></tr>
  </tbody>
</table>""", unsafe_allow_html=True)

    # ── 6. مرجع سريع ─────────────────────────────────────────
    sec("6", "مرجع سريع")
    st.markdown("""
<table class="qr-table">
  <thead><tr><th>الإجراء</th><th>الطريقة</th></tr></thead>
  <tbody>
    <tr><td>تشغيل الفحص</td><td>اضغط إرسال أو Enter في ChatGPT / Gemini (يتطلب تفعيل الفحص التلقائي)</td></tr>
    <tr><td>إرسال المطالبة الأصلية</td><td>اضغط ⟶ إرسال الأصلي</td></tr>
    <tr><td>إرسال النص بدون معلومات خاصة</td><td>اضغط ⟶ إرسال الأمر بدون معلومات خاصة</td></tr>
    <tr><td>إرسال النسخة المُعادة صياغتها</td><td>اضغط إعادة الصياغة ثم ⟶ إرسال المُعاد كتابته</td></tr>
    <tr><td>الإلغاء دون إرسال</td><td>اضغط ✕ إلغاء</td></tr>
    <tr><td>فتح الإعدادات</td><td>انقر ⚙ في رأس النافذة المنبثقة</td></tr>
    <tr><td>تخطي النافذة للمحتوى الآمن</td><td>عطِّل «عرض النافذة للمحتوى الآمن» في الإعدادات</td></tr>
    <tr><td>تعطيل الفحص التلقائي</td><td>عطِّل «الفحص التلقائي» في الإعدادات</td></tr>
  </tbody>
</table>""", unsafe_allow_html=True)

    st.markdown("""
<div class="guide-footer">
  <span>PromptScanner</span> — دليل المستخدم · الجزء الثاني: إضافة المتصفح · ChatGPT & Gemini
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────
def render_user_guide():
    inject_css()

    logo_b64   = img_b64("assets/logo.png")
    lang       = st.session_state.get("guide_lang", "ar")
    active_tab = st.session_state.get("guide_tab", "website")
    L          = LANG[lang]
    is_rtl     = lang == "ar"

    # ── Top bar: language toggle only ────────────────────────
    c_space, c_lang = st.columns([8, 1])
    with c_lang:
        if st.button(L["lang_btn"], key="guide_lang_toggle", use_container_width=True):
            st.session_state.guide_lang = "en" if lang == "ar" else "ar"
            st.rerun()

    # ── Hero ─────────────────────────────────────────────────
    hero(logo_b64, lang=lang)

    # ── Tab buttons ──────────────────────────────────────────
    if is_rtl:
        tc1, tc2, tc3 = st.columns([2, 2, 4])
    else:
        tc1, tc2, tc3 = st.columns([2, 2, 4])

    with tc1:
        if st.button(L["tab1"], key="tab_website",
                     type="primary" if active_tab == "website" else "secondary",
                     use_container_width=True):
            st.session_state.guide_tab = "website"
            st.rerun()
    with tc2:
        if st.button(L["tab2"], key="tab_extension",
                     type="primary" if active_tab == "extension" else "secondary",
                     use_container_width=True):
            st.session_state.guide_tab = "extension"
            st.rerun()

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # ── Render content ────────────────────────────────────────
    if active_tab == "website":
        render_website(logo_b64)
    else:
        render_extension(logo_b64)


if __name__ == "__main__":
    st.set_page_config(
        page_title="PromptScanner — دليل المستخدم",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    render_user_guide()
