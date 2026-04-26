import streamlit as st
import torch
import torch.nn.functional as F
import json
import re
import os
import time
import threading
import numpy as np
from pathlib import Path
from collections import Counter
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    AutoModelForSequenceClassification,
)
from huggingface_hub import snapshot_download

HF_TOKEN = st.secrets.get("HF_TOKEN", os.environ.get("HF_TOKEN", ""))

@st.cache_resource(show_spinner="جارٍ تحميل النماذج…")
def download_models():
    if not Path("models").exists():
        snapshot_download(
            repo_id="aynaalh/promptscanner-models",
            token=HF_TOKEN,
            local_dir="models",
        )

download_models()

st.set_page_config(
    page_title="PromptScanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,300;1,9..144,600&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --cream:   #EAE4D9;
    --card:    #F3EDE3;
    --white:   #FDFAF5;
    --navy:    #0F1C35;
    --blue:    #2D5BE3;
    --orange:  #E8520A;
    --orange2: #F26A22;
    --gold:    #C8960A;
    --ink:     #1A1714;
    --muted:   #7A7068;
    --border:  rgba(0,0,0,0.08);
    --teal:    #00C9A7;
    --red:     #D93025;
    --purple:  #6B4FBB;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: var(--cream) !important;
    color: var(--ink) !important;
}

.block-container { padding: 2rem 3rem 4rem; max-width: 1140px; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }

/* ── HEADER ── */
.ps-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 0.5rem;
}
.ps-logo-img {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    object-fit: cover;
}
.ps-wordmark {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    letter-spacing: -1.5px;
    line-height: 1;
}
.ps-wordmark .dark { color: var(--navy); }
.ps-wordmark .orng { color: var(--orange); }
.ps-slogan {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-weight: 300;
    font-size: 0.95rem;
    color: var(--muted);
    margin-top: 2px;
}
.ps-slogan strong { color: var(--orange); font-style: italic; font-weight: 300; }
.ps-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    opacity: 0.6;
    margin-bottom: 1.2rem;
    margin-top: 0.3rem;
}
.ps-rule {
    height: 1px;
    background: linear-gradient(90deg, var(--orange), var(--blue) 45%, transparent);
    margin-bottom: 2rem;
    opacity: 0.25;
}

/* ── TEXTAREA ── */
.stTextArea textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--ink) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 1rem !important;
    line-height: 1.7 !important;
    direction: rtl;
    transition: border-color .2s, box-shadow .2s;
    box-shadow: 0 1px 0 rgba(255,255,255,0.8) inset !important;
}
.stTextArea textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(232,82,10,0.12) !important;
}

/* ── BUTTONS ── */
div[data-testid="stButton"] button {
    background: var(--orange) !important;
    color: #fff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: .82rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .6rem 1.6rem !important;
    letter-spacing: .06em !important;
    transition: all .2s !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(232,82,10,0.25) !important;
}
div[data-testid="stButton"] button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(232,82,10,0.3) !important;
}

/* ── STATUS BAR ── */
.sbar {
    display: flex; flex-wrap: wrap; gap: .75rem;
    padding: .7rem 1.1rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 1.4rem;
    font-size: .78rem;
    box-shadow: 0 1px 0 rgba(255,255,255,0.8) inset;
}
.si { display: flex; align-items: center; gap: .35rem; }
.dot { width: 7px; height: 7px; border-radius: 50%; }
.dot-on  { background: var(--teal); box-shadow: 0 0 6px var(--teal); }
.dot-off { background: var(--muted); }
.si-label { color: var(--muted); font-family: 'JetBrains Mono', monospace; font-size: .72rem; }

