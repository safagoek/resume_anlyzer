# 📝 ATS Resume Analyzer

AI-powered resume analysis tool that scores and optimizes resumes against job descriptions using ATS (Applicant Tracking System) standards.

## 🚀 Features

- **Smart Resume Scoring**: Get percentage match scores between your resume and job requirements
- **Comprehensive Analysis**: Detailed feedback on skills, experience, and qualifications alignment
- **ATS Optimization**: Keyword suggestions and formatting recommendations for better ATS compatibility
- **Professional Reports**: Downloadable analysis reports for future reference
- **Real-time Processing**: Fast PDF text extraction and AI-powered analysis

## 🔧 Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **AI Processing**: OpenRouter API with DeepSeek Chat v3 model
- **PDF Processing**: PyMuPDF for text extraction
- **Deployment**: Streamlit Cloud

## 🎯 How It Works

1. **Upload Resume**: Upload your PDF resume (ensures text is selectable)
2. **Paste Job Description**: Add complete job posting details
3. **AI Analysis**: Advanced AI compares resume against job requirements
4. **Get Results**: Receive match score and detailed improvement suggestions
5. **Download Report**: Save analysis for resume optimization

## 📊 Analysis Features

- **Match Percentage**: Clear scoring with detailed breakdown
- **Key Strengths**: Highlighted skills and experiences that align
- **Missing Qualifications**: Critical gaps and requirements not met
- **Skill Gaps**: Technical and soft skills needing development
- **ATS Optimization**: Keywords and formatting improvements
- **Actionable Recommendations**: Specific steps for resume enhancement

## 🌐 Live Demo

Visit the live application: [ATS Resume Analyzer](https://resume-analyzer-safagoek.streamlit.app)

## 💻 Local Development

### Prerequisites
- Python 3.8+
- OpenRouter API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ats-resume-analyzer.git
cd ats-resume-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
OPENROUTER_API_KEY=your_api_key_here
SITE_URL=http://localhost:8501
SITE_NAME=ATS Resume Analyzer - Local
```

4. Run the application:
```bash
streamlit run app.py
```

## 🔑 API Configuration

This app uses OpenRouter API for AI analysis. To set up:

1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Create account and generate API key
3. Add key to Streamlit secrets or environment variables

## 📱 Deployment

### Streamlit Cloud Deployment

1. Fork this repository
2. Connect to [Streamlit Cloud](https://share.streamlit.io)
3. Add secrets in app settings:
   ```toml
   OPENROUTER_API_KEY = "your-api-key"
   SITE_URL = "https://your-app-url.streamlit.app"
   SITE_NAME = "Your App Name"
   ```
4. Deploy and share!

## 🛡️ Features & Limitations

### ✅ Supported
- PDF resume uploads (text-selectable)
- Comprehensive job description analysis
- Multi-language support (AI model dependent)
- Professional report generation
- Mobile-responsive design

### ⚠️ Limitations
- PDF must have selectable text (not scanned images)
- OpenRouter API rate limits apply
- Analysis quality depends on input detail
- No personal data storage (privacy-focused)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Safa Gök**
- LinkedIn: [linkedin.com/in/safa-gök](https://linkedin.com/in/safa-gök)
- GitHub: [@safagoek](https://github.com/safagoek)

## 🙏 Acknowledgments

- OpenRouter for AI API access
- Streamlit for the amazing framework
- PyMuPDF for PDF processing capabilities

---

**Made with ❤️ for job seekers worldwide**