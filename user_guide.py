import streamlit as st
from pathlib import Path
import base64

# ──────────────────────────────────────────────────────────────────────────────
# SHARED STYLES
# ──────────────────────────────────────────────────────────────────────────────

CSS = """
<style>
/* ── Remove Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; margin: auto;}
section[data-testid="stMain"] > div { padding-top: 0 !important; }

/* ── Colour palette ── */
:root {
    --navy:   #1a2340;
    --amber:  #e8941a;
    --teal:   #0a8a72;
    --red:    #c0392b;
    --purple: #6c3fc5;
    --blue:   #1a5fa8;
    --muted:  #6b6560;
    --border: #e0d8cc;
    --bg:     #EAE4D9;
    --surf:   #ffffff;
    --surf2:  #f9f6f0;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
}
/* ── Top bar (language switch area) ── */
.top-bar {
    background: var(--bg);  /* beige */
    justify-content: flex-end;

}


/* ── Section headers ── */
.sec-head {
  display: flex; align-items: center; gap: 14px;
  margin: 52px 0 28px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--navy);
}

.sec-num {
  background: var(--navy); color: #fff;
  font-weight: 800; font-size: 1rem;
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.sec-title { font-size: 1.35rem; font-weight: 700; }
.sec-part {
  font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--amber); font-weight: 700; margin-bottom: 2px;
}

.sub-title {
    font-size: 1.1rem; font-weight: 600; color: var(--navy); margin: 15px 0 14px;}
.sub-title[dir="rtl"] {
  text-align: right;
}
.sub-title[dir="ltr"] {
  text-align: left;
}

/* ── Step cards ── */
.step-row   { display: flex; gap: 0; margin-bottom: 0; }
.step-left  { display: flex; flex-direction: column; align-items: center; width: 46px; flex-shrink: 0; }
.step-num   {
    width: 32px; height: 32px; border-radius: 50%;
    background: var(--navy); color: #fff;
    font-weight: 800; font-size: 0.85rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; z-index: 1;
}
.step-num-ok  { background: var(--teal) !important; }
.step-num-warn{ background: var(--red) !important; }
.step-line  { width: 2px; flex: 1; min-height: 16px; background: var(--border); margin-top: 4px; }
.step-body  {
    background: var(--surf); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 18px;
    margin-bottom: 12px; flex: 1;
}
.step-label { font-weight: 700; font-size: 0.94rem; margin-bottom: 4px; color: var(--navy); }
.step-desc  { color: var(--muted); font-size: 0.88rem; line-height: 1.65; }
.step-row[dir="rtl"] {
  flex-direction: row-reverse;   /* flip children order */
  text-align: right;             /* align text inside */
}
.step-row[dir="ltr"] {
  flex-direction: row;
  text-align: left;
}

/* ── Callouts ── */
.callout {
    border-radius: 8px; padding: 11px 15px; margin: 12px 0;
    font-size: 0.87rem; display: flex; gap: 10px; align-items: flex-start;
}
.callout-tip  { background: #e8f4ff; border-left: 4px solid var(--blue); }
.callout-warn { background: #fff8e8; border-left: 4px solid var(--amber); }
.callout p    { margin: 0; }

/* ── Annotation labels ── */
.ann {
    display: inline-flex; align-items: center; justify-content: center;
    width: 18px; height: 18px; border-radius: 50%;
    background: var(--amber); color: var(--navy);
    font-weight: 800; font-size: 0.65rem;
    flex-shrink: 0; vertical-align: middle; margin-right: 4px;
}
.ann-row { display: flex; align-items: flex-start; gap: 9px; padding: 7px 0; border-bottom: 1px solid var(--border); font-size: 0.86rem; }
.ann-row:last-child { border-bottom: none; }

/* ── Component cards ── */
.comp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 11px; margin: 16px 0; }
.comp-card { border-radius: 9px; padding: 13px 15px; border: 1px solid var(--border); background: var(--surf2); }
.comp-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.comp-dot  { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.comp-name { font-weight: 700; font-size: 0.85rem; }
.comp-desc { font-size: 0.8rem; color: var(--muted); margin-bottom: 7px; }
.comp-cats { display: flex; flex-wrap: wrap; gap: 4px; }
.cat-pill  { font-size: 0.69rem; font-weight: 700; padding: 2px 7px; border-radius: 10px; letter-spacing: 0.03em; }

/* ── Flow diagram ── */
.flow      { display: flex; justify-content: center; align-items: center; gap: 0; margin: 14px auto; overflow-x: auto; flex-wrap: wrap; max-width: 100%;}
.flow-node { background: var(--navy); color: #fff; border-radius: 7px; padding: 8px 13px; font-size: 0.79rem; font-weight: 600; text-align: center; min-width: 95px; flex-shrink: 0; line-height: 1.4; margin: 3px 0; }
.flow-amber{ background: var(--amber) !important; color: var(--navy) !important; }
.flow-teal { background: var(--teal) !important; }
.flow-arr  { font-size: 1rem; color: var(--muted); padding: 0 4px; flex-shrink: 0; }

/* ── Badges ── */
.badge      { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.04em; vertical-align: middle; }
.b-safe     { background: #d4f5ee; color: #0a6b56; }
.b-warn     { background: #fef3dc; color: #7a4e00; }
.b-flag     { background: #fde8e8; color: #8b1a1a; }
.b-crit     { background: #ede8fc; color: #3d1b8a; }
.b-clean    { background: #d4f5ee; color: #0a6b56; }
.b-pii      { background: #fff3dc; color: #7a4e00; }

/* ── PII tag ── */
.pii-tag { display: inline-block; background: #fff3dc; color: #7a4e00; border: 1px solid #e8c068; border-radius: 4px; padding: 0 6px; font-size: 0.69rem; font-weight: 700; margin: 0 2px; }

/* ── Tables ── */
.guide-table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.86rem; }
.guide-table th { background: #2b365c; color: #fff; padding: 7px 12px; text-align: left; font-size: 0.76rem; letter-spacing: 0.06em; text-transform: uppercase; }
.guide-table td { padding: 8px 12px; border-bottom: 1px solid var(--border); }
.guide-table tr:nth-child(even) td { background: var(--surf2); }
.guide-table tr:nth-child(odd) td { background: var(--bg); }

/* ── Keyword attention highlight ── */
.hl-high  { display: inline-block; border-radius: 4px; padding: 2px 7px; margin: 2px; font-size: 0.86rem; background: rgba(92, 190, 251);  color: #fff; font-weight: 700; }
.hl-mid   { display: inline-block; border-radius: 4px; padding: 2px 7px; margin: 2px; font-size: 0.86rem; background: rgba(118, 199, 247);  color: #fff; font-weight: 600; }
.hl-low   { display: inline-block; border-radius: 4px; padding: 2px 7px; margin: 2px; font-size: 0.86rem; background: rgba(158, 210, 238);  color: #7dbfe6; }
.hl-stop  { display: inline-block; border-radius: 4px; padding: 2px 7px; margin: 2px; font-size: 0.86rem; background: rgba(160,160,160,0.1); color: #999; }
.hl-ph    { display: inline-block; border-radius: 4px; padding: 2px 7px; margin: 2px; font-size: 0.86rem; background: rgba(252, 148, 90); color: #fff; font-weight: 700; }
.hl-pm    { display: inline-block; border-radius: 4px; padding: 2px 7px; margin: 2px; font-size: 0.86rem; background: rgba(249, 187, 149); color: #e28743; font-weight: 600; }
.hl-pl    { display: inline-block; border-radius: 4px; padding: 2px 7px; margin: 2px; font-size: 0.86rem; background: rgba(247, 191, 155); color: #e28743; }

/* ── Rewrite comparison ── */
.rw-grid  { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 10px 0; }
.rw-col-title { font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; font-weight: 600; }
.rw-box   { background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 10px; font-size: 0.84rem; line-height: 1.7; direction: rtl; text-align: right; min-height: 65px; }

/* ── Extension popup mockup ── */
.ext-popup { background: #f2ede2; border: 1px solid #ddd; border-radius: 12px; overflow: hidden; width: 300px; box-shadow: 0 6px 24px rgba(0,0,0,0.1); }
.ext-header { background: #f2ede2; padding: 12px 14px 9px; border-bottom: 1px solid #ddd; display: flex; align-items: center; justify-content: space-between; }
.ext-logo   { font-weight: 800; font-size: 0.9rem; color: #1a2340; }
.ext-logo span { color: #e8941a; }
.ext-sub    { font-size: 0.62rem; color: #888; }
.ext-gear   { width: 26px; height: 26px; background: #ebe5d8; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; color: #555; flex-shrink: 0; }
.ext-sec    { padding: 9px 13px 3px; }
.ext-sec-t  { font-size: 0.62rem; letter-spacing: 0.12em; text-transform: uppercase; color: #888; margin-bottom: 5px; font-weight: 600; }
.ext-sec-t::before { content: "◆ "; font-size: 0.45rem; color: #e8941a; }
.ext-tbox   { background: #fff; border: 1px solid #ddd; border-radius: 7px; padding: 9px 11px; font-size: 0.8rem; line-height: 1.65; direction: rtl; text-align: right; color: #333; min-height: 48px; }
.ext-tox    { background: #fff; border-radius: 8px; padding: 10px 12px; border: 1px solid #ddd; }
.ext-tox-lbl{ font-size: 0.95rem; font-weight: 800; }
.ext-tox-cf { font-size: 0.7rem; color: #888; margin: 2px 0 5px; }
.ext-bar    { background: #ede8e0; border-radius: 3px; height: 5px; }
.ext-bar-f  { height: 100%; border-radius: 3px; }
.ext-badge  { float: right; display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.65rem; font-weight: 700; }
.ext-words  { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 4px; padding: 5px 2px; direction: rtl; }
.ext-div    { height: 1px; background: #ddd; margin: 5px 13px; }
.ext-btn    { border-radius: 7px; padding: 9px; text-align: center; font-weight: 700; font-size: 0.79rem; cursor: pointer; margin: 2px 0; }
.ext-set-row{ display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #ede8e0; }
.ext-set-row:last-child { border-bottom: none; }
.ext-set-lbl{ font-weight: 700; font-size: 0.82rem; color: #1a2340; }
.ext-set-sub{ font-size: 0.7rem; color: #888; margin-top: 1px; }
.ext-tog    { width: 38px; height: 21px; border-radius: 10px; position: relative; flex-shrink: 0; }
.ext-tog-on { background: #e8941a; }
.ext-tog-off{ background: #ccc; }
.ext-tog-k  { width: 15px; height: 15px; border-radius: 50%; background: #fff; position: absolute; top: 3px; }
.ext-tog-kon{ left: 20px; }
.ext-tog-kof{ left: 3px; }
.ext-lang   { display: flex; gap: 4px; }
.ext-lan-a  { padding: 3px 9px; border-radius: 5px; font-size: 0.72rem; font-weight: 600; background: #e8941a; color: #fff; }
.ext-lan-i  { padding: 3px 9px; border-radius: 5px; font-size: 0.72rem; font-weight: 600; background: #ebe5d8; color: #555; }
.ext-grp-t  { font-size: 0.62rem; letter-spacing: 0.13em; text-transform: uppercase; color: #888; font-weight: 700; padding: 9px 0 3px; }
.ext-grp-t::before { content: "◆ "; font-size: 0.42rem; color: #e8941a; }
.ext-save   { background: #e8941a; color: #fff; border-radius: 9px; padding: 11px; text-align: center; font-weight: 700; font-size: 0.85rem; margin-top: 9px; }
.tag-pii { display: inline-block; background: rgba(232,82,10,0.10); color: #E8520A; border: 1px solid rgba(232,82,10,0.3); border-radius: 5px; padding: 1px 6px; font-family: 'JetBrains Mono', monospace !important; font-size: .7rem; margin: 0 2px; vertical-align: middle; }


/* ── Doc footer ── */
.doc-footer { background: var(--navy); color: rgba(255,255,255,0.45); text-align: center; padding: 18px; font-size: 0.75rem; margin-top: 40px; }
.doc-footer span { color: var(--amber); }

/* ── RTL support ── */
.rtl { direction: rtl; text-align: right; }

/* ── EN/AR language toggle button ── */
button[data-testid="baseButton-secondary"][kind="secondary"]:has(+ *),
div[data-testid="stButton"]:has(button[key="guide_lang_toggle"]) button {
    background: var(--navy) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    padding: 6px 12px !important;
}
/* Broader selector to catch the lang toggle reliably 
div[data-testid="stVerticalBlock"] > div:first-child div[data-testid="stButton"] button {
    background: var(--navy) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: 8px !important;
}
/*
/* ── Guide header (navy cover with badge buttons) ── */
.guide-header {
    background: var(--navy);
    color: #fff;
    padding: 44px 48px 36px;
    margin-bottom: 0;
    width: 100vw;
    margin-left: calc(-50vw + 50%);
    margin-right: calc(-50vw + 50%);
}
.gh-logo-row {
    display: flex; align-items: center; gap: 14px; margin-bottom: 20px;
}
.gh-logo {
    width: 52px; height: 52px; border-radius: 11px;
    object-fit: contain; flex-shrink: 0;
}
.gh-name {
    font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; line-height: 1.1;
}
.gh-name span { color: var(--amber); }
.gh-sub {
    font-size: 0.75rem; letter-spacing: 0.15em; text-transform: uppercase;
    color: rgba(255,255,255,0.4); margin-top: 2px;
}
.gh-title {
    font-size: 1.9rem; font-weight: 300; margin-bottom: 10px;
}
.gh-desc {
    color: rgba(255,255,255,0.62); font-size: 0.91rem;
    max-width: 560px; line-height: 1.65; margin: 0;
}
.gh-bottom-rule {
    height: 3px;
    background: linear-gradient(90deg, var(--amber), transparent 60%);
    margin-top: 0;
}

/* ── Tab buttons inside the header ── */
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
    border-radius: 24px !important;
    font-weight: 700 !important;
    font-size: 0.83rem !important;
    letter-spacing: 0.04em !important;
    padding: 8px 20px !important;
    border: none !important;
    transition: all 0.2s !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button[kind="primary"] {
    background: var(--amber) !important;
    color: var(--navy) !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(255,255,255,0.15) !important;
    color: rgba(255,255,255,0.75) !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.25) !important;
    color: #fff !important;
}
div[data-testid="stHorizontalBlock"] {
    background: var(--navy) !important;
    padding: 20px 48px 20px !important;
    width: 100vw !important;
    max-width: 100vw !important;   /* prevent Streamlit container clipping */
    margin-left: calc(-50vw + 50%) !important;
    margin-right: calc(-50vw + 50%) !important;
    border: none !important;
}
</style>
"""


