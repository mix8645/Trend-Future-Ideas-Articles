from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
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

@app.get("/")
def read_root():
    return {"status": "🚀 Jenosize AI Backend is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": llm is not None}

@app.get("/model-status")
def model_status():
    return {
        "model_loaded": llm is not None,
        "model_path": MODEL_PATH,
        "model_exists": os.path.exists(MODEL_PATH),
    }

@app.post("/generate-article")
def generate_article(req: TopicRequest, api_key: str = Depends(verify_api_key)):
    """
    Generate article in English first, then translate to Thai using the same LLM 
    to maintain context and brand tone perfectly.
    """
    if not llm:
        raise HTTPException(status_code=500, detail="AI Model is not loaded properly.")

    logger.info(f"Generating bilingual article - Topic: {req.topic}, Tone: {req.tone}")
    
    tone_params = {
        "Casual": {"temperature": 0.75, "top_p": 0.88},
        "Professional": {"temperature": 0.65, "top_p": 0.85},
        "Visionary": {"temperature": 0.80, "top_p": 0.90},
        "Urgent": {"temperature": 0.70, "top_p": 0.85},
    }
    
    params = tone_params.get(req.tone, {"temperature": 0.70, "top_p": 0.85})

    try:
        # 1. Generate English article
        logger.info("Generating English article...")
        eng_prompt = f"""{SYSTEM_PROMPT}

Topic: {req.topic}
Industry: {req.industry}
Target Audience: {req.target_audience}
Tone: {req.tone}
{f"Reference: {req.source_url}" if req.source_url else ""}

Write the article:
"""

        eng_output = llm(
            eng_prompt,
            max_tokens=1500, # ขยาย max_tokens
            temperature=params["temperature"],
            top_p=params["top_p"],
            echo=False
        )
        
        eng_article = eng_output['choices'][0]['text'].strip()
        logger.info("✅ English article generated!")

        # 2. Translate to Thai using LLM to maintain context
        logger.info("Translating English to Thai using LLM for context awareness...")
        
        thai_prompt = f"""คุณคือนักแปลและนักเขียนบทความมืออาชีพของ Jenosize

จงแปลบทความภาษาอังกฤษด้านล่างนี้เป็นภาษาไทย โดยมีเงื่อนไขดังนี้:
1. รักษาความหมาย บริบท และโครงสร้างเดิมไว้ให้ครบถ้วน 100%
2. ใช้ภาษาที่สละสลวย เป็นธรรมชาติ และอ่านง่ายสำหรับกลุ่ม {req.target_audience}
3. คุมโทนการเขียนให้เป็นแบบ {req.tone}

บทความต้นฉบับ:
{eng_article}

แปลเป็นภาษาไทย:
"""

        thai_output = llm(
            thai_prompt,
            max_tokens=2500,
            temperature=0.1,
            top_p=0.9,
            echo=False
        )
        
        thai_article = thai_output['choices'][0]['text'].strip()
        logger.info("✅ Thai article generated (Context Maintained)!")
        
        return {
            "topic": req.topic,
            "industry": req.industry,
            "target_audience": req.target_audience,
            "tone": req.tone,
            "articles": {
                "en": eng_article,
                "th": thai_article
            },
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Generation Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation Error: {str(e)}")