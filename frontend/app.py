import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv

# โหลด environment variables
load_dotenv()

API_URL = os.getenv("BACKEND_URL", os.getenv("API_URL", "http://localhost:8000"))
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY", "default_secret_key")

st.set_page_config(
    page_title="Jenosize Trend Generator",
    page_icon="🚀",
    layout="wide"
)

# --- Initialize Session State ---
if "eng_article" not in st.session_state:
    st.session_state.eng_article = None
if "thai_article" not in st.session_state:
    st.session_state.thai_article = None
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# ฟังก์ชันสำหรับเปลี่ยนสถานะปุ่มเมื่อถูกกด
def start_generation():
    st.session_state.is_generating = True

st.title("🚀 Jenosize Future Ideas Generator")
st.markdown("Create insightful articles about trends and future ideas for businesses - in English and Thai!")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Configuration")
    topic = st.text_input("Topic / Keyword", placeholder="e.g. AI in Healthcare 2025")
    
    industry = st.selectbox(
        "Industry",
        ["Technology", "Marketing", "Finance", "Healthcare", "Retail", "Other"]
    )
    
    target_audience = st.selectbox(
        "Target Audience",
        ["Business Owners", "Tech Enthusiasts", "Investors", "General Public"]
    )
    
    tone = st.select_slider(
        "Tone & Style",
        options=["Casual", "Professional", "Visionary", "Urgent"]
    )
    
    source_url = st.text_input("Source URL (Optional)", placeholder="https://techcrunch.com/...")
    
    # อัปเดตปุ่มให้ Disable อัตโนมัติเมื่อ is_generating = True
    st.button(
        "⏳ Generating..." if st.session_state.is_generating else "✨ Generate Article", 
        use_container_width=True, 
        type="primary",
        disabled=st.session_state.is_generating,
        on_click=start_generation
    )

with col2:
    st.subheader("📝 Generated Article")
    
    # --- Handle API Request ---
    if st.session_state.is_generating:
        if not topic:
            st.warning("⚠️ Please enter a topic first.")
            st.session_state.is_generating = False
            st.rerun()
        else:
            with st.status("🚀 Initializing AI Engine...", expanded=True) as status:
                try:
                    st.write("🔍 Sending request to AI Server...")
                    
                    headers = {
                        "X-API-Key": SERVICE_API_KEY,
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "topic": topic,
                        "industry": industry,
                        "target_audience": target_audience,
                        "tone": tone,
                        "source_url": source_url
                    }
                    
                    # 1. ยิงรับบัตรคิว (ใช้เวลาไม่กี่วินาที)
                    response = requests.post(
                        f"{API_URL}/generate-article", 
                        headers=headers, 
                        json=payload,
                        timeout=30 
                    )
                    
                    if response.status_code == 200:
                        task_id = response.json().get("task_id")
                        st.write(f"🎫 Task ID received: `{task_id}`")
                        st.info("AI is actively generating and translating your article in the background. Please wait, this may take a few minutes without timing out...")
                        
                        # 2. วนลูปเช็กสถานะงาน (Polling)
                        while True:
                            time.sleep(5) # รอ 5 วินาทีก่อนถามใหม่
                            
                            status_res = requests.get(f"{API_URL}/task-status/{task_id}", timeout=10)
                            
                            if status_res.status_code == 200:
                                task_data = status_res.json()
                                
                                if task_data["status"] == "success":
                                    articles = task_data.get("articles", {})
                                    st.session_state.eng_article = articles.get("en", "")
                                    st.session_state.thai_article = articles.get("th", "")
                                    
                                    status.update(label="✅ Articles Generated Successfully!", state="complete", expanded=False)
                                    st.session_state.is_generating = False
                                    st.rerun()
                                    break # ออกจากลูป
                                    
                                elif task_data["status"] == "error":
                                    st.error(f"❌ Backend Generation Error: {task_data.get('detail')}")
                                    status.update(label="❌ Error", state="error", expanded=True)
                                    st.session_state.is_generating = False
                                    break # ออกจากลูป
                                    
                            else:
                                st.error("❌ Failed to fetch task status.")
                                st.session_state.is_generating = False
                                break
                                
                    elif response.status_code == 401:
                        st.error("❌ Authentication Error: API Key mismatch or missing.")
                        status.update(label="❌ Error", state="error", expanded=True)
                        st.session_state.is_generating = False
                        
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                        status.update(label="❌ Error", state="error", expanded=True)
                        st.session_state.is_generating = False
                        
                except Exception as e:
                    st.error(f"Connection Error: {e}")
                    status.update(label="❌ Connection Failed", state="error", expanded=True)
                    st.session_state.is_generating = False

    # --- Display Articles from Session State ---
    if not st.session_state.is_generating and st.session_state.eng_article and st.session_state.thai_article:
        tab1, tab2 = st.tabs(["🇬🇧 English", "🇹🇭 Thai"])
        
        with tab1:
            st.markdown(st.session_state.eng_article)
            st.divider()
            
            st.download_button(
                label="📥 Download English as Markdown",
                data=st.session_state.eng_article,
                file_name=f"{topic.replace(' ', '_')}_jenosize_en.md",
                mime="text/markdown"
            )
        
        with tab2:
            st.markdown(st.session_state.thai_article)
            st.divider()
            
            st.download_button(
                label="📥 Download Thai as Markdown",
                data=st.session_state.thai_article,
                file_name=f"{topic.replace(' ', '_')}_jenosize_th.md",
                mime="text/markdown"
            )

st.markdown("---")
st.caption("Powered by Jenosize AI Model | Bilingual Support (English & Thai) | Designed for Test Assignment Option 1")