# ──────────────────────────────────────────────────────────────────────────────
# TRANSLATION STRINGS
# ──────────────────────────────────────────────────────────────────────────────

T = {
    "en": {
        # tabs
        "tab_web":  "Part 1 - Website",
        "tab_ext":  "Part 2 - Browser Extension",
        # shared section labels
        "sec_overview":     "Getting started",
        "sec_interface":    "Interface overview",
        "sec_steps":        "Step-by-step",
        "sec_pii_ref":      "PII reference",
        "sec_quickref":     "Quick reference",
        "sec_install":      "Installation",
        "sec_states":       "Popup states",
        "sec_settings":     "Settings",
        # intro box
        "intro_web": "PromptScanner analyses your Arabic prompts <strong>before</strong> you send them to an AI chatbot. It simultaneously detects private personal information and checks for harmful content; protecting your privacy and helping you communicate more safely.",
        "intro_ext": "The PromptScanner extension adds a safety layer directly inside AI chatbot websites like <strong>ChatGPT</strong> and <strong>Gemini</strong>. When you press Send or Enter, it intercepts your prompt, scans it, and shows you the results in a popup <strong>before</strong> anything reaches the AI. You then choose to send the original, send a rewritten version, or cancel.",
        # flow labels
        "flow_type":    "Type a prompt",
        "flow_scan":    "Press Scan",
        "flow_run":     "3 models run in parallel",
        "flow_result":  "Results appear",
        "flow_type2":   "Type in AI chatbot eg.ChatGPT / Gemini",
        "flow_send":    "Press Send / Enter",
        "flow_catch":   "Extension processes the prompt",
        "flow_decide":  "You decide",
        # component names/descs
        "comp_arabert_name": "AraBERT NER",
        "comp_arabert_desc": "Detects names, organisations, addresses and dates using a fine-tuned Arabic language model.",
        "comp_xlmr_name":    "XLM-RoBERTa",
        "comp_xlmr_desc":    "Detects IDs and credentials, including Latin values inside Arabic sentences.",
        "comp_regex_name":   "Regex Engine",
        "comp_regex_desc":   "Pattern-based detection for phone, email, IP, MAC, URL and financial info.",
        "comp_tox_name":     "AraBERT v2 - Toxicity",
        "comp_tox_desc":     "Classifies prompts into 7 safety categories with keyword attention highlighting.",
        # interface annotations
        "ann_a": "<strong>Model status panel (left sidebar)</strong> - shows which AI components are loaded and ready (green dot = active). Describes what each model detects.",
        "ann_b": "<strong>Example buttons</strong> - click any example to automatically load a pre-written Arabic prompt into the input box. Useful for trying the tool without typing.",
        "ann_c": "<strong>Prompt input box</strong> - type or paste Arabic prompt here. The box is right-to-left aligned.",
        "ann_d": "<strong>Scan and clear buttons</strong> - starts the scan for PII and toxicity simultaneously, clears the input and resets the results panel.",
        "ann_e": "<strong>Top-right controls</strong> - toggle dark/light mode (🌙) and interface language (EN / AR).",
        # steps - website
        "step1_lbl":  "Enter your Arabic prompt",
        "step1_desc": "Click the text box and type or paste Arabic text. You can also click any example button in the left sidebar to auto-fill a pre-written test prompt.",
        "step2_lbl":  "Press Scan",
        "step2_desc": "All four components analyse simultaneously. Results appear in 1-2 seconds. Press Clear to clear and start over.",
        "step3_lbl":  "Read the PII result (left card)",
        "step3_desc": "Shows CLEAN (no PII found) or N found. When PII is detected the masked text appears with [TYPE] placeholders, and coloured pills list every detected entity with its value, type, and which model found it (RGX / NER / XLM).",
        "step4_lbl":  "Read the toxicity result (right card)",
        "step4_desc": "Shows the predicted category, confidence percentage, and a full breakdown of all 7 categories. A badge indicates severity.",
        "step5_lbl":  "Read the keyword attention map",
        "step5_desc": "Each word is colour-coded by how much it influenced the toxicity decision. Darker = more influential. Common connecting words appear in grey.",
        "step6_lbl":  "Use إعادة الصياغة (Rewrite)",
        "step6_desc": "When toxic content is detected the rewrite panel appears. It shows a safe alternative. Press the button to regenerate, or copy the rewritten text to use instead of the original.",
        # toxicity badge table
        "badge_lbl":  "Badge",
        "meaning_lbl":"Meaning",
        "cats_lbl":   "Categories",
        "safe_meaning":  "No toxic content",
        "warn_meaning":  "Mildly harmful",
        "flag_meaning":  "Clearly harmful",
        "crit_meaning":  "Requires care",
        # tip callouts
        "tip_examples":  "You can click any <strong>example button</strong> in the left sidebar to load a pre-written test prompt. Useful for seeing results without typing.",
        "tip_masked":    "Always use the <strong>masked text</strong> (shown in the PII card) as your prompt instead of the original - the chatbot still understands your request without receiving your private data.",
        "tip_save":      "Always press <strong>Save Settings</strong> after making changes in the extension. Changes are not applied until saved.",
        "tip_autoscan":  "If <strong>Auto Scan</strong> is enabled and content is safe, the extension can be configured to send automatically without showing a popup.",
        # HL legend
        "hl_high": "High (>0.7)",
        "hl_mid":  "Medium (0.4-0.7)",
        "hl_low":  "Low (0.1-0.4)",
        "hl_stop": "Stop word",
        # rewrite labels
        "rw_rewritten": "Rewritten text",
        "rw_original":  "Original text",
        # PII table headers + types
        "tag_col": "Tag", "entity_col": "Entity type", "example_col": "Example", "detected_col": "Detected by",
        "pers_desc": "Person name", "org_desc": "Organisation", "addr_desc": "Location / address",
        "dt_desc": "Date / time", "id_desc": "National ID / passport", "cred_desc": "Password / PIN / OTP",
        "phone_desc": "Phone number", "email_desc": "Email address", "ip_desc": "IP address",
        "mac_desc": "MAC address", "url_desc": "Web URL", "fin_desc": "Card number / IBAN",
        # Quick ref
        "action_col": "Action", "how_col": "How",
        "qr1":  ("Scan a prompt",              "Type or paste text → press Scan"),
        "qr2":  ("Clear the input",            "Press Clear"),
        "qr3":  ("Try a pre-written example",  "Click any button in the left sidebar"),
        "qr4":  ("Switch dark / light mode",   "Click 🌙 (top right)"),
        "qr5":  ("Switch interface language",  "Click EN / AR (top right)"),
        "qr6":  ("See which model found a PII","Check the small label on each entity pill (RGX / NER / XLM)"),
        "qr7":  ("Get a safe rewrite",         "Press إعادة الصياغة in the rewrite panel"),
        "qr8":  ("Understand toxic keywords",  "Read the keyword attention map (bottom panel)"),
        # Install steps
        "inst1_lbl":  "Open Chrome Web Store",
        "inst1_desc": "Go to https://chromewebstore.google.com/, and search for PromptScanner or use the direct link on our website.",
        "inst2_lbl":  "Install the extension",
        "inst2_desc": "Click the \"Add to Chrome\" button and confirm the installation.",
        "inst3_lbl":  "Access the extension",
        "inst3_desc": "Click the puzzle-piece icon, find PromptScanner, and click the pin to keep it visible.",
        "inst4_lbl":  "Start using PromptScanner",
        "inst4_desc": "Enter AI chatbot like ChatGPT or Gemini, type a prompt, and press Send to see PromptScanner in action!",
        # Popup state labels
        "state_a": "State A - Safe content (no issues found)",
        "state_b": "State B - Issues detected",
        "state_c": "State C - Rewrite generated",
        "state_a_desc": "When your prompt is clean the popup shows a single button.",
        "state_b_desc": "When PII or toxicity is detected you see the analysis and two options.",
        "state_c_desc": "After pressing Rewrite, the safe alternative appears alongside two send options.",
        # Popup annotations
        "pa1a": "<strong>Masked text</strong> confirms no PII was found.",
        "pa1b": "<strong>Green Normal label</strong> - content is safe, high confidence.",
        "pa1c": "<strong>→ إرسال الأصلي</strong> - sends the prompt as-is. One click and done.",
        "pa2a": "<strong>Masked text</strong> - PII values appear as [TYPE] placeholders if detected.",
        "pa2b": "<strong>Critical badge + purple label</strong> - Mental Health classification detected.",
        "pa2c": "<strong>Key attention words</strong> - colour-coded words that drove the classification.",
        "pa2d": "<strong>إعادة الصياغة</strong> - generates a safe rewrite (moves to State C).",
        "pa2e": "<strong>→ إرسال الأصلي</strong> - always available; the choice is always yours.",
        "pa3a": "<strong>النص المُعاد كتابته panel</strong> - the safe alternative with a green border.",
        "pa3b": "<strong>→ إرسال المُعاد كتابته</strong> - sends the rewritten safe version.",
        "pa3c": "<strong>→ إرسال الأصلي</strong> - sends the original despite the warning.",
        "pa3d": "<strong>✕ إلغاء</strong> - closes the popup so you can edit manually without sending.",
        # Settings
        "set_intro":       "Click the ⚙ icon in the popup header to open settings.",
        "set_dark_lbl":    "Dark Mode",
        "set_dark_desc":   "Enable dark theme",
        "set_lang_lbl":    "Language",
        "set_lang_desc":   "Extension UI language",
        "set_popup_lbl":   "Show popup for safe content",
        "set_popup_desc":  "If safe, show popup. Otherwise send automatically",
        "set_auto_lbl":    "Auto Scan",
        "set_auto_desc":   "Scan when Send or Enter is pressed",
        "set_dark_what":   "Switches the popup to a dark colour scheme.",
        "set_lang_what":   "Choose English or Arabic for all popup labels and buttons.",
        "set_popup_what":  "ON: popup appears even for safe prompts. OFF: safe prompts send automatically with no interruption.",
        "set_auto_what":   "ON: scans automatically when Send/Enter is pressed. OFF: no automatic scanning.",
        # Ext quick ref
        "eqr1": ("Trigger a scan",             "Press Send or Enter in ChatGPT / Gemini (Auto Scan must be ON)"),
        "eqr2": ("Send original prompt",       "Press → إرسال الأصلي"),
        "eqr3": ("Send rewritten version",     "Press إعادة الصياغة then → إرسال المُعاد كتابته"),
        "eqr4": ("Cancel without sending",     "Press ✕ إلغاء"),
        "eqr5": ("Open settings",              "Click ⚙ in the popup header"),
        "eqr6": ("Skip popup for safe prompts","Turn OFF Show popup for safe content"),
        "eqr7": ("Disable auto-scanning",      "Turn OFF Auto Scan"),
        # footer
        "footer_web": "<span>PromptScanner</span> - User Guide · Part 1: Website",
        "footer_ext": "<span>PromptScanner</span> - User Guide · Part 2: Browser Extension · ChatGPT & Gemini",
    },
    "ar": {
        # tabs
        "tab_web":  "الجزء الأول - الموقع الإلكتروني",
        "tab_ext":  "الجزء الثاني - إضافة المتصفح",
        # shared section labels
        "sec_overview":     "البداية",
        "sec_interface":    "نظرة عامة على الواجهة",
        "sec_steps":        "خطوة بخطوة",
        "sec_pii_ref":      "أنواع المعلومات الشخصية",
        "sec_quickref":     "مرجع سريع",
        "sec_install":      "التثبيت",
        "sec_states":       "حالات النافذة المنبثقة",
        "sec_settings":     "الإعدادات",
        # intro box
        "intro_web": "يحلل PromptScanner مطالباتك العربية <strong>قبل</strong> إرسالها إلى روبوت المحادثة. يكتشف المعلومات الشخصية الحساسة ويفحص المحتوى الضار في الوقت؛ لحماية خصوصيتك وتعزيز سلامة تفاعلاتك.",
        "intro_ext": "تضيف إضافة PromptScanner طبقةً أمنية مباشرةً في مواقع روبوتات الدردشة مثل <strong>ChatGPT</strong> و<strong>Gemini</strong>. عند الضغط على إرسال أو Enter، تعترض الإضافة مطالبتك وتفحصها وتعرض النتائج في نافذة منبثقة قبل وصول أي شيء إلى الذكاء الاصطناعي. ثم يختار المستخدم إرسال النص الأصلي أو النص المُعاد صياغته أو الإلغاء.",
        # flow
        "flow_type":    "اكتب مطالبتك",
        "flow_scan":    "اضغط فحص",
        "flow_run":     "3 نماذج تعمل في الوقت ذاته",
        "flow_result":  "تظهر النتائج",
        "flow_type2":   "اكتب في ChatGPT / Gemini",
        "flow_send":    "اضغط إرسال / Enter",
        "flow_catch":   "الإضافة تعترض المطالبة",
        "flow_decide":  "أنت تقرر",
        # components
        "comp_arabert_name": "AraBERT NER",
        "comp_arabert_desc": "يكتشف الأسماء والمؤسسات والعناوين والتواريخ باستخدام نموذج لغوي عربي.",
        "comp_xlmr_name":    "XLM-RoBERTa",
        "comp_xlmr_desc":    "يكتشف أرقام الهوية وبيانات الدخول، بما فيها القيم اللاتينية داخل الجمل العربية.",
        "comp_regex_name":   "محرك التعبيرات النمطية",
        "comp_regex_desc":   "كشف مبني على أنماط ثابتة للهاتف والبريد والـ IP والـ MAC والروابط والمعلومات المالية.",
        "comp_tox_name":     "AraBERT v2 - السمية",
        "comp_tox_desc":     "يصنّف المطالبات إلى 7 فئات أمان مع إبراز الكلمات المؤثرة.",
        # annotations
        "ann_a": "<strong>لوحة النماذج (الشريط الجانبي الأيسر)</strong> - يُظهر هذا القسم مكونات الذكاء الاصطناعي المُحمّلة والجاهزة للاستخدام (النقطة الخضراء = نشطة). ويصف ما يكتشفه كل نموذج.",
        "ann_b": "<strong>أزرار الأمثلة</strong> - انقر على أي مثال لتحميل نص عربي مكتوب مسبقًا تلقائيًا في مربع الإدخال. مفيد لتجربة الأداة دون الحاجة إلى الكتابة.",
        "ann_c": "<strong>حقل إدخال المطالبة</strong> - اكتب أو الصق النص العربي هنا. المربع محاذٍ من اليمين إلى اليسار.",
        "ann_d": "<strong>زر الفحص والمسح</strong> - يبدأ الفحص للكشف عن المعلومات الشخصية الحساسة والسامة في وقت واحد، ويمسح المدخلات ويعيد ضبط لوحة النتائج.",
        "ann_e": "<strong>عناصر التحكم في أعلى اليمين</strong> - للتبديل بين الوضع الليلي/النهاري (🌙) ولغة الواجهة (EN / AR).",
        # steps
        "step1_lbl":  "أدخل مطالبتك العربية",
        "step1_desc": "انقر في حقل الإدخال واكتب أو الصق النص العربي. يمكنك أيضاً النقر على أحد أزرار الأمثلة في الشريط الجانبي لتحميل نص تجريبي جاهز.",
        "step2_lbl":  "اضغط فحص",
        "step2_desc": "تعمل جميع المكونات الأربعة في آنٍ واحد. تظهر النتائج خلال 1-2 ثانية. اضغط مسح للبدء من جديد.",
        "step3_lbl":  "اقرأ نتيجة كشف المعلومات الشخصية (البطاقة اليسرى)",
        "step3_desc": "تُظهر إما «نظيف» (لم يُعثر على معلومات شخصية) أو عدد الكيانات المكتشفة. عند الاكتشاف، يظهر النص المُقنَّع مع بطاقات ملونة تُعدّد كل كيان ونوعه والنموذج الذي اكتشفه.",
        "step4_lbl":  "اقرأ نتيجة تحليل السمية (البطاقة اليمنى)",
        "step4_desc": "تُظهر الفئة المتوقعة ونسبة الثقة وتفصيل كامل لجميع الفئات السبع مع شارة تُشير إلى مستوى الخطورة.",
        "step5_lbl":  "اقرأ خريطة انتباه الكلمات",
        "step5_desc": "كل كلمة مُلوَّنة بحسب مدى تأثيرها في قرار التصنيف. اللون الداكن = تأثير أعلى. حروف الوصل الشائعة تظهر باللون الرمادي.",
        "step6_lbl":  "استخدم إعادة الصياغة",
        "step6_desc": "عند اكتشاف محتوى ضار يظهر قسم إعادة الصياغة. يعرض نسخة آمنة بديلة. اضغط الزر لإعادة التوليد، أو انسخ النص المُعاد كتابته للاستخدام بدلاً من النص الأصلي.",
        # tox table
        "badge_lbl":  "الشارة",
        "meaning_lbl":"المعنى",
        "cats_lbl":   "الفئات",
        "safe_meaning":  "لا يوجد محتوى ضار",
        "warn_meaning":  "ضار بشكل خفيف",
        "flag_meaning":  "ضار بشكل واضح",
        "crit_meaning":  "يستدعي العناية",
        # callouts
        "tip_examples":  "يمكنك النقر على أي <strong>زر مثال</strong> في الشريط الجانبي لتحميل نص تجريبي جاهز.",
        "tip_masked":    "استخدم دائماً <strong>النص المُقنَّع</strong> (الظاهر في بطاقة المعلومات الشخصية) بدلاً من النص الأصلي - سيظل روبوت المحادثة يفهم طلبك دون استقبال بياناتك الخاصة.",
        "tip_save":      "اضغط دائماً <strong>حفظ الإعدادات</strong> بعد إجراء أي تغيير. لن تُطبَّق التغييرات حتى يتم الحفظ.",
        "tip_autoscan":  "إذا كان <strong>الفحص التلقائي</strong> مفعَّلاً والمحتوى آمناً، يمكن تهيئة الإضافة للإرسال تلقائياً دون عرض النافذة المنبثقة.",
        # HL legend
        "hl_high": "عالٍ (>0.7)",
        "hl_mid":  "متوسط (0.4-0.7)",
        "hl_low":  "منخفض (0.1-0.4)",
        "hl_stop": "حرف وصل",
        # rewrite
        "rw_rewritten": "النص المُعاد كتابته",
        "rw_original":  "النص الأصلي",
        # PII table
        "tag_col": "البطاقة", "entity_col": "نوع الكيان", "example_col": "مثال", "detected_col": "يكتشفه",
        "pers_desc": "اسم شخص", "org_desc": "مؤسسة", "addr_desc": "موقع / عنوان",
        "dt_desc": "تاريخ / وقت", "id_desc": "رقم هوية / جواز سفر", "cred_desc": "كلمة مرور / PIN / OTP",
        "phone_desc": "رقم هاتف", "email_desc": "بريد إلكتروني", "ip_desc": "عنوان IP",
        "mac_desc": "عنوان MAC", "url_desc": "رابط إنترنت", "fin_desc": "رقم بطاقة / IBAN",
        # Quick ref
        "action_col": "الإجراء", "how_col": "الطريقة",
        "qr1": ("فحص مطالبة",              "اكتب أو الصق النص ← اضغط فحص"),
        "qr2": ("مسح حقل الإدخال",         "اضغط مسح"),
        "qr3": ("تجربة مثال جاهز",         "انقر أحد أزرار الأمثلة في الشريط الجانبي"),
        "qr4": ("التبديل بين الوضع الليلي/النهاري", "انقر 🌙 (أعلى اليمين)"),
        "qr5": ("تغيير لغة الواجهة",       "انقر EN / AR (أعلى اليمين)"),
        "qr6": ("معرفة النموذج الذي اكتشف الكيان", "تحقق من التسمية الصغيرة على كل بطاقة كيان (RGX / NER / XLM)"),
        "qr7": ("الحصول على إعادة صياغة آمنة", "اضغط إعادة الصياغة في قسم إعادة الصياغة"),
        "qr8": ("فهم الكلمات الضارة",     "اقرأ خريطة انتباه الكلمات (القسم السفلي)"),
        # Install
        "inst1_lbl":  "افتح متجر كروم الإلكتروني للإضافات",
        "inst1_desc": "اذهب إلى https://chromewebstore.google.com/ وابحث عن PromptScanner أو استخدم الرابط المباشر الموجود على موقعنا.",
        "inst2_lbl":  "فعّل وضع المطور",
        "inst2_desc": "فعّل مفتاح وضع المطور في الزاوية العلوية اليمنى من صفحة الإضافات.",
        "inst3_lbl":  "الوصول إلى الإضافة",
        "inst3_desc": "انقر على أيقونة قطعة الأحجية، ابحث عن PromptScanner، ثم اضغط على زر التثبيت (Pin) لإبقائها مرئية.",
        "inst4_lbl":  "ابدأ باستخدام PromptScanner",
        "inst4_desc": "ادخل إلى روبوتات الدردشة مثل ChatGPT أو Gemini، اكتب الأمر (Prompt)، ثم اضغط إرسال لترى PromptScanner يعمل!",
        # States
        "state_a": "الحالة أ - محتوى آمن (لا مشكلات)",
        "state_b": "الحالة ب - تم اكتشاف مشكلات",
        "state_c": "الحالة ج - تم توليد إعادة الصياغة",
        "state_a_desc": "عندما تكون مطالبتك نظيفة تظهر النافذة بزر واحد.",
        "state_b_desc": "عند اكتشاف معلومات شخصية أو محتوى ضار تظهر التحليلات وخياران.",
        "state_c_desc": "بعد ضغط إعادة الصياغة تظهر النسخة الآمنة مع خيارَي الإرسال.",
        # Popup annotations
        "pa1a": "<strong>النص المُقنَّع</strong> يؤكد عدم اكتشاف معلومات شخصية.",
        "pa1b": "<strong>التصنيف الأخضر «عادي»</strong> - المحتوى آمن بثقة عالية.",
        "pa1c": "<strong>→ إرسال الأصلي</strong> - يُرسل المطالبة كما هي. نقرة واحدة وتنتهي.",
        "pa2a": "<strong>النص المُقنَّع</strong> - قيم المعلومات الشخصية تظهر كعلامات [TYPE] عند اكتشافها.",
        "pa2b": "<strong>شارة حرجة + تصنيف أرجواني</strong> - تم اكتشاف فئة الصحة النفسية.",
        "pa2c": "<strong>الكلمات المؤثرة</strong> - كلمات ملونة تُشير إلى ما أثّر في التصنيف.",
        "pa2d": "<strong>إعادة الصياغة</strong> - يُولِّد نسخة آمنة (ينتقل إلى الحالة ج).",
        "pa2e": "<strong>→ إرسال الأصلي</strong> - متاح دائماً؛ القرار لك في النهاية.",
        "pa3a": "<strong>قسم النص المُعاد كتابته</strong> - البديل الآمن بحد أخضر.",
        "pa3b": "<strong>→ إرسال المُعاد كتابته</strong> - يُرسل النسخة الآمنة.",
        "pa3c": "<strong>→ إرسال الأصلي</strong> - يُرسل النص الأصلي رغم التحذير.",
        "pa3d": "<strong>✕ إلغاء</strong> - يغلق النافذة دون إرسال لتتمكن من التعديل يدوياً.",
        # Settings
        "set_intro":      "انقر أيقونة ⚙ في رأس النافذة المنبثقة لفتح الإعدادات.",
        "set_dark_lbl":   "الوضع الليلي",
        "set_dark_desc":  "تفعيل السمة الداكنة",
        "set_lang_lbl":   "اللغة",
        "set_lang_desc":  "لغة واجهة الإضافة",
        "set_popup_lbl":  "عرض النافذة للمحتوى الآمن",
        "set_popup_desc": "إذا كان آمناً اعرض النافذة، وإلا أرسل تلقائياً",
        "set_auto_lbl":   "الفحص التلقائي",
        "set_auto_desc":  "فحص المحتوى عند ضغط إرسال أو Enter",
        "set_dark_what":  "يُبدِّل النافذة المنبثقة إلى سمة ألوان داكنة.",
        "set_lang_what":  "اختر الإنجليزية أو العربية لجميع تسميات الأزرار.",
        "set_popup_what": "مفعّل: تظهر النافذة حتى للمطالبات الآمنة. معطّل: تُرسَل المطالبات الآمنة تلقائياً.",
        "set_auto_what":  "مفعّل: فحص تلقائي عند ضغط إرسال/Enter. معطّل: لا فحص تلقائي.",
        # Ext quick ref
        "eqr1": ("تشغيل الفحص",              "اضغط إرسال أو Enter في ChatGPT / Gemini (يتطلب تفعيل الفحص التلقائي)"),
        "eqr2": ("إرسال المطالبة الأصلية",   "اضغط → إرسال الأصلي"),
        "eqr3": ("إرسال النسخة المُعادة",     "اضغط إعادة الصياغة ثم → إرسال المُعاد كتابته"),
        "eqr4": ("الإلغاء دون إرسال",        "اضغط ✕ إلغاء"),
        "eqr5": ("فتح الإعدادات",            "انقر ⚙ في رأس النافذة"),
        "eqr6": ("تخطي النافذة للمحتوى الآمن","عطّل «عرض النافذة للمحتوى الآمن»"),
        "eqr7": ("تعطيل الفحص التلقائي",     "عطّل «الفحص التلقائي»"),
        # footer
        "footer_web": "<span>PromptScanner</span> - دليل المستخدم · الجزء الأول: الموقع الإلكتروني",
        "footer_ext": "<span>PromptScanner</span> - دليل المستخدم · الجزء الثاني: إضافة المتصفح · ChatGPT & Gemini",
    }
}


