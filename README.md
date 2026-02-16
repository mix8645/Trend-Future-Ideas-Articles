
---

# 🚀 Jenosize Future Ideas Generator (Bilingual AI Writer)

A sophisticated AI-driven article generation platform designed to create strategic business insights and future trends. This system produces high-quality content in both **English and Thai**, maintaining a consistent "human-centered" brand voice inspired by the Jenosize philosophy.

## 🏗️ System Architecture

The project utilizes a **Decoupled Monolith** architecture to optimize the performance of Large Language Models (LLMs) in a cloud environment:

* **Frontend**: [Streamlit Community Cloud](https://streamlit.io/) provides a reactive, state-managed user interface.
* **Backend API**: [FastAPI](https://fastapi.tiangolo.com/) hosted on **Hugging Face Spaces (Docker)**, acting as the primary AI inference engine.
* **Model Storage**: Hosted on **Hugging Face Model Hub**, allowing the backend to pull the 2.5GB model weights dynamically via `hf_hub_download` to bypass deployment storage limits.

---

## 🛠️ Tech Stack & Models

* **Language**: Python 3.10+
* **AI Engine**: `llama-cpp-python` for high-performance GGUF inference.
* **Core Model**: `chinda-qwen3-4b.Q4_K_M.gguf` (A Qwen-based model optimized for Thai/English bilingual tasks).
* **Frameworks**: FastAPI (Backend), Streamlit (Frontend), Pydantic (Data Validation).
* **DevOps**: Docker & Docker Compose for local orchestration.

---

## 🚀 Installation & Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/mix8645/trend-future-ideas-articles.git
cd trend-future-ideas-articles

```

### 2. Dependency Management

Install dependencies locally for development (optional if using Docker):

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
pip install -r requirements.txt

```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
SERVICE_API_KEY=your_secure_secret_key
BACKEND_URL=http://localhost:8000

```

### 4. Run with Docker Compose

The easiest way to start the full stack:

```bash
docker-compose up --build

```

* **Frontend**: `http://localhost:8501`
* **Backend API**: `http://localhost:8000`

---

## ☁️ Deployment Guide

### Backend (Hugging Face Spaces)

1. Create a new **Docker Space** on Hugging Face.
2. Set the `app_port` to **7860** in your Space settings.
3. Upload the `backend/` directory (excluding the heavy model file).
4. The system will automatically pull the model weights from your Model Hub repository at runtime.

### Frontend (Streamlit Cloud)

1. Connect your GitHub repository to Streamlit Community Cloud.
2. Set the `BACKEND_URL` and `SERVICE_API_KEY` in the **Advanced Settings > Secrets** section of the Streamlit dashboard.

---

## 📂 Project Structure

```text
.
├── backend/               # FastAPI Server & AI Logic
│   ├── model/             # (Git ignored) Local model storage
│   ├── services/          # LLM Engine & Web Crawling logic
│   └── main.py            # API Entry point
├── frontend/              # Streamlit Web App
│   └── app.py             # UI & Session Management
├── notebooks/             # Research & Data Augmentation experiments
└── docker-compose.yml     # Container orchestration

```

---

## 👤 Author

**Worachot Chanmuang (Mix)**

* **Position**: AI Agent Developer / Product Engineer at Avalant Co., Ltd.
* **Education**: B.Eng. in Computer Engineering, University of Phayao
* **GitHub**: [mix8645](https://www.google.com/search?q=https://github.com/mix8645)

---
