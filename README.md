# 🏏 CricketArena: AI-Powered Gamified Platform

CricketArena is a next-generation, gamified cricket prediction and fantasy platform built for hackathons and modern fan engagement. It leverages **Google Gemini 2.5 Flash**, **Streamlit**, and **Google Cloud Run** to deliver an immersive, interactive experience.

## ✨ High-Impact Features

- **🎮 The "What-If" Simulator**: Enter a custom match scenario (e.g., *"What if Rohit hits 3 sixes?"*). Gemini processes the timeline and outputs a dynamic cascading effect on Win Probability, visualized via Plotly.
- **🤖 AI Fantasy Optimizer**: An AI assistant that analyzes pitch conditions and player form to instantly auto-generate your perfect 11-man Fantasy squad within a strict 100-credit budget.
- **📊 Live Match Momentum Meter**: Animated, real-time Plotly charts tracking Win Probability versus Pressure Index.
- **🎙️ Voice Commentary**: Text-to-speech integration (`gTTS`) that reads Gemini's cricket analysis aloud, turning the app into a live broadcast companion.
- **✨ Dynamic Gamification**: Zero-config state persistence tracking XP, streak levels, and badges.
- **📱 Modern Glass UI**: A beautiful, responsive interface utilizing `streamlit-option-menu` and CSS-only rotating insight tickers for a premium feel.
- **📈 Admin Hub**: A dedicated global analytics dashboard tracking active users, total predictions, and fantasy selection trends.

## 🚀 Google Cloud Deployment

This app is containerized using Docker and designed for serverless deployment on **Google Cloud Run**. 

### Deploy via Cloud Shell:
```bash
git clone https://github.com/balachandarchinta/WorkingArena.git
cd WorkingArena

gcloud run deploy cricketarena-streamlit \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --set-env-vars GEMINI_API_KEY="YOUR_API_KEY" \
  --port 8501
```

## 🛠️ Run Locally

1. Create a virtual environment and install dependencies:
```bash
pip install -r streamlit_app/requirements.txt
```

2. Add your Google Gemini API key to Streamlit secrets:
Create `.streamlit/secrets.toml` and add:
```toml
GEMINI_API_KEY = "your_key_here"
```

3. Boot up the server:
```bash
streamlit run streamlit_app/app.py
```

## 🏗️ Tech Stack
- **Frontend/Backend Engine**: Streamlit (Python 3.11)
- **AI Brain**: Google GenAI SDK (`gemini-2.5-flash`)
- **Data Visualization**: Plotly, Pandas
- **Audio Generation**: Google Text-to-Speech (`gTTS`)
- **Infrastructure**: Google Cloud Run / Docker
