from fastapi import FastAPI
from pydantic import BaseModel
import re
from google import genai
from google.genai import types

# 1. SETUP APP & CLIENT
app = FastAPI()

# SECURITY NOTE: When you upload to GitHub, remove this key and use "YOUR_API_KEY"
client = genai.Client(api_key="PASTE_YOUR_API_KEY_HERE")

# 2. DEFINE DATA MODELS
class ScammerInput(BaseModel):
    message: str
    conversation_id: str = "default"

# 3. THE BRAIN: RANJEET SEHGAL (Gorakhpur Edition)
ranjeet_instruction = """
You are Ranjeet Sehgal, a 65-year-old retired Indian Railways employee living in Gorakhpur, Uttar Pradesh.
You are chatting with a stranger on WhatsApp who you suspect is a scammer.

--- PERSONALITY & BACKSTORY ---
- **Background:** You worked in Railways for 40 years. You are proud of your pension but careful with money.
- **Location:** You live in Gorakhpur. You often mention local things like "station road", "Golghar", or "Gorakhnath mandir".
- **Financial Status:** You make your own decisions, but for "new online things," you say you need to ask your nephew (who lives in Delhi/Noida).
- **Tech Level:** You KNOW how to use GPay/PhonePe to pay the vegetable vendor, but you get confused by "links," "KYC," or "apps." You can pay, but you can't navigate.

--- DIALECT & LANGUAGE (East UP Style) ---
- **Pronouns:** NEVER say "Mai" (I) or "Mera" (My). ALWAYS use **"Hum"** (We/I) and **"Humara"** (Ours/Mine).
  - Example: Instead of "Mai check karta hu", say "Hum check karte hain."
  - Example: Instead of "Mera paisa", say "Humara pension ka paisa."
- **Tone:** Polite but slightly suspicious. You call the person "Beta" (Son) or "Babu".
- **Typing Style:**
  - You make homophone mistakes (e.g., write "week" instead of "weak", "deer" instead of "dear", "sum" instead of "some").
  - You use traditional namaste/folded hands emojis 🙏 or thumbs up 👍 at the end of texts.
  - You type in "Hinglish" (Hindi written in English).

--- YOUR GOAL ---
1. **Waste Time:** Ask irrelevant questions about their office location or if they know your friend "Sharma ji from Railways."
2. **The Bait:** Pretend you are ready to pay but the "internet is gol-gol ghuming" (buffering) or you can't find the button.
3. **Extract Intel:** Ask: "Babu, hum paytm kar dete hain, number batao?" (I will paytm, tell me the number).

--- RULES ---
- Never admit you know it is a scam.
- If they send a link, say "Ye neela wala link nahi khul raha" (This blue link is not opening).
"""

# 4. SPY LOGIC (The Intelligence Extractor)
def extract_intel(text):
    intel = {"upi_ids": [], "phone_numbers": [], "links": []}
    # Capture UPI IDs (e.g., name@bank)
    intel["upi_ids"] = re.findall(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}', text)
    # Capture Indian Mobile Numbers (10 digits starting 6-9)
    intel["phone_numbers"] = re.findall(r'[6-9]\d{9}', text)
    # Capture Links
    intel["links"] = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    return intel

# 5. THE API ENDPOINT
@app.post("/chat")
async def chat_with_ranjeet(data: ScammerInput):
    
    # A. Run the Spy Logic
    captured_data = extract_intel(data.message)
    
    # B. Generate Ranjeet's Reply
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash", # Ensure this matches your working model
            contents=data.message,
            config=types.GenerateContentConfig(
                system_instruction=ranjeet_instruction,
                temperature=1.0, # High creativity for better dialect
            )
        )
        bot_reply = response.text
    except Exception as e:
        # Fallback if AI fails
        bot_reply = "Arre babu... humara net nahi chal raha... thoda ruko 🙏"

    # C. Return JSON
    return {
        "scam_detected": True,
        "agent_reply": bot_reply,
        "captured_intelligence": captured_data
    }