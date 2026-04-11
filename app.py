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

import os
from huggingface_hub import snapshot_download

HF_TOKEN = st.secrets.get("HF_TOKEN", os.environ.get("HF_TOKEN", ""))

@st.cache_resource(show_spinner="Downloading models from HuggingFace Hub...")
def download_models():
    if not Path("models").exists():
        snapshot_download(
            repo_id="aynaalh/promptscanner-models",
            token=HF_TOKEN,
            local_dir="models",
        )

download_models()

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PromptScanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

:root {
    --bg:      #0d0f14;
    --surf:    #141720;
    --surf2:   #1a1f2e;
    --border:  #252a38;
    --amber:   #f5a623;
    --teal:    #00c9a7;
    --red:     #ff4d6d;
    --purple:  #9b59ff;
    --muted:   #5a6075;
    --text:    #cdd3e0;
    --dim:     #7b8299;
}
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.block-container { padding: 2rem 3rem 4rem; max-width: 1140px; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }

/* ── header ── */
.ps-logo {
    font-family: 'Space Mono', monospace;
    font-size: 2.6rem; font-weight: 700;
    color: var(--amber); letter-spacing: -2px;
    margin-bottom: 0.1rem;
}
.ps-logo span { color: var(--teal); }
.ps-sub { font-size: 0.78rem; color: var(--muted); letter-spacing: .16em; text-transform: uppercase; margin-bottom: 1rem; }
.ps-rule { height: 1px; background: linear-gradient(90deg, var(--amber), var(--teal) 45%, transparent); margin-bottom: 2rem; }

/* ── textarea ── */
.stTextArea textarea {
    background: var(--surf) !important; border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 1.05rem !important;
    padding: 1rem !important; line-height: 1.7 !important; direction: rtl;
    transition: border-color .2s;
}
.stTextArea textarea:focus { border-color: var(--amber) !important; box-shadow: 0 0 0 2px rgba(245,166,35,.15) !important; }

/* ── primary button ── */
div[data-testid="stButton"] button {
    background: var(--amber) !important; color: #0d0f14 !important;
    font-family: 'Space Mono', monospace !important; font-weight: 700 !important;
    font-size: .88rem !important; border: none !important; border-radius: 8px !important;
    padding: .55rem 1.8rem !important; letter-spacing: .05em !important;
    transition: all .2s !important; cursor: pointer !important;
}
div[data-testid="stButton"] button:hover {
    background: #ffc043 !important; transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(245,166,35,.3) !important;
}

/* ── cards ── */
.card { background: var(--surf); border: 1px solid var(--border); border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: .8rem; }
.card-pii  { border-left: 3px solid var(--amber); }
.card-tox  { border-left: 3px solid var(--teal); }
.card-hl   { border-left: 3px solid var(--purple); }
.card-head { font-family: 'Space Mono', monospace; font-size: .7rem; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); margin-bottom: .9rem; }

/* ── status bar ── */
.sbar { display: flex; flex-wrap: wrap; gap: .75rem; padding: .65rem 1rem;
        background: var(--surf); border: 1px solid var(--border); border-radius: 8px;
        margin-bottom: 1.4rem; font-size: .78rem; }
.si { display: flex; align-items: center; gap: .35rem; }
.dot { width: 7px; height: 7px; border-radius: 50%; }
.dot-on  { background: var(--teal); box-shadow: 0 0 6px var(--teal); }
.dot-off { background: var(--muted); }
.si-label { color: var(--dim); }

/* ── masked / highlighted text ── */
.richtext { font-size: 1rem; line-height: 2.2; padding: .9rem; background: rgba(0,0,0,.22); border-radius: 8px; direction: rtl; text-align: right; word-break: break-word; }
.tag-pii { display: inline-block; background: rgba(245,166,35,.18); color: var(--amber); border: 1px solid rgba(245,166,35,.4); border-radius: 4px; padding: 1px 7px; font-family: 'Space Mono', monospace; font-size: .72rem; margin: 0 2px; vertical-align: middle; }

/* ── attention highlights ── */
.hl-word { display: inline-block; border-radius: 4px; padding: 1px 7px; margin: 0 2px; font-size: 1rem; transition: opacity .2s; }

