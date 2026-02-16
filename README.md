# 🚀 Jenosize - Trend & Future Ideas Generator (Generative AI Assignment)

[cite_start]This repository contains the solution for the **AI & Data Engineer (Generative AI)** technical assignment[cite: 1]. [cite_start]The project implements **Option 1: Trend & Future Ideas Articles** [cite: 7][cite_start], an automated content generation tool that proposes creative articles tailored to specific industries, target audiences, and tones[cite: 8, 9, 10].

## 🏗️ Architecture & Tech Stack

The project is built with a Full-Stack Generative AI architecture designed for scalability and local deployment:

* **Generative AI Model:** Local LLM using `llama-cpp-python` (Chinda-Qwen3-4B-GGUF) for optimized CPU/RAM inference.
* **Prompt Engineering:** Eng-to-Thai Prompt Chaining to maintain high context quality and output native-sounding Thai text.
* [cite_start]**Backend (API):** `FastAPI` providing high-performance RESTful endpoints[cite: 27].
* [cite_start]**Frontend (UI):** `Streamlit` for an interactive and user-friendly prototype[cite: 50].
* [cite_start]**Data Engineering:** Data augmentation and web crawling pipelines for dataset preparation[cite: 23].
* **Infrastructure:** Containerized using `Docker` and orchestrated via `Docker Compose`.

## 📁 Project Structure

```text
.
[cite_start]├── backend/                  # FastAPI Application [cite: 27]
│   ├── model/                # Directory for local GGUF models (e.g., chinda-qwen3-4b.Q4_K_M.gguf)
│   ├── services/             # Data Engineering pipelines (Crawler, Augmentation)
│   ├── main.py               # API endpoints and LLM logic
│   ├── schemas.py            # Pydantic models for request validation
[cite_start]│   ├── Dockerfile            # Backend container configuration [cite: 47]
│   └── requirements.txt      # Backend dependencies
├── frontend/                 # Streamlit UI Application
│   ├── app.py                # User interface and API integration
│   ├── Dockerfile            # Frontend container configuration
[cite_start]│   └── requirements.txt      # Frontend dependencies [cite: 50]
[cite_start]├── data/                     # Dataset storage [cite: 35]
│   ├── raw/                  # Raw scraped/collected data
│   └── processed/            # Cleaned data for fine-tuning
├── notebooks/                # ML Pipeline & Research
│   ├── Convert_to_GGUF.ipynb # Script for model conversion
[cite_start]│   └── jenosize_model_unsloth.ipynb # Fine-tuning script using Unsloth [cite: 18]
└── docker-compose.yml        # Multi-container orchestration

```

## ⚙️ Prerequisites

Before running the project locally, ensure you have the following installed:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* Git

**Note:** Ensure that your selected GGUF model file (e.g., `chinda-qwen3-4b.Q4_K_M.gguf`) is placed inside the `backend/model/` directory before building the containers.

## 🚀 How to Run Locally

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd <repository-folder>

```


2. **Environment Variables Configuration:**
Create a `.env` file in both `backend/` and `frontend/` (or configure via Docker Compose) and set your secure API Key:
```env
SERVICE_API_KEY=your_secure_api_key_here
BACKEND_URL=http://backend:8000

```


3. **Build and Start the Containers:**
Run the following command at the root of the project to build the images and start the services:
```bash
docker-compose up --build -d

```


4. **Access the Applications:**
* **Frontend (Streamlit UI):** Open your browser and go to `http://localhost:8501`
* **Backend API Documentation (Swagger UI):** Go to `http://localhost:8000/docs` to test the API endpoints directly.


5. **Stop the Application:**
```bash
docker-compose down

```



## 🌐 Public Prototype Testing (For Evaluators)

A live prototype is available for testing without local setup.
The Frontend is hosted on **Streamlit Community Cloud**, while the Backend API is securely tunneled to a local inference server using **ngrok** to handle the GenAI workload efficiently.

* **Test Link:** `(https://trend-future-ideas-articles-5pzcrgceozrhapppprtyp5xb.streamlit.app/)`
* *(Note: The backend server must be running and the ngrok tunnel active for the live link to function properly).*
