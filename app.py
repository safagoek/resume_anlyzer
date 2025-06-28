import streamlit as st
from openai import OpenAI
import pymupdf
import os
from dotenv import load_dotenv
import re
from datetime import datetime

# Load environment variables
load_dotenv()

# OpenRouter API Configuration
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))
SITE_URL = st.secrets.get("SITE_URL", os.getenv("SITE_URL", "https://resume-analyzer-safagoek.streamlit.app"))
SITE_NAME = st.secrets.get("SITE_NAME", os.getenv("SITE_NAME", "ATS Resume Analyzer - safagoek"))

if not OPENROUTER_API_KEY:
    st.error("🔑 API key Not found pls chek streamlid settings.")
    st.stop()

# Configure OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Enhanced PROMPT with extremely detailed analysis structure
PROMPT = """
Analyze the following resume against the job description and provide an extremely comprehensive and actionable analysis:

1. **MATCH PERCENTAGE**: 
   - Start with a clear percentage score (e.g., "75%") 
   - Break down how you calculated this score (skills matches, experience alignment, education fit, etc.)
   - Explain what the percentage means in terms of overall fit for this position
   - Note if certain critical requirements heavily affected the score

2. **KEY STRENGTHS**: 
   - List all specific skills, experiences, and qualifications that directly align with job requirements
   - Highlight the most impressive achievements that match employer priorities
   - Quantify the strength of alignment for each match (strong, moderate, weak)
   - Note any unique selling points that set the candidate apart from typical applicants
   - Identify any particularly valuable experiences that deserve emphasis

3. **MISSING QUALIFICATIONS**: 
   - List all important requirements from the job description not found in the resume
   - Categorize missing requirements by importance (critical, important, nice-to-have)
   - Identify any critical certifications, degrees, or technical skills that are missing
   - Explain the exact impact of these gaps on the candidate's application
   - Suggest specific ways to address or compensate for each missing qualification

4. **SKILL GAPS**: 
   - Detail all technical skills mentioned in the job description but not in the resume
   - Identify soft skills emphasized in the job posting but not demonstrated
   - Compare years of experience required vs. shown on resume for key areas
   - Suggest specific courses, certifications, or projects to address each gap
   - Provide language to use that can minimize the impact of these gaps

5. **ATS OPTIMIZATION**: 
   - List all specific keywords from the job description missing from the resume
   - Identify formatting issues that could prevent ATS from properly reading the resume
   - Suggest reorganization of sections to prioritize most relevant information
   - Recommend better keyword placement strategies throughout the document
   - Advise on optimal keyword density without keyword stuffing
   - Suggest improvements for section headers to better match industry standards
   - Identify any inconsistencies or errors that might trigger ATS rejection

6. **DETAILED RECOMMENDATIONS**: 
   - Provide section-by-section suggestions for improvement (Summary, Experience, Skills, etc.)
   - Suggest specific bullet point rewrites to better align with job requirements
   - Recommend content to remove that doesn't support this specific application
   - Suggest precise wording changes to better match job description terminology
   - Recommend additional sections that could strengthen the application
   - Provide 3-5 specific, actionable next steps in priority order

Format your response with clear section headers and bullet points. Make all feedback extremely specific, actionable, and prioritized. Leave no ambiguity or unanswered questions in your analysis. Focus on providing concrete suggestions that will directly improve the candidate's chances of getting an interview.
"""

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        pdf_file.seek(0)  # Reset file pointer
        with pymupdf.open(stream=pdf_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text("text")
        return text.strip()
    except Exception as e:
        st.error(f"❌ PDF okuma hatası: {str(e)}")
        return None

# Function to analyze resume against job description
def analyze_resume(resume_text, job_desc):
    try:
        prompt = f"{PROMPT}\n\n**RESUME CONTENT:**\n{resume_text}\n\n**JOB DESCRIPTION:**\n{job_desc}"
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS (Applicant Tracking System) analyzer and senior career counselor with 15+ years of experience in recruitment and HR. Provide extremely detailed, specific, and actionable feedback on resume-job fit. Always start your response with a clear match percentage and be comprehensive in your recommendations, leaving no questions unanswered."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,  # Lower temperature for more consistent results
            max_tokens=4000   # Increased for detailed analysis
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"❌ AI Analiz hatası: {str(e)}")
        return None

