# Resume ↔ Job Description Matcher

A full-stack tool that scores how well a resume matches a job description and
highlights which skills from the posting are missing from the resume.

**Problem:** Job seekers apply to dozens of postings without knowing how well
their resume actually matches. This tool gives an instant score and a
concrete list of missing keywords so applicants can tailor their resume
before applying.

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

## Quick start

See **SETUP_GUIDE.md** for full step-by-step instructions with VS Code.

Short version:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (in a second terminal)
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173` in your browser.

## Deployment

- **Frontend:** Deploy to [Vercel](https://vercel.com) — connect your GitHub
  repo, set the root directory to `frontend`, it auto-detects Vite.
- **Backend:** Deploy to [Render](https://render.com) or
  [Railway](https://railway.app) — connect your repo, set the root directory
  to `backend`, build command `pip install -r requirements.txt`, start
  command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- After deploying the backend, update `API_URL` in `frontend/src/App.jsx` to
  your live backend URL, and add your deployed frontend URL to the
  `allow_origins` list in `backend/app/main.py`.

## What I'd improve

- Upgrade keyword extraction from a fixed skill list to a trained NER model
- Upgrade TF-IDF similarity to sentence-transformer embeddings for better
  semantic matching (captures meaning, not just word overlap)
- Add user accounts and comparison history (Postgres + auth)
- Support scanned/image-based PDFs with OCR