# ──────────────────────────────────────────────────────────────────────────────
# SMALL RENDER HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def img_to_base64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

logo_base64 = img_to_base64("assets/logo.png")

def guide_header(t, active_tab, rtl=False):
    """
    Full navy header: logo + name, tagline, title, description,
    and the two badge-style tab buttons - exactly like the original HTML design.
    """
    tab_web_active  = active_tab == "website"
    tab_ext_active  = active_tab == "extension"
    dir_attr        = 'dir="rtl"' if rtl else ''

    # Render the static navy header HTML
    st.markdown(f"""
<div class="guide-header" {dir_attr}>

  <!-- Logo + name row -->
  <div class="gh-logo-row">
    <img src="data:image/png;base64,{logo_base64}" class="gh-logo" alt="PromptScanner logo"/>
    <div>
      <div class="gh-name">Prompt<span>Scanner</span></div>
      <div class="gh-sub">{'حارس خصوصيتك في عالم الذكاء الاصطناعي' if rtl else 'Your Privacy Guardian in the AI World'}</div>
    </div>
  </div>

  <!-- Title + description -->
  <div class="gh-title" style="text-align: {'right' if rtl else 'left'};">{'دليل المستخدم' if rtl else 'User Guide'}</div>
  <p class="gh-desc">{'تعليمات خطوة بخطوة لاستخدام PromptScanner للكشف عن المعلومات الشخصية والمحتوى الضار في مطالباتك العربية قبل إرسالها.' if rtl else 'Step-by-step instructions for using PromptScanner to detect personally identifiable information and toxic content in Arabic prompts before submitting them to an AI chatbot.'}</p>

</div>
""", unsafe_allow_html=True)

    # Tab buttons - rendered as Streamlit buttons styled as orange/grey badges
    btn_col1, btn_col2, spacer = st.columns([1.8, 2.4, 5])
    with btn_col1:
        if st.button(
            t["tab_web"],
            key="tab_btn_website",
            use_container_width=True,
            type="primary" if tab_web_active else "secondary",
        ):
            st.query_params["tab"] = "website"
            st.rerun()
    with btn_col2:
        if st.button(
            t["tab_ext"],
            key="tab_btn_extension",
            use_container_width=True,
            type="primary" if tab_ext_active else "secondary",
        ):
            st.query_params["tab"] = "extension"
            st.rerun()

    # Bottom border of the header area
    st.markdown('<div class="gh-bottom-rule"></div>', unsafe_allow_html=True)


