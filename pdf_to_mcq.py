import streamlit as st
import fitz
import json
import re
import os
from huggingface_hub import InferenceClient

# ========================
# CONFIGURATION
# ========================
st.set_page_config(page_title="🧠 IntellektAI | PDF → MCQ Generator", layout="wide")
st.title("🧠 IntellektAI: AI-Powered PDF → MCQ Generator")

st.markdown("""
Welcome to **IntellektAI**, an AI-driven assistant that turns your study PDFs into **exam-ready MCQs** 📚  
Built with **Streamlit** + **Hugging Face Fireworks Llama-3.1 8B Instruct** (no local model installation required).  
---
""")

st.warning("⚠️ Upload **only system-generated PDFs** (not scanned or image-based).")

# --- Session State ---
if "mcq_db" not in st.session_state:
    st.session_state.mcq_db = []

# --- Sidebar Options ---
st.sidebar.header("⚙️ Settings")
num_mcqs_per_chunk = st.sidebar.number_input("MCQs per chunk", 1, 20, 5)
chunk_size = st.sidebar.number_input("Chunk size (chars)", 500, 4000, 2000)

# --- Initialize Hugging Face Fireworks Llama client ---
HF_TOKEN = st.secrets["HF_TOKEN"]  # Add this to Streamlit secrets
client = InferenceClient(provider="fireworks-ai", api_key=HF_TOKEN)

# ========================
# Helper Functions
# ========================
def hf_generate_mcqs(text, num_mcqs):
    """Generate MCQs using Llama-3.1 8B Instruct via Hugging Face Fireworks."""
    try:
        # Define the system message to enforce structured JSON output
        system_message = (
            "You are an expert educational assistant. Generate exactly "
            f"{num_mcqs} multiple-choice questions (MCQs) from the provided text. "
            "You MUST return a valid JSON array of objects with the keys: 'question', 'options' (array of 4 strings), and 'correct_option' (0-based index). "
            "Return JSON only, no explanations, intro, or markdown fences."
        )

        user_prompt = f"""
        Text:
        {text}

        Generate {num_mcqs} MCQs based on the text above.
        """
        
        # CORRECTED: Use client.chat_completion() with the standard messages format
        response = client.chat_completion(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            # Pass additional parameters for reliability
            max_tokens=2048,
            temperature=0.1,
            response_format={"type": "json_object"} # Crucial for clean JSON output
        )
        
        # The response structure follows the OpenAI standard
        text_out = response.choices[0].message.content or ""

        # Use regex to robustly find the JSON array (still good practice)
        match = re.search(r"\[.*\]", text_out, re.DOTALL)
        json_str = match.group(0) if match else "[]"
        return json.loads(json_str)
        
    except Exception as e:
        # Note: If the model itself fails to generate JSON, the load will fail here.
        st.error(f"❌ Hugging Face Llama API error: {e}")
        return []

def parse_page_range(page_range_str, total_pages):
    pages = set()
    if not page_range_str:
        return list(range(total_pages))
    try:
        for part in page_range_str.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                pages.update(range(start-1, end))
            else:
                pages.add(int(part)-1)
    except Exception:
        return list(range(total_pages))
    return sorted(p for p in pages if 0 <= p < total_pages)

def split_text_into_chunks(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

# ========================
# TABS
# ========================
tab1, tab2 = st.tabs(["📘 Generate MCQs", "🔍 Search MCQs"])

# --- Tab 1: Generate MCQs ---
with tab1:
    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
    page_range = st.text_input("📑 Page Range (e.g. 1-3,5) — leave empty for all pages")

    if st.button("🚀 Generate MCQs"):
        if not uploaded_file:
            st.error("Please upload a PDF file.")
        else:
            pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            total_pages = pdf_doc.page_count
            selected_pages = parse_page_range(page_range, total_pages)
            text = "".join(pdf_doc[i].get_text("text") for i in selected_pages)
            pdf_doc.close()

            if not text.strip():
                st.error("No extractable text found in selected pages.")
            else:
                chunks = split_text_into_chunks(text, chunk_size)
                st.info(f"📖 Split PDF into {len(chunks)} text chunks. Generating MCQs...")
                progress = st.progress(0)
                all_mcqs = []

                for idx, chunk in enumerate(chunks, 1):
                    progress.progress(idx / len(chunks))
                    mcqs = hf_generate_mcqs(chunk, num_mcqs_per_chunk)
                    all_mcqs.extend(mcqs)

                progress.empty()

                if all_mcqs:
                    st.session_state.mcq_db.extend(all_mcqs)
                    st.success(f"✅ Generated {len(all_mcqs)} MCQs in total!")

                    for i, mcq in enumerate(all_mcqs, 1):
                        st.markdown(f"**Q{i}:** {mcq.get('question','N/A')}")
                        opts = mcq.get("options", [])
                        for j, opt in enumerate(opts):
                            st.write(f"{chr(65+j)}. {opt}")
                        correct = mcq.get("correct_option", 0)
                        st.markdown(f"**Answer:** :green[{chr(65+correct)}]")
                        st.divider()

                    st.download_button(
                        "📥 Download All MCQs (JSON)",
                        data=json.dumps(all_mcqs, indent=2),
                        file_name="intellektai_mcqs.json",
                        mime="application/json"
                    )
                else:
                    st.warning("No valid MCQs were generated. Try adjusting chunk size or topic context.")

# --- Tab 2: Search MCQs ---
with tab2:
    st.subheader(f"Search across {len(st.session_state.mcq_db)} generated MCQs")
    query = st.text_input("🔎 Enter keyword to search")
    limit = st.number_input("Max results", 1, 50, 5)

    if st.button("Search"):
        if query.strip():
            results = [
                mcq for mcq in st.session_state.mcq_db
                if query.lower() in mcq.get("question", "").lower()
            ][:limit]
            if results:
                st.success(f"Found {len(results)} MCQs matching '{query}'.")
                for i, mcq in enumerate(results, 1):
                    st.markdown(f"**Q{i}:** {mcq.get('question','N/A')}")
                    for j, opt in enumerate(mcq.get("options", [])):
                        st.write(f"{chr(65+j)}. {opt}")
                    st.markdown(f"**Answer:** :green[{chr(65 + mcq.get('correct_option', 0))}]")
                    st.divider()
            else:
                st.info("No results found.")
        else:
            st.warning("Enter a keyword first!")

# ========================
# FOOTER
# ========================
st.markdown("""
---
👨‍💻 **Developed by Niru Sanathara**  
🧩 Powered by **Hugging Face Fireworks Llama-3.1 8B Instruct** + **Streamlit**  
💡 *Simplifying learning through AI-generated MCQs.*  
📌 App Name: **IntellektAI**
""")
