from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.parser import extract_text
from app.matcher import compare_resume_to_job

app = FastAPI(title="Resume Job Matcher API")

# Allow the frontend (running on a different port/domain) to call this API.
# For local dev this covers Vite's default port. Add your deployed frontend
# URL here too once you deploy (see README "Deployment" section).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server default
        "http://127.0.0.1:5173",
        "https://resume-job-matcher-khaki-sigma.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Resume Job Matcher API is running"}


@app.post("/match")
async def match_resume_to_job(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not job_description or not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    file_bytes = await resume_file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded resume file is empty.")

    try:
        resume_text = extract_text(resume_file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract any text from the resume file. "
                   "If it's a scanned/image-based PDF, try a text-based file instead.",
        )

    result = compare_resume_to_job(resume_text, job_description)
    return result