def sec_header(num, part, title, rtl=False):
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(f"""
<div class="sec-head" {dir_attr}>
  <div class="sec-num">{num}</div>
  <div><div class="sec-part">{part}</div><div class="sec-title">{title}</div></div>
</div>""", unsafe_allow_html=True)


def intro_box(text, rtl=False):
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(
        f'<div style="background:#1a2340;color:rgba(255,255,255,0.8);'
        f'border-radius:10px;padding:20px 24px;margin:16px 0 24px;'
        f'line-height:1.7;font-size:1rem;" {dir_attr}>{text}</div>',
        unsafe_allow_html=True
    )


def flow_diagram(*nodes, rtl=False):
    parts = []
    for i, (label, cls) in enumerate(nodes):
        parts.append(f'<div class="flow-node {cls}">{label}</div>')
        if i < len(nodes) - 1:
            parts.append('<div class="flow-arr">→</div>')
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(
        f'<div class="flow">{"".join(parts)}</div>',
        unsafe_allow_html=True
    )


def comp_grid(items, rtl=False):
    """items: list of (dot_colour, name, desc, pills_html)"""
    cards = ""
    for colour, name, desc, pills in items:
        cards += f"""
<div class="comp-card">
  <div class="comp-head">
    <div class="comp-dot" style="background:{colour}"></div>
    <div class="comp-name">{name}</div>
  </div>
  <div class="comp-desc">{desc}</div>
  <div class="comp-cats">{pills}</div>
</div>"""
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(
        f'<div class="comp-grid" {dir_attr}>{cards}</div>',
        unsafe_allow_html=True
    )


