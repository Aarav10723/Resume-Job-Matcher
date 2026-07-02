"""
Core matching logic for the Resume <-> Job Description matcher.

Approach:
1. Clean both texts.
2. Vectorize both texts using TF-IDF (term frequency-inverse document frequency).
3. Compute cosine similarity between the two TF-IDF vectors -> overall match score.
4. Separately, scan both texts against a predefined list of common tech/professional
   skills to find which skills are mentioned in the job description but missing
   from the resume (and which ones matched).

Why TF-IDF + cosine similarity instead of a transformer embedding model:
- No large model download required (works fully offline after `pip install`)
- Fast, deterministic, and easy to explain in an interview
- A reasonable baseline NLP technique for a first project
  (See README "Stretch Goals" for how to upgrade this to sentence embeddings later.)
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# A predefined list of common tech/professional skills and keywords.
# This is intentionally simple -- feel free to expand this list for your resume story
# ("I built a keyword list of ~120 terms and matched them against both texts").
SKILL_KEYWORDS = [
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "r", "go",
    "rust", "swift", "kotlin", "php", "ruby", "scala", "matlab",
    # Web / frontend
    "react", "angular", "vue", "html", "css", "next.js", "node.js", "express",
    "redux", "tailwind", "bootstrap",
    # Backend / infra
    "fastapi", "flask", "django", "spring", "rest api", "graphql", "microservices",
    "docker", "kubernetes", "ci/cd", "jenkins", "terraform", "linux",
    # Data / ML
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "data analysis", "data visualization", "tableau", "power bi", "etl",
    "data pipeline", "statistics", "regression", "classification", "clustering",
    # Cloud
    "aws", "azure", "gcp", "cloud computing", "lambda", "s3", "ec2",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "sqlite", "database design",
    # Tools / practices
    "git", "github", "agile", "scrum", "jira", "unit testing", "debugging",
    "object-oriented programming", "data structures", "algorithms", "api design",
    # Soft skills (recruiters often screen for these too)
    "communication", "leadership", "teamwork", "problem solving", "project management",
    "collaboration", "mentoring", "presentation",
]


def clean_text(text: str) -> str:
    """Lowercase and strip excess whitespace/special characters for consistent matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\+\#\./]", " ", text)  # keep tokens like c++, c#, node.js
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_similarity_score(resume_text: str, job_text: str) -> float:
    """
    Returns a 0-1 similarity score between the resume and job description
    using TF-IDF vectorization + cosine similarity.
    """
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_text)

    if not resume_clean or not job_clean:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_clean, job_clean])

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(score), 4)


def extract_keywords(text: str) -> list[str]:
    """Return which predefined skill keywords appear in the given text."""
    text_clean = clean_text(text)
    found = []
    for skill in SKILL_KEYWORDS:
        skill_clean = clean_text(skill)
        # word-boundary-safe check, works for multi-word skills too
        if re.search(r"(?<!\w)" + re.escape(skill_clean) + r"(?!\w)", text_clean):
            found.append(skill)
    return found


def compare_resume_to_job(resume_text: str, job_text: str) -> dict:
    """
    Main entry point: given raw resume text and raw job description text,
    returns the match score and keyword breakdown.
    """
    score = compute_similarity_score(resume_text, job_text)

    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = set(extract_keywords(job_text))

    matched = sorted(resume_keywords & job_keywords)
    missing = sorted(job_keywords - resume_keywords)

    return {
        "score": score,
        "score_percent": round(score * 100, 1),
        "matched_keywords": matched,
        "missing_keywords": missing,
    }


if __name__ == "__main__":
    # Quick manual test -- run with: python matcher.py
    sample_resume = """
    Experienced software engineer skilled in Python, React, and SQL.
    Built REST APIs using FastAPI and deployed applications on AWS.
    Strong background in data structures, algorithms, and Git-based workflows.
    """
    sample_job = """
    Looking for a software engineer with experience in Python, React, Docker,
    and Kubernetes. Familiarity with AWS, CI/CD pipelines, and machine learning
    is a plus. Strong communication and teamwork skills required.
    """
    result = compare_resume_to_job(sample_resume, sample_job)
    print(result)
