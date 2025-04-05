import streamlit as st
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import tempfile
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flask")

# Helper: Extract text from typed PDF using PyMuPDF
def extract_text_from_pdf(pdf_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Helper: Convert PDF to images and OCR extract text (for handwritten)
def extract_text_from_handwritten_pdf(pdf_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_text = pytesseract.image_to_string(image)
        text += ocr_text
    return text

# Gemini Prompt
def get_evaluation(student_text, teacher_text):
    prompt = f"""
You are an expert evaluator. A student has written the following answer:\n\n
{student_text}

The teacher's answer key for evaluation is:\n\n
{teacher_text}

1. Please evaluate the student's response based on the key.
2. Give a score out of 10.
3. Provide specific feedback on strengths and weaknesses.
4. Suggest how the student can improve.

Respond in the format:
Score: /10
Feedback:
Suggestions:
"""
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("📚 AI Teacher Assistant - Paper Evaluator")
st.write("Upload the student's handwritten answer and the teacher's answer key.")

student_file = st.file_uploader("📄 Student Answer (Handwritten PDF)", type=["pdf"])
teacher_file = st.file_uploader("📄 Teacher Valuation Key (Typed PDF)", type=["pdf"])

if st.button("🧠 Evaluate") and student_file and teacher_file:
    with st.spinner("Extracting and evaluating..."):

        student_text = extract_text_from_handwritten_pdf(student_file.read())
        teacher_text = extract_text_from_pdf(teacher_file.read())

        result = get_evaluation(student_text, teacher_text)

    st.success("✅ Evaluation Complete!")
    st.markdown("### 📝 Result")
    st.markdown(result)

elif st.button("🧠 Evaluate"):
    st.warning("Please upload both student and teacher files to proceed.")
