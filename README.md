# Resume ↔ Job Description Matcher

A full-stack tool that scores how well a resume matches a job description and
highlights which skills from the posting are missing from the resume.

**Problem:** Job seekers apply to dozens of postings without knowing how well
their resume actually matches. This tool gives an instant score and a
concrete list of missing keywords so applicants can tailor their resume
before applying.

🔗 **Live demo:** https://resume-job-matcher-khaki-sigma.vercel.app/

## How it works

1. The user uploads a resume (PDF, DOCX, or TXT) and pastes a job description.
2. The backend extracts raw text from the resume file.
3. Both texts are vectorized using **TF-IDF** (term frequency–inverse document
   frequency) and compared using **cosine similarity** to produce an overall
   match score.
4. Both texts are separately scanned against a predefined list of ~100
   technical and professional skill keywords to compute which skills are
   matched vs. missing.

## Tech stack

- **Frontend:** React (Vite)
- **Backend:** FastAPI (Python)
- **NLP/ML:** scikit-learn (TF-IDF + cosine similarity)
- **File parsing:** pdfplumber (PDF), python-docx (DOCX)

## Project structure

```
resume-job-matcher/
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI app + /match endpoint
│   │   ├── matcher.py    # Core TF-IDF matching + keyword extraction logic
│   │   └── parser.py     # Resume file text extraction (PDF/DOCX/TXT)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main UI component
│   │   ├── App.css       # Styles
│   │   └── main.jsx
│   └── package.json
├── sample_data/           # Example resume + job description for testing
└── SETUP_GUIDE.md          # Full step-by-step run instructions (VS Code)
```