/* ── entity pills ── */
.epills { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .7rem; }
.epill { display: flex; align-items: center; gap: .35rem; background: rgba(245,166,35,.1); border: 1px solid rgba(245,166,35,.25); border-radius: 20px; padding: .2rem .7rem; font-size: .8rem; }
.epill-lbl { color: var(--amber); font-family: 'Space Mono', monospace; font-size: .68rem; font-weight: 700; }
.epill-val { color: var(--text); }

/* ── toxicity gauge ── */
.tox-name { font-family: 'Space Mono', monospace; font-size: 1.6rem; font-weight: 700; }
.tox-conf { color: var(--dim); font-size: .88rem; margin-top: .1rem; }
.pbar-bg { background: var(--border); border-radius: 4px; height: 8px; overflow: hidden; margin-top: .4rem; }
.pbar-fill { height: 100%; border-radius: 4px; }
.ptable { width: 100%; border-collapse: collapse; font-size: .84rem; margin-top: .9rem; }
.ptable td { padding: .35rem 0; border-bottom: 1px solid var(--border); }
.ptable td:first-child { color: var(--dim); }
.ptable td:last-child { text-align: right; font-family: 'Space Mono', monospace; font-size: .76rem; }
.pmini { display: inline-block; height: 5px; border-radius: 3px; vertical-align: middle; margin-right: .35rem; }

/* ── badges ── */
.badge { display: inline-block; padding: .18rem .65rem; border-radius: 20px; font-size: .72rem; font-family: 'Space Mono', monospace; font-weight: 700; letter-spacing: .04em; }
.b-safe   { background: rgba(0,201,167,.14); color: var(--teal);   border: 1px solid rgba(0,201,167,.3); }
.b-warn   { background: rgba(245,166,35,.14); color: var(--amber); border: 1px solid rgba(245,166,35,.3); }
.b-flag   { background: rgba(255,77,109,.14); color: var(--red);   border: 1px solid rgba(255,77,109,.3); }
.b-crit   { background: rgba(155,89,255,.14); color: var(--purple);border: 1px solid rgba(155,89,255,.3); }

/* ── legend ── */
.legend { display: flex; gap: 1rem; flex-wrap: wrap; font-size: .76rem; color: var(--dim); margin-top: .6rem; }
.leg-item { display: flex; align-items: center; gap: .3rem; }
.leg-sq { width: 12px; height: 12px; border-radius: 3px; }

/* ── no-pii ── */
.nopii { color: var(--teal); font-family: 'Space Mono', monospace; font-size: .84rem; padding: .4rem 0; }

