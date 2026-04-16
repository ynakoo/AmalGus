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

## 🧠 AI Tools Used
- **Sentence Transformers (`all-MiniLM-L6-v2`)**: A fast, lightweight embedding model used to capture the semantic meaning of free-text queries and product descriptions. It runs locally without relying on external API calls.
- **NumPy**: Leveraged for ultra-fast cosine similarity calculations. By normalizing our embeddings, we perform highly optimized dot-product multiplications to instantly compare a search query against the entire product catalog.

## 🔍 How the Matching Logic Works
1. **Catalog Pre-processing**: During server startup, every product's distinct data points (name, category, specifications, and long-form description) are flattened into a single, comprehensive string.
2. **Batch Embedding**: The model converts all product strings into 384-dimensional dense vectors and stores them in memory.
3. **Query Vectorization**: When a buyer searches (e.g., *"6mm frosted glass for bathrooms"*), the natural language query is actively embedded using the same Sentence Transformer model.
4. **Semantic Scoring**: The system calculates the cosine similarity between the query vector and all cached product vectors, determining the closest conceptual matches conceptually.
5. **Hard Filtering**: Optional exact-match UI filters (e.g., Max Price, specific Category) are applied as a boolean mask over the semantic scores, instantly pruning disqualified products.
6. **Dynamic Explanations**: A lightweight rule-based extraction system pulls structural keywords (like `6mm` or `bathroom`) from the query and cross-references them with the winning product's specs. This is used to output a human-friendly sentence explaining *why* the product matched.

## 🛑 Assumptions
- **Static In-Memory Catalog**: The current MVP utilizes 12 hardcoded, highly detailed products that are loaded dynamically into memory on startup. It is assumed the product data will not mutate during runtime for this prototype.
- **Text-Primary Search**: It is assumed that queries will primarily rely heavily on textual descriptions and industry specifications rather than image-based reverse search.
- **Synchronous Inference**: CPU-based model inference is handled synchronously.

## ⚖️ Trade-offs
- **Rule-Based Explanations vs. LLM Generation**: 
  - *Trade-off*: We utilize a highly specific regex and keyword-mapping system to generate "Match Explanations" rather than pinging an LLM (like GPT-4) to summarize the reasoning.
  - *Why*: This explicitly removes the high latency and token costs associated with LLMs, ensuring the search feels instantaneous, which is critical for an e-commerce/marketplace prototype.
- **NumPy Dot-Product vs. Vector Databases (Pinecone/Milvus)**: 
  - *Trade-off*: Finding matches via brute-force NumPy array multiplications instead of using an indexed Vector DB.
  - *Why*: For catalogs under a few thousand items, exhaustive distance metrics in NumPy are faster than network calls to an external database. It limits architectural complexity while still delivering accurate semantic search.
- **Local ML Models vs. Free-Tier Deployment Constraints**:
  - *Trade-off*: Running `sentence-transformers` and PyTorch natively on the backend server introduces severe **Memory Limitations** for cloud environments.
  - *Why*: The machine learning model and PyTorch use a significant chunk of memory (~300MB - 400MB). Free tiers on hosting platforms (like Render's Free tier which offers 512MB RAM) barely fit this footprint and frequently fail during build/startup with an "Out of Memory" error. To keep the prototype stable and online, it requires abandoning free-tier hosting for a basic paid tier (e.g., Render's $7/month tier).
