# Setup Guide — Running This Project in VS Code

This walks through everything from opening the folder in VS Code to seeing
the working app in your browser. Follow it top to bottom — don't skip steps
even if they seem obvious, since a broken environment is the #1 cause of
"it doesn't work" for a first project.

---

## 0. Prerequisites (install these first if you don't have them)

- **VS Code** — https://code.visualstudio.com
- **Python 3.10+** — https://www.python.org/downloads (on install, check
  "Add Python to PATH" on Windows)
- **Node.js 18+** — https://nodejs.org (install the LTS version)
- Verify both are installed by opening a terminal (see step 1) and running:
  ```bash
  python3 --version
  node --version
  ```
  If either command isn't found, close and reopen your terminal/VS Code
  after installing, or restart your computer.

**Recommended VS Code extensions** (open the Extensions panel — the icon
with four squares on the left sidebar — and search for these):
- **Python** (by Microsoft)
- **ES7+ React/Redux/React-Native snippets** (optional, but helpful)

---

## 1. Open the project in VS Code

1. Unzip the project folder you downloaded (`resume-job-matcher.zip`) somewhere
   you'll remember, e.g. `Documents/Projects/resume-job-matcher`.
2. Open VS Code.
3. `File → Open Folder...` → select the unzipped `resume-job-matcher` folder.
4. Open the integrated terminal: `Terminal → New Terminal` (or `` Ctrl+` ``).
   You'll run all commands below in this terminal.

---

## 2. Set up and run the backend

**In the VS Code terminal:**

```bash
cd backend
```

**Create a virtual environment** (keeps this project's Python packages
separate from everything else on your machine):

```bash
python3 -m venv venv
```

**Activate it:**

- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- Windows (PowerShell):
  ```bash
  venv\Scripts\Activate.ps1
  ```
- Windows (Command Prompt):
  ```bash
  venv\Scripts\activate.bat
  ```

You'll know it worked because your terminal prompt now starts with `(venv)`.

> **Tip:** In VS Code, once you have the venv created, press
> `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac), type
> "Python: Select Interpreter", and choose the one inside
> `backend/venv`. This makes VS Code's error-checking and autocomplete
> use the right packages.

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Run the backend server:**

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Verify it's working:** open `http://localhost:8000` in your browser — you
should see `{"status":"ok","message":"Resume Job Matcher API is running"}`.

Also try `http://localhost:8000/docs` — this is FastAPI's built-in interactive
API tester. You can test the `/match` endpoint directly here before ever
touching the frontend, which is a great way to confirm the backend works in
isolation.

**Leave this terminal running.** Don't close it — the server needs to stay
active while you use the app.

---

## 3. Set up and run the frontend

**Open a second terminal** in VS Code: click the `+` icon in the terminal
panel (or `Terminal → New Terminal` again). This keeps your backend running
in the first terminal while you set up the frontend in the second.

```bash
cd frontend
npm install
```

This will take a minute — it's downloading React and its dependencies.

**Run the frontend dev server:**

```bash
npm run dev
```

You should see something like:
```
VITE ready
➜  Local:   http://localhost:5173/
```

**Open `http://localhost:5173` in your browser.** You should see the app.

---

## 4. Test it end-to-end

1. Click the file upload field and select one of the sample files in
   `sample_data/sample_resume.txt`.
2. Copy the contents of `sample_data/sample_job_description.txt` into the
   job description box (open that file in VS Code, select all, copy, paste).
3. Click **"Check my match"**.
4. You should see a score, matched skills, and missing skills appear.

If this works, your full stack is running correctly end to end.

---

## 5. Common problems and fixes

| Problem | Fix |
|---|---|
| `python3: command not found` | Try `python` instead of `python3` (common on Windows) |
| `pip install` fails with permission errors | Make sure your venv is activated (`(venv)` should show in the prompt) |
| Frontend shows "Could not reach the server" | Make sure the backend terminal is still running and shows no errors |
| CORS error in browser console | Confirm the backend is running on port 8000 and frontend on port 5173 — these are hardcoded to match in `main.py` and `App.jsx` |
| `npm install` fails | Delete the `frontend/node_modules` folder and `package-lock.json`, then run `npm install` again |
| Port already in use | Another process is using port 8000 or 5173 — close other terminals running the app, or restart VS Code |

---

## 6. Making changes (your actual dev workflow from here)

- **Backend logic** lives in `backend/app/matcher.py` — this is the file
  you'll most likely want to extend (e.g. add more skill keywords, change
  the similarity algorithm).
- **Frontend UI** lives in `frontend/src/App.jsx` and `App.css`.
- Both servers **auto-reload** when you save a file — you don't need to
  restart them manually while developing.
- Use VS Code's built-in Git panel (source control icon, left sidebar) to
  commit your changes as you go. Commit early, commit often — this also
  gives you a visible commit history on GitHub, which recruiters do look at.

---

## 7. Pushing to GitHub (do this once your app works locally)

In the VS Code terminal, from the project root (`resume-job-matcher/`, not
inside `backend` or `frontend`):

```bash
git init
git add .
git commit -m "Initial working version of resume-job matcher"
```

Then create a new empty repository on GitHub (github.com → New repository →
don't initialize with a README, since you already have one), and follow the
"push an existing repository" instructions GitHub shows you, which will look
like:

```bash
git remote add origin https://github.com/YOUR_USERNAME/resume-job-matcher.git
git branch -M main
git push -u origin main
```

---

## 8. Deploying so you have a live link (do this once it's polished)

See the "Deployment" section in `README.md` for the Vercel + Render steps.
This is the step that turns your project from "code on my laptop" into
something you can actually put a link to on your resume.
