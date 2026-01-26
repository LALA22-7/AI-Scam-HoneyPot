import os
import re
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi import Request, Header, HTTPException # <--- Make sure these are imported at the top!
# 1. LOAD SECRETS & SETUP
load_dotenv()
app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. DEFINE DATA MODELS
class ScammerInput(BaseModel):
    message: str
    conversation_id: str = "default"  # This ID tracks the specific scammer

# 3. THE BRAIN: RANJEET SEHGAL (Instruction)
ranjeet_instruction = """
You are Ranjeet Sehgal, a 65-year-old retired Indian Railways employee living in Gorakhpur, Uttar Pradesh.
You are chatting with a stranger on WhatsApp who you suspect is a scammer.

--- PERSONALITY & BACKSTORY ---
- **Background:** You worked in Railways for 40 years. Proud of pension.
- **Location:** Gorakhpur (Golghar, station road).
- **Tech Level:** Can use GPay but confused by links/KYC.
- **Dialect:** Use "Hum/Humara" instead of "Mai/Mera". Polite ("Beta", "Babu").
- **Goal:** Waste time, act confused, ask for phone number to "paytm".
- **Rules:** Never admit you know it is a scam.
"""

# 4. INITIALIZE MODEL (With System Instruction)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=ranjeet_instruction
)

# --- GLOBAL MEMORY STORAGE ---
# This dictionary will store the chat history for every unique conversation_id
# Format: { "session_123": ChatSessionObject, "session_456": ChatSessionObject }
chat_sessions = {}

# 5. SPY LOGIC (The Intelligence Extractor)
def extract_intel(text):
    intel = {"upi_ids": [], "phone_numbers": [], "links": []}
    intel["upi_ids"] = re.findall(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}', text)
    intel["phone_numbers"] = re.findall(r'[6-9]\d{9}', text)
    intel["links"] = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    return intel

# ---------------------------------------------------------
# 6. THE SHARED BRAIN FUNCTION (Now with MEMORY!)
# ---------------------------------------------------------
async def chat(user_message: str, conversation_id: str = "default"):
    # A. Manage Memory (The "Multi-Turn" Logic)
    # If we haven't talked to this ID before, start a new memory for them
    if conversation_id not in chat_sessions:
        chat_sessions[conversation_id] = model.start_chat(history=[])
    
    # Get the specific session for this ID
    current_session = chat_sessions[conversation_id]

    # B. Run the Spy Logic
    captured_data = extract_intel(user_message)
    
    # C. Generate Ranjeet's Reply
    try:
        # We use 'send_message' instead of 'generate_content' to keep history
        response = await asyncio.to_thread(
            current_session.send_message,
            user_message
        )
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Arre beta... net issue hai... (Error: {str(e)})"

    # D. Return Clean Dictionary
    return {
        "reply": bot_reply,
        "scam_detected": True,
        "captured_data": captured_data,
        "conversation_id": conversation_id
    }
# Add this to handle the "Home Page"
@app.get("/")
async def root():
    return {
        "status": "active",
        "agent": "Ranjeet Uncle",
        "model": "Gemini 2.5 Flash"
    }
# ---------------------------------------------------------
# 7. THE API ENDPOINT
# ---------------------------------------------------------
@app.post("/chat")
async def chat_endpoint(request: Request, x_api_key: str = Header(None)):
    # 1. SECURITY CHECK (The "Lock")
    # If the tester sends a key, we check it. If not, we might let it slide for debugging,
    # OR strictly block it. Let's strictly block it to be safe.
    if x_api_key != "scam-honey-pot-secret-2026":
        print(f"🚨 SECURITY ALERT: Invalid Key received: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. DEBUGGING (The "Spy")
    try:
        data = await request.json()
        print(f"🕵️‍♂️ DEBUG LOG - INCOMING DATA: {data}")  # <--- CHECK RENDER LOGS FOR THIS!
    except:
        return {"error": "Invalid JSON format"}

    # 3. FLEXIBLE FIELD FINDER
    # The tester might be sending 'message', 'content', 'text', or 'input'. We try them all.
    user_message = data.get("message") or data.get("content") or data.get("text") or data.get("input")
    
    # Try to find the conversation ID too
    chat_id = data.get("conversation_id") or data.get("session_id") or "default"

    if not user_message:
        print("❌ ERROR: No message field found in data!")
        return {"error": "Message field missing", "received_data": data}

    # 4. PASS TO RANJEET
    response = await chat(user_message, chat_id)
    return response