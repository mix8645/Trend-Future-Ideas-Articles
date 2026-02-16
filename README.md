
---

# 🚀 Jenosize Future Ideas Generator

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
# Trend-Future-Ideas-Articles

This project is a content generation platform that uses a fine-tuned language model to create articles based on a given topic, industry, target audience, and tone. The backend is a FastAPI application that serves the model, and the frontend is a Streamlit application that provides a user interface.

## Documentation & Explanation

### Approach and Model Selection

The core of this project is a fine-tuned Large Language Model (LLM) designed to generate high-quality articles with a specific, human-centered brand voice for the company "Jenosize".

**Model:** The model used is `mix8645/jenosize-qwen-model`, specifically the `chinda-qwen3-4b.Q4_K_M.gguf` file.

*   **Rationale for Selection:**
    *   **Quantization (Q4_K_M.gguf):** This is a 4-bit quantized model, which offers a good balance between performance and resource consumption. It allows the model to run efficiently on consumer-grade hardware without a significant loss in quality.
    *   **Base Model (Qwen):** The Qwen family of models are known for their strong generative capabilities, especially in multilingual contexts.
    *   **Fine-tuning:** The model has been presumably fine-tuned on Jenosize's internal data to capture its unique brand voice and writing style, emphasizing authentic, human-centered insights. *Note: The fine-tuning notebooks (`01_data_pipeline.ipynb`, `02_finetuning.ipynb`) are currently empty and do not contain the fine-tuning process code.*

### API Deployment

The application is containerized using Docker and can be easily deployed using Docker Compose.

*   **Backend:** A FastAPI application that exposes the `/generate-article` endpoint. It downloads and loads the quantized GGUF model from Hugging Face Hub using the `llama-cpp-python` library.
*   **Frontend:** A Streamlit application that provides a user-friendly interface to interact with the backend API.
*   **Deployment:** The `docker-compose.yml` file orchestrates the deployment of both the frontend and backend services.

## How to Run and Test

### Prerequisites

*   Docker and Docker Compose installed.
*   An `.env` file with the required environment variables (see `.env.example` if available, or check the `docker-compose.yml`). You'll need to set the `SERVICE_API_KEY`.

### Running the Application

1.  **Create an `.env` file:**
    Create a `.env` file in the root of the project and add the following:
    ```
    SERVICE_API_KEY=your_secret_api_key
    ```
2.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```
3.  **Access the applications:**
    *   **Frontend:** Open your browser and go to `http://localhost:8501`.
    *   **Backend API Docs:** Open your browser and go to `http://localhost:8000/docs`.

### Testing the API

You can test the `/generate-article` endpoint using `curl` or any API client.

```bash
curl -X POST "http://localhost:8000/generate-article" \
-H "Content-Type: application/json" \
-H "X-API-Key: your_secret_api_key" \
-d '{
    "topic": "The Future of AI in Business",
    "industry": "Technology",
    "target_audience": "Business Leaders",
    "tone": "Visionary",
    "source_url": ""
}'
```

This will return a JSON response containing the generated article in both English and Thai.


---

## 👤 Author

**Worachot Chanmuang (Mix)**

* **Position**: AI Agent Developer / Product Engineer at Avalant Co., Ltd.
* **Education**: B.Eng. in Computer Engineering, University of Phayao
* **GitHub**: [mix8645](https://www.google.com/search?q=https://github.com/mix8645)

---