/* ── CARDS ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: .8rem;
    box-shadow: 0 1px 0 rgba(255,255,255,0.85) inset, 0 4px 20px rgba(15,28,53,0.06);
}
.card-pii    { border-top: 3px solid var(--orange); }
.card-tox    { border-top: 3px solid var(--blue); }
.card-hl     { border-top: 3px solid var(--purple); }
.card-head {
    font-family: 'JetBrains Mono', monospace;
    font-size: .68rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .9rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}

/* ── RICHTEXT / MASKED ── */
.richtext {
    font-size: 1rem;
    line-height: 2.2;
    padding: .9rem 1rem;
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    direction: rtl;
    text-align: right;
    word-break: break-word;
    color: var(--ink);
}
.tag-pii {
    display: inline-block;
    background: rgba(232,82,10,0.10);
    color: var(--orange);
    border: 1px solid rgba(232,82,10,0.3);
    border-radius: 5px;
    padding: 1px 7px;
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem;
    margin: 0 2px;
    vertical-align: middle;
}

/* ── ENTITY PILLS ── */
.epills { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .8rem; }
.epill {
    display: flex; align-items: center; gap: .35rem;
    background: rgba(232,82,10,0.07);
    border: 1px solid rgba(232,82,10,0.2);
    border-radius: 20px;
    padding: .22rem .75rem;
    font-size: .8rem;
}
.epill-lbl { color: var(--orange); font-family: 'JetBrains Mono', monospace; font-size: .68rem; font-weight: 700; }
.epill-val { color: var(--ink); }

/* ── TOXICITY ── */
.tox-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}
.tox-conf { color: var(--muted); font-size: .88rem; margin-top: .1rem; }
.pbar-bg {
    background: rgba(0,0,0,0.08);
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
    margin-top: .5rem;
}
.pbar-fill { height: 100%; border-radius: 4px; }
.ptable { width: 100%; border-collapse: collapse; font-size: .84rem; margin-top: .9rem; }
.ptable td { padding: .35rem 0; border-bottom: 1px solid var(--border); }
.ptable td:first-child { color: var(--muted); }
.ptable td:last-child { text-align: right; font-family: 'JetBrains Mono', monospace; font-size: .76rem; }
.pmini { display: inline-block; height: 5px; border-radius: 3px; vertical-align: middle; margin-right: .35rem; }

/* ── BADGES ── */
.badge {
    display: inline-block;
    padding: .18rem .7rem;
    border-radius: 20px;
    font-size: .7rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    letter-spacing: .06em;
}
.b-safe { background: rgba(0,201,167,0.10); color: var(--teal);   border: 1px solid rgba(0,201,167,0.3); }
.b-warn { background: rgba(232,82,10,0.10); color: var(--orange); border: 1px solid rgba(232,82,10,0.3); }
.b-flag { background: rgba(217,48,37,0.10); color: var(--red);    border: 1px solid rgba(217,48,37,0.3); }
.b-crit { background: rgba(107,79,187,0.10);color: var(--purple); border: 1px solid rgba(107,79,187,0.3); }

/* ── ATTENTION ── */
.hl-word { display: inline-block; border-radius: 5px; padding: 1px 7px; margin: 0 2px; font-size: 1rem; }

/* ── LEGEND ── */
.legend { display: flex; gap: 1rem; flex-wrap: wrap; font-size: .76rem; color: var(--muted); margin-top: .6rem; }
.leg-item { display: flex; align-items: center; gap: .3rem; }
.leg-sq { width: 12px; height: 12px; border-radius: 3px; }

/* ── NO PII ── */
.nopii {
    color: var(--teal);
    font-family: 'JetBrains Mono', monospace;
    font-size: .84rem;
    padding: .4rem 0;
}

/* ── EXAMPLE BUTTONS ── */
div[data-testid="stButton"] button[kind="secondary"] {
    background: var(--white) !important;
    color: var(--ink) !important;
    border: 1px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .72rem !important;
    box-shadow: none !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    border-color: var(--orange) !important;
    color: var(--orange) !important;
    box-shadow: none !important;
}

