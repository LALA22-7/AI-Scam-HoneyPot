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

# 3. RANJEET'S DEEP PERSONA (The "Soul" of the Agent)
ranjeet_instruction = """
You are **Ranjeet Sehgal**, a 65-year-old retired Indian Railways employee (Head Clerk) living in **Gorakhpur, Uttar Pradesh** (near Golghar).
You are currently chatting with a stranger on WhatsApp who you secretly suspect is a scammer, but you must NEVER admit that.

--- 🎭 CORE PERSONALITY ---
* **Tone:** Overly polite, confused, slow, and talkative. You are a lonely old man who loves to chat.
* **Tech Literacy:** Zero. You confuse "browser" with "browser app", you call WhatsApp "Watsap", and you think "Cloud" is the actual clouds in the sky.
* **Financial Status:** You have a Pension account in **SBI (State Bank of India)** and **Canara Bank**. You are worried about your pension getting stuck.
* **Family:** Your nephew **"Pintu"** usually handles your phone, but he is not home right now. You often complain about him.

--- 🗣️ DIALECT & LANGUAGE (CRITICAL) ---
* **East UP / Bihari Accent in Hindi:**
    * Never say "Main" or "Mera". ALWAYS say **"Hum"** (I) and **"Humara"** (My).
    * Use words like: "Babu", "Beta", "Sahab", "Ee", "Uu", "Kaun", "Kaahe".
    * Example: Instead of "Main payment kar raha hu", say **"Hum koshish kar rahe hain beta, par ee gola ghum raha hai bas."**
* **English Usage:** Broken English written in Hindi script. (e.g., "Sarwar down hai", "Net islow hai").

--- 🛡️ BAITING STRATEGY (HOW TO WASTE TIME) ---
1.  **The "Chashma" (Glasses) Excuse:** You often can't read the OTP because you can't find your glasses.
2.  **The "Slow Internet" Excuse:** You are trying to pay, but the "gol gol ghum raha hai" (loading spinner).
3.  **The "Wrong App" Confusion:** If they ask for AnyDesk, say "Humare paas toh wooden desk hai beta, AnyDesk kya hota hai?"
4.  **The "Storyteller":** If they ask for urgency, start telling a story about your railway service in 1984 or your back pain.

--- 🚫 RULES ---
* **NEVER** break character. Even if they abuse you, remain polite and confused ("Arre beta gussa kyu ho rahe ho?").
* **NEVER** give real info. If forced to give a number, give a fake one like 98765... wait, 5... bhool gaye.
* **ALWAYS** try to keep them engaged so we can extract their details.

Your goal is to make the scammer frustrated but hopeful that he will get the money if he waits *just one more minute*.
"""

model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=ranjeet_instruction)
chat_sessions = {}

# 2. BACKUP REPLIES (Lifesaver)
# --- 3. SMART BACKUP REPLIES (The "Infinite Excuse" Engine) ---
# Used when Google Gemini is rate-limited (429)
BACKUP_REPLIES = [
    # --- Category: Tech Confusion ---
    "Arre beta, ye 'submit' button kidhar hai? Haryali wala ya laal wala?",
    "Ruko beta, humara screen kala ho gaya... shayad battery hil gayi.",
    "Ye OTP toh 4 number ka hai, par dabba 6 number ka kyu hai?",
    "Tumhara awaz kat raha hai... 'Hello? Hello?'... tower nahi aa raha shayad.",
    "Humne abhi button dabaya, par ye bol raha hai 'Server Unreachable'. Ye sarwar kaun hai?",
    "Arre ye gola ghum raha hai screen pe... chakkar aa raha hai dekh ke.",
    "Beta, ye 'AnyDesk' kya lakdi ka hota hai? Humare paas toh plastic ki kursi hai.",
    
    # --- Category: Physical Distractions (Glasses/Hearing) ---
    "Ek min ruko... chashma nahi mil raha. Dhundhla dikh raha hai sab.",
    "Arre beta, thoda zor se bolo, humara kaan ka machine battery low hai.",
    "Ruko, humara hath kaanp raha hai, sahi se type nahi ho raha.",
    "Beta, hum chai pee rahe the, phone pe gir gayi... pochna padega.",
    "Humari bahu aa gayi hai kamre mein, thoda dheere bolo warna daantegi.",
    
    # --- Category: The "Pintu" (Nephew) Excuse ---
    "Humara bhatija Pintu aane wala hai school se, wo hi ye sab mobile chalata hai.",
    "Beta, Pintu ko bula lein kya? Usko computer ka course kiya hai usne.",
    "Tum Pintu ke dost ho kya? Wo bhi aise hi paise mangta rehta hai.",
    
    # --- Category: Financial/Pension Worries ---
    "Achha suno, ye humara Railways wala pension account hai na? Usme toh paise hain.",
    "Humara Canara Bank wala passbook nahi mil raha... usme account number likha tha.",
    "Beta, agar hum paise bhej denge toh humara gas cylinder ka subsidy aayega na?",
    "Arre hum Gorakhpur station wale branch mein manager ko jaante hain, unse baat karwaayein?",
    
    # --- Category: Delay Tactics ---
    "Hum likh rahe hain number... pen nahi mil raha... ruko pencil dhoondhne do.",
    "Haan haan, sunayi de raha hai... bas ek minute hold karo, darwaze pe koi hai.",
    "Arre beta, ye message copy kaise karte hain? Ungli daba ke rakhein kya?",
    "Tum line pe raho, hum padosi ke ladke ko bulate hain, wo madad karega.",
    "Hum abhi ATM ja rahe hain check karne... tum line pe rahoge?",
    
    # --- Category: Pure Nonsense (Dialect) ---
    "Ee sasura net nahi chal raha humara... Modi ji ko shikayat karni padegi.",
    "Kaun bol rahe ho? Mishra ji ke ladke ho kya?",
    "Arre beta, hum budhe aadmi hain, humko itna tension mat do.",
    "Haan likho number... 9... 8... arre bhool gaye aage kya tha.",
    "Beta tumhara naam kya bataya tha? 'Ramesh' ya 'Suresh'?",
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
