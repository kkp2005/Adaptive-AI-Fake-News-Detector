# \# Adaptive AI â€” Fake News Detector

#

# An AI-powered fake news classification web application built using a fine-tuned BERT model, FastAPI, and React. The application analyzes a news article and predicts whether its content is likely to be REAL or FAKE.

#

# > \*\*Academic project:\*\* This system is a machine-learning prototype, not a definitive fact-checking service. Predictions and confidence scores should not be treated as proof that a claim is true or false.

#

# \## Features

#

# \- \*\*BERT-based classification:\*\* Uses a fine-tuned `bert-base-uncased` model for text classification.

# \- \*\*Interactive web interface:\*\* React and Vite frontend for submitting news articles.

# \- \*\*REST API:\*\* FastAPI backend for model inference.

# \- \*\*Model status:\*\* Endpoint to check whether the model is loaded and ready.

# \- \*\*Sample dataset:\*\* A smaller CSV file is included for demonstration and data-format reference.

# \- \*\*Training workflow:\*\* Python scripts and a notebook support dataset preparation and model training.

#

# \## Technology Stack

#

# | Component | Technologies |

# |---|---|

# | Frontend | React, Vite, JavaScript, CSS |

# | Backend | Python, FastAPI, Uvicorn |

# | NLP | BERT, Hugging Face Transformers |

# | Machine learning | PyTorch, scikit-learn |

# | Data processing | Pandas |

# | Development tools | Git, VS Code, Google Colab |

#

# \## Project Architecture

#

# 1\. The user enters a news article in the React interface.

# 2\. The frontend sends the text to the FastAPI backend.

# 3\. The backend tokenizes the text using the BERT tokenizer.

# 4\. The fine-tuned model generates a classification prediction.

# 5\. The backend returns the predicted label and confidence score.

# 6\. The frontend displays the result.

#

# \## Repository Structure

#

# ```text

# Adaptive-AI-Fake-News-Detector/

# â”œâ”€â”€ backend/

# â”‚   â”œâ”€â”€ main.py

# â”‚   â”œâ”€â”€ train.py

# â”‚   â””â”€â”€ requirements.txt

# â”œâ”€â”€ data/

# â”‚   â””â”€â”€ news\_small.csv

# â”œâ”€â”€ frontend/

# â”‚   â”œâ”€â”€ src/

# â”‚   â”‚   â”œâ”€â”€ App.jsx

# â”‚   â”‚   â”œâ”€â”€ main.jsx

# â”‚   â”‚   â””â”€â”€ style.css

# â”‚   â”œâ”€â”€ .env.example

# â”‚   â”œâ”€â”€ package.json

# â”‚   â””â”€â”€ vite.config.js

# â”œâ”€â”€ notebooks/

# â”‚   â”œâ”€â”€ Fake\_News\_ULTIMATE\_PLUS.ipynb

# â”‚   â””â”€â”€ README.txt

# â”œâ”€â”€ prepare\_data.py

# â”œâ”€â”€ reduce\_data.py

# â”œâ”€â”€ .gitignore

# â””â”€â”€ README.md

# ```

#

# \## Requirements

#

# Install the following before running the project:

#

# \- Python 3.10 or 3.11

# \- Node.js and npm

# \- Git

#

# \## Model Setup

#

# The fine-tuned BERT model files are not included in this GitHub repository because they are large.

#

# To run predictions, place the trained model and tokenizer files in:

#

# `backend/models/fake-news-bert/`

#

# The directory should contain the model configuration, model weights, and tokenizer files.

#

# Alternatively, configure the `MODEL\_DIR` environment variable to point to your model directory, if supported by your backend configuration.

#

# The model must be loaded successfully before predictions can be made. Check the model status endpoint to confirm readiness.

#

# \## Installation and Execution

#

# \### 1. Clone the repository

#

# ```bash

# git clone https://github.com/kkp2005/Adaptive-AI-Fake-News-Detector.git

# cd Adaptive-AI-Fake-News-Detector

# ```

#

# \### 2. Set up the backend

#

# Open a terminal in the project root and run:

#

# ```powershell

# python -m venv venv

# .\\venv\\Scripts\\Activate.ps1

# python -m pip install --upgrade pip

# pip install -r backend/requirements.txt

# ```

#

# If PowerShell blocks virtual-environment activation, run:

#

# ```powershell

# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# .\\venv\\Scripts\\Activate.ps1

# ```

#

# Start the backend:

#

# ```powershell

# cd backend

# python -m uvicorn main:app --reload

# ```

#

# The API will normally be available at `http://127.0.0.1:8000`.

#

# Interactive API documentation: `http://127.0.0.1:8000/docs`

#

# \### 3. Set up the frontend

#

# Open a second terminal in the project root:

#

# ```powershell

# cd frontend

# npm install

# Copy-Item .env.example .env

# npm run dev

# ```

#

# Open the local URL displayed by Vite, normally `http://localhost:5173`.

#

# Keep the backend and frontend terminals running while testing the application.

#

# \## API Endpoints

#

# | Method | Endpoint | Purpose |

# |---|---|---|

# | GET | `/health` | Check backend health |

# | GET | `/model/status` | Check model readiness |

# | POST | `/predict` | Classify news text |

#

# Refer to the interactive API documentation at `/docs` for the request formats and available endpoints.

#

# \## Dataset

#

# The repository includes `data/news\_small.csv` as a small sample dataset. Larger CSV files used during development and training are intentionally excluded from GitHub.

#

# Use a sufficiently large, diverse, correctly labelled dataset for meaningful evaluation. Check the dataset's licence and attribution requirements before redistributing it.

#

# \## Model Evaluation and Limitations

#

# A model prediction is not the same as independent verification of a news claim. The model may misclassify articles, especially when they concern unfamiliar topics, satire, evolving events, or misleading wording.

#

# Confidence scores indicate the model's relative confidence in its prediction; they do not establish factual accuracy.

#

# Evaluate the model using a held-out labelled test set and report appropriate metrics, such as accuracy, precision, recall, F1-score, and a confusion matrix. Do not claim a performance percentage unless it has been measured and verified.

#

# \## Security and Large Files

#

# \- Do not commit API keys, passwords, or private environment files.

# \- Do not upload virtual environments or `node\_modules`.

# \- Model weights and large training datasets are excluded from the repository.

# \- Configure environment variables locally and keep secrets out of source control.

#

# \## Future Improvements

#

# \- Add verified evaluation metrics and test reports.

# \- Improve explainability and error analysis.

# \- Add trusted-source links to assist independent fact-checking.

# \- Deploy the frontend and backend for public demonstration.

# \- Explore model monitoring and retraining with carefully labelled data.

#

# \## Disclaimer

#

# This project is developed for academic and educational purposes. It should be used as an aid to news analysis, not as a replacement for human judgement or verification from reliable sources.