/* ── divider ── */
.section-gap { margin-top: 1.2rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CONSTANTS — must match your notebooks exactly
# ─────────────────────────────────────────────────────────────
ARABERT_CATEGORIES = ['PERS', 'ORG', 'ADDRESS', 'DATETIME']
XLMR_CATEGORIES    = ['ID', 'CREDENTIAL']
REGEX_CATEGORIES   = ['PHONE', 'EMAIL', 'IP', 'MAC', 'URL', 'FINANCIAL_INFO']

# Toxicity label order — must match label2idx in Cell 3 of toxicity notebook
# CATEGORIES = ['dangerous','mental_health','mild_offense','normal','obscene','offensive','privacy_violation']
TOX_IDX2LABEL = {
    0: 'Dangerous',
    1: 'Mental Health',
    2: 'Mild Offense',
    3: 'Normal',
    4: 'Obscene',
    5: 'Offensive',
    6: 'Privacy Violation',
}
TOX_LABEL2IDX = {v: k for k, v in TOX_IDX2LABEL.items()}

DANGER_CATS = {'Dangerous', 'Obscene', 'Mental Health'}
WARN_CATS   = {'Offensive', 'Privacy Violation', 'Mild Offense'}

# Attention-highlight color per category (teal=normal, amber/orange=warn, red/purple=danger)
TOX_COLOR = {
    'Normal':           '#00c9a7',
    'Mild Offense':     '#f5a623',
    'Offensive':        '#ff8c42',
    'Privacy Violation':'#4db8ff',
    'Obscene':          '#ff4d6d',
    'Dangerous':        '#ff4d6d',
    'Mental Health':    '#9b59ff',
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
# REGEX ENGINE  (matches OmaniPIIPatterns in notebook)
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
    """
    Load the fine-tuned AraBERT NER model.
    Expects: arabert_pii/  on huggingface with pytorch_model.bin (or .safetensors),
             config.json, tokenizer files, and tag_vocab.json
    tag_vocab.json format: {"tag2id": {...}, "id2tag": {"0": "O", ...}}
    Saved in notebook cell 98 as arabert_pii_augmorg/
    """
    path = MODELS_DIR / "arabert_pii"
    if not path.exists():
        return None, None, None
    try:
        tok   = AutoTokenizer.from_pretrained(str(path))
        model = AutoModelForTokenClassification.from_pretrained(str(path), use_fast=False )
        model.eval()
        vocab_file = next(
            (p for p in [path/"tag_vocab.json", path/"tag_vocab_augmorg.json"] if p.exists()),
            None
        )
        if vocab_file is None:
            return None, None, "tag_vocab.json not found"
        with open(vocab_file) as f:
            v = json.load(f)
        id2tag = {int(k): lbl for k, lbl in v["id2tag"].items()}
        return tok, model, id2tag
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None


@st.cache_resource(show_spinner=False)
def load_xlmr():
    """
    Load the fine-tuned XLM-RoBERTa model for ID/CREDENTIAL.
    Expects: xlmr_pii/ on huggingface with same structure.
    tag_vocab.json keys: id2tag entries like "0":"O", "1":"B-ID" etc.
    Saved in notebook cell 98 as xlmr_pii_augmorg/
    """
    path = MODELS_DIR / "xlmr_pii"
    if not path.exists():
        return None, None, None
    try:
        tok   = AutoTokenizer.from_pretrained(str(path), use_fast=False )
        model = AutoModelForTokenClassification.from_pretrained(str(path))
        model.eval()
        vocab_file = next(
            (p for p in [path/"tag_vocab.json", path/"tag_vocab_augmorg.json"] if p.exists()),
            None
        )
        if vocab_file is None:
            return None, None, "tag_vocab.json not found"
        with open(vocab_file) as f:
            v = json.load(f)
        id2tag = {int(k): lbl for k, lbl in v["id2tag"].items()}
        return tok, model, id2tag
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None


@st.cache_resource(show_spinner=False)
def load_toxicity():
    """
    Load the fine-tuned AraBERT toxicity classifier.
    Expects: models/tox_model/  with:
      - arabert_expanded.pt  OR  arabert_contrast.pt
        (torch checkpoint saved with torch.save({'model_state_dict':...}))
      - Uses aubmindlab/bert-base-arabertv02 as the base (downloaded automatically)
    """
    path = MODELS_DIR / "tox_model"
    if not path.exists():
        return None, None

    # Find the checkpoint file (.pt)
    ckpt_file = None
    for candidate in ["arabert_expanded.pt", "arabert_contrast.pt", "best_model.pt"]:
        if (path / candidate).exists():
            ckpt_file = path / candidate
            break
    if ckpt_file is None:
        # fallback: any .pt file
        pts = list(path.glob("*.pt"))
        if pts:
            ckpt_file = pts[0]

    if ckpt_file is None:
        return None, "No .pt checkpoint found in models/tox_model/"

    try:
        NUM_CLASSES  = 7
        BASE_MODEL   = "aubmindlab/bert-base-arabertv02"

        tok   = AutoTokenizer.from_pretrained(BASE_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(
            BASE_MODEL, num_labels=NUM_CLASSES,
            ignore_mismatched_sizes=True,
            attn_implementation="eager",
        )
        ckpt = torch.load(str(ckpt_file), map_location="cpu", weights_only=False)
        model.load_state_dict(ckpt["model_state_dict"])
        model.eval()
        return tok, model
    except Exception as e:
        return None, str(e)


# ─────────────────────────────────────────────────────────────
# ARABIC PREPROCESSING  (mirrors notebook Cell 2)
# ─────────────────────────────────────────────────────────────
def clean_arabic(text):
    if not text:
        return ""
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ؤ', 'و', text)
    text = re.sub(r'ئ', 'ي', text)
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()


# ─────────────────────────────────────────────────────────────
# HYBRID PII DETECTOR  (matches HybridPIIDetector in notebook)
# ─────────────────────────────────────────────────────────────
def _token_char_ranges(tokens):
    """Map token index → (char_start, char_end) in space-joined text."""
    ranges, pos = {}, 0
    for i, tok in enumerate(tokens):
        ranges[i] = (pos, pos + len(tok))
        pos += len(tok) + 1
    return ranges

def _token_overlaps_regex(tok_s, tok_e, tok_char, regex_spans):
    if tok_s not in tok_char:
        return False
    cs = tok_char[tok_s][0]
    ce = tok_char.get(tok_e - 1, tok_char[tok_s])[1]
    return any(not (ce <= rs or cs >= re_) for rs, re_ in regex_spans)

def _predict_ner(text, tokenizer, model, id2tag):
    tokens = text.split()
    if not tokens:
        return []
    inputs = tokenizer(
        tokens, is_split_into_words=True, return_tensors="pt",
        truncation=True, padding=True, max_length=256,
    )
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
    st.write(word_pred)
    print(word_pred)
    return entities

def hybrid_detect(text, arabert_tok, arabert_mdl, arabert_id2tag,
                  xlmr_tok, xlmr_mdl, xlmr_id2tag):
    """
    Mirrors HybridPIIDetector.detect() from notebook cell 79.
    Returns list of entity dicts with keys: value, type, source,
    and either (char_start, char_end) for regex or (token_start, token_end) for models.
    """
    tokens   = text.split()
    all_ents = []

    # 1. Regex — authoritative, runs first
    regex_hits = regex_detect(text)
    regex_spans = [(e["char_start"], e["char_end"]) for e in regex_hits]
    all_ents.extend(regex_hits)

    tok_char = _token_char_ranges(tokens)

    # 2. AraBERT (PERS, ORG, ADDRESS, DATETIME)
    if arabert_mdl is not None:
        for e in _predict_ner(text, arabert_tok, arabert_mdl, arabert_id2tag):
            if e["type"] not in ARABERT_CATEGORIES:
                continue
            if _token_overlaps_regex(e["token_start"], e["token_end"], tok_char, regex_spans):
                continue
            e["source"] = "arabert"
            all_ents.append(e)

    # 3. XLM-RoBERTa (ID, CREDENTIAL)
    if xlmr_mdl is not None:
        for e in _predict_ner(text, xlmr_tok, xlmr_mdl, xlmr_id2tag):
            if e["type"] not in XLMR_CATEGORIES:
                continue
            if _token_overlaps_regex(e["token_start"], e["token_end"], tok_char, regex_spans):
                continue
            e["source"] = "xlmr"
            all_ents.append(e)

    return all_ents


# ─────────────────────────────────────────────────────────────
# TOXICITY INFERENCE  (mirrors Cell 11 get_arabert_importance)
# ─────────────────────────────────────────────────────────────
def predict_toxicity_with_attention(text, tokenizer, model):
    """
    Returns dict with prediction, confidence, all_probs,
    and word-level attention scores for highlighting.
    Mirrors get_arabert_importance() from notebook.
    """
    processed = clean_arabic(text)
    if not processed:
        return None

    enc = tokenizer(processed, max_length=128, padding="max_length",
                    truncation=True, return_tensors="pt")
    ids  = enc["input_ids"]
    mask = enc["attention_mask"]
    tids = enc.get("token_type_ids", torch.zeros_like(ids))

    with torch.no_grad():
        out   = model(ids, attention_mask=mask, token_type_ids=tids, output_attentions=True)
        probs = F.softmax(out.logits, dim=1).squeeze().cpu().numpy()

    # Average attention from [CLS] across all layers and heads
    # shape: (num_layers, batch, heads, seq, seq) → mean over layers and heads, [CLS] row
    attn   = torch.stack(out.attentions)[:, 0, :, 0, :].mean(dim=(0, 1)).cpu().numpy()
    tokens = tokenizer.convert_ids_to_tokens(ids.squeeze().cpu().numpy())
    actual_len = mask.sum().item()
    tokens, attn = tokens[:actual_len], attn[:actual_len]

    # Reconstruct words from subword tokens (AraBERT uses + for clitics, ## for wordpiece)
    words, scores, cur_w, cur_s = [], [], "", []
    for tok, sc in zip(tokens, attn):
        if tok in ["[CLS]", "[SEP]", "[PAD]", "<s>", "</s>", "<pad>"]:
            continue
        if tok.startswith("##"):
            cur_w += tok[2:]; cur_s.append(sc)
        elif tok.startswith("+"):
            cur_w += tok.replace("+", ""); cur_s.append(sc)
        else:
            if cur_w:
                words.append(cur_w); scores.append(float(max(cur_s)))
            cur_w, cur_s = tok.replace("+", ""), [sc]
    if cur_w:
        words.append(cur_w); scores.append(float(max(cur_s)))

    # Zero out stop words, normalise
    scores_arr = np.array(scores, dtype=float)
    filtered   = np.array([0.0 if w in ARABIC_STOP_WORDS else s
                            for w, s in zip(words, scores_arr)])
    is_stop    = [w in ARABIC_STOP_WORDS for w in words]
    if filtered.max() > 0:
        filtered /= filtered.max()

    pred_idx   = int(np.argmax(probs))
    pred_label = TOX_IDX2LABEL[pred_idx]
    confidence = float(probs[pred_idx])
    all_probs  = {TOX_IDX2LABEL[i]: float(p) for i, p in enumerate(probs)}

    return {
        "prediction": pred_label,
        "confidence": confidence,
        "all_probs":  all_probs,
        "words":      words,
        "scores":     filtered.tolist(),
        "is_stop":    is_stop,
    }


# ─────────────────────────────────────────────────────────────
# HTML BUILDERS
# ─────────────────────────────────────────────────────────────
def build_masked_html(text, entities):
    """Replace PII spans with coloured [TYPE] tags."""
    char_ents = sorted(
        [e for e in entities if "char_start" in e],
        key=lambda x: x["char_start"], reverse=True
    )
    out = text
    for e in char_ents:
        tag = f'<span class="tag-pii">[{e["type"]}]</span>'
        out = out[:e["char_start"]] + tag + out[e["char_end"]:]

    # Token-based entities: simple string replace
    tok_ents = [e for e in entities if "token_start" in e]
    for e in tok_ents:
        if e["value"] and e["value"] in out:
            out = out.replace(e["value"],
                              f'<span class="tag-pii">[{e["type"]}]</span>', 1)
    return out


def build_highlight_html(words, scores, is_stop, color_hex):
    """Build attention-highlighted word spans matching notebook's render_arabert()."""
    def hex_rgb(h):
        h = h.lstrip("#")
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"

    rgb = hex_rgb(color_hex)
    parts = []
    for word, score, stop in zip(words, scores, is_stop):
        if stop:
            parts.append(
                f'<span class="hl-word" style="background:rgba(200,200,200,0.1);'
                f'color:#666;" title="stop word">{word}</span>'
            )
        elif score > 0.7:
            a = 0.15 + score * 0.75
            parts.append(
                f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});'
                f'color:#fff;font-weight:600;" title="score: {score:.2f} — KEY">{word}</span>'
            )
        elif score > 0.4:
            a = 0.1 + score * 0.65
            parts.append(
                f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});'
                f'color:{color_hex};" title="score: {score:.2f}">{word}</span>'
            )
        elif score > 0.1:
            a = 0.05 + score * 0.4
            parts.append(
                f'<span class="hl-word" style="background:rgba({rgb},{a:.2f});'
                f'color:#888;" title="score: {score:.2f}">{word}</span>'
            )
        else:
            parts.append(
                f'<span class="hl-word" style="background:rgba(200,200,200,0.08);'
                f'color:#555;" title="score: {score:.2f}">{word}</span>'
            )
    return " ".join(parts)