def pill(text, bg, fg):
    return f'<span class="cat-pill" style="background:{bg};color:{fg};">{text}</span>'


def annotations(items, rtl=False):
    rows = ""
    for label, text in items:
        rows += (
            f'<div class="ann-row">'
            f'<div class="ann" style="flex-shrink:0;">{label}</div>'
            f'<div style="color:#2a2a2a;font-size:0.87rem;line-height:1.6;">{text}</div>'
            f'</div>'
        )
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(
        f'<div style="background:#ffffff;border:1px solid var(--border);'
        f'border-radius:10px;padding:12px 16px;margin-top:8px;" {dir_attr}>{rows}</div>',
        unsafe_allow_html=True
    )


def step(num, label, desc, extra_html="", marker_class="", rtl=False, last=False):
    line = "" if last else '<div class="step-line"></div>'
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(f"""
<div class="step-row" {dir_attr}>
  <div class="step-left">
    <div class="step-num {marker_class}">{num}</div>
    {line}
  </div>
  <div class="step-body">
    <div class="step-label">{label}</div>
    <div class="step-desc">{desc}</div>
    {extra_html}
  </div>
</div>""", unsafe_allow_html=True)


def callout(icon, text, kind="tip", rtl=False):
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(
        f'<div class="callout callout-{kind}" {dir_attr}>'
        f'<div style="font-size:1rem;line-height:1.6;flex-shrink:0;">{icon}</div>'
        f'<p>{text}</p></div>',
        unsafe_allow_html=True
    )


def guide_table(headers, rows, rtl=False):
    thead = "".join(f"<th>{h}</th>" for h in headers)
    tbody = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
        for row in rows
    )
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(
        f'<table class="guide-table" {dir_attr}><thead><tr>{thead}</tr></thead>'
        f'<tbody>{tbody}</tbody></table>',
        unsafe_allow_html=True
    )


def hl_legend(t, rtl=False):
    items = [
        (f'rgba(192,57,43,0.82)', t["hl_high"]),
        (f'rgba(192,57,43,0.42)', t["hl_mid"]),
        (f'rgba(192,57,43,0.17)', t["hl_low"]),
        (f'rgba(160,160,160,0.1)', t["hl_stop"]),
    ]
    parts = ""
    for bg, label in items:
        parts += (f'<span><span style="display:inline-block;width:11px;height:11px;'
                  f'background:{bg};border-radius:3px;vertical-align:middle;margin-right:3px;"></span>'
                  f'{label}</span>')
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(
        f'<div style="display:flex;gap:14px;flex-wrap:wrap;font-size:.77rem;'
        f'color:#888;justify-content:flex-end;margin-top:8px;" {dir_attr}>{parts}</div>',
        unsafe_allow_html=True
    )


def ext_popup_safe(t, rtl=False):
    logo_src = f"data:image/png;base64,{logo_base64}"
    dir_attr = 'dir="rtl"' if rtl else ''
    return f"""
<div class="ext-popup" {dir_attr}>
  <div class="ext-header">
    <div style="display:flex;align-items:center;gap:8px;">
      <img src="{logo_src}" style="width:22px;height:22px;border-radius:5px;object-fit:contain;" alt="logo"/>
      <div><div class="ext-logo">Prompt<span>Scanner</span></div><div class="ext-sub">{'فحص الخصوصية والسلامة' if rtl else 'Privacy &amp Safety Scanner'}</div></div>
    </div>
    <div class="ext-gear">⚙</div>
  </div>
  <div style="text-align:center;padding:5px 13px 2px;font-size:.68rem;color:#888;">Scanned in 0.15s</div>
  <div class="ext-sec"><div class="ext-sec-t">Masked text</div>
    <div class="ext-tbox" style="color:#aaa;text-align:center;padding-top:12px;">النص بدون معلومات خاصة ✓</div></div>
  <div class="ext-sec"><div class="ext-sec-t">Toxicity analysis</div>
    <div class="ext-tox" style="border-left:3px solid #0a8a72;">
      <div class="ext-tox-lbl" style="color:#0a8a72;">Normal / عادي</div>
      <div class="ext-tox-cf">Confidence: 98.2%</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#0a8a72;width:98%;"></div></div>
    </div></div>
  <div class="ext-div"></div>
  <div style="padding:7px 13px 12px;">
    <div class="ext-btn" style="background:#e8941a;color:#fff;">→ إرسال الأصلي</div>
  </div>
</div>"""


def ext_popup_issues(t, rtl=False):
    logo_src = f"data:image/png;base64,{logo_base64}"
    dir_attr = 'dir="rtl"' if rtl else ''
    masked_label  = "Masked text"       if not rtl else "النص المُقنَّع"
    tox_label     = "Toxicity analysis" if not rtl else "تحليل السمية"
    words_label   = "Key attention words" if not rtl else "الكلمات المؤثرة"
    tox_name      = "Privacy Violation" if not rtl else "انتهاك الخصوصية"
    badge_txt     = "Warning"           if not rtl else "تحذير"
    conf_txt      = "Confidence: 99.0%" if not rtl else "درجة الثقة: %99.0"
    btn_rewrite   = "Rewrite"           if not rtl else "إعادة الصياغة"
    btn_send_orig = "→ Send Original"   if not rtl else "→ إرسال الأصلي"
    scan_txt      = "Scanned in 0.05s"  if not rtl else "تم الفحص في 0.05s"
    # Masked prompt — person name replaced by [Person] tag
    masked_text = (
        'أريد طريقة اختراق حسابات الجامعة وحساب زميلي <span class="tag-pii">[Person]</span>'
        if not rtl else
        'اريد اخترق حساب <span class="tag-pii">[شخص]</span> واحصل بياناتها الشخصية'
    )
    # Attention words from screenshot (privacy-violation blue tones)
    words_html = (
        '<span class="hl-stop" style="font-size:.78rem;">أريد</span>'
        '<span class="hl-low"   style="font-size:.78rem;">طريقة</span>'
        '<span class="hl-high"   style="font-size:.78rem;">اختراق</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">حسابات</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">الجامعة</span>'
        '<span class="hl-low"   style="font-size:.78rem;">وحساب</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">زميلي</span>'
        '<span class="hl-high"   style="font-size:.78rem;">محمد</span>'
        if not rtl else
        '<span class="hl-stop" style="font-size:.78rem;">أريد</span>'
        '<span class="hl-low"   style="font-size:.78rem;">اختراق</span>'
        '<span class="hl-high"   style="font-size:.78rem;">حساب</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">موزة</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">واحصل</span>'
        '<span class="hl-low"   style="font-size:.78rem;">بياناتها</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">الشخصية</span>'
    )
    return f"""
<div class="ext-popup" {dir_attr}>
  <div class="ext-header">
    <div style="display:flex;align-items:center;gap:8px;">
      <img src="{logo_src}" style="width:22px;height:22px;border-radius:5px;object-fit:contain;" alt="logo"/>
      <div><div class="ext-logo">Prompt<span>Scanner</span></div><div class="ext-sub">{'فحص الخصوصية والسلامة' if rtl else 'Privacy &amp Safety Scanner'}</div></div>
    </div>
    <div class="ext-gear">⚙</div>
  </div>
  <div style="text-align:center;padding:5px 13px 2px;font-size:.68rem;color:#888;">{scan_txt}</div>
  <div class="ext-sec"><div class="ext-sec-t">{masked_label}</div>
    <div class="ext-tbox">{masked_text}</div></div>
  <div class="ext-sec"><div class="ext-sec-t">{tox_label}</div>
    <div class="ext-tox" style="border-left:3px solid rgba(92, 190, 251);">
      <div class="ext-badge" style="background:#fef3dc;color:#7a4e00;">{badge_txt}</div>
      <div class="ext-tox-lbl" style="color:rgba(92, 190, 251);">{tox_name}</div>
      <div class="ext-tox-cf">{conf_txt}</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:rgba(92, 190, 251);width:99%;"></div></div>
    </div></div>
  <div class="ext-sec"><div class="ext-sec-t">{words_label}</div>
    <div class="ext-words">{words_html}</div></div>
  <div class="ext-div"></div>
  <div style="padding:7px 13px 12px;display:flex;flex-direction:column;gap:5px;">
    <div class="ext-btn" style="background:#1a2340;color:#fff;">{btn_rewrite}</div>
    <div class="ext-btn" style="background:#e8941a;color:#fff;">{btn_send_orig}</div>
  </div>
</div>"""


