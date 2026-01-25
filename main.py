import os
import re  # <--- THIS WAS MISSING
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types

# 1. LOAD SECRETS
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. SETUP APP & CLIENT
app = FastAPI()
client = genai.Client(api_key=api_key)

# 3. DEFINE DATA MODELS
class ScammerInput(BaseModel):
    message: str
    conversation_id: str = "default"

# 4. THE BRAIN: RANJEET SEHGAL (Instruction)
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
# 6. THE SHARED BRAIN FUNCTION (Streamlit + API)
# ---------------------------------------------------------
async def chat(user_message: str):
    # A. Run the Spy Logic
    captured_data = extract_intel(user_message)
    
    # B. Generate Ranjeet's Reply
    try:
        # We run this in a thread to keep the website fast
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="models/gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=ranjeet_instruction,
                temperature=1.0, 
            )
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