import streamlit as st
import requests
import time
import base64
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="AI Resume Tailoring",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint configuration
API_ENDPOINTS = {
    "upload_resume": "http://localhost:8000/upload-resume",
    "upload_jd": "http://localhost:8000/upload-jd",
}

# App title
st.title("🚀 AI Resume Tailoring System")
st.markdown("### Transform your resume to match job requirements using multi-agent AI")

# Session state initialization
if "resume_file" not in st.session_state:
    st.session_state.resume_file = None
if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "processing" not in st.session_state:
    st.session_state.processing = False
if "resume_id" not in st.session_state:
    st.session_state.resume_id = None

# Create two columns
col1, col2 = st.columns([1, 1])

# Resume upload section
with col1:
    st.markdown("### 📄 Upload Your Resume")
    
    uploaded_file = st.file_uploader("Upload PDF resume", type=["pdf"])
    
    if uploaded_file:
        st.session_state.resume_file = uploaded_file
        st.success(f"✅ Resume `{uploaded_file.name}` uploaded successfully!")

# Job description section
with col2:
    st.markdown("### 📋 Paste Job Description")
    
    job_description = st.text_area(
        "Paste the job description here", height=200, max_chars=5000
    )
    
    if job_description:
        st.session_state.job_description = job_description

# Submit button section
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

submit_button = st.button("✨ Generate Tailored Resume")

if submit_button:
    if not st.session_state.resume_file or not st.session_state.job_description:
        st.warning("⚠️ Please upload a resume and enter the job description before submitting.")
    else:
        st.session_state.processing = True

        # Upload resume
        bytes_data = st.session_state.resume_file.getvalue()
        files = {"file": (st.session_state.resume_file.name, bytes_data, "application/pdf")}
        resume_response = requests.post(API_ENDPOINTS["upload_resume"], files=files)

        if resume_response.status_code == 200:
            resume_id = resume_response.json().get("resume_id")
            st.session_state.resume_id = resume_id

            # Upload job description
            jd_data = {"job_description": st.session_state.job_description, "resume_id": resume_id}
            jd_response = requests.post(API_ENDPOINTS["upload_jd"], json=jd_data)

            if jd_response.status_code == 200:
                result = jd_response.json()
                st.success("✅ Resume tailoring complete!")

                # Display result
                tailored_resume = result.get("tailored_resume", "No tailored resume found.")
                st.text_area("Tailored Resume", value=tailored_resume, height=300)

                # Create download link
                def create_download_link(text, filename="Tailored_Resume.pdf"):
                    buffer = BytesIO()
                    buffer.write(text.encode("utf-8"))
                    buffer.seek(0)
                    b64 = base64.b64encode(buffer.read()).decode()
                    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="download-button">📥 Download Tailored Resume</a>'

                st.markdown(create_download_link(tailored_resume), unsafe_allow_html=True)
            else:
                st.error("🚨 Error processing job description.")
        else:
            st.error("🚨 Error uploading resume.")

        st.session_state.processing = False

st.markdown("</div>", unsafe_allow_html=True)
