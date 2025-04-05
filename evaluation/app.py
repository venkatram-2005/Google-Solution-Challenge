import streamlit as st
import PyPDF2

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

st.set_page_config(page_title="PDF Comparator", layout="centered")

st.title("📄 Exam Paper Evaluation Model")

st.write("Upload the questions with principles of valuation in 1 pdf and student responses in 1 pdf.")

# File uploaders
pdf1 = st.file_uploader("Upload principles of valuation PDF", type="pdf", key="pdf1")
pdf2 = st.file_uploader("Upload student responses PDF", type="pdf", key="pdf2")

if pdf1 and pdf2:
    with st.spinner("Extracting text from PDFs..."):
        text1 = extract_text_from_pdf(pdf1)
        text2 = extract_text_from_pdf(pdf2)

    st.subheader("📘 First PDF Content")
    st.text_area("Text from First PDF", text1, height=200)

    st.subheader("📙 Second PDF Content")
    st.text_area("Text from Second PDF", text2, height=200)

    # Optional comparison
    if st.button("Compare (basic)"):
        if text1.strip() == text2.strip():
            st.success("✅ The PDFs have identical text content.")
        else:
            st.warning("⚠️ The PDFs have different text content.")
else:
    st.info("Please upload two PDFs to begin.")