def tox_badge(label):
    if label == "Normal":
        return '<span class="badge b-safe">SAFE</span>'
    if label == "Mental Health":
        return '<span class="badge b-crit">CRITICAL</span>'
    if label in DANGER_CATS:
        return '<span class="badge b-flag">FLAGGED</span>'
    return '<span class="badge b-warn">WARNING</span>'


# ─────────────────────────────────────────────────────────────
# PARALLEL SCAN
# ─────────────────────────────────────────────────────────────
def run_scan(text, ar_tok, ar_mdl, ar_id2tag, xl_tok, xl_mdl, xl_id2tag, tx_tok, tx_mdl):
    results = {}

    def pii_job():
        results["pii"] = hybrid_detect(text, ar_tok, ar_mdl, ar_id2tag,
                                        xl_tok, xl_mdl, xl_id2tag)
    def tox_job():
        if tx_mdl is not None:
            results["tox"] = predict_toxicity_with_attention(text, tx_tok, tx_mdl)
        else:
            results["tox"] = None

    t1 = threading.Thread(target=pii_job)
    t2 = threading.Thread(target=tox_job)
    t1.start(); t2.start()
    t1.join();  t2.join()
    return results


# ─────────────────────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────────────────────
with st.spinner("Loading models…"):
    ar_tok,  ar_mdl,  ar_id2tag  = load_arabert()
    xl_tok,  xl_mdl,  xl_id2tag  = load_xlmr()
    tx_tok,  tx_mdl              = load_toxicity()

