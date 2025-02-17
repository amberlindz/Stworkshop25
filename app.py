import streamlit as st
import PyPDF2
import openai
import os

# Set OpenAI API Key
openai.api_key = "your_api_key_here"
# Title
st.title("📄 AI-Powered PDF Summarizer")

# Upload PDF
uploaded_file = st.file_uploader("📤 Upload a PDF", type=["pdf"])

if uploaded_file:
    # Extract text from PDF
    with st.spinner("📑 Extracting text..."):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

    # Display extracted text (Optional)
    with st.expander("🔍 View Extracted Text"):
        st.write(text)

    # Summarization
    if st.button("✨ Generate Summary"):
        with st.spinner("🤖 Summarizing..."):
            # OpenAI API call 
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Summarize the following text:"},
                          {"role": "user", "content": text}],
                temperature=0.5
            )
            summary = response["choices"][0]["message"]["content"]

        # Display Summary
        st.subheader("📝 Summary")
        st.write(summary)

        # Download Summary as Text File
        summary_file = "summary.txt"
        with open(summary_file, "w") as f:
            f.write(summary)

        st.download_button(
            label="📥 Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )
