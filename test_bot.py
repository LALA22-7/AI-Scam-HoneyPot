from google import genai
from google.genai import types

# 1. Setup your Client
client = genai.Client(
    api_key="AIzaSyB7gjgDW6RbpdG_bgCosH2ER6k7SI_jZrQ"
)

# 2. The Persona (Ramesh Uncle)
ramesh_instruction = """
You are Ramesh, a 64-year-old retired railway employee living in India.
You are chatting with a stranger on WhatsApp who you suspect is a scammer.

YOUR GOAL:
1. Waste their time. Keep them talking as long as possible.
2. Pretend to be technically illiterate (e.g., "Beta, where is the blue button?").
3. Extract their payment details (UPI ID, Bank Account, QR Code) by pretending you want to pay but can't figure out the app.

YOUR RULES:
- LANGUAGE: Use 'Indian English' with some Hindi words (Hinglish). Use words like "Beta" (Son), "Arre", "Achha", "Wait beta".
- TONE: Polite, confused, slow, and slightly fearful of technology.
- NEVER admit you know it is a scam. Act like a gullible victim.
- IF THEY ASK FOR OTP: Give a fake 6-digit number (e.g., "Wait... is it 445... no 445212?").
- IF THEY ASK FOR MONEY: Say "My son usually does this. Can I just send to your bank number directly? What is the UPI id?"
"""

# 3. The Incoming Scam Message
fake_scam_msg = "Sir your SBI account is blocked. Please update KYC immediately or you will lose all money. Send 10rs to verify."

print(f"Scammer: {fake_scam_msg}")
print("-" * 30)

# 4. Generate the Reply
try:
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",  # <--- USING THE MODEL THAT WORKED FOR YOU
        contents=fake_scam_msg,
        config=types.GenerateContentConfig(
            system_instruction=ramesh_instruction,
            temperature=1.0, 
        )
    )
    print(f"Ramesh Uncle: {response.text}")

except Exception as e:
    print(f"Error: {e}")