ar_ok = ar_mdl  is not None
xl_ok = xl_mdl  is not None
tx_ok = tx_mdl  is not None


# ─────────────────────────────────────────────────────────────
# UI — HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="ps-logo">Prompt<span>Scanner</span></div>
<div class="ps-sub">Arabic Prompt Privacy &amp; Safety Analysis</div>
<div class="ps-rule"></div>
""", unsafe_allow_html=True)

# Model status bar
st.markdown(f"""
<div class="sbar">
  <div class="si"><div class="dot {'dot-on' if ar_ok else 'dot-off'}"></div>
      <span class="si-label">PII Model — AraBERT/CamelBERT (PERS, ORG, ADDRESS, DATE)</span></div>
  <div class="si"><div class="dot {'dot-on' if xl_ok else 'dot-off'}"></div>
      <span class="si-label">XLM-RoBERTa (ID, CREDENTIAL)</span></div>
  <div class="si"><div class="dot dot-on"></div>
      <span class="si-label">Regex Engine (PHONE, EMAIL, IP, MAC, URL, FINANCIAL)</span></div>
  <div class="si"><div class="dot {'dot-on' if tx_ok else 'dot-off'}"></div>
      <span class="si-label">Toxicity Model — AraBERT v2</span></div>
</div>
""", unsafe_allow_html=True)

# Example prompts
EXAMPLES = [
    ("PII — name + org",      "اسمي أحمد المقبالي وأعمل في بنك مسقط"),
    ("PII — phone + email",   "رقمي +968 91234567 وبريدي ahmed@squ.edu.om"),
    ("PII — ID + credential", "رقم هويتي 12345678 وكلمة المرور MyPass123!"),
    ("Toxicity — dangerous",  "كيف أصنع قنبلة لتدمير مبنى"),
    ("Toxicity — mental",     "أريد أن أنهي حياتي لم أعد أتحمل"),
    ("Toxicity — offensive",  "يا حمار أنت غبي جداً"),
    ("Toxicity — normal",     "اكتب لي قصيدة عن الربيع"),
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
    scan_clicked = st.button("⟶  SCAN", use_container_width=True)
with c2:
    if st.button("✕  Clear", use_container_width=True):
        st.session_state.prompt = ""
        st.rerun()

# ─────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────
if scan_clicked and prompt.strip():
    with st.spinner("Scanning…"):
        t0 = time.time()
        res = run_scan(prompt.strip(),
                       ar_tok, ar_mdl, ar_id2tag,
                       xl_tok, xl_mdl, xl_id2tag,
                       tx_tok, tx_mdl)
        elapsed = round(time.time() - t0, 2)

    pii_ents = res.get("pii", [])
    tox_res  = res.get("tox")

    st.markdown(
        f"<div style='color:var(--muted);font-size:.76rem;font-family:Space Mono,monospace;"
        f"margin-bottom:1rem;'>Scanned in {elapsed}s</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="large")

    # ── LEFT: PII ──────────────────────────────────────────
    with left:
        n_pii = len(pii_ents)
        badge = (f'<span class="badge b-warn">{n_pii} found</span>'
                 if n_pii else '<span class="badge b-safe">CLEAN</span>')
        st.markdown(
            f'<div class="card card-pii">'
            f'<div class="card-head">◆ PII Detection &nbsp; {badge}</div>',
            unsafe_allow_html=True,
        )

        if pii_ents:
            masked = build_masked_html(prompt.strip(), pii_ents)
            st.markdown(f'<div class="richtext">{masked}</div>', unsafe_allow_html=True)

            # Entity pills grouped by type
            st.markdown('<div class="epills">', unsafe_allow_html=True)
            for e in pii_ents:
                src_label = {"regex": "RGX", "arabert": "NER", "xlmr": "XLM"}.get(
                    e.get("source", ""), "")
                st.markdown(
                    f'<div class="epill">'
                    f'<span class="epill-lbl">{e["type"]}</span>'
                    f'<span class="epill-val">{e["value"]}</span>'
                    f'<span style="color:var(--muted);font-size:.65rem;margin-left:.2rem;">{src_label}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            # Source breakdown
            src_counts = Counter(e.get("source", "?") for e in pii_ents)
            src_labels = {"regex": "Regex", "arabert": "AraBERT", "xlmr": "XLM-RoBERTa"}
            src_html = " &nbsp;·&nbsp; ".join(
                f'<span style="color:var(--dim);font-size:.76rem;">'
                f'{src_labels.get(k, k)}: '
                f'<span style="color:var(--text);">{v}</span></span>'
                for k, v in src_counts.items()
            )
            st.markdown(f'<div style="margin-top:.7rem;">{src_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="nopii">✓ No personally identifiable information detected.</div>',
                        unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: Toxicity ────────────────────────────────────
    with right:
        st.markdown(
            '<div class="card card-tox">'
            '<div class="card-head">◆ Toxicity Analysis</div>',
            unsafe_allow_html=True,
        )

        if tox_res:
            label  = tox_res["prediction"]
            conf   = tox_res["confidence"]
            probs  = tox_res["all_probs"]
            color  = TOX_COLOR.get(label, "#00c9a7")

            st.markdown(f"""
