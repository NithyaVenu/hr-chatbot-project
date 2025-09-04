# hr-chatbot-project
 
# HR Resource Chatbot - Full Project

This repository contains a lightweight FastAPI backend and a React + TypeScript frontend (Vite + Tailwind).
The project is intended to run locally.

## Run Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Run Frontend
```bash
cd frontend
npm install
npm run dev
```

Open the frontend at http://localhost:5173 (Vite default) and backend at http://localhost:8000

## Link to app
https://68b93cf282180ae732064f0b--glowing-kashata-adaf20.netlify.app/


## Notes
- The backend implements simple heuristic retrieval (no heavy ML dependencies). You can extend it later to add embeddings (sentence-transformers) and vector search.
- If you want to enable an LLM-based response, add code to the backend to call OpenAI or another provider.
