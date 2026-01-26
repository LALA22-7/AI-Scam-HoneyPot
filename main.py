import os
import re
import random
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# 1. SETUP & SECRETS
load_dotenv()
app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. RANJEET'S INSTRUCTIONS
ranjeet_instruction = """
You are Ranjeet Sehgal, a 65-year-old retired Indian Railways employee.
Dialect: East UP Hindi + English mixed. Polite ("Beta", "Babu").
Goal: Waste the scammer's time. Act confused.
Never admit it is a scam.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=ranjeet_instruction
)

chat_sessions = {}

# --- 3. SMART BACKUP REPLIES (Used when Server is Busy) ---
BACKUP_REPLIES = [
    "Arre beta, thoda dheere bolo, hum likh rahe hain... pen ki syahi khatam ho gayi thi.",
    "Haan haan, sunayi de raha hai. Tumhara awaz kat raha hai thoda. Wapas bolo number?",
    "Ek min ruko... chashma nahi mil raha. Tum line pe raho beta.",
    "Achha, SBI wala account? Ya Canara wala? Hum bhool gaye kisme paisa hai.",
    "Beta tumhara phone number kya tha? Hum save kar lete hain pehle.",
    "Arre net slow chal raha hai humara... ghum raha hai gola... ruko...",
    "Beta humko ye OTP dikh nahi raha, chashma saaf kar rahe hain.",
]

# --- 4. SUPERCHARGED SPY LOGIC (Runs Locally = 100% Uptime) ---
def extract_intel(text):
    intel = {
        "upi_ids": [],
        "phone_numbers": [],
        "bank_accounts": [],
        "links": []
    }
    if not text: return intel
    
    try:
        # 1. Capture UPI IDs (Matches example@okhdfc, 9876543210@paytm)
        intel["upi_ids"] = re.findall(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}', text)
        
        # 2. Capture Indian Phone Numbers (Smart Regex)
        # Matches: +91-9876543210, 98765 43210, 98765-43210, or plain 9876543210
        # It looks for 6-9 followed by digits, handling spaces/dashes in between.
        phone_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{3,4}[\-\s]?\d{3,4}[\-\s]?\d{3,4}'
        matches = re.findall(phone_pattern, text)
        # Clean up the numbers (remove spaces/dashes) for clean JSON
        intel["phone_numbers"] = [m.replace(" ", "").replace("-", "") for m in matches if len(m.replace(" ", "").replace("-", "")) >= 10]
        
        # 3. Capture Bank Accounts (9 to 18 digits, looking for word boundaries)
        intel["bank_accounts"] = re.findall(r'\b\d{9,18}\b', text)
        
        # 4. Capture Phishing Links
        intel["links"] = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
        
    except Exception as e:
        print(f"❌ Regex Error: {e}")
        
    return intel

# 5. CHAT ENGINE (Spy First, Talk Later)
async def chat(user_message: str, conversation_id: str = "default"):
    # A. Memory Management
    if conversation_id not in chat_sessions:
        chat_sessions[conversation_id] = model.start_chat(history=[])
    
    current_session = chat_sessions[conversation_id]

    # B. EXECUTE SPY LOGIC IMMEDIATELY
    # This runs on YOUR server. It does NOT need Google. 
    # Even if the next step fails, we already have the data!
    captured_data = extract_intel(user_message)
    
    # C. Generate Reply (With Safety Net)
    bot_reply = ""
    
    try:
        # Try asking Google Gemini
        response = await asyncio.to_thread(
            current_session.send_message,
            user_message
        )
        bot_reply = response.text

    except Exception as e:
        # IF GOOGLE IS BUSY/CRASHES -> USE BACKUP REPLY
        # The scammer gets a reply, and we still return the captured data!
        print(f"⚠️ API Error (Using Backup): {e}")
        bot_reply = random.choice(BACKUP_REPLIES)

    # D. Return Everything
    return {
        "reply": bot_reply,
        "scam_detected": True,
        "captured_data": captured_data,  # <--- DATA IS ALWAYS HERE
        "conversation_id": conversation_id
    }

# 6. API ENDPOINT
@app.post("/chat")
async def chat_endpoint(request: Request, x_api_key: str = Header(None)):
    if x_api_key != "scam-honey-pot-secret-2026":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        data = await request.json()
    except:
        return {"error": "Invalid JSON"}

    # Handle Nested JSON safely
    raw_message = data.get("message")
    if isinstance(raw_message, dict):
        user_message = raw_message.get("text")
    else:
        user_message = raw_message or data.get("content") or data.get("text")
        
    chat_id = data.get("sessionId") or data.get("conversation_id") or "default"

    if not user_message:
        user_message = "Hello?"

    response = await chat(str(user_message), str(chat_id))
    return response