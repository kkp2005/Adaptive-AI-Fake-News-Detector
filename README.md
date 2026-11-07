# Adaptive AI — Fake News Detector

A full-stack academic prototype that wraps the original Google Colab BERT fake-news notebook in a React frontend and FastAPI backend.

## Stack
- Frontend: React + Vite
- Backend: Python + FastAPI
- NLP model: BERT (`bert-base-uncased`) fine-tuned with Hugging Face Transformers
- ML: PyTorch, scikit-learn
- Feedback persistence: SQLite

## Important model limitation
The supplied Colab notebook creates only six toy examples (three REAL and three FAKE). That is not enough to train a reliable fake-news detector. This repository therefore does **not** include a pre-trained/fine-tuned model. The API clearly reports when the model is not ready instead of pretending to make valid predictions.

The small `data/news.csv` file is only a format/demo example. Replace it with a larger, diverse, carefully labelled dataset before evaluating or presenting model accuracy. Verify claims against trusted sources; model confidence is not factual proof.

## Project structure
```text
adaptive-ai-fake-news-detector/
├── backend/
│   ├── main.py
│   ├── train.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── data/news.csv
├── notebooks/Fake_News_ULTIMATE_PLUS.ipynb
├── .gitignore
└── README.md
```

## 1. Requirements
Install:
- Python 3.10 or 3.11
- Node.js 20 or later
- Git

## 2. Backend setup (Windows PowerShell)
Open a terminal in the project folder:

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Train the model
From the project root, after activating the backend environment:

```powershell
python backend/train.py --csv data/news.csv --epochs 3
```

This downloads the base BERT model and fine-tunes it. Training may take a long time and may need substantial RAM/GPU. The included tiny CSV is only a pipeline smoke test, not a meaningful training dataset. Use a larger labelled dataset for a useful model.

### Start the API
From the project root:
```powershell
uvicorn backend.main:app --reload
```
Open API docs: http://127.0.0.1:8000/docs

If Python cannot import `backend.main`, run from the project root and ensure `backend` is a Python package by creating an empty `backend/__init__.py`.

## 3. Frontend setup
Open a second terminal:
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```
Open the local website shown by Vite (normally http://localhost:5173).

## 4. API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Backend health |
| GET | `/model/status` | Model readiness |
| POST | `/predict` | Predict REAL / FAKE |
| POST | `/feedback` | Save a human correction |
| GET | `/feedback` | List recent feedback |

Example prediction request:
```json
{"text":"The election commission released the official voting schedule."}
```

Example feedback request:
```json
{"text":"The election commission released the official voting schedule.","label":"REAL"}
```

## 5. GitHub upload
Create a new empty repository on GitHub, then from the project root:

```powershell
git init
git add .
git commit -m "Initial full-stack Adaptive AI fake news detector"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Do not commit `.env`, API keys, virtual environments, model checkpoints, or SQLite feedback databases.

## 6. Deployment
- Frontend: deploy the `frontend` folder on Vercel or Netlify. Set `VITE_API_URL` to your deployed backend URL.
- Backend: deploy the FastAPI app on Render or another Python host. Configure `CORS_ORIGINS` to your frontend domain.
- Model hosting: BERT model files are large. Ensure the backend host has enough disk, RAM, and preferably GPU resources. A free/small instance may not be suitable.

## 7. Original notebook integration notes
The notebook's `predict()` and `explain()` logic is represented in the API. Feedback is now persisted in SQLite rather than only in in-memory Python lists. The original notebook's `trainer.train()` feedback retraining behavior was not copied as-is because its training dataset was not updated correctly; retraining is performed explicitly from a labelled CSV using `train.py`.

## License and dataset
Check the licence and terms of any external dataset/model before redistribution. Keep dataset attribution in the repository.
