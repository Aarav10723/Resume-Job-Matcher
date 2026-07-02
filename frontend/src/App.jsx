import { useState } from "react";
import "./App.css";

// If you deploy the backend elsewhere, change this URL (see README "Deployment").
const API_URL = "http://localhost:8000";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0] || null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!resumeFile) {
      setError("Please upload a resume file (PDF, DOCX, or TXT).");
      return;
    }
    if (!jobDescription.trim()) {
      setError("Please paste a job description.");
      return;
    }

    const formData = new FormData();
    formData.append("resume_file", resumeFile);
    formData.append("job_description", jobDescription);

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/match`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || "Something went wrong. Please try again.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Could not reach the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const scoreLabel = (percent) => {
    if (percent >= 70) return "Strong match";
    if (percent >= 40) return "Partial match";
    return "Low match";
  };

  return (
    <div className="page">
      <header className="header">
        <span className="eyebrow">01 — Upload</span>
        <h1>Resume &rarr; Job Fit</h1>
        <p className="subtitle">
          Upload your resume and paste a job description to see how well they
          match, and exactly which skills you're missing.
        </p>
      </header>

      <form className="card form" onSubmit={handleSubmit}>
        <label className="field">
          <span className="field-label">Resume (PDF, DOCX, or TXT)</span>
          <input type="file" accept=".pdf,.docx,.txt" onChange={handleFileChange} />
        </label>

        <label className="field">
          <span className="field-label">Job description</span>
          <textarea
            rows={8}
            placeholder="Paste the full job posting here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </label>

        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Check my match"}
        </button>
      </form>

      {result && (
        <section className="card result">
          <span className="eyebrow">02 — Result</span>
          <div className="score-row">
            <div className="score-circle">
              <span className="score-number">{result.score_percent}%</span>
            </div>
            <div>
              <h2>{scoreLabel(result.score_percent)}</h2>
              <p className="score-explain">
                Based on overall text similarity between your resume and this
                job description.
              </p>
            </div>
          </div>

          <div className="keywords-grid">
            <div>
              <h3>Matched skills ({result.matched_keywords.length})</h3>
              <div className="tag-list">
                {result.matched_keywords.length === 0 && (
                  <span className="muted">None found</span>
                )}
                {result.matched_keywords.map((kw) => (
                  <span key={kw} className="tag tag-matched">
                    {kw}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3>Missing skills ({result.missing_keywords.length})</h3>
              <div className="tag-list">
                {result.missing_keywords.length === 0 && (
                  <span className="muted">None — great coverage!</span>
                )}
                {result.missing_keywords.map((kw) => (
                  <span key={kw} className="tag tag-missing">
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      <footer className="footer">
        Built with FastAPI, scikit-learn, and React.
      </footer>
    </div>
  );
}

export default App;