def extract_match_percentage(text):
    # Enhanced patterns to catch percentage with explanation
    patterns = [
        r'(\d{1,3})%',
        r'match.*?(\d{1,3})%',
        r'score.*?(\d{1,3})%',
        r'percentage.*?(\d{1,3})%',
        r'rating.*?(\d{1,3})%'
    ]
    
    # Look for the first percentage that makes sense
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                percentage = int(match)
                if 0 <= percentage <= 100:
                    return percentage
    return None

# Streamlit Page Configuration
st.set_page_config(
    page_title="ATS Resume Analyzer - safagoek",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0
if 'last_analysis_time' not in st.session_state:
    st.session_state.last_analysis_time = None
if 'api_connection_tested' not in st.session_state:
    st.session_state.api_connection_tested = False
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'job_description' not in st.session_state:
    st.session_state.job_description = None
if 'match_percentage' not in st.session_state:
    st.session_state.match_percentage = None

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Main theme */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 95%;
    }
    
    /* Header styling */
    .title-area {
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Input containers */
    .input-container {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Section headers */
    .section-header {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }
    
    .section-header img, .section-header span {
        margin-right: 0.5rem;
    }
    
    /* API status indicator */
    .api-status {
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 0.8rem;
        background: rgba(0, 0, 0, 0.3);
        padding: 5px 10px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 5px;
        z-index: 100;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    
    /* Analysis section */
    .analysis-section {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
        border-left: 3px solid #667eea;
    }
    
    /* Match score display */
    .match-score {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1.5rem 0;
        padding: 1.5rem;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Info cards */
    .info-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border-left: 3px solid #667eea;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.2) 0%, rgba(32, 134, 55, 0.2) 100%);
        color: #98c379;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #98c379;
        margin: 1rem 0;
    }
    
    /* Error message */
    .error-message {
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.2) 0%, rgba(176, 42, 55, 0.2) 100%);
        color: #e06c75;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #e06c75;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 0.9rem;
        opacity: 0.7;
    }
    
    /* How to use section */
    .how-to-use {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 3px solid #FFC107;
    }
    
    .how-to-use h3 {
        color: #FFC107;
        margin-bottom: 1rem;
    }
    
    .step-container {
        display: flex;
        gap: 15px;
        margin-bottom: 1rem;
    }
    
    .step-number {
        background: rgba(255, 255, 255, 0.1);
        color: #FFC107;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    
    .step-content {
        flex: 1;
    }
    
    /* Mini API button */
    .mini-api-button {
        position: absolute;
        top: 10px;
        right: 20px;
        background: rgba(0,0,0,0.3);
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    /* Remove extra padding/margins */
    .stTextInput, .stFileUploader, .stTextArea {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Download button special styling */
    .download-btn {
        background: linear-gradient(135deg, #28a745 0%, #218838 100%) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="title-area">
    <h1>📝 ATS Resume Score & Optimization Tool</h1>
    <p>AI-powered resume match scoring & personalized feedback</p></div>
""", unsafe_allow_html=True)

# API Status - Minimal in corner
api_status = "Connected" if st.session_state.api_connection_tested else "Not Tested"
status_color = "#4CAF50" if st.session_state.api_connection_tested else "#FFA500"

st.markdown(f"""
<div class="api-status">
    <span class="status-dot" style="background: {status_color};"></span>
    API: {api_status}
</div>
""", unsafe_allow_html=True)

# Simple API test button in main flow
col_api, col_spacer = st.columns([1, 10])
with col_api:
    if st.button("Test API", key="api_test"):
        try:
            test_completion = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            st.session_state.api_connection_tested = True
            st.success("✅ API Connection Successful!")
            st.rerun()  # Refresh to update the status indicator
        except Exception as e:
            st.error(f"❌ API Connection Failed: {str(e)}")

# How to use section - At the top
st.markdown("""
### 🔍 How to Use This Tool

1. Upload your resume – Ensure it's a selectable-text PDF and not password protected.  
2. Paste job description – Include all details from the job posting.  
3. Start analysis – Click the button and wait about 30–60 seconds.  
4. Review results – Get your match score and feedback for improvement.  
5. Download report – Save the analysis to help update your resume.

""", unsafe_allow_html=True)

# Create columns for the main content
col1, col2 = st.columns([1, 1], gap="medium")

# Left Column - File Upload
with col1:
    st.markdown('<div class="section-header">📂 Upload Your Resume</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your resume (PDF format)",
        type=["pdf"],
        help="Upload your most recent resume in PDF format",
        key="resume_upload",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.markdown(f"""
        <div class="success-message">
            ✅ <b>Resume Uploaded:</b> {uploaded_file.name}
        </div>
        """, unsafe_allow_html=True)
        
        file_size = uploaded_file.size / 1024  # Convert to KB
        
        st.markdown(f"""
        <div class="info-card">
            📊 <b>Size:</b> {file_size:.1f} KB | <b>Type:</b> {uploaded_file.type} | <b>Status:</b> Ready
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
            Please upload a PDF resume (1-2 pages recommended)
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Right Column - Job Description
with col2:
    st.markdown('<div class="section-header">📝 Job Description Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    job_description = st.text_area(
        "Paste the complete job description",
        height=220,
        placeholder="Paste the complete job description here...\n\nInclude all requirements, qualifications, and responsibilities.",
        key="job_desc_input",
        label_visibility="collapsed"
    )
    
    if job_description:
        word_count = len(job_description.split())
        
        # Quality assessment
        if word_count >= 100:
            quality = "Excellent"
            quality_color = "#4CAF50"
        elif word_count >= 50:
            quality = "Good"
            quality_color = "#FFC107"
        else:
            quality = "Too Short"
            quality_color = "#F44336"
        
        st.markdown(f"""
        <div class="info-card">
            📊 <b>Words:</b> {word_count} | <b>Quality:</b> <span style="color: {quality_color};">{quality}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if word_count < 50:
            st.warning("⚠️ Job description seems short. Add more details for better analysis.")
    else:
        st.markdown("""
        <div class="info-card">
            Add a detailed job description (100+ words recommended)
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis Button - Centered
st.markdown("<div style='display: flex; justify-content: center; margin: 2rem 0;'>", unsafe_allow_html=True)
analyze_button = st.button("🚀 Start Professional Analysis", type="primary", key="analyze_btn", use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)

# Analysis Logic
if analyze_button:
    if not uploaded_file:
        st.error("❌ Please upload your PDF resume first.")
    elif not job_description.strip():
        st.error("❌ Please paste the job description.")
    elif len(job_description.split()) < 20:
        st.warning("⚠️ Job description is too short. Please provide more details.")
    else:
        # Enhanced progress tracking
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Step 1: PDF Text Extraction
        status_text.markdown("📄 **Step 1/4:** Extracting text from PDF...")
        progress_bar.progress(10)
        
        resume_text = extract_text_from_pdf(uploaded_file)
        progress_bar.progress(25)
        
        if resume_text and len(resume_text.strip()) > 100:
            extracted_words = len(resume_text.split())
            status_text.markdown(f"✅ **Text Extracted:** {extracted_words} words found")
            
            # Step 2: AI Analysis Preparation
            status_text.markdown("🤖 **Step 2/4:** Preparing AI analysis...")
            progress_bar.progress(35)
            
            # Step 3: Running AI Analysis
            status_text.markdown("🧠 **Step 3/4:** AI analyzing resume vs job requirements...")
            progress_bar.progress(50)
            
            analysis = analyze_resume(resume_text, job_description)
            progress_bar.progress(80)
            
            if analysis:
                # Step 4: Processing Results
                status_text.markdown("📊 **Step 4/4:** Processing results...")
                progress_bar.progress(95)
                
                # Extract match percentage
                match_percentage = extract_match_percentage(analysis)
                progress_bar.progress(100)
                
                # Store data in session state to prevent page refresh issues
                st.session_state.analysis_result = analysis
                st.session_state.resume_text = resume_text
                st.session_state.job_description = job_description
                st.session_state.match_percentage = match_percentage
                
                # Update session state
                st.session_state.analysis_count += 1
                st.session_state.last_analysis_time = datetime.now()
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Success notification
                st.success("🎉 **Analysis Complete!** Your professional resume analysis is ready.")
                
                # Display Results
                st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                st.markdown("## 📊 Professional Resume Analysis Report")
                
                # Enhanced Match Score Display
                if match_percentage is not None:
                    if match_percentage >= 85:
                        color = "#4CAF50"
                        emoji = "🎉"
                        status = "Outstanding Match!"
                    elif match_percentage >= 70:
                        color = "#8BC34A"
                        emoji = "⭐"
                        status = "Strong Match"
                    elif match_percentage >= 55:
                        color = "#FFC107"
                        emoji = "⚡"
                        status = "Good Potential"
                    elif match_percentage >= 40:
                        color = "#FF9800"
                        emoji = "🔧"
                        status = "Needs Enhancement"
                    else:
                        color = "#F44336"
                        emoji = "🚨"
                        status = "Significant Gaps"
                    
                    st.markdown(f"""
                    <div class="match-score" style="border-left: 3px solid {color};">
                        <div style="color: {color};">
                            {emoji} <b>{match_percentage}%</b>
                        </div>
                        <div style="font-size: 1.2rem; margin: 0.5rem 0;">
                            {status}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar
                    st.progress(match_percentage / 100)
                else:
                    st.warning("⚠️ Could not extract match percentage. Review the analysis below.")
                
                # Analysis Content
                st.markdown("### 📋 Analysis Report")
                st.markdown("---")
                
                # Display the analysis
                analysis_formatted = analysis.replace("**", "**").replace("*", "*")
                st.markdown(analysis_formatted)
                
                # Action buttons
                st.markdown("---")
                st.markdown("### 🎯 Next Steps")
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Generate report in session to avoid reloading
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ATS_Analysis_Report_{timestamp}.txt"
                    
                    extracted_words = len(resume_text.split())
                    job_desc_words = len(job_description.split())
                    
                    detailed_report = f"""
===============================================================
                ATS RESUME ANALYSIS REPORT
===============================================================

📊 ANALYSIS SUMMARY:
• Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Match Score: {match_percentage}%
• Resume Words: {extracted_words:,}
• Job Description Words: {job_desc_words:,}

===============================================================
                    DETAILED ANALYSIS
===============================================================

{analysis}

===============================================================
                     REPORT FOOTER
===============================================================

📌 Generated by ATS Resume Analyzer by safagoek
🔗 Platform: OpenRouter API with DeepSeek Chat v3
📅 Version: 2.0 | Date: {datetime.now().strftime('%Y-%m-%d')}

💡 IMPORTANT NOTES:
• This analysis is AI-generated and should be used as guidance
• Consider industry-specific requirements not covered here
• Review with a human recruiter for best results
• Update your resume based on priority recommendations

===============================================================
                     END OF REPORT
===============================================================
"""
                    
                    # Use download button with on_click handler to avoid page refresh
                    st.download_button(
                        label="📥 Download Report",
                        data=detailed_report,
                        file_name=filename,
                        mime="text/plain",
                        key="download_report"
                    )
                
                with col2:
                    if st.button("🔄 New Analysis", type="secondary"):
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Celebration effect
                st.balloons()
                
            else:
                progress_bar.empty()
                status_text.empty()
                st.error("❌ AI Analysis Failed. Please check your connection and try again.")
        else:
            progress_bar.empty()
            status_text.empty()
            if not resume_text:
                st.error("❌ PDF Processing Failed. Please ensure your PDF is readable.")
            else:
                st.error("❌ Resume Content Too Brief for meaningful analysis.")
# Show previous analysis if it exists
elif st.session_state.analysis_result is not None:
    # Display the previous analysis
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    st.markdown("## 📊 Previous Analysis Report")
    
    # Match Score Display
    if st.session_state.match_percentage is not None:
        match_percentage = st.session_state.match_percentage
        
        if match_percentage >= 85:
            color = "#4CAF50"
            emoji = "🎉"
            status = "Outstanding Match!"
        elif match_percentage >= 70:
            color = "#8BC34A"
            emoji = "⭐"
            status = "Strong Match"
        elif match_percentage >= 55:
            color = "#FFC107"
            emoji = "⚡"
            status = "Good Potential"
        elif match_percentage >= 40:
            color = "#FF9800"
            emoji = "🔧"
            status = "Needs Enhancement"
        else:
            color = "#F44336"
            emoji = "🚨"
            status = "Significant Gaps"
        
        st.markdown(f"""
        <div class="match-score" style="border-left: 3px solid {color};">
            <div style="color: {color};">
                {emoji} <b>{match_percentage}%</b>
            </div>
            <div style="font-size: 1.2rem; margin: 0.5rem 0;">
                {status}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(match_percentage / 100)
    
    # Analysis Content
    st.markdown("### 📋 Analysis Report")
    st.markdown("---")
    
    # Display the analysis
    analysis_formatted = st.session_state.analysis_result.replace("**", "**").replace("*", "*")
    st.markdown(analysis_formatted)
    
    # Action buttons
    st.markdown("---")
    st.markdown("### 🎯 Next Steps")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Generate report from stored session data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ATS_Analysis_Report_{timestamp}.txt"
        
        extracted_words = len(st.session_state.resume_text.split())
        job_desc_words = len(st.session_state.job_description.split())
        
        detailed_report = f"""
===============================================================
                ATS RESUME ANALYSIS REPORT
===============================================================

📊 ANALYSIS SUMMARY:
• Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Match Score: {st.session_state.match_percentage}%
• Resume Words: {extracted_words:,}
• Job Description Words: {job_desc_words:,}

===============================================================
                    DETAILED ANALYSIS
===============================================================

{st.session_state.analysis_result}

===============================================================
                     REPORT FOOTER
===============================================================

📌 Generated by ATS Resume Analyzer by safagoek
🔗 Platform: OpenRouter API with DeepSeek Chat v3
📅 Version: 2.0 | Date: {datetime.now().strftime('%Y-%m-%d')}

💡 IMPORTANT NOTES:
• This analysis is AI-generated and should be used as guidance
• Consider industry-specific requirements not covered here
• Review with a human recruiter for best results
• Update your resume based on priority recommendations

===============================================================
                     END OF REPORT
===============================================================
"""
        
        # Download button uses session state data
        st.download_button(
            label="📥 Download Report",
            data=detailed_report,
            file_name=filename,
            mime="text/plain",
            key="download_report_previous"
        )
    
    with col2:
        if st.button("🔄 New Analysis", type="secondary"):
            # Clear the previous analysis
            st.session_state.analysis_result = None
            st.session_state.resume_text = None
            st.session_state.job_description = None
            st.session_state.match_percentage = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer with information
st.markdown("""
<div class="footer" style="text-align: center; font-size: 14px; color: #555;">
    <p><strong>ATS Resume Analyzer v2.0</strong> | Developed by safagoek</p>
    <p>Powered by OpenRouter AI with DeepSeek Chat v3</p>
    <p>© 2025 | <a href="https://github.com/safagoek/resume_anlyzer" target="_blank" style="color: #667eea;">GitHub Repository</a></p>
    <p>This tool helps job seekers optimize their resumes for Applicant Tracking Systems (ATS)</p>
    <p>For questions and more: <a href="https://linkedin.com/in/safa-gök" target="_blank" style="color: #667eea;">LinkedIn Profile</a></p>
</div>
""", unsafe_allow_html=True)

