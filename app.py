import streamlit as st 
import torch
import torch.nn.functional as F
import json
import re
import os
import time
import threading
import numpy as np
import requests
from pathlib import Path
from collections import Counter
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    AutoModelForSequenceClassification,
)
from huggingface_hub import snapshot_download

st.set_page_config(
    page_title="PromptScanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Page routing ────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "scanner"

if st.session_state.page == "guide":
    from user_guide import render_user_guide
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        margin-top: 10px;
        background-color: #bbb6ae;
        color: #fff;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 6px 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("← Back to Scanner"):
        st.session_state.page = "scanner"
        st.rerun()
    render_user_guide()
    st.stop()

if "dark_mode"    not in st.session_state: st.session_state.dark_mode    = False
if "language"     not in st.session_state: st.session_state.language     = "ar"
if "scan_result"  not in st.session_state: st.session_state.scan_result  = None
if "rewritten"    not in st.session_state: st.session_state.rewritten    = None
if "prompt_reset" not in st.session_state: st.session_state.prompt_reset = 0
if "prompt_value" not in st.session_state: st.session_state.prompt_value = ""

RAILWAY_URL = "https://promptscanner-production.up.railway.app"

STRINGS = {
    "ar": {
        "tagline":      "حارس خصوصيتك في عالم الذكاء الاصطناعي",
        "placeholder":  "اكتب أو الصق النص العربي هنا…",
        "btn_scan":     "فحص",
        "btn_clear":    "مسح",
        "btn_rewrite":  "إعادة الصياغة",
        "scanning":     "جارٍ الفحص…",
        "rewriting":    "جارٍ إعادة الصياغة…",
        "scanned_in":   "تم الفحص في",
        "pii_head":     "◆ النص بدون معلومات خاصة",
        "tox_head":     "◆ تحليل السمية",
        "hl_head":      "◆ الكلمات المؤثرة",
        "rewrite_head": "◆ إعادة الصياغة",
        "orig_label":   "النص الأصلي",
        "new_label":    "النص المُعاد كتابته",
        "no_pii":       "✓ لا توجد معلومات شخصية في هذا النص.",
        "confidence":   "درجة الثقة",
        "top_words":    "أبرز الكلمات",
        "tox_unavail":  "نموذج السمية غير محمّل.",
        "warn_empty":   "الرجاء إدخال نص قبل الفحص.",
        "rewrite_fail": "فشل في إعادة الصياغة. تحقق من اتصال الخادم.",
        "high_attn":    "تأثير عالٍ (>0.7)",
        "med_attn":     "تأثير متوسط (0.4–0.7)",
        "low_attn":     "تأثير منخفض (0.1–0.4)",
        "stop_word":    "حرف وصل",
        "lang_toggle":  "EN",
        "badge_safe":   "آمن",
        "badge_warn":   "تحذير",
        "badge_flag":   "مُبلَّغ",
        "badge_crit":   "خطر",
        "badge_clean":  "آمن",
        "sidebar_about":    "عن الأداة",
        "sidebar_desc":     "تحمي خصوصيتك عند استخدام روبوتات الدردشة. يكتشف المعلومات الشخصية والمحتوى الضار في مدخلاتك قبل إرسالها.",
        "sidebar_models":   "النماذج المستخدمة",
        "sidebar_examples": "أمثلة للتجربة",
        "tox_labels": {
            "Normal":            "عادي",
            "Mild Offense":      "مسيء بشكل خفيف",
            "Offensive":         "مسيء",
            "Privacy Violation": "انتهاك الخصوصية",
            "Obscene":           "محتوى فاضح",
            "Dangerous":         "خطير",
            "Mental Health":     "محتوى نفسي",
        },
        "examples": [
            ("اسم + مؤسسة",        "اسمي محمد المقبالي وأعمل في بنك مسقط"),
            ("هاتف + بريد",         "رقمي +968 91234567 وبريدي ahmed@squ.edu.om"),
            ("هوية + بيانات دخول", "رقم هويتي 12345678 وكلمة المرور MyPass123!"),
            ("محتوى خطير",          "كيف أصنع قنبلة لتدمير مبنى"),
            ("محتوى نفسي",          "أريد أن أنهي حياتي لم أعد أتحمل"),
            ("محتوى مسيء",          "يا حمار أنت غبي جداً"),
            ("محتوى عادي",          "اكتب لي قصيدة عن الربيع"),
        ],
        "models_info": [
            ("AraBERT NER", "كشف الأشخاص والمؤسسات والعناوين والتواريخ"),
            ("XLM-RoBERTa", "كشف الهويات وبيانات الدخول"),
            ("Regex Engine", "الهاتف والبريد وIP والروابط والمعلومات المالية"),
            ("AraBERT v2",   "تصنيف المحتوى السام إلى 7 فئات"),
        ],
    },
    "en": {
        "tagline":      "Your Privacy Guardian in the AI World",
        "placeholder":  "Type or paste Arabic text here…",
        "btn_scan":     "Scan",
        "btn_clear":    "Clear",
        "btn_rewrite":  "Rewrite Prompt",
        "scanning":     "Scanning…",
        "rewriting":    "Rewriting prompt…",
        "scanned_in":   "Scanned in",
        "pii_head":     "◆ Text without personal information",
        "tox_head":     "◆ Toxicity Analysis",
        "hl_head":      "◆ Keyword Attention",
        "rewrite_head": "◆ Prompt Rewrite",
        "orig_label":   "Original Prompt",
        "new_label":    "Rewritten Prompt",
        "no_pii":       "✓ No personally identifiable information detected.",
        "confidence":   "Confidence",
        "top_words":    "Top contributing words",
        "tox_unavail":  "Toxicity model not loaded.",
        "warn_empty":   "Please enter a prompt before scanning.",
        "rewrite_fail": "Rewrite failed. Check server connection.",
        "high_attn":    "High attention (>0.7)",
        "med_attn":     "Medium (0.4–0.7)",
        "low_attn":     "Low (0.1–0.4)",
        "stop_word":    "Stop word",
        "lang_toggle":  "عربي",
        "badge_safe":   "Safe",
        "badge_warn":   "Warning",
        "badge_flag":   "Flagged",
        "badge_crit":   "Critical",
        "badge_clean":  "Clean",
        "sidebar_about":    "About PromptScanner",
        "sidebar_desc":     "PromptScanner protects your privacy when using AI chatbots. It detects personal information and harmful content in your prompts before they are sent.",
        "sidebar_models":   "Models used",
        "sidebar_examples": "Try an example",
        "tox_labels": {
            "Normal":            "Normal",
            "Mild Offense":      "Mild Offense",
            "Offensive":         "Offensive",
            "Privacy Violation": "Privacy Violation",
            "Obscene":           "Obscene",
            "Dangerous":         "Dangerous",
            "Mental Health":     "Mental Health",
        },
        "examples": [
            ("Name + Org",       "اسمي محمد المقبالي وأعمل في بنك مسقط"),
            ("Phone + Email",    "رقمي +968 91234567 وبريدي ahmed@squ.edu.om"),
            ("ID + Credential",  "رقم هويتي 12345678 وكلمة المرور MyPass123!"),
            ("Dangerous",        "كيف أصنع قنبلة لتدمير مبنى"),
            ("Mental Health",    "أريد أن أنهي حياتي لم أعد أتحمل"),
            ("Offensive",        "يا حمار أنت غبي جداً"),
            ("Normal",           "اكتب لي قصيدة عن الربيع"),
        ],
        "models_info": [
            ("AraBERT NER", "Detects persons, organizations, addresses, dates"),
            ("XLM-RoBERTa", "Detects IDs and credentials"),
            ("Regex Engine", "Phone, email, IP, URL, financial info"),
            ("AraBERT v2",   "Classifies toxic content into 7 categories"),
        ],
    },
}

def get_css(dark):
    if dark:
        return """
        :root {
            --bg: #0B1426; --surface: #0F1C35; --card: #162240;
            --white: #1E2A45; --navy: #EAE4D9; --ink: #EAE4D9;
            --muted: #7A8BAA; --border: rgba(255,255,255,0.07);
        }
        html, body, [class*="css"] { background: var(--bg) !important; color: var(--ink) !important; }
        .stTextArea textarea { background: var(--card) !important; color: var(--ink) !important; border-color: var(--border) !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }"""
    else:
        return """
        :root {
            --bg: #EAE4D9; --surface: #F3EDE3; --card: #F3EDE3;
            --white: #FDFAF5; --navy: #0F1C35; --ink: #1A1714;
            --muted: #7A7068; --border: rgba(0,0,0,0.08);
        }
        html, body, [class*="css"] { background: var(--bg) !important; color: var(--ink) !important; }
        .stTextArea textarea { background: var(--white) !important; color: var(--ink) !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }"""

COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
* { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 900px; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }
.stApp,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],
[data-testid="stHeader"],[data-testid="stBottomBlockContainer"],.main .block-container {
    background: var(--bg) !important; color: var(--ink) !important;
}
.ps-wordmark { font-weight: 800; font-size: 2rem; letter-spacing: -1px; line-height: 1; }
.ps-wordmark .dark { color: var(--navy); }
.ps-wordmark .orng { color: #E8520A; }
.ps-slogan { font-style: italic; font-weight: 300; font-size: 0.9rem; color: var(--muted); margin-top: 3px; }
.ps-rule { height: 1px; background: linear-gradient(90deg, #E8520A, #2D5BE3 45%, transparent); margin-bottom: 1.3rem; opacity: 0.2; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stTextArea textarea {
    border: 1px solid var(--border) !important; border-radius: 12px !important;
    font-size: 1.05rem !important; padding: 1rem !important; line-height: 1.7 !important;
    direction: rtl; transition: border-color .2s;
}
.stTextArea textarea:focus { border-color: var(--border) !important; box-shadow: none !important; outline: none !important; }
.stTextArea textarea:focus-visible { outline: none !important; box-shadow: none !important; }
textarea { caret-color: #E8520A !important; }
[data-baseweb="textarea"] { border: none !important; box-shadow: none !important; }
div[data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important; }
div[data-testid="stButton"] button {
    background: #0F1C35 !important; color: #EAE4D9 !important;
    font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important;
    font-size: .85rem !important; border: none !important; border-radius: 10px !important;
    padding: .55rem 1.6rem !important; letter-spacing: .04em !important;
    transition: all .2s !important; cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(15,28,53,0.2) !important;
    white-space: nowrap !important; width: auto !important;
}
div[data-testid="stButton"] button:hover { opacity: 0.85 !important; transform: translateY(-1px); }
div[data-testid="stFormSubmitButton"] button {
    background: #0F1C35 !important; color: #EAE4D9 !important;
    font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important;
    font-size: .85rem !important; border: none !important; border-radius: 10px !important;
    padding: .55rem 2rem !important; letter-spacing: .04em !important;
    transition: all .2s !important; cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(15,28,53,0.2) !important; width: auto !important;
}
div[data-testid="stFormSubmitButton"] button:hover { opacity: 0.85 !important; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 1.3rem 1.5rem; margin-bottom: .8rem; transition: all .2s ease; }
.card:hover { transform: translateY(-2px); }
.card-pii  { border-top: 3px solid #E8520A; }
.card-tox  { border-top: 3px solid #2D5BE3; }
.card-hl   { border-top: 3px solid #6B4FBB; }
.card-rw   { border-top: 3px solid #00C9A7; }
.card-head { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 1rem; font-weight: 700; color: var(--ink); margin-bottom: .85rem; }
.richtext { font-size: 1rem; line-height: 2.2; padding: .85rem 1rem; background: var(--white); border: 1px solid var(--border); border-radius: 10px; direction: rtl; text-align: right; word-break: break-word; color: var(--ink); }
.tag-pii { display: inline-block; background: rgba(232,82,10,0.10); color: #E8520A; border: 1px solid rgba(232,82,10,0.3); border-radius: 5px; padding: 1px 6px; font-family: 'JetBrains Mono', monospace !important; font-size: .7rem; margin: 0 2px; vertical-align: middle; }
.epills { display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .75rem; }
.epill { display: flex; align-items: center; gap: .3rem; background: rgba(232,82,10,0.07); border: 1px solid rgba(232,82,10,0.2); border-radius: 20px; padding: .2rem .7rem; font-size: .78rem; }
.epill-lbl { color: #E8520A; font-family: 'JetBrains Mono', monospace !important; font-size: .66rem; font-weight: 700; }
.epill-val { color: var(--ink); }
.tox-name { font-size: 1.45rem; font-weight: 800; letter-spacing: -0.5px; }
.tox-conf { color: var(--muted); font-size: .86rem; margin-top: .1rem; }
.pbar-bg { background: var(--border); border-radius: 4px; height: 7px; overflow: hidden; margin-top: .45rem; }
.pbar-fill { height: 100%; border-radius: 4px; }
.ptable { width: 100%; border-collapse: separate; border-spacing: 0 8px; margin-top: 1rem; }
.ptable tr { background: rgba(255,255,255,0.03); border-radius: 10px; }
.ptable td { padding: .55rem .7rem; border: none !important; color: var(--ink); }
.ptable td:first-child { color: var(--muted); font-weight: 600; }
.ptable td:last-child { text-align: left; font-family: 'JetBrains Mono', monospace !important; }
.pmini { display: inline-block; height: 5px; border-radius: 3px; vertical-align: middle; margin-right: .3rem; }
.badge { display: inline-block; padding: .16rem .65rem; border-radius: 20px; font-size: .68rem; font-family: 'JetBrains Mono', monospace !important; font-weight: 700; letter-spacing: .06em; }
.b-safe { background: rgba(0,201,167,0.10); color: #00C9A7;  border: 1px solid rgba(0,201,167,0.3); }
.b-warn { background: rgba(232,82,10,0.10); color: #E8520A;  border: 1px solid rgba(232,82,10,0.3); }
.b-flag { background: rgba(217,48,37,0.10); color: #D93025;  border: 1px solid rgba(217,48,37,0.3); }
.b-crit { background: rgba(107,79,187,0.10);color: #6B4FBB;  border: 1px solid rgba(107,79,187,0.3); }
.hl-word { display: inline-block; border-radius: 5px; padding: 1px 6px; margin: 0 2px; font-size: 1rem; }
.legend { display: flex; gap: 1rem; flex-wrap: wrap; font-size: .74rem; color: var(--muted); margin-top: .55rem; }
.leg-item { display: flex; align-items: center; gap: .3rem; }
.leg-sq { width: 11px; height: 11px; border-radius: 3px; }
.nopii { color: #00C9A7; font-family: 'JetBrains Mono', monospace !important; font-size: .82rem; padding: .3rem 0; }
.rw-box { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: .85rem 1rem; font-size: 1rem; line-height: 1.8; direction: rtl; text-align: right; color: var(--ink); white-space: pre-wrap; margin-bottom: .6rem; }
.rw-label { font-family: 'JetBrains Mono', monospace !important; font-size: .66rem; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); margin-bottom: .3rem; }
.sb-title { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: .88rem; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; color: #0F1C35; margin-bottom: .6rem; padding-bottom: 6px; border-bottom: 2px solid rgba(15,28,53,0.15); }
.sb-desc { font-size: .84rem; color: var(--ink); line-height: 1.6; margin-bottom: 0; }
.info-panel { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem 1.1rem; margin-bottom: .8rem; }
.sb-model { display: flex; gap: 8px; align-items: flex-start; margin-bottom: .55rem; }
.sb-model-desc { font-size: .77rem; color: var(--muted); line-height: 1.4; }
.section-gap { margin-top: 1rem; }
"""

def inject_css():
    st.markdown(f"<style>{get_css(st.session_state.dark_mode)}{COMMON_CSS}</style>", unsafe_allow_html=True)

TOX_IDX2LABEL = {
    0: 'Dangerous', 1: 'Mental Health', 2: 'Mild Offense',
    3: 'Normal',    4: 'Obscene',       5: 'Offensive',
    6: 'Privacy Violation',
}
ARABERT_CATEGORIES = ['PERS', 'ORG', 'ADDRESS', 'DATETIME']
XLMR_CATEGORIES    = ['ID', 'CREDENTIAL']
DANGER_CATS        = {'Dangerous', 'Obscene', 'Mental Health'}

TOX_COLOR = {
    'Normal':            '#00C9A7',
    'Mild Offense':      '#E8520A',
    'Offensive':         '#F26A22',
    'Privacy Violation': '#2D5BE3',
    'Obscene':           '#D93025',
    'Dangerous':         '#D93025',
    'Mental Health':     '#6B4FBB',
}

ARABIC_STOP_WORDS = {
    'في','من','الي','علي','عن','مع','بين','حتي','منذ','خلال','عند','لدي','نحو',
    'فوق','تحت','امام','وراء','حول','ضد','و','او','ثم','لكن','بل','حيث','اذا',
    'لان','كي','اذ','هو','هي','هم','هن','نحن','انا','انت','انتم','هذا','هذه',
    'ذلك','تلك','هولاء','الذي','التي','الذين','اللاتي','ما','ماذا','هل','كم',
    'اين','متي','لماذا','كيف','كان','يكون','ليس','يمكن','يجب','قد','سوف','لن',
    'لم','ال','لا','ان','اي','كل','بعض','غير','نفس','جدا','ايضا','فقط','بس',
    'يعني','طيب','مش','دي','ده','لي','بي','الا','اما','اذن','مثل','عبر','ذات',
}

MODELS_DIR = Path("models")
REGEX_PATTERNS = {
    'PHONE':        [r'\+968\s?[79]\d{7}', r'00968\s?[79]\d{7}', r'\b[79]\d{7}\b', r'\b[79]\d{3}[\s\-]\d{4}\b'],
    'EMAIL':        [r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'],
    'IP':           [r'\b(?:\d{1,3}\.){3}\d{1,3}\b'],
    'MAC':          [r'\b([0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}\b'],
    'URL':          [r'https?://[^\s<>"]+', r'www\.[^\s<>"]+'],
    'FINANCIAL_INFO':[r'\b4\d{3}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b', r'\bOM\d{2}[A-Z]{3}\d{16}\b'],
}

LATIN_OR_DIGIT = re.compile(r'[a-zA-Z0-9]')
HF_TOKEN = st.secrets.get("HF_TOKEN", os.environ.get("HF_TOKEN", ""))

@st.cache_resource(show_spinner="جارٍ تحميل النماذج…")
def download_models():
    if not Path("models").exists():
        snapshot_download(repo_id="aynaalh/promptscanner-models", token=HF_TOKEN, local_dir="models")

download_models()

@st.cache_resource(show_spinner=False)
def load_arabert():
    path = MODELS_DIR / "arabert_pii_aug" / "arabert_pii_aug"
    if not path.exists(): return None, None, None
    try:
        tok = AutoTokenizer.from_pretrained(str(path))
        model = AutoModelForTokenClassification.from_pretrained(str(path))
        model.eval()
        vf = next((p for p in [path/"tag_vocab.json", path/"tag_vocab_aug.json"] if p.exists()), None)
        if not vf: return None, None, None
        id2tag = {int(k): v for k, v in json.load(open(vf))["id2tag"].items()}
        return tok, model, id2tag
    except: return None, None, None

@st.cache_resource(show_spinner=False)
def load_xlmr():
    path = MODELS_DIR / "xlmr_pii" / "xlmr_pii_augmorg"
    if not path.exists(): return None, None, None
    try:
        tok = AutoTokenizer.from_pretrained(str(path))
        model = AutoModelForTokenClassification.from_pretrained(str(path))
        model.eval()
        vf = next((p for p in [path/"tag_vocab.json", path/"tag_vocab_augmorg.json"] if p.exists()), None)
        if not vf: return None, None, None
        id2tag = {int(k): v for k, v in json.load(open(vf))["id2tag"].items()}
        return tok, model, id2tag
    except: return None, None, None

@st.cache_resource(show_spinner=False)
def load_toxicity():
    path = MODELS_DIR / "tox_model"
    if not path.exists(): return None, None
    ckpt_file = next((path/c for c in ["arabert_expanded.pt","arabert_contrast.pt","best_model.pt"] if (path/c).exists()), None)
    if not ckpt_file:
        pts = list(path.glob("*.pt"))
        ckpt_file = pts[0] if pts else None
    if not ckpt_file: return None, None
    try:
        tok = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
        model = AutoModelForSequenceClassification.from_pretrained(
            "aubmindlab/bert-base-arabertv02", num_labels=7,
            ignore_mismatched_sizes=True, attn_implementation="eager")
        ckpt = torch.load(str(ckpt_file), map_location="cpu", weights_only=False)
        model.load_state_dict(ckpt["model_state_dict"])
        model.eval()
        return tok, model
    except: return None, None

def clean_arabic(text):
    if not text: return ""
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    for a, b in [('[إأآا]','ا'),('ى','ي'),('ة','ه'),('ؤ','و'),('ئ','ي')]:
        text = re.sub(a, b, text)
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def is_mostly_english(text, threshold=0.7):
    english_chars = re.findall(r'[A-Za-z]', text)
    arabic_chars  = re.findall(r'[\u0600-\u06FF]', text)
    total = len(english_chars) + len(arabic_chars)
    if total == 0: return False
    return (len(english_chars) / total) > threshold

def regex_detect(text):
    found = []
    for pii_type, patterns in REGEX_PATTERNS.items():
        for pat in patterns:
            for m in re.finditer(pat, text):
                found.append({'value': m.group(), 'type': pii_type, 'char_start': m.start(), 'char_end': m.end(), 'source': 'regex'})
    found.sort(key=lambda x: (x['char_start'], -(x['char_end']-x['char_start'])))
    filtered, last_end = [], -1
    for it in found:
        if it['char_start'] >= last_end:
            filtered.append(it); last_end = it['char_end']
    return filtered

def is_valid_id_or_credential(value):
    if not value or len(value.strip()) < 2: return False
    return bool(LATIN_OR_DIGIT.search(value))

def filter_invalid_entities(entities):
    filtered = []
    for e in entities:
        if e['type'] in ('ID', 'CREDENTIAL'):
            if not is_valid_id_or_credential(e['value']): continue
        filtered.append(e)
    return filtered

def _token_char_ranges(tokens):
    ranges, pos = {}, 0
    for i, tok in enumerate(tokens):
        ranges[i] = (pos, pos + len(tok)); pos += len(tok) + 1
    return ranges

def _token_overlaps_regex(ts, te, tok_char, regex_spans):
    if ts not in tok_char: return False
    cs = tok_char[ts][0]; ce = tok_char.get(te-1, tok_char[ts])[1]
    return any(not (ce <= rs or cs >= re_) for rs, re_ in regex_spans)

def _predict_ner(text, tokenizer, model, id2tag):
    tokens = text.split()
    if not tokens: return []
    inputs = tokenizer(tokens, is_split_into_words=True, return_tensors="pt",
                       truncation=True, padding=True, max_length=256)
    with torch.no_grad():
        preds = torch.argmax(model(**inputs).logits, dim=2)[0].tolist()
    word_ids = inputs.word_ids(0)
    word_pred = {}
    for idx, wid in enumerate(word_ids):
        if wid is not None and wid not in word_pred:
            word_pred[wid] = id2tag.get(preds[idx], "O")
    entities, cur, cur_toks = [], None, []
    for i, tok in enumerate(tokens):
        tag = word_pred.get(i, "O")
        if tag.startswith("B-"):
            if cur: entities.append({"value": " ".join(cur_toks), "type": cur, "token_start": i-len(cur_toks), "token_end": i})
            cur, cur_toks = tag[2:], [tok]
        elif tag.startswith("I-") and cur == tag[2:]:
            cur_toks.append(tok)
        else:
            if cur: entities.append({"value": " ".join(cur_toks), "type": cur, "token_start": i-len(cur_toks), "token_end": i})
            cur, cur_toks = None, []
    if cur: entities.append({"value": " ".join(cur_toks), "type": cur, "token_start": len(tokens)-len(cur_toks), "token_end": len(tokens)})
    return entities

def hybrid_detect(text, ar_tok, ar_mdl, ar_id2tag, xl_tok, xl_mdl, xl_id2tag):
    tokens = text.split(); all_ents = []
    regex_hits  = regex_detect(text)
    regex_spans = [(e["char_start"], e["char_end"]) for e in regex_hits]
    all_ents.extend(regex_hits)
    tok_char = _token_char_ranges(tokens)
    if ar_mdl:
        for e in _predict_ner(text, ar_tok, ar_mdl, ar_id2tag):
            if e["type"] not in ARABERT_CATEGORIES: continue
            if _token_overlaps_regex(e["token_start"], e["token_end"], tok_char, regex_spans): continue
            e["source"] = "arabert"; all_ents.append(e)
    if xl_mdl:
        for e in _predict_ner(text, xl_tok, xl_mdl, xl_id2tag):
            if e["type"] not in XLMR_CATEGORIES: continue
            if _token_overlaps_regex(e["token_start"], e["token_end"], tok_char, regex_spans): continue
            e["source"] = "xlmr"; all_ents.append(e)
    all_ents = filter_invalid_entities(all_ents)
    return all_ents

def predict_toxicity_with_attention(text, tokenizer, model):
    processed = clean_arabic(text)
    if not processed: return None
    enc  = tokenizer(processed, max_length=128, padding="max_length", truncation=True, return_tensors="pt")
    ids  = enc["input_ids"]; mask = enc["attention_mask"]
    tids = enc.get("token_type_ids", torch.zeros_like(ids))
    with torch.no_grad():
        out   = model(ids, attention_mask=mask, token_type_ids=tids, output_attentions=True)
        probs = F.softmax(out.logits, dim=1).squeeze().cpu().numpy()
    attn       = torch.stack(out.attentions)[:, 0, :, 0, :].mean(dim=(0,1)).cpu().numpy()
    tokens     = tokenizer.convert_ids_to_tokens(ids.squeeze().cpu().numpy())
    actual_len = mask.sum().item()
    tokens, attn = tokens[:actual_len], attn[:actual_len]
    words, scores, cur_w, cur_s = [], [], "", []
    for tok, sc in zip(tokens, attn):
        if tok in ["[CLS]","[SEP]","[PAD]","<s>","</s>","<pad>"]: continue
        if tok.startswith("##"): cur_w += tok[2:]; cur_s.append(sc)
        elif tok.startswith("+"): cur_w += tok.replace("+",""); cur_s.append(sc)
        else:
            if cur_w: words.append(cur_w); scores.append(float(max(cur_s)))
            cur_w, cur_s = tok.replace("+",""), [sc]
    if cur_w: words.append(cur_w); scores.append(float(max(cur_s)))
    scores_arr = np.array(scores, dtype=float)
    filtered   = np.array([0.0 if w in ARABIC_STOP_WORDS else s for w, s in zip(words, scores_arr)])
    is_stop    = [w in ARABIC_STOP_WORDS for w in words]
    if filtered.max() > 0: filtered /= filtered.max()
    pred_idx = int(np.argmax(probs))
    return {
        "prediction": TOX_IDX2LABEL[pred_idx],
        "confidence": float(probs[pred_idx]),
        "all_probs":  {TOX_IDX2LABEL[i]: float(p) for i, p in enumerate(probs)},
        "words": words, "scores": filtered.tolist(), "is_stop": is_stop,
    }

def run_scan(text, ar_tok, ar_mdl, ar_id2tag, xl_tok, xl_mdl, xl_id2tag, tx_tok, tx_mdl):
    results = {}
    def pii_job(): results["pii"] = hybrid_detect(text, ar_tok, ar_mdl, ar_id2tag, xl_tok, xl_mdl, xl_id2tag)
    def tox_job(): results["tox"] = predict_toxicity_with_attention(text, tx_tok, tx_mdl) if tx_mdl else None
    t1 = threading.Thread(target=pii_job); t2 = threading.Thread(target=tox_job)
    t1.start(); t2.start(); t1.join(); t2.join()
    return results

def build_masked_html(text, entities):
    char_ents = sorted([e for e in entities if "char_start" in e], key=lambda x: x["char_start"], reverse=True)
    out = text
    for e in char_ents:
        out = out[:e["char_start"]] + f'<span class="tag-pii">[{e["type"]}]</span>' + out[e["char_end"]:]
    for e in [e for e in entities if "token_start" in e]:
        if e["value"] and e["value"] in out:
            out = out.replace(e["value"], f'<span class="tag-pii">[{e["type"]}]</span>', 1)
    return out

def build_masked_plain(text, entities):
    char_ents = sorted([e for e in entities if "char_start" in e], key=lambda x: x["char_start"], reverse=True)
    out = text
    for e in char_ents:
        out = out[:e["char_start"]] + f'[{e["type"]}]' + out[e["char_end"]:]
    for e in [e for e in entities if "token_start" in e]:
        if e["value"] and e["value"] in out:
            out = out.replace(e["value"], f'[{e["type"]}]', 1)
    return out

def build_highlight_html(words, scores, is_stop, color_hex):
    def hex_rgb(h):
        h = h.lstrip("#")
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
    rgb = hex_rgb(color_hex); parts = []
    for word, score, stop in zip(words, scores, is_stop):
        if stop:
            parts.append(f'<span class="hl-word" style="background:rgba(0,0,0,0.05);color:#999;">{word}</span>')
        elif score > 0.7:
            a = 0.15 + score * 0.75
            parts.append(f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});color:#fff;font-weight:700;">{word}</span>')
        elif score > 0.4:
            a = 0.1 + score * 0.65
            parts.append(f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});color:{color_hex};">{word}</span>')
        elif score > 0.1:
            a = 0.05 + score * 0.4
            parts.append(f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});color:#888;">{word}</span>')
        else:
            parts.append(f'<span class="hl-word" style="color:#aaa;">{word}</span>')
    return " ".join(parts)

def tox_badge(label, T):
    if label == "Normal":        return f'<span class="badge b-safe">{T["badge_safe"]}</span>'
    if label == "Mental Health": return f'<span class="badge b-crit">{T["badge_crit"]}</span>'
    if label in DANGER_CATS:     return f'<span class="badge b-flag">{T["badge_flag"]}</span>'
    return f'<span class="badge b-warn">{T["badge_warn"]}</span>'

def call_rewrite(original, masked, tox_label):
    try:
        resp = requests.post(f"{RAILWAY_URL}/rewrite",
            json={"text": original, "masked_text": masked, "tox_label": tox_label}, timeout=30)
        return resp.json().get("rewritten", "") if resp.ok else None
    except: return None

# ─── LOAD MODELS ────────────────────────────────────────────
with st.spinner("جارٍ تحميل النماذج…"):
    ar_tok, ar_mdl, ar_id2tag = load_arabert()
    xl_tok, xl_mdl, xl_id2tag = load_xlmr()
    tx_tok, tx_mdl            = load_toxicity()

ar_ok = ar_mdl is not None
xl_ok = xl_mdl is not None
tx_ok = tx_mdl is not None

inject_css()
T         = STRINGS[st.session_state.language]
models_ok = [ar_ok, xl_ok, True, tx_ok]

# ─── TOP BAR ────────────────────────────────────────────────
logo_path = Path("assets/logo.png")
import base64
logo_html = ""
if logo_path.exists():
    logo_b64 = base64.b64encode(open(str(logo_path), "rb").read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:44px;height:44px;object-fit:contain;border-radius:10px;flex-shrink:0;" />'

is_ar = st.session_state.language == "ar"
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            flex-direction:{'row-reverse' if is_ar else 'row'};
            flex-wrap:nowrap;gap:8px;margin-bottom:8px;">
  <div style="display:flex;align-items:center;gap:10px;
              flex-direction:{'row-reverse' if is_ar else 'row'};">
    {logo_html}
    <div style="{'text-align:right;' if is_ar else ''}">
      <div class="ps-wordmark"><span class="dark">Prompt</span><span class="orng">Scanner</span></div>
      <div class="ps-slogan">{T["tagline"]}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Buttons row — always horizontal using CSS override
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 6px !important;
}
div[data-testid="stHorizontalBlock"] > div {
    min-width: 0 !important;
    flex: 1 !important;
}
</style>
""", unsafe_allow_html=True)

# Place buttons in a hidden row at the top using absolute positioning trick
_, btn_col = st.columns([4, 1])
with btn_col:
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="toggle_dark", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with b2:
        if st.button(T["lang_toggle"], key="toggle_lang", use_container_width=True):
            st.session_state.language = "en" if st.session_state.language == "ar" else "ar"
            st.rerun()
    with b3:
        if st.button("📖", key="btn_guide", use_container_width=True):
            st.session_state.page = "guide"
            st.rerun()

# Pull buttons up to overlap with logo row using negative margin
st.markdown("""
<style>
/* Pull the button row up to sit beside the logo */
div[data-testid="stVerticalBlock"] > div:nth-child(3) {
    margin-top: -72px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="ps-rule"></div>', unsafe_allow_html=True)

# ─── MAIN 2-COLUMN LAYOUT ───────────────────────────────────
col_info, col_main = st.columns([3, 7], gap="large")

with col_info:
    # About
    st.markdown(f'''
<div class="info-panel">
  <div class="sb-title">{T["sidebar_about"]}</div>
  <div class="sb-desc">{T["sidebar_desc"]}</div>
</div>''', unsafe_allow_html=True)

    # Models — solid color badges matching guide exactly
    st.markdown(f'<div class="sb-title" style="margin-top:1rem">{T["sidebar_models"]}</div>', unsafe_allow_html=True)
    models_html = '<div class="info-panel">'
    for (name, desc), ok in zip(T["models_info"], models_ok):
        dot = "🟢" if ok else "🔴"
        bg  = "#2D5BE3" if "AraBERT v2" in name else "#E8520A"
        models_html += f'<div class="sb-model"><span style="font-family:JetBrains Mono,monospace;font-size:.68rem;font-weight:700;color:#fff;background:{bg};border-radius:4px;padding:2px 8px;white-space:nowrap;flex-shrink:0;display:inline-block;">{name}</span><span class="sb-model-desc">{dot} {desc}</span></div>'
    models_html += "</div>"
    st.markdown(models_html, unsafe_allow_html=True)

    # Examples
    st.markdown(f'<div class="sb-title" style="margin-top:1.2rem;margin-bottom:.5rem">{T["sidebar_examples"]}</div>', unsafe_allow_html=True)
    for lbl, ex in T["examples"]:
        if st.button(lbl, key=f"ex_{lbl}", use_container_width=True):
            st.session_state.prompt_value = ex
            st.session_state.prompt_reset += 1
            st.session_state.scan_result  = None
            st.session_state.rewritten    = None
            st.rerun()

with col_main:
    prompt = st.text_area(
        "prompt_input",
        value=st.session_state.prompt_value,
        height=130,
        placeholder=T["placeholder"],
        label_visibility="collapsed",
        key=f"prompt_{st.session_state.prompt_reset}"
    )

    with st.form(key="scan_form", clear_on_submit=False):
        scan_clicked = st.form_submit_button(T["btn_scan"])

    if scan_clicked and prompt.strip():
        if is_mostly_english(prompt):
            st.error("⚠️ يُرجى كتابة النص بالعربية فقط." if st.session_state.language == "ar" else "⚠️ Prompt must be written in Arabic.")
            st.stop()
        with st.spinner(T["scanning"]):
            t0      = time.time()
            res     = run_scan(prompt.strip(), ar_tok, ar_mdl, ar_id2tag, xl_tok, xl_mdl, xl_id2tag, tx_tok, tx_mdl)
            elapsed = round(time.time() - t0, 2)
        st.session_state.scan_result = {"res": res, "prompt": prompt.strip(), "elapsed": elapsed}
        st.session_state.rewritten   = None
    elif scan_clicked and not prompt.strip():
        st.warning(T["warn_empty"])

    if st.session_state.scan_result:
        if st.button(T["btn_clear"], key="btn_clear"):
            st.session_state.scan_result = None
            st.session_state.rewritten   = None
            st.session_state.prompt_reset += 1
            st.rerun()

        sr       = st.session_state.scan_result
        res      = sr["res"]; prompt_ = sr["prompt"]; elapsed = sr["elapsed"]
        pii_ents = res.get("pii", []); tox_res = res.get("tox")

        st.markdown(f'<div style="color:var(--muted);font-size:.74rem;font-family:JetBrains Mono,monospace;margin:.8rem 0 .4rem;direction:rtl;text-align:right;">{T["scanned_in"]} <bdi>{elapsed}s</bdi></div>', unsafe_allow_html=True)

        r_left, r_right = st.columns(2, gap="medium")

        with r_left:
            n_pii = len(pii_ents)
            badge = f'<span class="badge b-warn">{n_pii}</span>' if n_pii else f'<span class="badge b-safe">{T["badge_clean"]}</span>'
            st.markdown(f'<div class="card card-pii"><div class="card-head">{T["pii_head"]} &nbsp; {badge}</div>', unsafe_allow_html=True)
            if pii_ents:
                st.markdown(f'<div class="richtext">{build_masked_html(prompt_, pii_ents)}</div>', unsafe_allow_html=True)
                st.markdown('<div class="epills">', unsafe_allow_html=True)
                for e in pii_ents:
                    src = {"regex":"RGX","arabert":"NER","xlmr":"XLM"}.get(e.get("source",""),"")
                    st.markdown(f'<div class="epill"><span class="epill-lbl">{e["type"]}</span><span class="epill-val">{e["value"]}</span><span style="color:var(--muted);font-size:.62rem;margin-right:.3rem;">{src}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                src_counts = Counter(e.get("source","?") for e in pii_ents)
                src_labels = {"regex":"Regex","arabert":"AraBERT","xlmr":"XLM-RoBERTa"}
                src_html   = " · ".join(f'<span style="color:var(--muted);font-size:.74rem;">{src_labels.get(k,k)}: <span style="color:var(--ink);">{v}</span></span>' for k, v in src_counts.items())
                st.markdown(f'<div style="margin-top:.6rem;">{src_html}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="nopii">{T["no_pii"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with r_right:
            st.markdown(f'<div class="card card-tox"><div class="card-head">{T["tox_head"]}</div>', unsafe_allow_html=True)
            if tox_res:
                label  = tox_res["prediction"]; conf  = tox_res["confidence"]
                probs  = tox_res["all_probs"];  color = TOX_COLOR.get(label, "#00C9A7")
                ar_lbl = T["tox_labels"].get(label, label)
                st.markdown(f'''
<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
  <div><div class="tox-name" style="color:{color};">{ar_lbl}</div>
       <div class="tox-conf"><span dir="ltr">{conf*100:.1f}%</span> {T["confidence"]}</div></div>
  <div style="margin-top:.2rem;">{tox_badge(label, T)}</div>
</div>
<div class="pbar-bg"><div class="pbar-fill" style="width:{conf*100:.1f}%;background:{color};"></div></div>
''', unsafe_allow_html=True)
                rows = ""
                for lbl, p in sorted(probs.items(), key=lambda x: -x[1]):
                    w   = max(2, int(p * 110)); c2 = TOX_COLOR.get(lbl, "#7A7068")
                    ar  = T["tox_labels"].get(lbl, lbl)
                    rows += f'<tr><td>{ar}</td><td><span class="pmini" style="width:{w}px;background:{c2};"></span><span dir="ltr">{p*100:.1f}%</span></td></tr>'
                st.markdown(f'<table class="ptable">{rows}</table>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color:var(--muted);font-size:.84rem;">{T["tox_unavail"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if tox_res and tox_res.get("words"):
            label     = tox_res["prediction"]; color = TOX_COLOR.get(label, "#00C9A7")
            hl_html   = build_highlight_html(tox_res["words"], tox_res["scores"], tox_res["is_stop"], color)
            key_words = sorted([(w,s) for w,s,stop in zip(tox_res["words"],tox_res["scores"],tox_res["is_stop"]) if not stop and s>0.4], key=lambda x:-x[1])[:3]
            key_str   = " · ".join(f'<span style="color:{color};font-weight:700;">{w}</span> <span style="color:var(--muted);font-size:.74rem;">({s:.2f})</span>' for w,s in key_words) if key_words else "—"
            desc_text = "يوضح المخطط تأثير الكلمات في التصنيف، بحيث تظهر الكلمات الأكثر تأثيراً بلون داكن." if st.session_state.language == "ar" else "This map highlights words that influenced the toxicity classification. Darker = more influential."
            st.markdown(f'''
<div class="card card-hl section-gap">
  <div class="card-head">{T["hl_head"]}</div>
  <div style="font-size:.82rem;color:var(--muted);margin-bottom:.8rem;line-height:1.6;">{desc_text}</div>
  <div class="richtext" style="margin-bottom:.7rem;">{hl_html}</div>
  <div style="font-size:.78rem;color:var(--muted);margin-bottom:.45rem;">{T["top_words"]}: {key_str}</div>
  <div class="legend">
    <div class="leg-item"><div class="leg-sq" style="background:{color};opacity:.9;"></div><span>{T["high_attn"]}</span></div>
    <div class="leg-item"><div class="leg-sq" style="background:{color};opacity:.5;"></div><span>{T["med_attn"]}</span></div>
    <div class="leg-item"><div class="leg-sq" style="background:{color};opacity:.2;"></div><span>{T["low_attn"]}</span></div>
    <div class="leg-item"><div class="leg-sq" style="background:rgba(0,0,0,0.06);"></div><span>{T["stop_word"]}</span></div>
  </div>
</div>''', unsafe_allow_html=True)

        if tox_res and tox_res["prediction"] != "Normal":
            st.markdown(f'<div class="card card-rw section-gap"><div class="card-head">{T["rewrite_head"]}</div>', unsafe_allow_html=True)
            if st.session_state.rewritten is None:
                if st.button(T["btn_rewrite"], key="do_rewrite"):
                    masked_plain = build_masked_plain(prompt_, pii_ents)
                    with st.spinner(T["rewriting"]):
                        result = call_rewrite(prompt_, masked_plain, tox_res["prediction"])
                    if result:
                        st.session_state.rewritten = result; st.rerun()
                    else:
                        st.error(T["rewrite_fail"])
            if st.session_state.rewritten:
                rw_left, rw_right = st.columns(2, gap="medium")
                with rw_left:
                    st.markdown(f'<div class="rw-label">{T["orig_label"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="rw-box">{prompt_}</div>', unsafe_allow_html=True)
                with rw_right:
                    st.markdown(f'<div class="rw-label">{T["new_label"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="rw-box">{st.session_state.rewritten}</div>', unsafe_allow_html=True)
                if st.button(T["btn_rewrite"], key="re_rewrite"):
                    masked_plain = build_masked_plain(prompt_, pii_ents)
                    with st.spinner(T["rewriting"]):
                        result = call_rewrite(prompt_, masked_plain, tox_res["prediction"])
                    if result:
                        st.session_state.rewritten = result; st.rerun()
                    else:
                        st.error(T["rewrite_fail"])
            st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────────
st.markdown('''
<div style="margin-top:3rem;padding-top:1rem;border-top:1px solid var(--border);
            display:flex;justify-content:space-between;align-items:center;
            font-size:.72rem;color:var(--muted);">
  <span style="font-family:JetBrains Mono,monospace;font-weight:700;color:var(--navy);">PromptScanner</span>
  <a href="mailto:promptscanner.om@gmail.com" style="color:var(--muted);text-decoration:none;font-family:JetBrains Mono,monospace;">promptscanner.om@gmail.com</a>
</div>
''', unsafe_allow_html=True)
