# AmalGus — Smart Product Discovery & Matching

AmalGus is a prototype B2B marketplace application for the glass industry, featuring **semantic search** to match natural-language buyer queries against a product catalog using AI.
# Demo Video Url 
https://drive.google.com/file/d/1a_A7sHyRA__n4G5HondJKOjmnyF0O8Yb/view?usp=sharing

## Project Structure

- `/` - FastAPI Backend (Semantic Matcher)
- `/frontend` - React + Tailwind CSS Frontend (Discovery UI)

---

## 🚀 Backend (FastAPI)

Uses `Sentence Transformers` and `NumPy` to compute embeddings and cosine similarity.

### Setup & Run
```bash
# 1. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the API
uvicorn main:app --reload
```
API runs on: `http://localhost:8000`
Docs: `http://localhost:8000/docs`

---

## 💻 Frontend (React)

Modern Discovery UI built with Vite, Tailwind CSS, and Framer-motion inspired animations.

### Setup & Run
```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Edit .env to point to your backend URL

# 3. Start development server
npm run dev
```
Dev server runs on: `http://localhost:5173`

---

## 📦 Deployment Readiness

### Deployment Config
- **Backend**: Serve with `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Frontend**: 
  - Build using `npm run build`
  - Set the `VITE_API_URL` environment variable to your production backend URL during the build process.

### Environment Variables
| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | (Frontend) URL of the running FastAPI backend. |

## Feature Set
- **Semantic Matching**: Understands technical intent (e.g., "6mm tempered" vs "thickness requirements").
- **Dynamic Explanations**: Generates human-readable reasoning for matches.
- **Smart Filters**: Combines vector search with hard filters (Category, Price, Thickness).
- **Modern UI**: Full-featured prototype with loading skeletons, error handling, and suggestions.
