# PromptScanner Web Application

A Streamlit web application that provides a browser-based interface for scanning Arabic prompts for personal information and harmful content. It uses the same backend models as the Chrome extension and is designed for users who want to test or use PromptScanner without installing anything.

## Live Demo

https://promptscanner-demo.streamlit.app

## What It Does

The user types or pastes an Arabic prompt into the text area, or uploads a PDF or Word document, and presses Scan. The application sends the text to the PromptScanner backend and displays four result cards: a PII card showing the masked text with detected entities highlighted, a toxicity card showing the predicted category and confidence score, a keyword attention card showing which words influenced the classification, and a rewrite card that appears when harmful content is detected and generates a safe alternative.

## File Structure

```
webapp/
├── app.py
├── userguide.py
├── requirements.txt
└── assets/
    └── logo.png
```

## File Descriptions

### app.py
The entire web application in a single file. It handles page routing, model loading, the scanner interface, and all result rendering.

At the top, it checks the session state page variable. If the user has navigated to the guide, it imports and renders `userguide.py` and stops. Otherwise it proceeds to render the main scanner.

The CSS section defines the full visual identity of the application: the cream background, navy text, orange accent colour, Plus Jakarta Sans for body text, and JetBrains Mono for code and labels. It also handles dark mode by swapping CSS variables, and hides Streamlit's default toolbar and footer.

The STRINGS dictionary holds all interface text in both Arabic and English. Switching language changes every label, placeholder, button, and badge text simultaneously without reloading.

Model loading uses `@st.cache_resource` so the four models (AraBERT NER, XLM-RoBERTa, Regex Engine, AraBERT v2 toxicity) are downloaded once and reused across all sessions. The actual scanning calls the Railway backend via HTTP rather than running models locally, keeping the Streamlit app lightweight.

The layout is a permanent two-column split. The left column shows the about panel, model status indicators, and example prompt buttons. The right column contains the file uploader, text area, scan button, and all result cards.

The file upload section supports PDF and Word documents. PDF text is extracted using PyMuPDF, which handles Arabic font encoding better than most alternatives. Word documents are parsed with python-docx. Extracted text is loaded into the text area so the user can review it before scanning.

The result section renders four cards. The PII card shows the masked text with entity tags styled as inline chips, each labelled with the entity type and the model that detected it. The toxicity card shows the predicted category name, confidence percentage, a colour-coded progress bar, and a full breakdown of all seven category probabilities. The keyword attention card renders each word as a coloured chip where the saturation indicates the word's attention score. The rewrite card appears only for flagged prompts and calls the backend rewrite endpoint, displaying the original and rewritten prompts side by side.

### userguide.py
A fully bilingual user guide rendered as a Streamlit page. It is imported by `app.py` when the user clicks the guide button and is stopped with `st.stop()` so nothing else from `app.py` renders.

The guide has two tabs: Part 1 for the web application and Part 2 for the Chrome extension. Each tab contains numbered step sections, flow diagrams, model description cards, PII type tables, toxicity category tables, popup state mockups, and a quick reference table. All content exists in both Arabic and English and switches when the user toggles the language button in the guide header.

The guide header contains a back button that sets the session page back to scanner and a language toggle. The hero section uses the navy brand card with the PromptScanner logo and a subtitle.

Step items render with the number circle on the right side for Arabic and the left side for English. Flow diagrams reverse their node order and arrow direction for Arabic so they read right to left. All tables have `direction: rtl` applied when Arabic is active.

The popup mockups in Part 2 are built entirely from HTML and CSS inside the Python file. They show accurate reproductions of the four popup states using the exact button labels and badge text from the real extension.

### requirements.txt
Lists all Python dependencies for the Streamlit Cloud deployment. Key packages include streamlit, requests for backend calls, transformers and torch for the model loading functions (even though inference runs on Railway), huggingface-hub for model download utilities, pymupdf for PDF parsing, and python-docx for Word document parsing.

### assets/logo.png
The PromptScanner logo mark. A rectangular magnifier icon in the navy and orange brand colours. Used in the top bar of the main app and in the hero section of the user guide.

## How a Scan Works

1. The user enters text in the text area or loads it from a file.
2. Pressing Scan triggers `run_scan()` which posts the text to `POST /scan` on the Railway backend.
3. The backend runs PII detection and toxicity analysis in parallel and returns a JSON response within one to two seconds.
4. The app stores the result in `st.session_state` and re-renders the result cards.
5. If the toxicity prediction is not Normal, a rewrite button appears. Clicking it calls `POST /rewrite` on the backend and displays the result.

## Language Support

The interface supports Arabic and English. The default is Arabic. All strings, result labels, badge text, and error messages switch when the user toggles the language button in the top bar. The text area uses `direction: rtl` for correct Arabic text rendering.

## Dark Mode

A moon icon in the top bar toggles dark mode. The colour scheme switches from cream and navy to a dark navy background with light text. The toggle state is stored in `st.session_state` for the duration of the browser session.

## Example Prompts

The left panel includes seven example buttons covering all detection scenarios: a name and organisation, a phone number and email, a national ID and credential, dangerous content, mental health content, offensive content, and a clean normal prompt. Clicking any example loads the text directly into the scanner without typing.

## Backend

The web application communicates with the same Railway backend as the Chrome extension at `https://promptscanner-production.up.railway.app`. The `/health` endpoint is not called on startup in the web app, but model status is indicated by the coloured dots next to each model name in the left panel, which reflect whether each model loaded successfully at Railway startup.

## Deployment

The application is deployed on Streamlit Community Cloud connected to the GitHub repository. Any push to the main branch triggers an automatic redeployment. The `HF_TOKEN` secret is configured in the Streamlit Cloud dashboard for authenticated model downloads from HuggingFace Hub.