.section-gap { margin-top: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
ARABERT_CATEGORIES = ['PERS', 'ORG', 'ADDRESS', 'DATETIME']
XLMR_CATEGORIES    = ['ID', 'CREDENTIAL']
REGEX_CATEGORIES   = ['PHONE', 'EMAIL', 'IP', 'MAC', 'URL', 'FINANCIAL_INFO']

TOX_IDX2LABEL = {
    0: 'Dangerous', 1: 'Mental Health', 2: 'Mild Offense',
    3: 'Normal',    4: 'Obscene',       5: 'Offensive',
    6: 'Privacy Violation',
}
TOX_LABEL2IDX = {v: k for k, v in TOX_IDX2LABEL.items()}
DANGER_CATS   = {'Dangerous', 'Obscene', 'Mental Health'}
WARN_CATS     = {'Offensive', 'Privacy Violation', 'Mild Offense'}

TOX_COLOR = {
    'Normal':            '#00C9A7',
    'Mild Offense':      '#E8520A',
    'Offensive':         '#F26A22',
    'Privacy Violation': '#2D5BE3',
    'Obscene':           '#D93025',
    'Dangerous':         '#D93025',
    'Mental Health':     '#6B4FBB',
}

TOX_LABELS_AR = {
    'Normal':            'عادي',
    'Mild Offense':      'مسيء بشكل خفيف',
    'Offensive':         'مسيء',
    'Privacy Violation': 'انتهاك الخصوصية',
    'Obscene':           'محتوى فاضح',
    'Dangerous':         'خطير',
    'Mental Health':     'صحة نفسية',
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

# ─────────────────────────────────────────────────────────────
# REGEX ENGINE
# ─────────────────────────────────────────────────────────────
REGEX_PATTERNS = {
    'PHONE': [
        r'\+968\s?[79]\d{7}', r'00968\s?[79]\d{7}',
        r'\b[79]\d{7}\b', r'\b[79]\d{3}[\s\-]\d{4}\b',
        r'\+968\s[79]\d{3}\s\d{4}',
    ],
    'EMAIL':          [r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'],
    'IP':             [r'\b(?:\d{1,3}\.){3}\d{1,3}\b'],
    'MAC':            [r'\b([0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}\b', r'\b[0-9A-Fa-f]{12}\b'],
    'URL':            [r'https?://[^\s<>"]+', r'www\.[^\s<>"]+'],
    'FINANCIAL_INFO': [
        r'\b4\d{3}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
        r'\b5[1-5]\d{2}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
        r'\bOM\d{2}[A-Z]{3}\d{16}\b',
    ],
}

def regex_detect(text):
    found = []
    for pii_type, patterns in REGEX_PATTERNS.items():
        for pat in patterns:
            for m in re.finditer(pat, text):
                found.append({'value': m.group(), 'type': pii_type,
                               'char_start': m.start(), 'char_end': m.end(), 'source': 'regex'})
    found.sort(key=lambda x: (x['char_start'], -(x['char_end'] - x['char_start'])))
    filtered, last_end = [], -1
    for it in found:
        if it['char_start'] >= last_end:
            filtered.append(it)
            last_end = it['char_end']
    return filtered

# ─────────────────────────────────────────────────────────────
# MODEL LOADING
# ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_arabert():
    path = MODELS_DIR / "arabert_pii_aug" / "arabert_pii_aug"
    if not path.exists():
        return None, None, None
    try:
        tok   = AutoTokenizer.from_pretrained(str(path))
        model = AutoModelForTokenClassification.from_pretrained(str(path))
        model.eval()
        vocab_file = next(
            (p for p in [path/"tag_vocab.json", path/"tag_vocab_aug.json"] if p.exists()), None
        )
        if vocab_file is None:
            return None, None, None
        with open(vocab_file) as f:
            v = json.load(f)
        id2tag = {int(k): lbl for k, lbl in v["id2tag"].items()}
        return tok, model, id2tag
    except Exception as e:
        return None, None, str(e)

@st.cache_resource(show_spinner=False)
def load_xlmr():
    path = MODELS_DIR / "xlmr_pii" / "xlmr_pii_augmorg"
    if not path.exists():
        return None, None, None
    try:
        tok   = AutoTokenizer.from_pretrained(str(path))
        model = AutoModelForTokenClassification.from_pretrained(str(path))
        model.eval()
        vocab_file = next(
            (p for p in [path/"tag_vocab.json", path/"tag_vocab_augmorg.json"] if p.exists()), None
        )
        if vocab_file is None:
            return None, None, None
        with open(vocab_file) as f:
            v = json.load(f)
        id2tag = {int(k): lbl for k, lbl in v["id2tag"].items()}
        return tok, model, id2tag
    except Exception as e:
        return None, None, str(e)

@st.cache_resource(show_spinner=False)
def load_toxicity():
    path = MODELS_DIR / "tox_model"
    if not path.exists():
        return None, None
    ckpt_file = None
    for candidate in ["arabert_expanded.pt", "arabert_contrast.pt", "best_model.pt"]:
        if (path / candidate).exists():
            ckpt_file = path / candidate
            break
    if ckpt_file is None:
        pts = list(path.glob("*.pt"))
        if pts:
            ckpt_file = pts[0]
    if ckpt_file is None:
        return None, None
    try:
        tok   = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
        model = AutoModelForSequenceClassification.from_pretrained(
            "aubmindlab/bert-base-arabertv02", num_labels=7,
            ignore_mismatched_sizes=True, attn_implementation="eager",
        )
        ckpt = torch.load(str(ckpt_file), map_location="cpu", weights_only=False)
        model.load_state_dict(ckpt["model_state_dict"])
        model.eval()
        return tok, model
    except Exception as e:
        return None, str(e)

# ─────────────────────────────────────────────────────────────
# ARABIC PREPROCESSING
# ─────────────────────────────────────────────────────────────
def clean_arabic(text):
    if not text: return ""
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ؤ', 'و', text)
    text = re.sub(r'ئ', 'ي', text)
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

# ─────────────────────────────────────────────────────────────
# NER + HYBRID DETECT
# ─────────────────────────────────────────────────────────────
def _token_char_ranges(tokens):
    ranges, pos = {}, 0
    for i, tok in enumerate(tokens):
        ranges[i] = (pos, pos + len(tok))
        pos += len(tok) + 1
    return ranges

def _token_overlaps_regex(tok_s, tok_e, tok_char, regex_spans):
    if tok_s not in tok_char: return False
    cs = tok_char[tok_s][0]
    ce = tok_char.get(tok_e - 1, tok_char[tok_s])[1]
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
            if cur:
                entities.append({"value": " ".join(cur_toks), "type": cur,
                                   "token_start": i - len(cur_toks), "token_end": i})
            cur, cur_toks = tag[2:], [tok]
        elif tag.startswith("I-") and cur == tag[2:]:
            cur_toks.append(tok)
        else:
            if cur:
                entities.append({"value": " ".join(cur_toks), "type": cur,
                                   "token_start": i - len(cur_toks), "token_end": i})
            cur, cur_toks = None, []
    if cur:
        entities.append({"value": " ".join(cur_toks), "type": cur,
                           "token_start": len(tokens) - len(cur_toks), "token_end": len(tokens)})
    return entities

def hybrid_detect(text, arabert_tok, arabert_mdl, arabert_id2tag,
                  xlmr_tok, xlmr_mdl, xlmr_id2tag):
    tokens     = text.split()
    all_ents   = []
    regex_hits = regex_detect(text)
    regex_spans = [(e["char_start"], e["char_end"]) for e in regex_hits]
    all_ents.extend(regex_hits)
    tok_char = _token_char_ranges(tokens)
    if arabert_mdl is not None:
        for e in _predict_ner(text, arabert_tok, arabert_mdl, arabert_id2tag):
            if e["type"] not in ARABERT_CATEGORIES: continue
            if _token_overlaps_regex(e["token_start"], e["token_end"], tok_char, regex_spans): continue
            e["source"] = "arabert"; all_ents.append(e)
    if xlmr_mdl is not None:
        for e in _predict_ner(text, xlmr_tok, xlmr_mdl, xlmr_id2tag):
            if e["type"] not in XLMR_CATEGORIES: continue
            if _token_overlaps_regex(e["token_start"], e["token_end"], tok_char, regex_spans): continue
            e["source"] = "xlmr"; all_ents.append(e)
    return all_ents

# ─────────────────────────────────────────────────────────────
# TOXICITY INFERENCE
# ─────────────────────────────────────────────────────────────
def predict_toxicity_with_attention(text, tokenizer, model):
    processed = clean_arabic(text)
    if not processed: return None
    enc  = tokenizer(processed, max_length=128, padding="max_length",
                     truncation=True, return_tensors="pt")
    ids  = enc["input_ids"]
    mask = enc["attention_mask"]
    tids = enc.get("token_type_ids", torch.zeros_like(ids))
    with torch.no_grad():
        out   = model(ids, attention_mask=mask, token_type_ids=tids, output_attentions=True)
        probs = F.softmax(out.logits, dim=1).squeeze().cpu().numpy()
    attn   = torch.stack(out.attentions)[:, 0, :, 0, :].mean(dim=(0, 1)).cpu().numpy()
    tokens = tokenizer.convert_ids_to_tokens(ids.squeeze().cpu().numpy())
    actual_len = mask.sum().item()
    tokens, attn = tokens[:actual_len], attn[:actual_len]
    words, scores, cur_w, cur_s = [], [], "", []
    for tok, sc in zip(tokens, attn):
        if tok in ["[CLS]", "[SEP]", "[PAD]", "<s>", "</s>", "<pad>"]: continue
        if tok.startswith("##"):
            cur_w += tok[2:]; cur_s.append(sc)
        elif tok.startswith("+"):
            cur_w += tok.replace("+", ""); cur_s.append(sc)
        else:
            if cur_w: words.append(cur_w); scores.append(float(max(cur_s)))
            cur_w, cur_s = tok.replace("+", ""), [sc]
    if cur_w: words.append(cur_w); scores.append(float(max(cur_s)))
    scores_arr = np.array(scores, dtype=float)
    filtered   = np.array([0.0 if w in ARABIC_STOP_WORDS else s for w, s in zip(words, scores_arr)])
    is_stop    = [w in ARABIC_STOP_WORDS for w in words]
    if filtered.max() > 0: filtered /= filtered.max()
    pred_idx   = int(np.argmax(probs))
    pred_label = TOX_IDX2LABEL[pred_idx]
    return {
        "prediction": pred_label,
        "confidence": float(probs[pred_idx]),
        "all_probs":  {TOX_IDX2LABEL[i]: float(p) for i, p in enumerate(probs)},
        "words":      words,
        "scores":     filtered.tolist(),
        "is_stop":    is_stop,
    }

# ─────────────────────────────────────────────────────────────
# HTML BUILDERS
# ─────────────────────────────────────────────────────────────
def build_masked_html(text, entities):
    char_ents = sorted([e for e in entities if "char_start" in e],
                       key=lambda x: x["char_start"], reverse=True)
    out = text
    for e in char_ents:
        out = out[:e["char_start"]] + f'<span class="tag-pii">[{e["type"]}]</span>' + out[e["char_end"]:]
    for e in [e for e in entities if "token_start" in e]:
        if e["value"] and e["value"] in out:
            out = out.replace(e["value"], f'<span class="tag-pii">[{e["type"]}]</span>', 1)
    return out

def build_highlight_html(words, scores, is_stop, color_hex):
    def hex_rgb(h):
        h = h.lstrip("#")
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
    rgb = hex_rgb(color_hex)
    parts = []
    for word, score, stop in zip(words, scores, is_stop):
        if stop:
            parts.append(f'<span class="hl-word" style="background:rgba(0,0,0,0.05);color:#999;">{word}</span>')
        elif score > 0.7:
            a = 0.15 + score * 0.75
            parts.append(f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});color:#fff;font-weight:700;" title="{score:.2f}">{word}</span>')
        elif score > 0.4:
            a = 0.1 + score * 0.65
            parts.append(f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});color:{color_hex};" title="{score:.2f}">{word}</span>')
        elif score > 0.1:
            a = 0.05 + score * 0.4
            parts.append(f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});color:#666;" title="{score:.2f}">{word}</span>')
        else:
            parts.append(f'<span class="hl-word" style="color:#aaa;">{word}</span>')
    return " ".join(parts)