<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
  <div>
    <div class="tox-name" style="color:{color};">{label}</div>
    <div class="tox-conf">Confidence: {conf*100:.1f}%</div>
  </div>
  <div style="margin-top:.25rem;">{tox_badge(label)}</div>
</div>
<div class="pbar-bg" style="margin-top:.7rem;">
  <div class="pbar-fill" style="width:{conf*100:.1f}%;background:{color};"></div>
</div>
""", unsafe_allow_html=True)

            # Probability breakdown
            rows = ""
            for lbl, p in sorted(probs.items(), key=lambda x: -x[1]):
                w   = max(2, int(p * 120))
                c2  = TOX_COLOR.get(lbl, "#5a6075")
                rows += (f'<tr><td>{lbl}</td>'
                         f'<td><span class="pmini" style="width:{w}px;background:{c2};"></span>'
                         f'{p*100:.1f}%</td></tr>')
            st.markdown(f'<table class="ptable">{rows}</table>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="color:var(--muted);font-size:.86rem;padding:.5rem 0;">'
                'Toxicity model not loaded.<br>'
                'Place checkpoint in <code>models/tox_model/</code>.</div>',
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── ATTENTION HIGHLIGHT (full width) ──────────────────
    if tox_res and tox_res.get("words"):
        label  = tox_res["prediction"]
        color  = TOX_COLOR.get(label, "#00c9a7")
        hl_html = build_highlight_html(
            tox_res["words"], tox_res["scores"], tox_res["is_stop"], color
        )

        # Top-3 key words
        key_words = sorted(
            [(w, s) for w, s, stop in zip(tox_res["words"], tox_res["scores"], tox_res["is_stop"])
             if not stop and s > 0.4],
            key=lambda x: -x[1]
        )[:3]
        key_str = " · ".join(
            f'<span style="color:{color};font-weight:600;">{w}</span> '
            f'<span style="color:var(--muted);font-size:.76rem;">({s:.2f})</span>'
            for w, s in key_words
        ) if key_words else "—"

        st.markdown(f"""
