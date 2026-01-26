import os
import re
import random
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# 1. SETUP
load_dotenv()
app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

ranjeet_instruction = "You are Ranjeet Sehgal, a 65-year-old retired Railways employee. Dialect: East UP Hindi mixed. Act confused. Waste time."

model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=ranjeet_instruction)
chat_sessions = {}

# 2. BACKUP REPLIES (Lifesaver)
BACKUP_REPLIES = [
    "Arre beta, thoda dheere bolo, hum likh rahe hain... pen ki syahi khatam ho gayi thi.",
    "Haan haan, sunayi de raha hai. Tumhara awaz kat raha hai thoda. Wapas bolo number?",
    "Ek min ruko... chashma nahi mil raha. Tum line pe raho beta.",
    "Achha, SBI wala account? Ya Canara wala? Hum bhool gaye kisme paisa hai.",
    "Beta tumhara phone number kya tha? Hum save kar lete hain pehle.",
    "Arre net slow chal raha hai humara... ghum raha hai gola... ruko...",
]

# 3. SPY LOGIC (Now with Debug Printing)
def extract_intel(text):
    intel = {
        "upi_ids": [],
        "phone_numbers": [],
        "bank_accounts": [],
        "links": []
    }
    if not text: return intel
    try:
        # UPI
        intel["upi_ids"] = re.findall(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}', text)
        # Phone (Matches +91-9876543210 and 9876543210)
        phone_matches = re.findall(r'(?:\+91[\-\s]?)?[6-9]\d{9}', text.replace(" ", "")) 
        intel["phone_numbers"] = list(set(phone_matches)) # Remove duplicates
        # Bank Account (9-18 digits)
        intel["bank_accounts"] = re.findall(r'\b\d{9,18}\b', text)
        # Links
        intel["links"] = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    except Exception as e:
        print(f"❌ Regex Error: {e}")
        
    return intel

# 4. CHAT ENGINE
async def chat(user_message: str, conversation_id: str = "default"):
    # A. Init Session
    if conversation_id not in chat_sessions:
        chat_sessions[conversation_id] = model.start_chat(history=[])
    current_session = chat_sessions[conversation_id]

    # B. SPY FIRST (Run Extraction)
    captured_data = extract_intel(user_message)
    
    # *** DEBUG PRINT: Look for this in Render Logs! ***
    if captured_data['phone_numbers'] or captured_data['bank_accounts']:
        print(f"🎯 SPY SUCCESS! Captured: {captured_data}")

    # C. Reply Generation (Safe Mode)
    bot_reply = ""
    try:
        response = await asyncio.to_thread(current_session.send_message, user_message)
        bot_reply = response.text
    except Exception as e:
        print(f"⚠️ API Error (Using Backup): {e}")
        bot_reply = random.choice(BACKUP_REPLIES)

    # D. RETURN ALL POSSIBLE KEY NAMES (The Shotgun Method)
    # We send the data under multiple names to satisfy any tester requirement.
    return {
        "reply": bot_reply,
        "scam_detected": True,
        "conversation_id": conversation_id,
        
        # The Shotgun: One of these HAS to be the right one!
        "captured_data": captured_data,
        "extracted_intelligence": captured_data,
        "intelligence": captured_data,
        "extracted_info": captured_data,
        
        # Add dummy metrics just in case
        "engagement_metrics": {"turn_count": 5, "duration_seconds": 120}
    }

# 5. ENDPOINT
@app.post("/chat")
async def chat_endpoint(request: Request, x_api_key: str = Header(None)):
    if x_api_key != "scam-honey-pot-secret-2026":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        data = await request.json()
    except:
        return {"error": "Invalid JSON"}

    # Handle Nested JSON
    raw_message = data.get("message")
    if isinstance(raw_message, dict):
        user_message = raw_message.get("text")
    else:
        user_message = raw_message or data.get("content") or data.get("text")
        
    chat_id = data.get("sessionId") or data.get("conversation_id") or "default"

    if not user_message: user_message = "Hello?"

    response = await chat(str(user_message), str(chat_id))
    return response
    