def tox_badge(label):
    if label == "Normal":        return '<span class="badge b-safe">آمن</span>'
    if label == "Mental Health": return '<span class="badge b-crit">خطر</span>'
    if label in DANGER_CATS:     return '<span class="badge b-flag">مُبلَّغ</span>'
    return '<span class="badge b-warn">تحذير</span>'

# ─────────────────────────────────────────────────────────────
# PARALLEL SCAN
# ─────────────────────────────────────────────────────────────
def run_scan(text, ar_tok, ar_mdl, ar_id2tag, xl_tok, xl_mdl, xl_id2tag, tx_tok, tx_mdl):
    results = {}
    def pii_job():
        results["pii"] = hybrid_detect(text, ar_tok, ar_mdl, ar_id2tag, xl_tok, xl_mdl, xl_id2tag)
    def tox_job():
        results["tox"] = predict_toxicity_with_attention(text, tx_tok, tx_mdl) if tx_mdl else None
    t1 = threading.Thread(target=pii_job)
    t2 = threading.Thread(target=tox_job)
    t1.start(); t2.start(); t1.join(); t2.join()
    return results

# ─────────────────────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────────────────────
with st.spinner("جارٍ تحميل النماذج…"):
    ar_tok, ar_mdl, ar_id2tag = load_arabert()
    xl_tok, xl_mdl, xl_id2tag = load_xlmr()
    tx_tok, tx_mdl            = load_toxicity()