<div class="card card-hl section-gap">
  <div class="card-head">◆ Keyword Attention — words driving the classification</div>
  <div class="richtext" style="margin-bottom:.8rem;">{hl_html}</div>
  <div style="font-size:.8rem;color:var(--dim);margin-bottom:.5rem;">
    Top contributing words: {key_str}
  </div>
  <div class="legend">
    <div class="leg-item">
      <div class="leg-sq" style="background:{color};opacity:.9;"></div>
      <span>High attention (&gt;0.7)</span>
    </div>
    <div class="leg-item">
      <div class="leg-sq" style="background:{color};opacity:.5;"></div>
      <span>Medium (0.4–0.7)</span>
    </div>
    <div class="leg-item">
      <div class="leg-sq" style="background:{color};opacity:.2;"></div>
      <span>Low (0.1–0.4)</span>
    </div>
    <div class="leg-item">
      <div class="leg-sq" style="background:rgba(200,200,200,0.2);"></div>
      <span>Stop word</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

elif scan_clicked and not prompt.strip():
    st.warning("Please enter a prompt before scanning.")

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:4rem;padding-top:1rem;border-top:1px solid var(--border);
            display:flex;justify-content:space-between;align-items:center;
            font-size:.74rem;color:var(--muted);">
  <span style="font-family:Space Mono,monospace;">PromptScanner</span>
  <span>Arabic PII Detection · Toxicity Classification · Final Year Project</span>
</div>
""", unsafe_allow_html=True)
