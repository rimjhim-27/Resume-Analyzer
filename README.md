# Resume Analyzer v3

Resume Analyzer v3 is a Streamlit-based application that helps job seekers evaluate their resumes, understand ATS compatibility, and receive personalized improvement suggestions.

## Features
- ATS score analysis across multiple resume dimensions
- Skill gap identification and role prediction
- Personalized learning roadmap suggestions
- Visual charts for resume quality and improvement areas
- Clean interactive dashboard for easy review

## Project Structure
```text
resume-analyzer-v3/
├── app.py                    # Main Streamlit application
├── ats_calculator.py         # ATS scoring logic
├── resume_classifier.py      # Role prediction engine
├── skills_database.py        # Skill database and scoring weights
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .streamlit/config.toml    # Streamlit theme settings
├── resumes/
│   ├── resume_parser.py      # Resume text parsing logic
│   └── skill_extractor.py    # Skill extraction logic
└── utils/
    ├── charts.py             # Visualization helpers
    ├── suggestions.py        # Improvement recommendations
    ├── roadmap_generator.py  # Learning roadmap generation
    └── wordcloud_generator.py
```

## Installation
```bash
pip install -r requirements.txt
```

## Run the App
```bash
streamlit run app.py
```

## Usage
1. Launch the app with Streamlit.
2. Upload or analyze a resume.
3. Review the ATS score, skill gaps, and suggestions.
4. Use the roadmap to improve your resume for target roles.

## License
This project is for educational and personal use.

