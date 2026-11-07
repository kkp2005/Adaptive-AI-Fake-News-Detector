import os
import sqlite3
from pathlib import Path
from typing import Literal

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSequenceClassification

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = Path(os.getenv("MODEL_DIR", BASE_DIR / "models" / "fake-news-bert"))
DB_PATH = Path(os.getenv("FEEDBACK_DB", BASE_DIR / "feedback.db"))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = FastAPI(
    title="Adaptive AI - Fake News Detector API",
    description="BERT-based experimental news-text classification API.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer = None
model = None
model_error = None

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                label INTEGER NOT NULL CHECK(label IN (0, 1)),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def load_model():
    global tokenizer, model, model_error
    if not MODEL_DIR.exists():
        model_error = (
            f"Trained model not found at {MODEL_DIR}. "
            "Prepare a labelled CSV dataset and run the training command in README.md."
        )
        return
    try:
        tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
        model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))
        model.to(DEVICE)
        model.eval()
        model_error = None
    except Exception as exc:
        model_error = str(exc)
        tokenizer = model = None

init_db()
load_model()

class PredictRequest(BaseModel):
    text: str = Field(min_length=10, max_length=10000)

class FeedbackRequest(BaseModel):
    text: str = Field(min_length=10, max_length=10000)
    label: Literal["REAL", "FAKE"]

@app.get("/")
def root():
    return {"name": "Adaptive AI - Fake News Detector", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "device": str(DEVICE), "model_ready": model is not None}

@app.get("/model/status")
def model_status():
    return {
        "model_ready": model is not None,
        "model_name": "BERT fine-tuned for fake-news classification",
        "device": str(DEVICE),
        "message": "Model loaded and ready." if model is not None else model_error,
    }

def find_feedback(text: str):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT label FROM feedback WHERE lower(trim(text)) = lower(trim(?)) ORDER BY id DESC LIMIT 1",
            (text,),
        ).fetchone()
    return row[0] if row else None

@app.post("/predict")
def predict(payload: PredictRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Please enter news text.")

    remembered = find_feedback(text)
    if remembered is not None:
        return {
            "label": "REAL" if remembered == 0 else "FAKE",
            "confidence": None,
            "source": "saved_feedback",
            "note": "This exact text has a saved human feedback label. It is not a new model prediction.",
        }

    if model is None or tokenizer is None:
        raise HTTPException(
            status_code=503,
            detail="The trained BERT model is not ready. Follow the dataset training steps in README.md.",
        )

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
    with torch.inference_mode():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=1)[0]
    predicted = int(torch.argmax(probabilities).item())
    confidence = float(probabilities[predicted].item())

    return {
        "label": "REAL" if predicted == 0 else "FAKE",
        "confidence": round(confidence, 4),
        "source": "bert_model",
        "note": "Confidence is the model's score, not proof that the news is true or false.",
    }

@app.post("/feedback")
def add_feedback(payload: FeedbackRequest):
    label_id = 0 if payload.label == "REAL" else 1
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO feedback(text, label) VALUES (?, ?)",
            (payload.text.strip(), label_id),
        )
        conn.commit()
    return {"message": "Feedback saved.", "label": payload.label}

@app.get("/feedback")
def list_feedback():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT id, text, label, created_at FROM feedback ORDER BY id DESC LIMIT 100"
        ).fetchall()
    return [
        {"id": r[0], "text": r[1], "label": "REAL" if r[2] == 0 else "FAKE", "created_at": r[3]}
        for r in rows
    ]
