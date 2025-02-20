import streamlit as st
import requests
import time
import base64
from io import BytesIO
import os
import json

# Configure page
st.set_page_config(
    page_title="AI Resume Tailoring",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7ff;
    }
    .stButton>button {
        background-color: #4c6ef5;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #364fc7;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .upload-section {
        background-color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    .job-section {
        background-color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d3f9d8;
        border-left: 5px solid #37b24d;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .header-text {
        margin: 0;
        color: #364fc7;
    }
    .header-icon {
        font-size: 2rem;
    }
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# API endpoint configuration
# Replace with your actual endpoints
API_ENDPOINTS = {
    "upload_resume": "http://localhost:8000/upload-resume",
    "upload_jd": "http://localhost:8000/upload-jd",
}

# App title
st.title("🚀 AI Resume Tailoring System")
st.markdown("### Transform your resume to match job requirements using multi-agent AI")

# Session state initialization
if 'resume_uploaded' not in st.session_state:
    st.session_state.resume_uploaded = False
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'resume_id' not in st.session_state:
    st.session_state.resume_id = None
if 'jd_id' not in st.session_state:
    st.session_state.jd_id = None

# Create two columns
col1, col2 = st.columns([1, 1])

# Resume upload section
with col1:
    with st.container():
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("""
        <div class="header-container">
            <h3 class="header-text">Upload Your Existing Resume</h3>
            <div class="header-icon">📄</div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload PDF resume", type=['pdf'])
        
        if uploaded_file is not None:
            # Display success message with file details
            file_details = {
                "Filename": uploaded_file.name,
                "Size": f"{uploaded_file.size / 1024:.2f} KB"
            }
            
            # Show file preview
            st.markdown("### Resume Preview")
            st.markdown(f"""
            <div class="success-message">
                <p><strong>✅ Resume uploaded successfully!</strong></p>
                <p>Filename: {uploaded_file.name}</p>
                <p>Size: {file_details['Size']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Store in session state
            st.session_state.resume_uploaded = True
            
            # Only process the upload if not already processed
            if not st.session_state.resume_id:
                try:
                    # Prepare file for upload to API
                    bytes_data = uploaded_file.getvalue()
                    files = {"file": (uploaded_file.name, bytes_data, "application/pdf")}
                    response = requests.post(API_ENDPOINTS["upload_resume"], files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.resume_id = result.get("resume_id")
                    else:
                        st.error(f"Error uploading resume: {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to API: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Job description section
with col2:
    with st.container():
        st.markdown('<div class="job-section">', unsafe_allow_html=True)
        st.markdown("""
        <div class="header-container">
            <h3 class="header-text">Paste Job Description</h3>
            <div class="header-icon">📋</div>
        </div>
        """, unsafe_allow_html=True)
        
        job_description = st.text_area(
            "Paste the job description text below",
            height=300,
            max_chars=5000,
            help="Maximum 5000 characters"
        )
        
        # Character counter
        current_chars = len(job_description)
        st.markdown(f"<p style='text-align: right; color: {'#4c6ef5' if current_chars < 4000 else '#e03131'};'>{current_chars}/5000 characters</p>", unsafe_allow_html=True)
        
        if job_description:
            st.session_state.job_description = job_description
        
        st.markdown('</div>', unsafe_allow_html=True)

# Submit button section
st.markdown('<div style="text-align: center; margin-top: 2rem;">', unsafe_allow_html=True)

# Check if both resume and job description are provided
submit_disabled = not (st.session_state.resume_uploaded and st.session_state.job_description)

if submit_disabled:
    st.warning("Please upload your resume and paste the job description to continue")

submit_button = st.button("✨ Generate Tailored Resume", disabled=submit_disabled)

if submit_button and not st.session_state.processing:
    # Set processing state
    st.session_state.processing = True
    
    try:
        # Upload job description to API
        jd_data = {"job_description": st.session_state.job_description, "resume_id": st.session_state.resume_id}
        response = requests.post(API_ENDPOINTS["upload_jd"], json=jd_data)
        
        if response.status_code == 200:
            result = response.json()
            st.session_state.jd_id = result.get("jd_id")
            
            # Create a loading animation
            with st.container():
                st.markdown('<div class="loading-container">', unsafe_allow_html=True)
                
                # Processing steps with animations
                steps = [
                    "⏳ Analyzing your resume...",
                    "🔍 Extracting key skills from job description...",
                    "🧩 Matching your experience with job requirements...",
                    "📝 Creating optimized content...",
                    "🎨 Formatting your new resume..."
                ]
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, step in enumerate(steps):
                    status_text.markdown(f"<h4>{step}</h4>", unsafe_allow_html=True)
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(1.5)  # Simulate processing time
                
                st.success("✅ Resume tailoring complete!")
                
                # Display download option (mockup)
                st.markdown("""
                <div style="text-align: center; margin-top: 2rem;">
                    <p>Your tailored resume is ready! Click below to download.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a mock PDF for download demo
                def create_download_link(filename="Tailored_Resume.pdf"):
                    # This is a placeholder - in a real app, you'd get the actual PDF from your backend
                    buffer = BytesIO()
                    buffer.write(b"Sample PDF content - this would be your actual resume")
                    buffer.seek(0)
                    b64 = base64.b64encode(buffer.read()).decode()
                    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="download-button">Download Tailored Resume</a>'
                
                st.markdown(f"""
                <div style="text-align: center; margin: 2rem;">
                    <style>
                        .download-button {{
                            background-color: #37b24d;
                            color: white;
                            padding: 0.75rem 2rem;
                            border-radius: 0.5rem;
                            text-decoration: none;
                            font-weight: bold;
                            display: inline-block;
                            transition: all 0.3s;
                        }}
                        .download-button:hover {{
                            background-color: #2b9a3f;
                            transform: translateY(-2px);
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        }}
                    </style>
                    {create_download_link()}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(f"Error processing job description: {response.text}")
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
    
    # Reset processing state
    st.session_state.processing = False

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<footer style="margin-top: 5rem; text-align: center; color: #6c757d; padding: 1rem;">
    <p>🛠️ Powered by Gemini AI & LangChain</p>
    <p>© 2025 AI Resume Tailoring System</p>
</footer>
""", unsafe_allow_html=True)