def ext_popup_rewrite(t, rtl=False):
    logo_src = f"data:image/png;base64,{logo_base64}"
    dir_attr = 'dir="rtl"' if rtl else ''
    masked_label    = "Masked text"          if not rtl else "النص المُقنَّع"
    tox_label       = "Toxicity analysis"    if not rtl else "تحليل السمية"
    words_label     = "Key attention words"  if not rtl else "الكلمات المؤثرة"
    rewrite_label   = "Rewritten prompt"     if not rtl else "النص المُعاد كتابته"
    tox_name        = "Privacy Violation"    if not rtl else "انتهاك الخصوصية"
    badge_txt       = "Warning"              if not rtl else "تحذير"
    conf_txt        = "Confidence: 99.0%"    if not rtl else "درجة الثقة: %99.0"
    btn_send_rw     = "→ Send Rewritten"     if not rtl else "→ إرسال المُعاد كتابته"
    btn_send_orig   = "→ Send Original"      if not rtl else "→ إرسال الأصلي"
    btn_cancel      = "✕ Cancel"             if not rtl else "✕ إلغاء"
    scan_txt        = "Scanned in 0.05s"     if not rtl else "تم الفحص في 0.05s"
    masked_text = (
        'أريد طريقة اختراق حسابات الجامعة وحساب <span class="tag-pii">[Person]</span>'
        if not rtl else
        'اريد اخترق حساب <span class="tag-pii">[شخص]</span> واحصل بياناتها الشخصية'
    )
    words_html = (
        '<span class="hl-stop" style="font-size:.78rem;">أريد</span>'
        '<span class="hl-low"   style="font-size:.78rem;">طريقة</span>'
        '<span class="hl-high"   style="font-size:.78rem;">اختراق</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">حسابات</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">الجامعة</span>'
        '<span class="hl-low"   style="font-size:.78rem;">وحساب</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">زميلي</span>'
        '<span class="hl-high"   style="font-size:.78rem;">محمد</span>'
        if not rtl else
        '<span class="hl-stop" style="font-size:.78rem;">أريد</span>'
        '<span class="hl-low"   style="font-size:.78rem;">اختروق</span>'
        '<span class="hl-high"   style="font-size:.78rem;">حساب</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">موزة</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">واحصل</span>'
        '<span class="hl-low"   style="font-size:.78rem;">بياناتها</span>'
        '<span class="hl-mid"   style="font-size:.78rem;">الشخصية</span>'
    )
    rewritten_text = (
        'لمنع أي اختراق، أريد طريقة تحسين أمان حسابات الجامعة وحساب زميلي <span class="tag-pii">[PERS]</span>.'
        if not rtl else
        'أريد تعلم كيفية حماية الحسابات الشخصية من الوصول غير المصرح به.'
    )
    return f"""
<div class="ext-popup" {dir_attr}>
  <div class="ext-header">
    <div style="display:flex;align-items:center;gap:8px;">
      <img src="{logo_src}" style="width:22px;height:22px;border-radius:5px;object-fit:contain;" alt="logo"/>
      <div><div class="ext-logo">Prompt<span>Scanner</span></div><div class="ext-sub">{'فحص الخصوصية والسلامة' if rtl else 'Privacy &amp; Safety Scanner'}</div></div>
    </div>
    <div class="ext-gear">⚙</div>
  </div>
  <div style="text-align:center;padding:5px 13px 2px;font-size:.68rem;color:#888;">{scan_txt}</div>
  <div class="ext-sec"><div class="ext-sec-t">{masked_label}</div>
    <div class="ext-tbox">{masked_text}</div></div>
  <div class="ext-sec"><div class="ext-sec-t">{tox_label}</div>
    <div class="ext-tox" style="border-left:3px solid rgba(92, 190, 251);">
      <div class="ext-badge" style="background:#fef3dc;color:#7a4e00;">{badge_txt}</div>
      <div class="ext-tox-lbl" style="color:rgba(92, 190, 251);">{tox_name}</div>
      <div class="ext-tox-cf">{conf_txt}</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:rgba(92, 190, 251);width:99%;"></div></div>
    </div></div>
  <div class="ext-sec"><div class="ext-sec-t">{words_label}</div>
    <div class="ext-words">{words_html}</div></div>
  <div class="ext-sec" style="padding-bottom:7px;">
    <div class="ext-sec-t" style="color:#0a8a72;">{rewrite_label}</div>
    <div class="ext-tbox" style="border-color:#0a8a72;border-width:1.5px;font-size:.78rem;">
      {rewritten_text}
    </div></div>
  <div class="ext-div"></div>
  <div style="padding:7px 13px 5px;display:grid;grid-template-columns:1fr 1fr;gap:5px;">
    <div class="ext-btn" style="background:#0a8a72;color:#fff;font-size:.74rem;">{btn_send_rw}</div>
    <div class="ext-btn" style="background:#e8941a;color:#fff;font-size:.74rem;">{btn_send_orig}</div>
  </div>
  <div style="padding:0 13px 11px;">
    <div class="ext-btn" style="background:#ebe5d8;color:#555;font-size:.76rem;">{btn_cancel}</div>
  </div>
</div>"""


def ext_popup_settings(t, rtl=False):
    logo_src = f"data:image/png;base64,{logo_base64}"
    return f"""
<div class="ext-popup">
  <div class="ext-header">
    <div style="display:flex;align-items:center;gap:8px;">
      <img src="{logo_src}" style="width:22px;height:22px;border-radius:5px;object-fit:contain;" alt="logo"/>
      <div><div class="ext-logo">Prompt<span>Scanner</span></div><div class="ext-sub">{'فحص الخصوصية والسلامة' if rtl else 'Privacy &amp; Safety Scanner'}</div></div>
    </div>
    <div class="ext-gear" style="background:#e74c3c;color:#fff;">✕</div>
  </div>
  <div style="padding:9px 15px 4px;">
    <div class="ext-grp-t">{t['set_dark_lbl'][:11] if len(t['set_dark_lbl']) > 5 else 'Appearance'}</div>
    <div style="background:#fff;border-radius:9px;padding:9px 13px;border:1px solid #ddd;">
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">{t['set_dark_lbl']}</div><div class="ext-set-sub">{t['set_dark_desc']}</div></div>
        <div class="ext-tog ext-tog-off"><div class="ext-tog-k ext-tog-kof"></div></div>
      </div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">{t['set_lang_lbl']}</div><div class="ext-set-sub">{t['set_lang_desc']}</div></div>
        <div class="ext-lang"><div class="ext-lan-i">العربية</div><div class="ext-lan-a">English</div></div>
      </div>
    </div>
    <div class="ext-grp-t" style="margin-top:9px;">{t['set_auto_lbl'][:8] if len(t['set_auto_lbl'])>5 else 'Behavior'}</div>
    <div style="background:#fff;border-radius:9px;padding:9px 13px;border:1px solid #ddd;">
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">{t['set_popup_lbl']}</div><div class="ext-set-sub">{t['set_popup_desc']}</div></div>
        <div class="ext-tog ext-tog-on"><div class="ext-tog-k ext-tog-kon"></div></div>
      </div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">{t['set_auto_lbl']}</div><div class="ext-set-sub">{t['set_auto_desc']}</div></div>
        <div class="ext-tog ext-tog-on"><div class="ext-tog-k ext-tog-kon"></div></div>
      </div>
    </div>
    <div class="ext-save">✓ Save Settings</div>
  </div>
</div>"""


def popup_with_annotations(popup_html, ann_items, rtl=False):
    """Renders popup mockup and annotation list side by side."""
    col_popup, col_ann = st.columns([1, 1.3])
    with col_popup:
        st.markdown(popup_html, unsafe_allow_html=True)
    with col_ann:
        annotations(ann_items, rtl=rtl)


def doc_footer(text, rtl=False):
    dir_attr = 'dir="rtl"' if rtl else ''
    st.markdown(
        f'<div class="doc-footer" {dir_attr}>{text}</div>',
        unsafe_allow_html=True
    )


# ──────────────────────────────────────────────────────────────────────────────
# WEBSITE GUIDE
# ──────────────────────────────────────────────────────────────────────────────

