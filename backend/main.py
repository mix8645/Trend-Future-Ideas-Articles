from fastapi import FastAPI, HTTPException, Depends, Security, status, BackgroundTasks
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import uuid
from dotenv import load_dotenv
from llama_cpp import Llama
from schemas import TopicRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Jenosize AI Writer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key security
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY", "default_secret_key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != SERVICE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key

# --- Load Local GGUF Model ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "chinda-qwen3-4b.Q4_K_M.gguf")

logger.info(f"⏳ Loading Local Model from: {MODEL_PATH}")
try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,
        n_threads=4,
        verbose=False
    )
    logger.info("✅ Model loaded successfully!")
except Exception as e:
    logger.error(f"❌ Error loading model: {e}")
    llm = None

# --- SYSTEM PROMPTS ---
SYSTEM_PROMPT = """You are a professional article writer for Jenosize - a company known for authentic, human-centered insights about business transformation.

Your writing style:
- Authentic and human-centered (focus on customer understanding, not technology hype)
- Conversational yet insightful (warm, relatable tone, never robotic)
- Story-driven (use real-world examples and narratives)
- Actionable (provide practical insights readers can implement)
- Grounded in reality (honest about both opportunities and challenges)

CRITICAL OUTPUT RULES:
1. Write ONLY the article content - no thinking, reasoning, or meta-commentary
2. Start directly with a compelling markdown headline (#)
3. Use proper markdown formatting (###, ####, bullet points)
4. Include real-world examples and actionable insights
5. Never explain your approach or process
6. Focus on customer value and business impact
7. Maintain authentic, warm tone throughout"""

# ตัวแปรสำหรับเก็บสถานะงาน (In-memory Storage)
job_status = {}

def process_article_task(task_id: str, req: TopicRequest, params: dict):
    """ฟังก์ชันทำงานเบื้องหลัง สำหรับสร้างและแปลบทความโดยไม่ให้ API หลักค้าง"""
    try:
        # 1. Generate English article
        logger.info(f"[Task {task_id}] Generating English article...")
        eng_prompt = f"""{SYSTEM_PROMPT}\n\nTopic: {req.topic}\nIndustry: {req.industry}\nTarget Audience: {req.target_audience}\nTone: {req.tone}\n{f"Reference: {req.source_url}" if req.source_url else ""}\n\nWrite a SHORT and concise article (maximum 2-3 paragraphs):\n"""

        eng_output = llm(
            eng_prompt,
            max_tokens=800,
            temperature=params["temperature"],
            top_p=params["top_p"],
            echo=False
        )
        
        eng_article = eng_output['choices'][0]['text'].strip()
        logger.info(f"[Task {task_id}] ✅ English article generated!")

        # 2. Translate to Thai
        logger.info(f"[Task {task_id}] Translating English to Thai...")
        thai_prompt = f"""คุณคือนักแปลและนักเขียนบทความมืออาชีพของ Jenosize\n\nจงแปลบทความภาษาอังกฤษด้านล่างนี้เป็นภาษาไทย โดยมีเงื่อนไขดังนี้:\n1. รักษาความหมาย บริบท และโครงสร้างเดิมไว้ให้ครบถ้วน 100%\n2. ใช้ภาษาที่สละสลวย เป็นธรรมชาติ และอ่านง่ายสำหรับกลุ่ม {req.target_audience}\n3. คุมโทนการเขียนให้เป็นแบบ {req.tone}\n\nบทความต้นฉบับ:\n{eng_article}\n\nแปลเป็นภาษาไทย:\n"""

        thai_output = llm(
            thai_prompt,
            max_tokens=1500,
            temperature=0.1,
            top_p=0.9,
            echo=False
        )
        
        thai_article = thai_output['choices'][0]['text'].strip()
        logger.info(f"[Task {task_id}] ✅ Thai article generated!")
        
        # บันทึกผลลัพธ์ลงใน memory
        job_status[task_id] = {
            "status": "success",
            "articles": {
                "en": eng_article,
                "th": thai_article
            }
        }
        
    except Exception as e:
        logger.error(f"[Task {task_id}] Error: {str(e)}")
        job_status[task_id] = {
            "status": "error",
            "detail": str(e)
        }

@app.get("/")
def read_root():
    return {"status": "🚀 Jenosize AI Backend is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": llm is not None}

@app.post("/generate-article")
def generate_article(req: TopicRequest, background_tasks: BackgroundTasks, api_key: str = Depends(verify_api_key)):
    """API หลักสำหรับรับ Request คืนค่า Task ID ทันทีเพื่อกัน Timeout"""
    if not llm:
        raise HTTPException(status_code=500, detail="AI Model is not loaded properly.")
    
    task_id = str(uuid.uuid4())
    job_status[task_id] = {"status": "processing"}
    
    tone_params = {
        "Casual": {"temperature": 0.75, "top_p": 0.88},
        "Professional": {"temperature": 0.65, "top_p": 0.85},
        "Visionary": {"temperature": 0.80, "top_p": 0.90},
        "Urgent": {"temperature": 0.70, "top_p": 0.85},
    }
    params = tone_params.get(req.tone, {"temperature": 0.70, "top_p": 0.85})

    # โยนงานไปทำเบื้องหลัง
    background_tasks.add_task(process_article_task, task_id, req, params)
    
    return {"task_id": task_id, "status": "processing"}

@app.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    """API สำหรับ Frontend เข้ามาเช็กสถานะงาน"""
    if task_id not in job_status:
        raise HTTPException(status_code=404, detail="Task not found")
    return job_status[task_id]