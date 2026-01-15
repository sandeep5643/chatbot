# 🤖 AI Chatbot

A **web-based AI Chatbot** built using **Flask** and **Google Gemini API**.  
It supports **rich markdown formatting**, left-right chat UI, and production-ready deployment.

---

## 🛠 Features

- Chat with AI using **Google Gemini API**  
- Markdown support for formatting responses  
- Styled UI with **user** and **bot messages** alignment  
- Responsive design (works on desktop & mobile)  
- Production-ready with **Render deployment**  
- Easy to update & extend  

---

## ⚡ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **API:** Google Gemini API (Free Tier supported)  
- **Deployment:** Render  

---

## 🚀 Setup & Run Locally

1. Clone the repo:

```bash
git clone https://github.com/sandeep5643/chatbot.git
cd chatbot


## ui and chat flow ready hai ab tisra step LLM Configuration for NVIDIA 

## docker run -p 5000:5000 --env-file .env nvidia-capacity-chatbot
## docker build -t nvidia-capacity-chatbot .

# =========================
# Core Web
# =========================
Flask==2.3.3
gunicorn==21.2.0
python-dotenv==1.0.1
requests==2.31.0
httpx==0.24.1

Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7

# =========================
# LLM Providers
# =========================
openai==1.37.2
groq==0.33.0
typing_extensions>=4.10.0

# =========================
# Market Data
# =========================
yfinance==0.1.87
multitasking==0.0.11

# =========================
# LangChain / RAG
# =========================
langchain==0.1.16
langchain-community==0.0.36
langchain-huggingface==0.0.3

faiss-cpu==1.7.4
pypdf==4.2.0

# =========================
# 🔥 CPU ONLY (NO CUDA)
# =========================
torch==2.1.2
sentence-transformers==2.6.1