ar_ok = ar_mdl is not None
xl_ok = xl_mdl is not None
tx_ok = tx_mdl is not None

# ─────────────────────────────────────────────────────────────
# UI — HEADER
# ─────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 11])
with col_logo:
    from pathlib import Path as P
    logo_path = P("assets/logo.png")
    if logo_path.exists():
        st.image(str(logo_path), width=52)
with col_title:
    st.markdown("""
<div class="ps-wordmark">
  <span class="dark">Prompt</span><span class="orng">Scanner</span>
</div>
<div class="ps-slogan">حارس خصوصيتك في عالم <strong>الذكاء الاصطناعي</strong></div>
""", unsafe_allow_html=True)

st.markdown('<div class="ps-sub">Arabic PII Detection · Toxicity Classification · Final Year Project — SQU</div>', unsafe_allow_html=True)
st.markdown('<div class="ps-rule"></div>', unsafe_allow_html=True)

# Model status bar
st.markdown(f"""
<div class="sbar">
  <div class="si"><div class="dot {'dot-on' if ar_ok else 'dot-off'}"></div>
    <span class="si-label">AraBERT — كشف الأشخاص والمؤسسات والعناوين</span></div>
  <div class="si"><div class="dot {'dot-on' if xl_ok else 'dot-off'}"></div>
    <span class="si-label">XLM-RoBERTa — كشف الهويات والبيانات الحساسة</span></div>
  <div class="si"><div class="dot dot-on"></div>
    <span class="si-label">محرك Regex — الهاتف والبريد وIP والروابط</span></div>
  <div class="si"><div class="dot {'dot-on' if tx_ok else 'dot-off'}"></div>
    <span class="si-label">AraBERT v2 — تحليل السمية</span></div>
</div>
""", unsafe_allow_html=True)