def render_website_guide(t, rtl=False):

    # ── Section 1: What is PromptScanner ──────────────────────────────────────
    sec_header("1", t["sec_overview"], "PromptScanner", rtl=rtl)
    intro_box(t["intro_web"], rtl=rtl)

    flow_diagram(
        (t["flow_type"],   ""),
        (t["flow_scan"],   "flow-amber"),
        (t["flow_run"],    "flow-teal"),
        (t["flow_result"], ""),
        rtl=rtl,
    )

    comp_grid([
        ("#e8941a", t["comp_arabert_name"], t["comp_arabert_desc"],
         pill("PERS","#fff3dc","#7a4e00") + pill("ORG","#fff3dc","#7a4e00") +
         pill("ADDRESS","#fff3dc","#7a4e00") + pill("DATETIME","#fff3dc","#7a4e00")),
        ("#0a8a72", t["comp_xlmr_name"], t["comp_xlmr_desc"],
         pill("ID","#d4f5ee","#0a4d3a") + pill("CREDENTIAL","#d4f5ee","#0a4d3a")),
        ("#1a5fa8", t["comp_regex_name"], t["comp_regex_desc"],
         pill("PHONE","#e8f0fc","#0e3a7a") + pill("EMAIL","#e8f0fc","#0e3a7a") +
         pill("IP","#e8f0fc","#0e3a7a") + pill("MAC","#e8f0fc","#0e3a7a") +
         pill("URL","#e8f0fc","#0e3a7a") + pill("FINANCIAL","#e8f0fc","#0e3a7a")),
        ("#6c3fc5", t["comp_tox_name"], t["comp_tox_desc"],
         pill("7 cat.","#ede8fc","#3d1b8a") + pill("keywords","#ede8fc","#3d1b8a")),
    ], rtl=rtl)

    # ── Section 2: Interface layout ───────────────────────────────────────────
    sec_header("2", t["sec_interface"], t["sec_interface"], rtl=rtl)

    # Interface preview mockup with A-E annotation markers
    rtl_style = "direction:rtl;text-align:right;" if rtl else ""
    st.markdown(f"""
<div style="background:#f0ebe0;border:1px solid var(--border);border-radius:12px;
            padding:18px;margin:16px 0 8px;{rtl_style}">

  <!-- Nav bar -->
  <div style="display:flex;align-items:center;justify-content:space-between;
              padding-bottom:12px;border-bottom:1px solid #ddd;margin-bottom:14px;">
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="width:30px;height:30px;background:var(--navy);border-radius:7px;
                  display:flex;align-items:center;justify-content:center;font-size:.9rem;">⬡</div>
      <div style="font-weight:800;font-size:.95rem;color:var(--navy);">
        Prompt<span style="color:var(--amber);">Scanner</span>
      </div>
    </div>
    <div style="display:flex;gap:7px;">
      <div style="background:var(--navy);color:#fff;border-radius:7px;
                  padding:5px 11px;font-size:.75rem;font-weight:700;">🌙</div>
      <div style="background:var(--navy);color:#fff;border-radius:7px;
                  padding:5px 11px;font-size:.75rem;font-weight:700;">EN</div>
    </div>
  </div>

  <!-- Body: sidebar + main -->
  <div style="display:grid;grid-template-columns:200px 1fr;gap:12px;">

<!-- Sidebar -->
<div style="background:#ebe5d8;border-radius:8px;padding:12px;position:relative;">
  <div class="ann" style="position:absolute;top:-8px;left:-8px;z-index:2;">A</div>
  <div style="font-size:.65rem;font-weight:700;text-transform:uppercase;
              letter-spacing:.1em;color:#888;margin-bottom:8px;">
    {'النماذج المستخدمة' if rtl else 'Models'}
  </div>
  <div style="background:#fff;border-radius:6px;padding:6px 9px;margin-bottom:5px;
              border:1px solid #ddd;display:flex;align-items:flex-start;gap:7px;">
    <div style="width:7px;height:7px;border-radius:50%;background:#0a8a72;margin-top:3px;flex-shrink:0;"></div>
    <div>
      <div style="font-weight:700;font-size:.72rem;color:var(--navy);">AraBERT NER</div>
      <div style="font-size:.65rem;color:#888;">{'كشف الأشخاص والمؤسسات' if rtl else 'Names, orgs, dates'}</div>
    </div>
  </div>
  <div style="background:#fff;border-radius:6px;padding:6px 9px;margin-bottom:5px;
              border:1px solid #ddd;display:flex;align-items:flex-start;gap:7px;">
    <div style="width:7px;height:7px;border-radius:50%;background:#0a8a72;margin-top:3px;flex-shrink:0;"></div>
    <div>
      <div style="font-weight:700;font-size:.72rem;color:var(--navy);">XLM-RoBERTa</div>
      <div style="font-size:.65rem;color:#888;">{'كشف الهويات وبيانات الدخول' if rtl else 'IDs, credentials'}</div>
    </div>
  </div>
  <div style="background:#fff;border-radius:6px;padding:6px 9px;margin-bottom:5px;
              border:1px solid #ddd;display:flex;align-items:flex-start;gap:7px;">
    <div style="width:7px;height:7px;border-radius:50%;background:#0a8a72;margin-top:3px;flex-shrink:0;"></div>
    <div>
      <div style="font-weight:700;font-size:.72rem;color:var(--navy);">Regex Engine</div>
      <div style="font-size:.65rem;color:#888;">{'الهاتف والبريد والروابط' if rtl else 'Phone, email, URL'}</div>
    </div>
  </div>
  <div style="background:#fff;border-radius:6px;padding:6px 9px;margin-bottom:12px;
              border:1px solid #ddd;display:flex;align-items:flex-start;gap:7px;">
    <div style="width:7px;height:7px;border-radius:50%;background:#0a8a72;margin-top:3px;flex-shrink:0;"></div>
    <div>
      <div style="font-weight:700;font-size:.72rem;color:var(--navy);">AraBERT v2</div>
      <div style="font-size:.65rem;color:#888;">{'تصنيف المحتوى السام' if rtl else 'Toxicity classifier'}</div>
    </div>
  </div>
  <!-- Example buttons -->
  <div class="ann" style="position:absolute;top:260px;left:-8px;z-index:2;">B</div>
  <div style="font-size:.65rem;font-weight:700;text-transform:uppercase;
              letter-spacing:.1em;color:#888;margin-bottom:6px;">
    {'أمثلة للتجربة' if rtl else 'Examples'}
  </div>
  <div style="background:var(--navy);color:#fff;border-radius:6px;padding:6px 9px;
              margin-bottom:5px;font-size:.73rem;font-weight:600;text-align:center;">
    {'اسم + مؤسسة' if rtl else 'Name + Org'}
  </div>
  <div style="background:var(--navy);color:#fff;border-radius:6px;padding:6px 9px;
              margin-bottom:5px;font-size:.73rem;font-weight:600;text-align:center;">
    {'هاتف + بريد' if rtl else 'Phone + Email'}
  </div>
  <div style="background:var(--navy);color:#fff;border-radius:6px;padding:6px 9px;
              margin-bottom:5px;font-size:.73rem;font-weight:600;text-align:center;">
    {'هوية + بيانات دخول' if rtl else 'ID + Credential'}
  </div>
  <div style="background:var(--navy);color:#fff;border-radius:6px;padding:6px 9px;
              font-size:.73rem;font-weight:600;text-align:center;">
    {'محتوى خطير' if rtl else 'Dangerous content'}
  </div>
</div>

<!-- Main area -->
<div style="display:flex;flex-direction:column;gap:10px;position:relative;">
  <!-- Text area -->
  <div style="position:relative;">
    <div class="ann" style="position:absolute;top:-8px;right:-8px;z-index:2;">C</div>
    <div style="background:#fff;border:1px solid #ccc;border-radius:8px;
                padding:10px 13px;min-height:68px;font-size:.84rem;
                color:#aaa;direction:rtl;text-align:right;">
      {'اكتب نصك العربي هنا…' if rtl else 'اكتب نصك العربي هنا…'}
    </div>
  </div>
<!-- Buttons -->
<div style="display:flex;gap:8px;position:relative;">
    <div class="ann" style="position:absolute;top:-8px;{{ 'right:-8px;' if rtl else 'left:-8px;' }}z-index:2;">D</div>
    <div style="background:var(--navy);color:#fff;border-radius:8px;
                padding:8px 20px;font-weight:700;font-size:.82rem;">
      {'فحص' if rtl else 'فحص'}
    </div>
    <div style="background:var(--navy);color:#fff;border-radius:8px;
                padding:8px 16px;font-size:.82rem;">
      {'مسح' if rtl else 'مسح'}
    </div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Annotation legend
    ann_items_web = [
        ("A", t["ann_a"]),
        ("B", t["ann_b"]),
        ("C", t["ann_c"]),
        ("D", t["ann_d"]),
        ("E", t["ann_e"]),
    ]
    # Render E separately as a plain callout (it describes top-right buttons not in mockup)
    annotations(ann_items_web[:4], rtl=rtl)
    st.markdown(
        f'<div style="display:flex;gap:9px;margin-top:8px;flex-wrap:wrap;">'
        f'<div style="background:var(--navy);color:#fff;border-radius:8px;'
        f'padding:6px 14px;font-size:.8rem;font-weight:700;">🌙 Dark mode</div>'
        f'<div style="background:var(--navy);color:#fff;border-radius:8px;'
        f'padding:6px 14px;font-size:.8rem;font-weight:700;">EN / AR toggle</div>'
        f'</div>'
        f'<p style="font-size:.84rem;color:var(--muted);margin-top:6px;'
        f'{"direction:rtl;text-align:right;" if rtl else ""}">{t["ann_e"]}</p>',
        unsafe_allow_html=True
    )

    # ── Section 3: Scanning steps ─────────────────────────────────────────────
    sec_header("3", t["sec_steps"], t["sec_steps"], rtl=rtl)
    callout("💡", t["tip_examples"], "tip", rtl=rtl)

    tox_badge_table = f"""
<table class="guide-table" style="margin-top:12px;" {'dir="rtl"' if rtl else ''}>
  <thead><tr>
    <th>{t['badge_lbl']}</th><th>{t['meaning_lbl']}</th><th>{t['cats_lbl']}</th>
  </tr></thead>
  <tbody>
    <tr><td><span class="badge b-safe">SAFE</span></td><td>{t['safe_meaning']}</td><td>Normal / عادي</td></tr>
    <tr><td><span class="badge b-warn">WARNING</span></td><td>{t['warn_meaning']}</td><td>Offensive · Privacy · Mild Offense</td></tr>
    <tr><td><span class="badge b-flag">FLAGGED</span></td><td>{t['flag_meaning']}</td><td>Dangerous · Obscene</td></tr>
    <tr><td><span class="badge b-crit">CRITICAL</span></td><td>{t['crit_meaning']}</td><td>Mental Health</td></tr>
  </tbody>
</table>"""

    hl_example = """
<div style="background:#fff;border:1px solid #ddd;border-radius:8px;padding:11px;
            margin-top:10px;text-align:right;direction:rtl;line-height:2.4;">
  <span class="hl-stop">كيف</span>
  <span class="hl-ph">أفهم</span>
  <span class="hl-pm">الناس</span>
  <span class="hl-pm">الغبية</span>
  <span class="hl-ph">أنهم</span>
  <span class="hl-pm">أغبياء</span>
</div>"""

    rw_example = f"""
<div class="rw-grid">
  <div>
    <div class="rw-col-title">{t['rw_rewritten']}</div>
    <div class="rw-box">.كيف يمكنني فهم الناس الذين يحتاجون إلى مساعدة إضافية في فهم بعض الأمور</div>
  </div>
  <div>
    <div class="rw-col-title">{t['rw_original']}</div>
    <div class="rw-box" style="color:#999;">كيف افهم الناس الغبية أنهم اغبياء </div>
  </div>
</div>"""

    step("1", t["step1_lbl"], t["step1_desc"], rtl=rtl)
    step("2", t["step2_lbl"], t["step2_desc"], rtl=rtl)
    step("3", t["step3_lbl"], t["step3_desc"], rtl=rtl)
    step("4", t["step4_lbl"], t["step4_desc"], extra_html=tox_badge_table, rtl=rtl)
    step("5", t["step5_lbl"], t["step5_desc"], extra_html=hl_example, rtl=rtl)
    hl_legend(t, rtl=rtl)
    step("6", t["step6_lbl"], t["step6_desc"], extra_html=rw_example,
         marker_class="", last=True, rtl=rtl)
    callout("💡", t["tip_masked"], "tip", rtl=rtl)

    # ── Section 4: PII reference ──────────────────────────────────────────────
    sec_header("4", t["sec_pii_ref"], t["sec_pii_ref"], rtl=rtl)
    guide_table(
        [t["tag_col"], t["entity_col"], t["example_col"], t["detected_col"]],
        [
            ['<span class="pii-tag">[PERS]</span>',    t["pers_desc"],  "أحمد المقبالي",     "AraBERT NER"],
            ['<span class="pii-tag">[ORG]</span>',     t["org_desc"],   "بنك مسقط",          "AraBERT NER"],
            ['<span class="pii-tag">[ADDRESS]</span>', t["addr_desc"],  "مسقط، عُمان",       "AraBERT NER"],
            ['<span class="pii-tag">[DATETIME]</span>',t["dt_desc"],    "الثلاثاء 5 مارس",   "AraBERT NER"],
            ['<span class="pii-tag">[ID]</span>',      t["id_desc"],    "12345678",           "XLM-RoBERTa"],
            ['<span class="pii-tag">[CREDENTIAL]</span>',t["cred_desc"],"MyPass123!",        "XLM-RoBERTa"],
            ['<span class="pii-tag">[PHONE]</span>',   t["phone_desc"], "+968 91234567",      "Regex"],
            ['<span class="pii-tag">[EMAIL]</span>',   t["email_desc"], "ahmed@squ.edu.om",   "Regex"],
            ['<span class="pii-tag">[IP]</span>',      t["ip_desc"],    "192.168.1.1",        "Regex"],
            ['<span class="pii-tag">[MAC]</span>',     t["mac_desc"],   "AA:BB:CC:DD:EE:FF",  "Regex"],
            ['<span class="pii-tag">[URL]</span>',     t["url_desc"],   "https://example.com","Regex"],
            ['<span class="pii-tag">[FINANCIAL]</span>',t["fin_desc"],  "OM21BMI…",          "Regex"],
        ],
        rtl=rtl,
    )

    # ── Section 5: Quick reference ────────────────────────────────────────────
    sec_header("5", t["sec_quickref"], t["sec_quickref"], rtl=rtl)
    guide_table(
        [t["action_col"], t["how_col"]],
        [list(t[k]) for k in ["qr1","qr2","qr3","qr4","qr5","qr6","qr7","qr8"]],
        rtl=rtl,
    )

    doc_footer(t["footer_web"], rtl=rtl)


# ──────────────────────────────────────────────────────────────────────────────
# EXTENSION GUIDE
# ──────────────────────────────────────────────────────────────────────────────

def render_extension_guide(t, rtl=False):

    # ── Section 1: What it does ───────────────────────────────────────────────
    sec_header("1", t["sec_overview"], t["sec_overview"], rtl=rtl)
    intro_box(t["intro_ext"], rtl=rtl)

    flow_diagram(
        (t["flow_type2"], ""),
        (t["flow_send"],  "flow-amber"),
        (t["flow_catch"], "flow-teal"),
        (t["flow_decide"],""),
        rtl=rtl,
    )

    # ── Section 2: Installation ───────────────────────────────────────────────
    sec_header("2", t["sec_install"], t["sec_install"], rtl=rtl)
    step("1", t["inst1_lbl"], t["inst1_desc"], rtl=rtl)
    step("2", t["inst2_lbl"], t["inst2_desc"], rtl=rtl)
    step("3", t["inst3_lbl"], t["inst3_desc"], rtl=rtl)
    step("4", t["inst4_lbl"], t["inst4_desc"], last=True, rtl=rtl)

    # ── Section 3: Popup states ───────────────────────────────────────────────
    sec_header("3", t["sec_states"], t["sec_states"], rtl=rtl)

    st.markdown(
        f'<p style="color:#6b6560;font-size:1rem;margin-bottom:18px;'
        f'{"text-align:right;direction:rtl;" if rtl else ""}">'
        f'{"عند ضغط إرسال داخل ChatGPT أو Gemini تظهر نافذة منبثقة تعرض نتيجة الفحص. لها ثلاث حالات." if rtl else "When you press Send inside ChatGPT or Gemini, a popup appears showing the scan result. It has three states."}'
        f'</p>',
        unsafe_allow_html=True
    )

    # State A
    st.markdown(f'<div class="sub-title" {"dir=rtl" if rtl else ""}>{t["state_a"]}</div>',
                unsafe_allow_html=True)
    popup_with_annotations(
        ext_popup_safe(t, rtl=rtl),
        [("1", t["pa1a"]), ("2", t["pa1b"]), ("3", t["pa1c"])],
        rtl=rtl,
    )
    callout("💡", t["tip_autoscan"], "tip", rtl=rtl)

    # State B
    st.markdown(f'<div class="sub-title" {"dir=rtl" if rtl else ""}>{t["state_b"]}</div>',
                unsafe_allow_html=True)
    popup_with_annotations(
        ext_popup_issues(t, rtl=rtl),
        [("1",t["pa2a"]),("2",t["pa2b"]),("3",t["pa2c"]),("4",t["pa2d"]),("5",t["pa2e"])],
        rtl=rtl,
    )

    # State C
    st.markdown(f'<div class="sub-title" {"dir=rtl" if rtl else ""}>{t["state_c"]}</div>',
                unsafe_allow_html=True)
    popup_with_annotations(
        ext_popup_rewrite(t, rtl=rtl),
        [("1",t["pa3a"]),("2",t["pa3b"]),("3",t["pa3c"]),("4",t["pa3d"])],
        rtl=rtl,
    )

    # ── Section 4: Settings ───────────────────────────────────────────────────
    sec_header("4", t["sec_settings"], t["sec_settings"], rtl=rtl)
    st.markdown(
        f'<p style="color:#6b6560;font-size:1rem;margin-bottom:16px;'
        f'{"text-align:right;direction:rtl;" if rtl else ""}">'
        f'{t["set_intro"]}</p>',
        unsafe_allow_html=True
    )

    col_s, col_t = st.columns([1, 1.2])
    with col_s:
        st.markdown(ext_popup_settings(t, rtl=rtl), unsafe_allow_html=True)
    with col_t:
        guide_table(
            [t["action_col"] if rtl else "Setting",
             t["how_col"] if rtl else "What it does"],
            [
                [f"<strong>{t['set_dark_lbl']}</strong>",  t["set_dark_what"]],
                [f"<strong>{t['set_lang_lbl']}</strong>",  t["set_lang_what"]],
                [f"<strong>{t['set_popup_lbl']}</strong>", t["set_popup_what"]],
                [f"<strong>{t['set_auto_lbl']}</strong>",  t["set_auto_what"]],
            ],
            rtl=rtl,
        )
    callout("⚠", t["tip_save"], "warn", rtl=rtl)

    # ── Section 5: Quick reference ────────────────────────────────────────────
    sec_header("5", t["sec_quickref"], t["sec_quickref"], rtl=rtl)
    guide_table(
        [t["action_col"], t["how_col"]],
        [list(t[k]) for k in ["eqr1","eqr2","eqr3","eqr4","eqr5","eqr6","eqr7"]],
        rtl=rtl,
    )

    doc_footer(t["footer_ext"], rtl=rtl)


# ──────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ──────────────────────────────────────────────────────────────────────────────

def render_user_guide():
    """Render the PromptScanner user guide. Call this from app.py."""

    st.markdown(CSS, unsafe_allow_html=True)

    # ── Determine active tab early (needed for header) ────────────────────────
    active_tab = st.query_params.get("tab", "website")

    # ── Language toggle - beige pill matching app.py style, top-right ─────────
    lang_state = st.session_state.get("guide_lang", "en")

    # Render EN/AR toggle as a small button in top-right corner
    # We use a single-column float trick: empty left col + button right col
    st.markdown('<div class="top-bar">', unsafe_allow_html=True)
    
    _, lang_col = st.columns([11, 1])
    with lang_col:
        current_label = "AR" if lang_state == "en" else "EN"
        if st.button(current_label, key="guide_lang_toggle", use_container_width=True):
            st.session_state.guide_lang = "ar" if lang_state == "en" else "en"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    lang_state = st.session_state.get("guide_lang", "en")
    rtl = lang_state == "ar"
    t   = T["ar"] if rtl else T["en"]

    # ── Navy header with logo, name, title and tab buttons ────────────────────
    guide_header(t, active_tab, rtl=rtl)

    # ── Render active tab ─────────────────────────────────────────────────────
    if active_tab == "website":
        render_website_guide(t, rtl=rtl)
    else:
        render_extension_guide(t, rtl=rtl)


# ── Standalone run ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(
        page_title="PromptScanner – User Guide",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    render_user_guide()
