import streamlit as st
from pathlib import Path
import base64

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
GUIDE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
* { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 900px; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
:root {
    --bg: #EAE4D9; --card: #F3EDE3; --white: #FDFAF5;
    --navy: #0F1C35; --ink: #1A1714; --muted: #7A7068;
    --border: rgba(0,0,0,0.08);
}
html, body, [class*="css"] { background: var(--bg) !important; color: var(--ink) !important; }
.stApp,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],
[data-testid="stHeader"],[data-testid="stBottomBlockContainer"],.main .block-container {
    background: var(--bg) !important; color: var(--ink) !important;
}
.guide-hero { background: var(--navy); color: #EAE4D9; border-radius: 16px; padding: 32px 36px; margin-bottom: 1.5rem; }
.guide-hero-logo { font-weight: 800; font-size: 1.9rem; letter-spacing: -1px; color: #EAE4D9; }
.guide-hero-logo span { color: #E8520A; }
.guide-hero-sub { font-family: 'JetBrains Mono', monospace !important; font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(234,228,217,0.5); margin-top: 3px; }
.guide-hero-title { font-size: 1.4rem; font-weight: 300; color: rgba(234,228,217,0.85); margin-top: 18px; margin-bottom: 8px; }
.guide-hero-desc { font-size: 0.9rem; color: rgba(234,228,217,0.6); line-height: 1.7; max-width: 560px; }
.guide-rule { height: 3px; background: linear-gradient(90deg, #E8520A, transparent 60%); margin-top: 20px; border-radius: 2px; }
.sec-head { display: flex; align-items: center; gap: 12px; margin: 36px 0 18px; padding-bottom: 12px; border-bottom: 2px solid var(--navy); }
.sec-num { background: var(--navy); color: #EAE4D9; font-weight: 800; font-size: 0.88rem; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-family: 'JetBrains Mono', monospace !important; }
.sec-title { font-size: 1.15rem; font-weight: 700; color: var(--navy); }
.step-wrap { display: flex; gap: 0; margin-bottom: 0; }
.step-num-col { display: flex; flex-direction: column; align-items: center; width: 44px; flex-shrink: 0; }
.step-num { width: 30px; height: 30px; border-radius: 50%; background: var(--navy); color: #EAE4D9; font-weight: 800; font-size: 0.82rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; z-index: 1; font-family: 'JetBrains Mono', monospace !important; }
.step-line { width: 2px; flex: 1; min-height: 16px; background: var(--border); margin-top: 4px; }
.step-body { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; flex: 1; }
.step-label { font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: var(--navy); }
.step-desc { color: var(--muted); font-size: 0.86rem; line-height: 1.65; }
.callout { border-radius: 10px; padding: 12px 16px; margin: 12px 0; font-size: 0.87rem; display: flex; gap: 10px; align-items: flex-start; }
.callout-tip  { background: rgba(45,91,227,0.06); border-right: 3px solid #2D5BE3; }
.callout-warn { background: rgba(232,82,10,0.06);  border-right: 3px solid #E8520A; }
.flow { display: flex; justify-content: center; align-items: center; gap: 0; margin: 16px auto; flex-wrap: wrap; }
.flow-node { background: var(--navy); color: #EAE4D9; border-radius: 8px; padding: 8px 14px; font-size: 0.8rem; font-weight: 600; text-align: center; min-width: 100px; flex-shrink: 0; line-height: 1.4; }
.flow-orange { background: #E8520A !important; }
.flow-teal   { background: #00C9A7 !important; color: #0F1C35 !important; }
.flow-arr    { font-size: 1rem; color: var(--muted); padding: 0 4px; flex-shrink: 0; }
.model-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0; }
.model-card { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; }
.model-name-orange { font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-bottom: 6px; background: #E8520A; color: #fff; }
.model-name-blue   { font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-bottom: 6px; background: #2D5BE3; color: #fff; }
.model-desc { font-size: 0.82rem; color: var(--muted); line-height: 1.5; margin-bottom: 7px; }
.model-cats { display: flex; flex-wrap: wrap; gap: 4px; }
.cat-pill { font-size: 0.67rem; font-weight: 700; padding: 2px 7px; border-radius: 8px; font-family: 'JetBrains Mono', monospace !important; }
.guide-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; margin: 12px 0; }
.guide-table th { background: var(--navy); color: #EAE4D9; padding: 8px 12px; font-size: 0.73rem; letter-spacing: 0.06em; text-transform: uppercase; font-family: 'JetBrains Mono', monospace !important; }
.guide-table td { padding: 8px 12px; border-bottom: 1px solid var(--border); }
.guide-table tr:nth-child(even) td { background: var(--white); }
.pii-tag { display: inline-block; background: rgba(232,82,10,0.10); color: #E8520A; border: 1px solid rgba(232,82,10,0.3); border-radius: 4px; padding: 1px 6px; font-size: 0.68rem; font-family: 'JetBrains Mono', monospace !important; font-weight: 700; }
.badge { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 0.68rem; font-weight: 700; font-family: 'JetBrains Mono', monospace !important; }
.b-safe { background: rgba(0,201,167,0.10); color: #00C9A7; border: 1px solid rgba(0,201,167,0.3); }
.b-warn { background: rgba(232,82,10,0.10); color: #E8520A; border: 1px solid rgba(232,82,10,0.3); }
.b-flag { background: rgba(217,48,37,0.10); color: #D93025; border: 1px solid rgba(217,48,37,0.3); }
.b-crit { background: rgba(107,79,187,0.10); color: #6B4FBB; border: 1px solid rgba(107,79,187,0.3); }
.ann-panel { background: var(--white); border: 1px solid var(--border); border-radius: 12px; padding: 12px 16px; }
.ann-row { display: flex; gap: 10px; align-items: flex-start; padding: 7px 0; border-bottom: 1px solid var(--border); font-size: 0.85rem; line-height: 1.6; }
.ann-row:last-child { border-bottom: none; }
.ann-dot { width: 20px; height: 20px; border-radius: 50%; background: #E8520A; color: #fff; font-weight: 800; font-size: 0.62rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-family: 'JetBrains Mono', monospace !important; }
.hl-h { display:inline-block;border-radius:4px;padding:2px 6px;margin:1px;font-size:.8rem;background:rgba(217,48,37,0.75);color:#fff;font-weight:700; }
.hl-m { display:inline-block;border-radius:4px;padding:2px 6px;margin:1px;font-size:.8rem;background:rgba(217,48,37,0.40);color:#c0392b;font-weight:600; }
.hl-l { display:inline-block;border-radius:4px;padding:2px 6px;margin:1px;font-size:.8rem;background:rgba(217,48,37,0.15);color:#c0392b; }
.hl-s { display:inline-block;border-radius:4px;padding:2px 6px;margin:1px;font-size:.8rem;background:rgba(0,0,0,0.05);color:#aaa; }
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
.ext-tox-cf { font-size: 0.68rem; color: #7A7068; margin: 2px 0 5px; direction: rtl; }
.ext-bar { background: rgba(0,0,0,0.08); border-radius: 3px; height: 5px; overflow: hidden; }
.ext-bar-f { height: 100%; border-radius: 3px; }
.ext-hl { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 3px; padding: 5px 2px; direction: rtl; }
.ext-div { height: 1px; background: rgba(0,0,0,0.08); margin: 6px 12px; }
.ext-btn-navy   { background: #0F1C35; color: #EAE4D9; border-radius: 9px; padding: 8px 10px; text-align: center; font-weight: 700; font-size: 0.76rem; margin: 3px 0; font-family: 'JetBrains Mono', monospace !important; }
.ext-btn-orange { background: #E8520A; color: #fff; border-radius: 9px; padding: 8px 10px; text-align: center; font-weight: 700; font-size: 0.76rem; margin: 3px 0; font-family: 'JetBrains Mono', monospace !important; }
.ext-btn-teal   { background: #00C9A7; color: #0F1C35; border-radius: 9px; padding: 8px 10px; text-align: center; font-weight: 700; font-size: 0.76rem; margin: 3px 0; font-family: 'JetBrains Mono', monospace !important; }
.ext-btn-ghost  { background: transparent; color: #7A7068; border: 1px solid rgba(0,0,0,0.1); border-radius: 9px; padding: 8px 10px; text-align: center; font-size: 0.76rem; margin: 3px 0; }
.ext-set-row { display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid rgba(0,0,0,0.06); }
.ext-set-row:last-child { border-bottom: none; }
.ext-set-lbl { font-weight: 700; font-size: 0.8rem; color: #0F1C35; }
.ext-set-sub { font-size: 0.67rem; color: #7A7068; margin-top: 1px; }
.ext-tog-on  { width: 36px; height: 20px; background: #E8520A; border-radius: 10px; position: relative; flex-shrink: 0; }
.ext-tog-off { width: 36px; height: 20px; background: rgba(0,0,0,0.15); border-radius: 10px; position: relative; flex-shrink: 0; }
.ext-tog-k-on  { width: 14px; height: 14px; background: #fff; border-radius: 50%; position: absolute; top: 3px; left: 19px; }
.ext-tog-k-off { width: 14px; height: 14px; background: #fff; border-radius: 50%; position: absolute; top: 3px; left: 3px; }
.ext-lang { display: flex; gap: 4px; }
.ext-lang-active { padding: 3px 9px; border-radius: 5px; font-size: 0.7rem; font-weight: 700; background: #E8520A; color: #fff; }
.ext-lang-off    { padding: 3px 9px; border-radius: 5px; font-size: 0.7rem; font-weight: 700; background: rgba(0,0,0,0.06); color: #7A7068; }
.guide-footer { background: var(--navy); color: rgba(234,228,217,0.5); text-align: center; padding: 18px; font-size: 0.75rem; border-radius: 12px; margin-top: 3rem; }
.guide-footer span { color: #E8520A; }
div[data-testid="stButton"] button { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; font-size: .82rem !important; border: none !important; border-radius: 10px !important; padding: .5rem 1.4rem !important; transition: all .2s !important; cursor: pointer !important; white-space: nowrap !important; }
div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }
div[data-testid="stButton"] button[kind="primary"]   { background: #E8520A !important; color: #fff !important; }
div[data-testid="stButton"] button[kind="secondary"] { background: var(--card) !important; color: var(--muted) !important; box-shadow: none !important; border: 1px solid var(--border) !important; }
"""

def inject_css():
    st.markdown(f"<style>{GUIDE_CSS}</style>", unsafe_allow_html=True)

def img_b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

# ─────────────────────────────────────────────────────────────
# ALL TEXT STRINGS — Arabic and English
# ─────────────────────────────────────────────────────────────
T = {
"ar": {
    "lang_btn":    "EN",
    "hero_sub":    "حارس خصوصيتك في عالم الذكاء الاصطناعي",
    "hero_title":  "دليل المستخدم",
    "hero_desc":   "تعليمات خطوة بخطوة لاستخدام PromptScanner للكشف عن المعلومات الشخصية والمحتوى الضار في مطالباتك العربية قبل إرسالها إلى روبوتات الدردشة.",
    "tab1":        "الجزء الأول — الموقع الإلكتروني",
    "tab2":        "الجزء الثاني — إضافة المتصفح",
    "dir":         "rtl",
    "align":       "right",
    # website
    "w_s1": "ما هو PromptScanner؟",
    "w_intro": "يحلل <strong>PromptScanner</strong> نصوصك العربية <strong>قبل</strong> إرسالها إلى روبوت الدردشة. يكتشف المعلومات الشخصية الحساسة ويفحص المحتوى الضار في وقت واحد لحماية خصوصيتك.",
    "w_flow": [("اكتب نصك",""), ("اضغط فحص","flow-orange"), ("4 نماذج تعمل معاً","flow-teal"), ("تظهر النتائج","")],
    "w_s2": "النماذج المستخدمة",
    "w_models": [
        ("model-name-orange","AraBERT NER","يكتشف الأسماء والمؤسسات والعناوين والتواريخ باستخدام نموذج لغوي عربي.","rgba(232,82,10,0.1)","#E8520A",["PERS","ORG","ADDRESS","DATETIME"]),
        ("model-name-orange","XLM-RoBERTa","يكتشف أرقام الهوية وبيانات الدخول، بما فيها القيم اللاتينية داخل الجمل العربية.","rgba(232,82,10,0.1)","#E8520A",["ID","CREDENTIAL"]),
        ("model-name-orange","Regex Engine","كشف مبني على أنماط ثابتة للهاتف والبريد الإلكتروني وعناوين IP والروابط والمعلومات المالية.","rgba(232,82,10,0.1)","#E8520A",["PHONE","EMAIL","IP","URL"]),
        ("model-name-blue","AraBERT v2","يصنّف النص إلى 7 فئات أمان مع إبراز الكلمات المؤثرة في قرار التصنيف.","rgba(45,91,227,0.1)","#2D5BE3",["7 فئات","تحليل الكلمات"]),
    ],
    "w_s3": "خطوة بخطوة",
    "w_tip1": "يمكنك النقر على أي <strong>زر مثال</strong> في الشريط الأيسر لتحميل نص تجريبي جاهز.",
    "w_steps": [
        ("أدخل نصك العربي", "انقر في حقل الإدخال واكتب أو الصق النص العربي. يمكنك أيضاً الضغط على أحد أزرار الأمثلة في الشريط الأيسر."),
        ("اضغط فحص", "تعمل جميع النماذج الأربعة في آنٍ واحد. تظهر النتائج خلال 1-2 ثانية. اضغط مسح للبدء من جديد."),
        ("اقرأ نتيجة المعلومات الشخصية", "تُظهر إما «آمن» إذا لم تُكتشف معلومات شخصية، أو النص المُقنَّع مع بطاقات ملونة تُعدّد كل كيان ونوعه والنموذج الذي اكتشفه."),
        ("اقرأ نتيجة تحليل السمية", "تُظهر الفئة المتوقعة ودرجة الثقة وتفصيل كامل للفئات السبع مع شارة تُشير إلى مستوى الخطورة."),
        ("اقرأ خريطة الكلمات المؤثرة", "كل كلمة مُلوَّنة بحسب مدى تأثيرها في قرار التصنيف. اللون الداكن يعني تأثيراً أعلى."),
        ("استخدم إعادة الصياغة", "عند اكتشاف محتوى ضار يظهر قسم إعادة الصياغة. يعرض نسخة آمنة بديلة مع الحفاظ على المعنى الأصلي."),
    ],
    "w_tip2": "استخدم دائماً <strong>النص المُقنَّع</strong> بدلاً من النص الأصلي — روبوت الدردشة سيفهم طلبك دون استقبال بياناتك الشخصية.",
    "w_s4": "أنواع المعلومات الشخصية",
    "w_pii_headers": ["البطاقة","النوع","مثال","يكتشفه"],
    "w_pii_rows": [
        ("[PERS]","اسم شخص","أحمد المقبالي","AraBERT NER"),
        ("[ORG]","مؤسسة","بنك مسقط","AraBERT NER"),
        ("[ADDRESS]","موقع / عنوان","مسقط، عُمان","AraBERT NER"),
        ("[DATETIME]","تاريخ / وقت","الثلاثاء 5 مارس","AraBERT NER"),
        ("[ID]","رقم هوية / جواز","12345678","XLM-RoBERTa"),
        ("[CREDENTIAL]","كلمة مرور / PIN","MyPass123!","XLM-RoBERTa"),
        ("[PHONE]","رقم هاتف","+968 91234567","Regex"),
        ("[EMAIL]","بريد إلكتروني","ahmed@squ.edu.om","Regex"),
        ("[IP]","عنوان IP","192.168.1.1","Regex"),
        ("[URL]","رابط إنترنت","https://example.com","Regex"),
        ("[FINANCIAL_INFO]","رقم بطاقة / IBAN","OM21BMI…","Regex"),
    ],
    "w_s5": "فئات تحليل السمية",
    "w_tox_headers": ["الفئة","الشارة","المعنى"],
    "w_tox_rows": [
        ("عادي","<span class='badge b-safe'>آمن</span>","لا يوجد محتوى ضار"),
        ("مسيء بشكل خفيف","<span class='badge b-warn'>تحذير</span>","محتوى مسيء خفيف"),
        ("مسيء","<span class='badge b-warn'>تحذير</span>","محتوى مسيء واضح"),
        ("انتهاك الخصوصية","<span class='badge b-warn'>تحذير</span>","يتضمن طلباً ينتهك الخصوصية"),
        ("محتوى فاضح","<span class='badge b-flag'>مُبلَّغ</span>","محتوى غير لائق"),
        ("خطير","<span class='badge b-flag'>مُبلَّغ</span>","محتوى خطير يستدعي التنبيه"),
        ("محتوى نفسي","<span class='badge b-crit'>خطر</span>","يتضمن مؤشرات تستدعي العناية"),
    ],
    "w_s6": "مرجع سريع",
    "w_qr_headers": ["الإجراء","الطريقة"],
    "w_qr_rows": [
        ("فحص نص","اكتب أو الصق النص ← اضغط فحص"),
        ("مسح حقل الإدخال","اضغط مسح (يظهر بعد الفحص)"),
        ("تجربة مثال جاهز","انقر أحد أزرار الأمثلة في الشريط الأيسر"),
        ("التبديل بين الوضع الليلي/النهاري","انقر 🌙 في أعلى يمين الصفحة"),
        ("تغيير لغة الواجهة","انقر EN / عربي في أعلى يمين الصفحة"),
        ("معرفة النموذج الذي اكتشف الكيان","تحقق من التسمية الصغيرة (RGX / NER / XLM) على كل بطاقة"),
        ("الحصول على إعادة صياغة آمنة","اضغط «إعادة الصياغة» في قسم النتائج"),
    ],
    "w_footer": "دليل المستخدم · الجزء الأول: الموقع الإلكتروني",
    # extension
    "e_s1": "ما الذي تفعله الإضافة؟",
    "e_intro": "تضيف إضافة <strong>PromptScanner</strong> طبقةً أمنية مباشرةً داخل مواقع روبوتات الدردشة مثل <strong>ChatGPT</strong> و<strong>Gemini</strong>. عند الضغط على إرسال أو Enter، تعترض الإضافة النص وتفحصه وتعرض النتائج في نافذة منبثقة <strong>قبل</strong> وصول أي شيء إلى الذكاء الاصطناعي.",
    "e_flow": [("اكتب في ChatGPT / Gemini",""), ("اضغط إرسال / Enter","flow-orange"), ("الإضافة تفحص النص","flow-teal"), ("أنت تقرر","")],
    "e_s2": "تثبيت الإضافة",
    "e_steps_install": [
        ("افتح متجر Chrome الإلكتروني", "اذهب إلى <strong>chromewebstore.google.com</strong> وابحث عن PromptScanner، أو استخدم الرابط المباشر الموجود على موقعنا."),
        ("انقر «إضافة إلى Chrome»", "اضغط على زر «Add to Chrome» ثم أكّد التثبيت عند ظهور نافذة التأكيد."),
        ("ثبّت الإضافة في شريط الأدوات", "انقر على أيقونة قطعة الأحجية 🧩 في أعلى يمين المتصفح، ابحث عن PromptScanner، ثم انقر أيقونة الدبوس 📌 لإبقائها ظاهرة دائماً."),
        ("ابدأ الاستخدام", "ادخل إلى ChatGPT أو Gemini، اكتب مطالبتك، واضغط إرسال — ستظهر نافذة PromptScanner تلقائياً."),
    ],
    "e_tip_install": "تأكد من أن الإضافة تظهر في شريط الأدوات قبل البدء. يمكنك التحقق بالنقر على أيقونة PromptScanner مباشرةً.",
    "e_s3": "حالات النافذة المنبثقة",
    "e_states_intro": "عند الضغط على إرسال تظهر نافذة PromptScanner بإحدى الحالات الأربع التالية حسب نتيجة الفحص:",
    "e_state_a": "الحالة أ — محتوى آمن ✓",
    "e_state_b": "الحالة ب — تم اكتشاف معلومات شخصية",
    "e_state_c": "الحالة ج — تم اكتشاف محتوى ضار",
    "e_state_d": "الحالة د — بعد إعادة الصياغة",
    "e_ann_a": [
        ("1","النص المُقنَّع يؤكد عدم وجود معلومات شخصية."),
        ("2","التصنيف الأخضر «عادي» بثقة عالية — المحتوى آمن تماماً."),
        ("3","<strong>⟶ إرسال</strong> — يرسل المطالبة كما هي. نقرة واحدة وتنتهي."),
    ],
    "e_ann_b": [
        ("1","النص المُقنَّع يعرض المطالبة مع استبدال البيانات الشخصية بعلامات مثل <span class='pii-tag'>[PERS]</span>."),
        ("2","<strong>⟶ إرسال الأمر بدون معلومات خاصة</strong> — يُرسل النسخة الآمنة دون بياناتك الشخصية."),
        ("3","<strong>⟶ إرسال الأصلي</strong> — يُرسل النص كما كتبته. القرار لك دائماً."),
    ],
    "e_ann_c": [
        ("1","قسم «الكلمات المؤثرة» يُظهر الكلمات التي أثّرت في قرار التصنيف بألوان متدرجة."),
        ("2","<strong>إعادة الصياغة</strong> — يُولِّد نسخة آمنة تحافظ على المعنى الأصلي قدر الإمكان."),
        ("3","<strong>⟶ إرسال الأصلي</strong> — إرسال النص رغم التحذير. القرار النهائي لك."),
    ],
    "e_ann_d": [
        ("1","قسم «النص المُعاد كتابته» بحد أخضر يعرض البديل الآمن."),
        ("2","<strong>⟶ إرسال المُعاد كتابته</strong> — يُرسل النسخة الآمنة مباشرةً."),
        ("3","<strong>⟶ إرسال الأصلي</strong> — يُرسل النص الأصلي رغم التحذير."),
        ("4","<strong>✕ إلغاء</strong> — يغلق النافذة دون إرسال لتتمكن من التعديل يدوياً."),
    ],
    "e_s4": "الإعدادات",
    "e_settings_intro": "انقر أيقونة ⚙ في رأس النافذة المنبثقة للوصول إلى الإعدادات.",
    "e_settings_headers": ["الإعداد","الوظيفة"],
    "e_settings_rows": [
        ("الوضع الداكن","يُبدِّل النافذة إلى سمة ألوان داكنة."),
        ("اللغة","اختر العربية أو الإنجليزية لجميع نصوص الإضافة."),
        ("عرض النافذة للمحتوى الآمن","مفعَّل: تظهر حتى للمطالبات الآمنة. معطَّل: تُرسَل تلقائياً دون توقف."),
        ("الفحص التلقائي","مفعَّل: يبدأ تلقائياً عند ضغط إرسال أو Enter. معطَّل: لا فحص تلقائي."),
    ],
    "e_tip_save": "اضغط دائماً <strong>حفظ الإعدادات</strong> بعد أي تغيير. لن تُطبَّق التغييرات حتى يتم الحفظ.",
    "e_s5": "المواقع المدعومة",
    "e_sites_headers": ["الموقع","الرابط"],
    "e_sites_rows": [("ChatGPT","chatgpt.com"),("Gemini","gemini.google.com"),("Claude","claude.ai"),("Microsoft Copilot","copilot.microsoft.com"),("Perplexity","perplexity.ai")],
    "e_s6": "مرجع سريع",
    "e_qr_headers": ["الإجراء","الطريقة"],
    "e_qr_rows": [
        ("تشغيل الفحص","اضغط إرسال أو Enter في ChatGPT / Gemini"),
        ("إرسال المطالبة الأصلية","اضغط ⟶ إرسال الأصلي"),
        ("إرسال النص بدون معلومات خاصة","اضغط ⟶ إرسال الأمر بدون معلومات خاصة"),
        ("إرسال النسخة المُعادة صياغتها","اضغط إعادة الصياغة ثم ⟶ إرسال المُعاد كتابته"),
        ("الإلغاء دون إرسال","اضغط ✕ إلغاء"),
        ("فتح الإعدادات","انقر ⚙ في رأس النافذة المنبثقة"),
        ("تخطي النافذة للمحتوى الآمن","عطِّل «عرض النافذة للمحتوى الآمن»"),
        ("تعطيل الفحص التلقائي","عطِّل «الفحص التلقائي»"),
    ],
    "e_footer": "دليل المستخدم · الجزء الثاني: إضافة المتصفح · ChatGPT & Gemini",
    # popup strings
    "p_tagline":    "فحص الخصوصية والسلامة",
    "p_elapsed_a":  "تم الفحص في 0.18s",
    "p_elapsed_b":  "تم الفحص في 0.31s",
    "p_elapsed_c":  "تم الفحص في 0.28s",
    "p_masked_lbl": "◆ النص بدون معلومات خاصة",
    "p_tox_lbl":    "◆ تحليل السمية",
    "p_kw_lbl":     "◆ الكلمات المؤثرة",
    "p_rw_lbl":     "◆ النص المُعاد كتابته",
    "p_no_pii":     "✓ لا توجد معلومات شخصية",
    "p_normal":     "عادي",
    "p_danger":     "خطير",
    "p_conf_a":     "درجة الثقة: 98.2%",
    "p_conf_b":     "درجة الثقة: 99.1%",
    "p_conf_c":     "درجة الثقة: 99.4%",
    "p_badge_safe": "<span class='badge b-safe'>آمن</span>",
    "p_badge_flag": "<span class='badge b-flag'>مُبلَّغ</span>",
    "p_btn_send":   "⟶ إرسال",
    "p_btn_masked": "⟶ إرسال الأمر بدون معلومات خاصة",
    "p_btn_orig":   "⟶ إرسال الأصلي",
    "p_btn_rewrite":"إعادة الصياغة",
    "p_btn_rw_send":"⟶ إرسال المُعاد كتابته",
    "p_btn_cancel": "✕ إلغاء",
    "p_rw_text":    "كيف تعمل المواد المتفجرة من الناحية الكيميائية؟",
    "p_pii_text":   'اسمي <span class="pii-tag">[PERS]</span> وأعمل في <span class="pii-tag">[ORG]</span> ورقمي <span class="pii-tag">[PHONE]</span>',
    "p_tox_text":   "كيف أصنع قنبلة لتدمير مبنى",
    "p_set_dark_lbl": "الوضع الداكن",
    "p_set_dark_sub": "تفعيل المظهر الداكن",
    "p_set_lang_lbl": "اللغة",
    "p_set_lang_sub": "لغة واجهة الإضافة",
    "p_set_safe_lbl": "عرض النافذة للمحتوى الآمن",
    "p_set_safe_sub": "إذا كان آمناً اعرض النافذة، وإلا أرسل تلقائياً",
    "p_set_auto_lbl": "الفحص التلقائي",
    "p_set_auto_sub": "فحص المحتوى عند ضغط إرسال أو Enter",
    "p_set_save":     "✓ حفظ الإعدادات",
    "p_set_appear":   "◆ المظهر",
    "p_set_behav":    "◆ السلوك",
    "p_lang_active":  "العربية",
    "p_lang_off":     "English",
},
"en": {
    "lang_btn":    "عربي",
    "hero_sub":    "Your Privacy Guardian in the AI World",
    "hero_title":  "User Guide",
    "hero_desc":   "Step-by-step instructions for using PromptScanner to detect personal information and harmful content in your Arabic prompts before sending them to AI chatbots.",
    "tab1":        "Part 1 — Website",
    "tab2":        "Part 2 — Browser Extension",
    "dir":         "ltr",
    "align":       "left",
    # website
    "w_s1": "What is PromptScanner?",
    "w_intro": "<strong>PromptScanner</strong> analyses your Arabic prompts <strong>before</strong> you send them to an AI chatbot. It detects sensitive personal information and harmful content simultaneously, protecting your privacy.",
    "w_flow": [("Type your prompt",""), ("Press Scan","flow-orange"), ("4 models run together","flow-teal"), ("Results appear","")],
    "w_s2": "Models Used",
    "w_models": [
        ("model-name-orange","AraBERT NER","Detects names, organisations, addresses and dates using a fine-tuned Arabic language model.","rgba(232,82,10,0.1)","#E8520A",["PERS","ORG","ADDRESS","DATETIME"]),
        ("model-name-orange","XLM-RoBERTa","Detects IDs and credentials, including Latin values inside Arabic sentences.","rgba(232,82,10,0.1)","#E8520A",["ID","CREDENTIAL"]),
        ("model-name-orange","Regex Engine","Pattern-based detection for phone, email, IP, URL and financial information.","rgba(232,82,10,0.1)","#E8520A",["PHONE","EMAIL","IP","URL"]),
        ("model-name-blue","AraBERT v2","Classifies text into 7 safety categories with keyword attention highlighting.","rgba(45,91,227,0.1)","#2D5BE3",["7 categories","keyword map"]),
    ],
    "w_s3": "Step by Step",
    "w_tip1": "Click any <strong>example button</strong> in the left sidebar to load a pre-written test prompt.",
    "w_steps": [
        ("Enter your Arabic prompt", "Click the text box and type or paste Arabic text. You can also click any example button in the left sidebar."),
        ("Press Scan", "All four models run simultaneously. Results appear in 1-2 seconds. Press Clear to start over."),
        ("Read the PII result (left card)", "Shows Clean if no PII found, or the masked text with coloured pills listing each detected entity, its type and which model found it."),
        ("Read the toxicity result (right card)", "Shows the predicted category, confidence score and a full breakdown of all 7 categories with a severity badge."),
        ("Read the keyword attention map", "Each word is colour-coded by how much it influenced the classification. Darker = more influential."),
        ("Use Rewrite (when needed)", "When harmful content is detected the rewrite panel appears. It shows a safe alternative preserving the original meaning."),
    ],
    "w_tip2": "Always use the <strong>masked text</strong> instead of the original — the chatbot will still understand your request without receiving your personal data.",
    "w_s4": "PII Types Detected",
    "w_pii_headers": ["Tag","Entity Type","Example","Detected By"],
    "w_pii_rows": [
        ("[PERS]","Person name","Ahmed Al-Maqbali","AraBERT NER"),
        ("[ORG]","Organisation","Bank Muscat","AraBERT NER"),
        ("[ADDRESS]","Location / address","Muscat, Oman","AraBERT NER"),
        ("[DATETIME]","Date / time","Tuesday 5 March","AraBERT NER"),
        ("[ID]","National ID / passport","12345678","XLM-RoBERTa"),
        ("[CREDENTIAL]","Password / PIN","MyPass123!","XLM-RoBERTa"),
        ("[PHONE]","Phone number","+968 91234567","Regex"),
        ("[EMAIL]","Email address","ahmed@squ.edu.om","Regex"),
        ("[IP]","IP address","192.168.1.1","Regex"),
        ("[URL]","Web URL","https://example.com","Regex"),
        ("[FINANCIAL_INFO]","Card number / IBAN","OM21BMI…","Regex"),
    ],
    "w_s5": "Toxicity Categories",
    "w_tox_headers": ["Category","Badge","Meaning"],
    "w_tox_rows": [
        ("Normal","<span class='badge b-safe'>Safe</span>","No harmful content"),
        ("Mild Offense","<span class='badge b-warn'>Warning</span>","Mildly harmful"),
        ("Offensive","<span class='badge b-warn'>Warning</span>","Clearly offensive"),
        ("Privacy Violation","<span class='badge b-warn'>Warning</span>","Privacy-invasive request"),
        ("Obscene","<span class='badge b-flag'>Flagged</span>","Inappropriate content"),
        ("Dangerous","<span class='badge b-flag'>Flagged</span>","Dangerous content"),
        ("Mental Health","<span class='badge b-crit'>Critical</span>","Requires care"),
    ],
    "w_s6": "Quick Reference",
    "w_qr_headers": ["Action","How"],
    "w_qr_rows": [
        ("Scan a prompt","Type or paste text → press Scan"),
        ("Clear the input","Press Clear (appears after scan)"),
        ("Try a pre-written example","Click any example button in the left sidebar"),
        ("Toggle dark / light mode","Click 🌙 at top right of page"),
        ("Switch interface language","Click EN / عربي at top right"),
        ("See which model found a PII","Check the small label (RGX / NER / XLM) on each pill"),
        ("Get a safe rewrite","Press Rewrite in the results panel"),
    ],
    "w_footer": "User Guide · Part 1: Website",
    # extension
    "e_s1": "What Does the Extension Do?",
    "e_intro": "The <strong>PromptScanner</strong> extension adds a safety layer directly inside AI chatbot websites like <strong>ChatGPT</strong> and <strong>Gemini</strong>. When you press Send or Enter, it intercepts your prompt, scans it, and shows results in a popup <strong>before</strong> anything reaches the AI.",
    "e_flow": [("Type in ChatGPT / Gemini",""), ("Press Send / Enter","flow-orange"), ("Extension scans the text","flow-teal"), ("You decide","")],
    "e_s2": "Installation",
    "e_steps_install": [
        ("Open the Chrome Web Store", "Go to <strong>chromewebstore.google.com</strong> and search for PromptScanner, or use the direct link on our website."),
        ("Click 'Add to Chrome'", "Press the 'Add to Chrome' button and confirm when the confirmation dialog appears."),
        ("Pin the extension to the toolbar", "Click the puzzle-piece icon 🧩 at the top right of Chrome, find PromptScanner, then click the pin icon 📌 to keep it always visible."),
        ("Start using PromptScanner", "Go to ChatGPT or Gemini, type your prompt, and press Send — the PromptScanner popup will appear automatically."),
    ],
    "e_tip_install": "Make sure the extension is visible in the toolbar before you start. You can check by clicking the PromptScanner icon directly.",
    "e_s3": "Popup States",
    "e_states_intro": "When you press Send, the PromptScanner popup appears in one of four states depending on the scan result:",
    "e_state_a": "State A — Safe content ✓",
    "e_state_b": "State B — Personal information detected",
    "e_state_c": "State C — Harmful content detected",
    "e_state_d": "State D — After rewrite",
    "e_ann_a": [
        ("1","The masked text confirms no personal information was found."),
        ("2","Green Normal label at high confidence — content is completely safe."),
        ("3","<strong>⟶ Send</strong> — sends the prompt as-is. One click and done."),
    ],
    "e_ann_b": [
        ("1","The masked text shows the prompt with personal data replaced by tags like <span class='pii-tag'>[PERS]</span>."),
        ("2","<strong>⟶ Send Masked</strong> — sends the safe version without your personal data."),
        ("3","<strong>⟶ Send Original</strong> — sends the text as you typed it. The choice is always yours."),
    ],
    "e_ann_c": [
        ("1","The Key Attention Words section shows colour-coded words that drove the classification."),
        ("2","<strong>Rewrite</strong> — generates a safe alternative preserving the original meaning."),
        ("3","<strong>⟶ Send Original</strong> — sends despite the warning. The final decision is yours."),
    ],
    "e_ann_d": [
        ("1","The Rewritten Prompt section with a green border shows the safe alternative."),
        ("2","<strong>⟶ Send Rewritten</strong> — sends the safe version directly."),
        ("3","<strong>⟶ Send Original</strong> — sends the original text despite the warning."),
        ("4","<strong>✕ Cancel</strong> — closes the popup without sending so you can edit manually."),
    ],
    "e_s4": "Settings",
    "e_settings_intro": "Click the ⚙ icon in the popup header to open settings.",
    "e_settings_headers": ["Setting","What it does"],
    "e_settings_rows": [
        ("Dark Mode","Switches the popup to a dark colour scheme."),
        ("Language","Choose Arabic or English for all popup labels."),
        ("Show popup for safe content","ON: popup appears even for safe prompts. OFF: safe prompts send automatically."),
        ("Auto Scan","ON: scans automatically when Send/Enter is pressed. OFF: no automatic scanning."),
    ],
    "e_tip_save": "Always press <strong>Save Settings</strong> after making changes. Changes are not applied until saved.",
    "e_s5": "Supported Sites",
    "e_sites_headers": ["Site","URL"],
    "e_sites_rows": [("ChatGPT","chatgpt.com"),("Gemini","gemini.google.com"),("Claude","claude.ai"),("Microsoft Copilot","copilot.microsoft.com"),("Perplexity","perplexity.ai")],
    "e_s6": "Quick Reference",
    "e_qr_headers": ["Action","How"],
    "e_qr_rows": [
        ("Trigger a scan","Press Send or Enter in ChatGPT / Gemini"),
        ("Send original prompt","Press ⟶ Send Original"),
        ("Send without personal data","Press ⟶ Send Masked"),
        ("Send rewritten version","Press Rewrite then ⟶ Send Rewritten"),
        ("Cancel without sending","Press ✕ Cancel"),
        ("Open settings","Click ⚙ in the popup header"),
        ("Skip popup for safe prompts","Turn OFF Show popup for safe content"),
        ("Disable auto-scanning","Turn OFF Auto Scan"),
    ],
    "e_footer": "User Guide · Part 2: Browser Extension · ChatGPT & Gemini",
    # popup strings
    "p_tagline":    "Privacy & Safety Scanner",
    "p_elapsed_a":  "Scanned in 0.18s",
    "p_elapsed_b":  "Scanned in 0.31s",
    "p_elapsed_c":  "Scanned in 0.28s",
    "p_masked_lbl": "◆ Masked Text",
    "p_tox_lbl":    "◆ Toxicity Analysis",
    "p_kw_lbl":     "◆ Key Attention Words",
    "p_rw_lbl":     "◆ Rewritten Prompt",
    "p_no_pii":     "✓ No personal information found",
    "p_normal":     "Normal",
    "p_danger":     "Dangerous",
    "p_conf_a":     "Confidence: 98.2%",
    "p_conf_b":     "Confidence: 99.1%",
    "p_conf_c":     "Confidence: 99.4%",
    "p_badge_safe": "<span class='badge b-safe'>Safe</span>",
    "p_badge_flag": "<span class='badge b-flag'>Flagged</span>",
    "p_btn_send":   "⟶ Send",
    "p_btn_masked": "⟶ Send Masked",
    "p_btn_orig":   "⟶ Send Original",
    "p_btn_rewrite":"Rewrite",
    "p_btn_rw_send":"⟶ Send Rewritten",
    "p_btn_cancel": "✕ Cancel",
    "p_rw_text":    "How do explosive materials work from a chemistry perspective?",
    "p_pii_text":   'My name is <span class="pii-tag">[PERS]</span> and I work at <span class="pii-tag">[ORG]</span>, my number is <span class="pii-tag">[PHONE]</span>',
    "p_tox_text":   "How do I make a bomb to destroy a building",
    "p_set_dark_lbl": "Dark Mode",
    "p_set_dark_sub": "Enable dark theme",
    "p_set_lang_lbl": "Language",
    "p_set_lang_sub": "Extension UI language",
    "p_set_safe_lbl": "Show popup for safe content",
    "p_set_safe_sub": "If safe, show popup. Otherwise send automatically",
    "p_set_auto_lbl": "Auto Scan",
    "p_set_auto_sub": "Scan content when Send or Enter is pressed",
    "p_set_save":     "✓ Save Settings",
    "p_set_appear":   "◆ Appearance",
    "p_set_behav":    "◆ Behavior",
    "p_lang_active":  "العربية",
    "p_lang_off":     "English",
},
}

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def get_lang():
    return st.session_state.get("guide_lang", "ar")

def d(lang):
    return "rtl" if lang == "ar" else "ltr"

def a(lang):
    return "right" if lang == "ar" else "left"

def hero(logo_b64, lang):
    L = T[lang]
    st.markdown(f"""
<div class="guide-hero" style="direction:{d(lang)};text-align:{a(lang)};">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
    <img src="data:image/png;base64,{logo_b64}" style="width:46px;height:46px;border-radius:10px;object-fit:contain;" />
    <div>
      <div class="guide-hero-logo">Prompt<span>Scanner</span></div>
      <div class="guide-hero-sub">{L["hero_sub"]}</div>
    </div>
  </div>
  <div class="guide-hero-title">{L["hero_title"]}</div>
  <p class="guide-hero-desc">{L["hero_desc"]}</p>
  <div class="guide-rule"></div>
</div>""", unsafe_allow_html=True)

def sec(num, title, lang):
    flex = "row-reverse" if lang == "ar" else "row"
    st.markdown(f"""
<div class="sec-head" style="direction:{d(lang)};flex-direction:{flex};">
  <div class="sec-num">{num}</div>
  <div class="sec-title">{title}</div>
</div>""", unsafe_allow_html=True)

def step_item(num, label, desc, lang, last=False):
    line = "" if last else '<div class="step-line"></div>'
    if lang == "ar":
        html = f"""
<div style="display:flex;flex-direction:row;gap:0;margin-bottom:0;direction:rtl;">
  <div style="display:flex;flex-direction:column;align-items:center;width:44px;flex-shrink:0;">
    <div class="step-num">{num}</div>
    {line}
  </div>
  <div class="step-body" style="text-align:right;margin-right:10px;margin-left:0;">
    <div class="step-label">{label}</div>
    <div class="step-desc">{desc}</div>
  </div>
</div>"""
    else:
        html = f"""
<div style="display:flex;flex-direction:row;gap:0;margin-bottom:0;direction:ltr;">
  <div style="display:flex;flex-direction:column;align-items:center;width:44px;flex-shrink:0;">
    <div class="step-num">{num}</div>
    {line}
  </div>
  <div class="step-body" style="text-align:left;margin-left:10px;margin-right:0;">
    <div class="step-label">{label}</div>
    <div class="step-desc">{desc}</div>
  </div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)

def tip(text, lang, warn=False):
    kind = "warn" if warn else "tip"
    icon = "⚠" if warn else "💡"
    st.markdown(
        f'<div class="callout callout-{kind}" style="direction:{d(lang)};text-align:{a(lang)};">'
        f'<span style="font-size:1rem;flex-shrink:0;">{icon}</span><div>{text}</div></div>',
        unsafe_allow_html=True)

def flow_diagram(nodes, lang):
    if lang == "ar":
        nodes_display = list(reversed(nodes))
        arr = "←"
    else:
        nodes_display = nodes
        arr = "→"
    parts = []
    for i, (label, cls) in enumerate(nodes_display):
        parts.append(f'<div class="flow-node {cls}">{label}</div>')
        if i < len(nodes_display) - 1:
            parts.append(f'<div class="flow-arr">{arr}</div>')
    st.markdown(f'<div class="flow">{"".join(parts)}</div>', unsafe_allow_html=True)

def guide_table(headers, rows, lang):
    th = "".join(f'<th style="text-align:{a(lang)};">{h}</th>' for h in headers)
    tbody = ""
    for row in rows:
        cells = "".join(f'<td style="text-align:{a(lang)};">{c}</td>' for c in row)
        tbody += f"<tr>{cells}</tr>"
    st.markdown(
        f'<table class="guide-table" style="direction:{d(lang)};">'
        f'<thead><tr>{th}</tr></thead><tbody>{tbody}</tbody></table>',
        unsafe_allow_html=True)

def pii_table(headers, rows, lang):
    th = "".join(f'<th style="text-align:{a(lang)};">{h}</th>' for h in headers)
    tbody = ""
    for tag, *rest in rows:
        first = f'<td style="text-align:{a(lang)};"><span class="pii-tag">{tag}</span></td>'
        others = "".join(f'<td style="text-align:{a(lang)};">{c}</td>' for c in rest)
        tbody += f"<tr>{first}{others}</tr>"
    st.markdown(
        f'<table class="guide-table" style="direction:{d(lang)};">'
        f'<thead><tr>{th}</tr></thead><tbody>{tbody}</tbody></table>',
        unsafe_allow_html=True)

def ann_panel(items, lang):
    rows = "".join(
        f'<div class="ann-row" style="direction:{d(lang)};text-align:{a(lang)};">'
        f'<div class="ann-dot" style="flex-shrink:0;">{lbl}</div><div>{txt}</div></div>'
        for lbl, txt in items)
    st.markdown(f'<div class="ann-panel">{rows}</div>', unsafe_allow_html=True)

def popup_with_ann(popup_html, items, lang):
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown(popup_html, unsafe_allow_html=True)
    with c2:
        ann_panel(items, lang)

# ─────────────────────────────────────────────────────────────
# POPUP MOCKUPS
# ─────────────────────────────────────────────────────────────
def popup_header(logo_b64, L, gear_active=False):
    gear_style = "background:#E8520A;color:#fff;" if gear_active else ""
    return f"""
  <div class="ext-hdr">
    <div style="display:flex;align-items:center;gap:8px;">
      <img src="data:image/png;base64,{logo_b64}" style="width:24px;height:24px;border-radius:6px;object-fit:contain;" />
      <div>
        <div class="ext-logo-txt">Prompt<span>Scanner</span></div>
        <div class="ext-logo-sub">{L["p_tagline"]}</div>
      </div>
    </div>
    <div class="ext-gear" style="{gear_style}">{'✕' if gear_active else '⚙'}</div>
  </div>"""

def popup_safe(logo_b64, L):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64, L)}
  <div class="ext-elapsed">{L["p_elapsed_a"]}</div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_masked_lbl"]}</div>
    <div class="ext-tbox" style="color:#00C9A7;text-align:center;padding-top:10px;">{L["p_no_pii"]}</div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_tox_lbl"]}</div>
    <div class="ext-tox-card" style="border-right:3px solid #00C9A7;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;">
        <div class="ext-tox-name" style="color:#00C9A7;">{L["p_normal"]}</div>
        {L["p_badge_safe"]}
      </div>
      <div class="ext-tox-cf">{L["p_conf_a"]}</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#00C9A7;width:98%;"></div></div>
    </div>
  </div>
  <div class="ext-div"></div>
  <div style="padding:6px 12px 10px;">
    <div class="ext-btn-orange">{L["p_btn_send"]}</div>
    <div class="ext-btn-ghost" style="margin-top:4px;">{L["p_btn_cancel"]}</div>
  </div>
</div>"""

def popup_pii(logo_b64, L):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64, L)}
  <div class="ext-elapsed">{L["p_elapsed_b"]}</div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_masked_lbl"]}</div>
    <div class="ext-tbox">{L["p_pii_text"]}</div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_tox_lbl"]}</div>
    <div class="ext-tox-card" style="border-right:3px solid #00C9A7;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;">
        <div class="ext-tox-name" style="color:#00C9A7;">{L["p_normal"]}</div>
        {L["p_badge_safe"]}
      </div>
      <div class="ext-tox-cf">{L["p_conf_b"]}</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#00C9A7;width:99%;"></div></div>
    </div>
  </div>
  <div class="ext-div"></div>
  <div style="padding:6px 12px 10px;">
    <div class="ext-btn-teal">{L["p_btn_masked"]}</div>
    <div class="ext-btn-orange" style="margin-top:4px;">{L["p_btn_orig"]}</div>
    <div class="ext-btn-ghost" style="margin-top:4px;">{L["p_btn_cancel"]}</div>
  </div>
</div>"""

def popup_toxic(logo_b64, L):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64, L)}
  <div class="ext-elapsed">{L["p_elapsed_c"]}</div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_masked_lbl"]}</div>
    <div class="ext-tbox">{L["p_tox_text"]}</div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_tox_lbl"]}</div>
    <div class="ext-tox-card" style="border-right:3px solid #D93025;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;">
        <div class="ext-tox-name" style="color:#D93025;">{L["p_danger"]}</div>
        {L["p_badge_flag"]}
      </div>
      <div class="ext-tox-cf">{L["p_conf_c"]}</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#D93025;width:99%;"></div></div>
    </div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_kw_lbl"]}</div>
    <div class="ext-hl">
      <span class="hl-s">كيف</span><span class="hl-m">أصنع</span>
      <span class="hl-h">قنبلة</span><span class="hl-h">تدمير</span><span class="hl-m">مبنى</span>
    </div>
  </div>
  <div class="ext-div"></div>
  <div style="padding:6px 12px 10px;">
    <div class="ext-btn-navy">{L["p_btn_rewrite"]}</div>
    <div class="ext-btn-orange" style="margin-top:4px;">{L["p_btn_orig"]}</div>
    <div class="ext-btn-ghost" style="margin-top:4px;">{L["p_btn_cancel"]}</div>
  </div>
</div>"""

def popup_rewritten(logo_b64, L):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64, L)}
  <div class="ext-elapsed">{L["p_elapsed_c"]}</div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_masked_lbl"]}</div>
    <div class="ext-tbox">{L["p_tox_text"]}</div>
  </div>
  <div class="ext-sec">
    <div class="ext-sec-t">{L["p_tox_lbl"]}</div>
    <div class="ext-tox-card" style="border-right:3px solid #D93025;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;">
        <div class="ext-tox-name" style="color:#D93025;">{L["p_danger"]}</div>
        {L["p_badge_flag"]}
      </div>
      <div class="ext-tox-cf">{L["p_conf_c"]}</div>
      <div class="ext-bar"><div class="ext-bar-f" style="background:#D93025;width:99%;"></div></div>
    </div>
  </div>
  <div class="ext-sec" style="padding-bottom:7px;">
    <div class="ext-sec-t" style="color:#00C9A7;">{L["p_rw_lbl"]}</div>
    <div class="ext-tbox" style="border-color:#00C9A7;border-width:1.5px;font-size:0.76rem;">{L["p_rw_text"]}</div>
  </div>
  <div class="ext-div"></div>
  <div style="padding:6px 12px 5px;display:grid;grid-template-columns:1fr 1fr;gap:5px;">
    <div class="ext-btn-teal" style="font-size:0.68rem;">{L["p_btn_rw_send"]}</div>
    <div class="ext-btn-orange" style="font-size:0.68rem;">{L["p_btn_orig"]}</div>
  </div>
  <div style="padding:0 12px 10px;"><div class="ext-btn-ghost">{L["p_btn_cancel"]}</div></div>
</div>"""

def popup_settings(logo_b64, L):
    return f"""
<div class="ext-popup">
  {popup_header(logo_b64, L, gear_active=True)}
  <div style="padding:10px 13px;">
    <div style="background:#FDFAF5;border:1px solid rgba(0,0,0,0.08);border-radius:10px;padding:8px 13px;margin-bottom:8px;">
      <div style="font-size:0.72rem;font-weight:700;color:#7A7068;text-transform:uppercase;letter-spacing:0.1em;padding:6px 0 8px;border-bottom:1px solid rgba(0,0,0,0.06);margin-bottom:4px;">{L["p_set_appear"]}</div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">{L["p_set_dark_lbl"]}</div><div class="ext-set-sub">{L["p_set_dark_sub"]}</div></div>
        <div class="ext-tog-off"><div class="ext-tog-k-off"></div></div>
      </div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">{L["p_set_lang_lbl"]}</div><div class="ext-set-sub">{L["p_set_lang_sub"]}</div></div>
        <div class="ext-lang"><div class="ext-lang-active">{L["p_lang_active"]}</div><div class="ext-lang-off">{L["p_lang_off"]}</div></div>
      </div>
    </div>
    <div style="background:#FDFAF5;border:1px solid rgba(0,0,0,0.08);border-radius:10px;padding:8px 13px;margin-bottom:8px;">
      <div style="font-size:0.72rem;font-weight:700;color:#7A7068;text-transform:uppercase;letter-spacing:0.1em;padding:6px 0 8px;border-bottom:1px solid rgba(0,0,0,0.06);margin-bottom:4px;">{L["p_set_behav"]}</div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">{L["p_set_safe_lbl"]}</div><div class="ext-set-sub">{L["p_set_safe_sub"]}</div></div>
        <div class="ext-tog-on"><div class="ext-tog-k-on"></div></div>
      </div>
      <div class="ext-set-row">
        <div><div class="ext-set-lbl">{L["p_set_auto_lbl"]}</div><div class="ext-set-sub">{L["p_set_auto_sub"]}</div></div>
        <div class="ext-tog-on"><div class="ext-tog-k-on"></div></div>
      </div>
    </div>
    <div style="background:#E8520A;color:#fff;border-radius:10px;padding:10px;text-align:center;font-weight:700;font-size:0.84rem;">{L["p_set_save"]}</div>
  </div>
</div>"""

# ─────────────────────────────────────────────────────────────
# WEBSITE GUIDE
# ─────────────────────────────────────────────────────────────
def render_website(logo_b64, lang):
    L = T[lang]

    sec("1", L["w_s1"], lang)
    st.markdown(f'<div style="background:#0F1C35;color:rgba(234,228,217,0.85);border-radius:12px;padding:18px 22px;margin:12px 0 18px;line-height:1.7;font-size:0.92rem;direction:{d(lang)};text-align:{a(lang)};">{L["w_intro"]}</div>', unsafe_allow_html=True)
    flow_diagram(L["w_flow"], lang)

    sec("2", L["w_s2"], lang)
    cards = ""
    for name_cls, name, desc, pill_bg, pill_fg, pills in L["w_models"]:
        pill_html = "".join(f'<span class="cat-pill" style="background:{pill_bg};color:{pill_fg};">{p}</span>' for p in pills)
        cards += f'<div class="model-card" style="text-align:{a(lang)};"><span class="{name_cls}">{name}</span><div class="model-desc">{desc}</div><div class="model-cats">{pill_html}</div></div>'
    st.markdown(f'<div class="model-grid">{cards}</div>', unsafe_allow_html=True)

    sec("3", L["w_s3"], lang)
    tip(L["w_tip1"], lang)
    for i, (lbl, desc) in enumerate(L["w_steps"]):
        step_item(i+1, lbl, desc, lang, last=(i==len(L["w_steps"])-1))
    tip(L["w_tip2"], lang)

    sec("4", L["w_s4"], lang)
    pii_table(L["w_pii_headers"], L["w_pii_rows"], lang)

    sec("5", L["w_s5"], lang)
    guide_table(L["w_tox_headers"], L["w_tox_rows"], lang)

    sec("6", L["w_s6"], lang)
    guide_table(L["w_qr_headers"], L["w_qr_rows"], lang)

    st.markdown(f'<div class="guide-footer"><span>PromptScanner</span> — {L["w_footer"]}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# EXTENSION GUIDE
# ─────────────────────────────────────────────────────────────
def render_extension(logo_b64, lang):
    L = T[lang]

    sec("1", L["e_s1"], lang)
    st.markdown(f'<div style="background:#0F1C35;color:rgba(234,228,217,0.85);border-radius:12px;padding:18px 22px;margin:12px 0 18px;line-height:1.7;font-size:0.92rem;direction:{d(lang)};text-align:{a(lang)};">{L["e_intro"]}</div>', unsafe_allow_html=True)
    flow_diagram(L["e_flow"], lang)

    sec("2", L["e_s2"], lang)
    for i, (lbl, desc) in enumerate(L["e_steps_install"]):
        step_item(i+1, lbl, desc, lang, last=(i==len(L["e_steps_install"])-1))
    tip(L["e_tip_install"], lang)

    sec("3", L["e_s3"], lang)
    st.markdown(f'<p style="color:var(--muted);font-size:0.9rem;direction:{d(lang)};text-align:{a(lang)};margin-bottom:16px;">{L["e_states_intro"]}</p>', unsafe_allow_html=True)

    for state_key, ann_key in [("e_state_a","e_ann_a"),("e_state_b","e_ann_b"),("e_state_c","e_ann_c"),("e_state_d","e_ann_d")]:
        popup_fn = [popup_safe, popup_pii, popup_toxic, popup_rewritten][[
            "e_state_a","e_state_b","e_state_c","e_state_d"].index(state_key)]
        st.markdown(f'<div style="font-size:1rem;font-weight:700;color:var(--navy);direction:{d(lang)};text-align:{a(lang)};margin:16px 0 8px;">{L[state_key]}</div>', unsafe_allow_html=True)
        popup_with_ann(popup_fn(logo_b64, L), L[ann_key], lang)

    sec("4", L["e_s4"], lang)
    st.markdown(f'<p style="color:var(--muted);font-size:0.9rem;direction:{d(lang)};text-align:{a(lang)};margin-bottom:14px;">{L["e_settings_intro"]}</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.markdown(popup_settings(logo_b64, L), unsafe_allow_html=True)
    with c2:
        guide_table(L["e_settings_headers"], L["e_settings_rows"], lang)
    tip(L["e_tip_save"], lang, warn=True)

    sec("5", L["e_s5"], lang)
    guide_table(L["e_sites_headers"], L["e_sites_rows"], lang)

    sec("6", L["e_s6"], lang)
    guide_table(L["e_qr_headers"], L["e_qr_rows"], lang)

    st.markdown(f'<div class="guide-footer"><span>PromptScanner</span> — {L["e_footer"]}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def render_user_guide():
    inject_css()
    logo_b64   = img_b64("assets/logo.png")
    lang       = st.session_state.get("guide_lang", "ar")
    active_tab = st.session_state.get("guide_tab", "website")
    L          = T[lang]
    is_rtl     = lang == "ar"

    # Global RTL for Arabic
    if is_rtl:
        st.markdown('<style>body,.block-container{direction:rtl;}</style>', unsafe_allow_html=True)
    else:
        st.markdown('<style>body,.block-container{direction:ltr;}</style>', unsafe_allow_html=True)

    # ── Top bar: back button + language toggle on same row ────
    st.markdown("""<style>
div[data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;}
div[data-testid="stHorizontalBlock"]>div[data-testid="stColumn"]{min-width:0!important;flex:1 1 0!important;}
</style>""", unsafe_allow_html=True)

    if is_rtl:
        c_lang, c_space, c_back = st.columns([1, 6, 2])
    else:
        c_back, c_space, c_lang = st.columns([2, 6, 1])

    with c_back:
        if st.button("← رجوع" if is_rtl else "← Back", key="guide_back", use_container_width=True):
            st.session_state.page = "scanner"
            st.rerun()
    with c_lang:
        if st.button(L["lang_btn"], key="guide_lang_toggle", use_container_width=True):
            st.session_state.guide_lang = "en" if lang == "ar" else "ar"
            st.rerun()

    # ── Hero ─────────────────────────────────────────────────
    hero(logo_b64, lang)

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

    # ── Content ───────────────────────────────────────────────
    if active_tab == "website":
        render_website(logo_b64, lang)
    else:
        render_extension(logo_b64, lang)


if __name__ == "__main__":
    st.set_page_config(
        page_title="PromptScanner — User Guide",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    render_user_guide()