# Example prompts
EXAMPLES = [
    ("اسم + مؤسسة",        "اسمي محمد المقبالي وأعمل في بنك مسقط"),
    ("هاتف + بريد",         "رقمي +968 91234567 وبريدي ahmed@squ.edu.om"),
    ("هوية + بيانات دخول", "رقم هويتي 12345678 وكلمة المرور MyPass123!"),
    ("محتوى خطير",          "كيف أصنع قنبلة لتدمير مبنى"),
    ("صحة نفسية",           "أريد أن أنهي حياتي لم أعد أتحمل"),
    ("محتوى مسيء",          "يا حمار أنت غبي جداً"),
    ("محتوى عادي",          "اكتب لي قصيدة عن الربيع"),
]

if "prompt" not in st.session_state:
    st.session_state.prompt = ""

cols = st.columns(len(EXAMPLES))
for col, (lbl, ex) in zip(cols, EXAMPLES):
    with col:
        if st.button(lbl, key=f"ex_{lbl}", use_container_width=True):
            st.session_state.prompt = ex

prompt = st.text_area(
    "prompt_input",
    value=st.session_state.prompt,
    height=110,
    placeholder="اكتب أو الصق النص العربي هنا…",
    label_visibility="collapsed",
)

c1, c2, _ = st.columns([1, 1, 6])
with c1:
    scan_clicked = st.button("⟶ فحص", use_container_width=True)
