import os
import re
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# 1. LOAD SECRETS & SETUP
load_dotenv()
app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. DEFINE DATA MODELS
class ScammerInput(BaseModel):
    message: str
    conversation_id: str = "default"

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

# 4. INITIALIZE MODEL (UPDATED TO 2.5 FLASH) ⚡️
# We pass the instruction HERE in the stable SDK
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",  # <--- UPDATED HERE
    system_instruction=ranjeet_instruction
)

# 5. SPY LOGIC (The Intelligence Extractor)
def extract_intel(text):
    intel = {"upi_ids": [], "phone_numbers": [], "links": []}
    # Capture UPI IDs
    intel["upi_ids"] = re.findall(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}', text)
    # Capture Phone Numbers
    intel["phone_numbers"] = re.findall(r'[6-9]\d{9}', text)
    # Capture Links
    intel["links"] = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    return intel

# ---------------------------------------------------------
# 6. THE SHARED BRAIN FUNCTION
# ---------------------------------------------------------
async def chat(user_message: str):
    # A. Run the Spy Logic
    captured_data = extract_intel(user_message)
    
    # B. Generate Ranjeet's Reply
    try:
        # We use 'model.generate_content', NOT 'client.models...'
        response = await asyncio.to_thread(
            model.generate_content,
            user_message
        )
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Arre beta... net issue hai... (Error: {str(e)})"

    # C. Return Clean Dictionary
    return {
        "reply": bot_reply,
        "scam_detected": True,
        "captured_data": captured_data
    }

# ---------------------------------------------------------
# 7. THE API ENDPOINT
# ---------------------------------------------------------
@app.post("/chat")
async def chat_endpoint(data: ScammerInput):
    response = await chat(data.message)
    return response