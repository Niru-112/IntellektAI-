# 🧠 IntellektAI — AI-Powered PDF → MCQ Generator

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/HuggingFace-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black"/>
  <img src="https://img.shields.io/badge/Llama_3.1_8B-6C63FF?style=for-the-badge&logo=meta&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  <b>Transform any study PDF into structured, exam-ready MCQs using Llama 3.1 — in seconds.</b>
</p>

---

## 📌 Overview

**IntellektAI** is an AI-driven study assistant that converts text-based PDFs into well-structured **Multiple Choice Questions (MCQs)** using the **Llama-3.1 8B Instruct** model via Hugging Face. With a clean multi-tab Streamlit interface, students and educators can generate, search, and export exam-ready questions without any local model setup.

> ⚠️ **Note:** Upload only **system-generated PDFs** (not scanned or image-based documents).

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📄 **PDF Upload & Parsing** | Extracts text from any digital PDF using PyMuPDF |
| 📑 **Page Range Selection** | Generate MCQs from specific pages (e.g. `1-3,5`) |
| 🤖 **LLM-Powered Generation** | Llama-3.1 8B Instruct via SambaNova (Hugging Face) |
| 🗂️ **Chunk-Based Processing** | Splits large PDFs into configurable text chunks |
| 🔍 **In-Session MCQ Search** | Keyword search across all generated questions |
| 📥 **JSON Export** | Download all MCQs as a structured JSON file |
| ⚙️ **Configurable Settings** | Adjust chunk size and MCQs per chunk via sidebar |

---

## 🧠 How It Works

```
PDF Upload
    │
    ▼
Text Extraction (PyMuPDF)
    │
    ▼
Split into Chunks (configurable size)
    │
    ▼
LLM Prompt → Llama-3.1 8B Instruct
    │
    ▼
Structured JSON Output
{ question, options[4], correct_option }
    │
    ▼
Streamlit UI Display + JSON Export
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.8+ |
| **UI Framework** | Streamlit |
| **LLM** | Llama-3.1 8B Instruct (SambaNova via Hugging Face) |
| **PDF Parsing** | PyMuPDF (fitz) |
| **LLM Client** | `huggingface_hub` InferenceClient |
| **Output Format** | JSON (question · 4 options · correct index) |

---

## 📂 Project Structure

```
intellektai/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # HF_TOKEN (add your key here)
└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/nirusanathara/intellektai.git
cd intellektai
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your Hugging Face Token
Create `.streamlit/secrets.toml`:
```toml
HF_TOKEN = "your_huggingface_token_here"
```
> Get your token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 5️⃣ Run the App
```bash
streamlit run app.py
```
Open in browser: `http://localhost:8501`

---

## 🚀 Usage

1. **Upload** a text-based PDF file
2. *(Optional)* Specify a page range — e.g. `1-5` or `2,4,6`
3. Adjust **chunk size** and **MCQs per chunk** in the sidebar
4. Click **🚀 Generate MCQs**
5. Browse generated questions in **Tab 1**
6. **Search** across MCQs by keyword in **Tab 2**
7. Click **📥 Download All MCQs (JSON)** to export

---

## 📤 Sample Output (JSON)

```json
[
  {
    "question": "What is the primary function of mitochondria?",
    "options": [
      "Protein synthesis",
      "Energy production (ATP)",
      "DNA replication",
      "Cell division"
    ],
    "correct_option": 1
  }
]
```

---

## 🔮 Roadmap

- [ ] Support for scanned PDFs (OCR integration)
- [ ] Difficulty level selection (Easy / Medium / Hard)
- [ ] Export to PDF / DOCX quiz format
- [ ] User authentication & MCQ history
- [ ] FastAPI backend for REST API access
- [ ] Docker deployment

---

## 👨‍💻 Author

**Niru Sanathara**  
AI/ML Engineer | Applied Scientist  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/nirusanathara)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/nirusanathara)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center"><i>💡 Simplifying learning through AI-generated MCQs.</i></p>
