# PromptScanner — Upload & Deployment Guide

## Folder structure the app expects

```
prompt_scanner/
├── app.py
├── requirements.txt
└── models/
    ├── arabert_pii/           ← fine-tuned AraBERT/CamelBERT NER model
    │   ├── config.json
    │   ├── pytorch_model.bin  (or model.safetensors)
    │   ├── tokenizer_config.json
    │   ├── vocab.txt
    │   └── tag_vocab.json     ← see below
    ├── xlmr_pii/              ← fine-tuned XLM-RoBERTa NER model
    │   ├── config.json
    │   ├── pytorch_model.bin  (or model.safetensors)
    │   ├── tokenizer_config.json
    │   ├── sentencepiece.bpe.model
    │   └── tag_vocab.json
    └── tox_model/
        └── arabert_expanded.pt   ← OR arabert_contrast.pt (whichever scored better)
```

---

## Step 1 — Save PII models from Colab (run in your PII notebook)

The models were already saved in your notebook cell 98.
Your files are currently at:
  /content/drive/MyDrive/FYP_PromptScanner/PII/saved_models/arabert_pii_augmorg/
  /content/drive/MyDrive/FYP_PromptScanner/PII/saved_models/xlmr_pii_augmorg/

Run this in a new Colab cell to confirm and create the tag_vocab.json files
with the exact format the app expects:

```python
import json, os

# Confirm vocab files exist and show content
arabert_path = '/content/drive/MyDrive/FYP_PromptScanner/PII/saved_models/arabert_pii_augmorg'
xlmr_path    = '/content/drive/MyDrive/FYP_PromptScanner/PII/saved_models/xlmr_pii_augmorg'

# Check what vocab file was saved
for path in [arabert_path, xlmr_path]:
    for name in ['tag_vocab.json', 'tag_vocab_augmorg.json']:
        f = os.path.join(path, name)
        if os.path.exists(f):
            with open(f) as fp:
                v = json.load(fp)
            print(f"\n{f}")
            print("  tag2id keys:", list(v['tag2id'].keys())[:5])
            print("  id2tag keys:", list(v['id2tag'].keys())[:5])
```

The app accepts both tag_vocab.json and tag_vocab_augmorg.json automatically.

---

## Step 2 — Save toxicity model from Colab (run in your toxicity notebook)

The toxicity model was saved as a raw PyTorch checkpoint (.pt file), NOT as a
HuggingFace model directory. This is different from the PII models.

Your checkpoint is at:
  /content/drive/MyDrive/toxic/arabert_expanded.pt
  (or arabert_contrast.pt — whichever had the higher F1)

Verify the checkpoint format:
```python
import torch
ckpt = torch.load('/content/drive/MyDrive/toxic/arabert_expanded.pt', weights_only=False)
print(ckpt.keys())   # should print: dict_keys(['model_state_dict', ...])
```

If it prints model_state_dict — you're ready. Nothing else needed.

---

## Step 3 — Download model files from Google Drive

In your Colab notebook (PII notebook), run:

```python
import shutil

# Zip all three model folders
shutil.make_archive('/content/arabert_pii', 'zip',
                    '/content/drive/MyDrive/FYP_PromptScanner/PII/saved_models',
                    'arabert_pii_augmorg')

shutil.make_archive('/content/xlmr_pii', 'zip',
                    '/content/drive/MyDrive/FYP_PromptScanner/PII/saved_models',
                    'xlmr_pii_augmorg')

from google.colab import files
files.download('/content/arabert_pii.zip')
files.download('/content/xlmr_pii.zip')
```

In your Colab notebook (toxicity notebook), run:

```python
from google.colab import files
files.download('/content/drive/MyDrive/toxic/arabert_expanded.pt')
# or: files.download('/content/drive/MyDrive/toxic/arabert_contrast.pt')
```

---

## Step 4 — Organise files locally

Unzip the downloaded files and rename/arrange into this structure:

```
models/
  arabert_pii/        ← contents of arabert_pii_augmorg.zip
  xlmr_pii/           ← contents of xlmr_pii_augmorg.zip
  tox_model/
    arabert_expanded.pt
```

IMPORTANT: The arabert_pii folder should contain the HuggingFace model files
(config.json, pytorch_model.bin / model.safetensors, vocab files).
The tox_model folder contains ONLY the .pt checkpoint file.
The base model (aubmindlab/bert-base-arabertv02) is downloaded automatically
by the app the first time it runs.

---

## Step 5 — Host model files on Hugging Face Hub (FREE, recommended)

Model files are too large for GitHub. Use HuggingFace Hub:

1. Create a free account at https://huggingface.co
2. Create a new **private** repository: e.g. your-username/promptscanner-models
3. Upload all files from arabert_pii/, xlmr_pii/, and tox_model/ into this repo,
   preserving the subfolder structure
4. Get your access token from: https://huggingface.co/settings/tokens

Then add this to the top of app.py to download models at startup on Streamlit Cloud:

```python
import os
from huggingface_hub import snapshot_download

HF_TOKEN = st.secrets.get("HF_TOKEN", os.environ.get("HF_TOKEN", ""))

@st.cache_resource(show_spinner="Downloading models from HuggingFace Hub...")
def download_models():
    if not Path("models").exists():
        snapshot_download(
            repo_id="your-username/promptscanner-models",
            token=HF_TOKEN,
            local_dir="models",
        )

download_models()
```

Add huggingface_hub to requirements.txt.

---

## Step 6 — Deploy to Streamlit Community Cloud (FREE)

1. Push app.py and requirements.txt to a public GitHub repo
   (do NOT push the models/ folder — it goes on HuggingFace)
2. Go to https://share.streamlit.io → sign in with GitHub
3. Click "New app" → select repo → select app.py
4. Under "Advanced settings" → "Secrets", add:
   HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxx"
5. Click Deploy

The app will be live at:
  https://your-username-repo-name.streamlit.app

First load will take 2-5 minutes while it downloads models.
Subsequent loads use the @st.cache_resource cache.

---

## Step 7 — Local testing

```bash
pip install streamlit torch transformers arabert

# Place models/ folder next to app.py
streamlit run app.py
# Opens at: http://localhost:8501
```

---

## How the hybrid PII system works in the app

The HybridPIIDetector from your notebook is reimplemented as a function
(hybrid_detect) in app.py. The logic is identical:

1. Regex runs FIRST and is authoritative for its 6 categories
2. AraBERT runs next — any prediction overlapping a regex span is suppressed
3. XLM-RoBERTa runs last — same overlap suppression rule

This matches exactly what HybridPIIDetector.detect() does in notebook cell 79.
The class is not imported from the notebook because the notebook cannot be
imported as a module — but the logic is a direct line-by-line port.

## How the toxicity keyword highlighting works

The highlight uses BERT attention weights — specifically the average attention
from the [CLS] token across all 12 layers and all attention heads.
High attention score = the model was "looking at" that word more when making
its classification decision. Stop words are zeroed out. Scores are normalised
to [0,1]. This is the same method as get_arabert_importance() in notebook cell 11.

The colour of highlights matches the toxicity category:
  - Normal: teal
  - Dangerous / Obscene: red
  - Mental Health: purple
  - Offensive: orange
  - Privacy Violation: blue
  - Mild Offense: amber