with c2:
    if st.button("✕ مسح", use_container_width=True):
        st.session_state.prompt = ""
        st.rerun()

# ─────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────
if scan_clicked and prompt.strip():
    with st.spinner("جارٍ الفحص…"):
        t0 = time.time()
        res = run_scan(prompt.strip(),
                       ar_tok, ar_mdl, ar_id2tag,
                       xl_tok, xl_mdl, xl_id2tag,
                       tx_tok, tx_mdl)
        elapsed = round(time.time() - t0, 2)

    pii_ents = res.get("pii", [])
    tox_res  = res.get("tox")

    st.markdown(
        f'<div style="color:var(--muted);font-size:.76rem;font-family:JetBrains Mono,monospace;'
        f'margin-bottom:1rem;">تم الفحص في {elapsed}s</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="large")

    # ── LEFT: PII ──────────────────────────────────────────
    with left:
        n_pii = len(pii_ents)
        badge = (f'<span class="badge b-warn">{n_pii} نتيجة</span>'
                 if n_pii else '<span class="badge b-safe">نظيف</span>')
        st.markdown(
            f'<div class="card card-pii">'
            f'<div class="card-head">◆ كشف المعلومات الشخصية &nbsp; {badge}</div>',
            unsafe_allow_html=True,
        )
        if pii_ents:
            masked = build_masked_html(prompt.strip(), pii_ents)
            st.markdown(f'<div class="richtext">{masked}</div>', unsafe_allow_html=True)
            st.markdown('<div class="epills">', unsafe_allow_html=True)
            for e in pii_ents:
                src_label = {"regex": "RGX", "arabert": "NER", "xlmr": "XLM"}.get(e.get("source",""), "")
                st.markdown(
                    f'<div class="epill">'
                    f'<span class="epill-lbl">{e["type"]}</span>'
                    f'<span class="epill-val">{e["value"]}</span>'
                    f'<span style="color:var(--muted);font-size:.65rem;margin-right:.3rem;">{src_label}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
            src_counts = Counter(e.get("source","?") for e in pii_ents)
            src_labels = {"regex": "Regex", "arabert": "AraBERT", "xlmr": "XLM-RoBERTa"}
            src_html = " · ".join(
                f'<span style="color:var(--muted);font-size:.76rem;">{src_labels.get(k,k)}: '
                f'<span style="color:var(--ink);">{v}</span></span>'
                for k, v in src_counts.items()
            )
            st.markdown(f'<div style="margin-top:.7rem;">{src_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="nopii">✓ لا توجد معلومات شخصية في هذا النص.</div>',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: Toxicity ────────────────────────────────────
    with right:
        st.markdown(
            '<div class="card card-tox">'
            '<div class="card-head">◆ تحليل السمية</div>',
            unsafe_allow_html=True,
        )
        if tox_res:
            label = tox_res["prediction"]
            conf  = tox_res["confidence"]
            probs = tox_res["all_probs"]
            color = TOX_COLOR.get(label, "#00C9A7")
            ar_label = TOX_LABELS_AR.get(label, label)
            st.markdown(f"""
<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
  <div>
    <div class="tox-name" style="color:{color};">{ar_label}</div>
    <div class="tox-conf">درجة الثقة: {conf*100:.1f}%</div>
  </div>
  <div style="margin-top:.25rem;">{tox_badge(label)}</div>
</div>
<div class="pbar-bg">
  <div class="pbar-fill" style="width:{conf*100:.1f}%;background:{color};"></div>
</div>
""", unsafe_allow_html=True)
            rows = ""
            for lbl, p in sorted(probs.items(), key=lambda x: -x[1]):
                w  = max(2, int(p * 120))
                c2 = TOX_COLOR.get(lbl, "#7A7068")
                ar = TOX_LABELS_AR.get(lbl, lbl)
                rows += (f'<tr><td>{ar}</td>'
                         f'<td><span class="pmini" style="width:{w}px;background:{c2};"></span>'
                         f'{p*100:.1f}%</td></tr>')
            st.markdown(f'<table class="ptable">{rows}</table>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="color:var(--muted);font-size:.86rem;padding:.5rem 0;">'
                'نموذج السمية غير محمّل.</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ATTENTION HIGHLIGHT ────────────────────────────────
    if tox_res and tox_res.get("words"):
        label   = tox_res["prediction"]
        color   = TOX_COLOR.get(label, "#00C9A7")
        hl_html = build_highlight_html(tox_res["words"], tox_res["scores"], tox_res["is_stop"], color)
        key_words = sorted(
            [(w, s) for w, s, stop in zip(tox_res["words"], tox_res["scores"], tox_res["is_stop"])
             if not stop and s > 0.4],
            key=lambda x: -x[1]
        )[:3]
        key_str = " · ".join(
            f'<span style="color:{color};font-weight:700;">{w}</span> '
            f'<span style="color:var(--muted);font-size:.76rem;">({s:.2f})</span>'
            for w, s in key_words
        ) if key_words else "—"
        st.markdown(f"""
<div class="card card-hl section-gap">
  <div class="card-head">◆ الكلمات المؤثرة — الكلمات التي أثّرت في التصنيف</div>
  <div class="richtext" style="margin-bottom:.8rem;">{hl_html}</div>
  <div style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem;">
    أبرز الكلمات: {key_str}
  </div>
  <div class="legend">
    <div class="leg-item"><div class="leg-sq" style="background:{color};opacity:.9;"></div><span>تأثير عالٍ (&gt;0.7)</span></div>
    <div class="leg-item"><div class="leg-sq" style="background:{color};opacity:.5;"></div><span>تأثير متوسط (0.4–0.7)</span></div>
    <div class="leg-item"><div class="leg-sq" style="background:{color};opacity:.2;"></div><span>تأثير منخفض (0.1–0.4)</span></div>
    <div class="leg-item"><div class="leg-sq" style="background:rgba(0,0,0,0.06);"></div><span>حرف وصل</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

elif scan_clicked and not prompt.strip():
    st.warning("الرجاء إدخال نص قبل الفحص.")

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:4rem;padding-top:1rem;border-top:1px solid var(--border);
            display:flex;justify-content:space-between;align-items:center;
            font-size:.74rem;color:var(--muted);">
  <span style="font-family:JetBrains Mono,monospace;font-weight:700;color:var(--navy);">PromptScanner</span>
  <span>كشف المعلومات الشخصية · تحليل السمية · مشروع التخرج — SQU</span>
</div>
""", unsafe_allow_html=True)
