import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

# ==========================================
# 🎨 CUSTOM CSS FOR PROFESSIONAL LOOK
# ==========================================
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Center the main title with a nice gradient */
    h1 {
        background: -webkit-linear-gradient(45deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 700;
        padding-bottom: 10px;
    }

    /* Style the subtitle */
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Style the input boxes */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        padding: 10px;
    }

    /* Style the Analyze Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #4F46E5, #06B6D4);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Button hover effect */
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(79, 70, 229, 0.3);
        color: white;
    }

    /* Style the result box */
    .result-box {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #4F46E5;
        margin-top: 20px;
        color: #1F2937;
    }

        .result-box h3 {
        color: #4F46E5; 
        margin-top: 15px;
        margin-bottom: 10px;
    }
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔑 SETUP & API KEY
# ==========================================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ ERROR: API key not found. Check your .env file or Streamlit Secrets.")
    st.stop()
else:
    client = genai.Client(api_key=api_key)

# ==========================================
# 🖥️ BUILD THE UI
# ==========================================
st.set_page_config(page_title="ResumeLens", page_icon="🧠", layout="centered")

st.title("🧠 ResumeLens")
st.markdown('<p class="subtitle">Upload your resume and paste a job description to see how well you match.</p>', unsafe_allow_html=True)

# Layout columns for a cleaner look
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])

with col2:
    st.write("") # Spacer
    st.write("") # Spacer
    st.caption("Supported format: PDF")

job_description = st.text_area("📋 Paste the Job Description here", height=200)

st.write("") # Spacer

# Button to trigger analysis
if st.button("✨ Analyze Resume"):
    if uploaded_file is not None and job_description:
        with st.spinner("🤖 Analyzing your resume against the job description..."):
            
            # Extract text from the uploaded PDF
            reader = PdfReader(uploaded_file)
            resume_text = ""
            for page in reader.pages:
                resume_text += page.extract_text()

            # Create the prompt
            prompt = f"""
            You are an expert HR recruiter. Compare the following resume to the job description.

            RESUME:
            {resume_text}

            JOB DESCRIPTION:
            {job_description}

            Return the analysis in this exact format:
            ### 1. Match Score (0-100)
            [score]

            ### 2. Missing Skills
            [list them]

            ### 3. Strengths
            [list them]
            """

            # Send to Gemini
            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            # Display the result
            st.success("✅ Analysis Complete!")
            
            # Put the result in our styled box
            st.markdown(f'<div class="result-box">{interaction.output_text}</div>', unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ Please upload a PDF and paste a job description first.")