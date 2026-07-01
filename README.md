# Resume Analyzer v3 — AI-Powered Career Assistant

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features
- Modern dashboard UI matching professional design
- Weighted ATS scoring across 7 dimensions
- Skill gap analysis with color-coded chips
- Role prediction with confidence scores
- 8-week personalized learning roadmap
- Section checklist, radar chart, ATS gauge

## Structure
```
resume-analyzer-v3/
├── app.py                    # Main Streamlit app (full dashboard UI)
├── ats_calculator.py         # Weighted 7-dimension ATS scoring
├── resume_classifier.py      # Role prediction engine
├── skills_database.py        # 110+ skills with weights by category
├── requirements.txt
├── .streamlit/config.toml    # Theme — purple/indigo palette
├── resumes/
│   ├── resume_parser.py      # Layout-aware PDF text extraction
│   └── skill_extractor.py    # Phrase-matching skill extractor
└── utils/
    ├── charts.py             # Gauge, radar, bar, role charts
    ├── suggestions.py        # Prioritized improvement tips
    ├── roadmap_generator.py  # Dynamic 8-week roadmap
    └── wordcloud_generator.py
```
