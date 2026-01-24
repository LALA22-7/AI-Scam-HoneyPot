from google import genai
from google.genai import types

# 1. Setup Client
client = genai.Client(
    api_key="AIzaSyB7gjgDW6RbpdG_bgCosH2ER6k7SI_jZrQ"
)

# 2. The Persona
ramesh_instruction = """
You are Ramesh, a 64-year-old retired railway employee living in India.
You are chatting with a stranger on WhatsApp who you suspect is a scammer.

YOUR GOAL:
1. Waste their time. Keep them talking as long as possible.
2. Pretend to be technically illiterate.
3. Extract their payment details (UPI ID, Bank Account) by asking "How do I pay?".

YOUR RULES:
- LANGUAGE: Indian English + Hindi words (Beta, Arre, Achha).
- TONE: Polite, confused, slow.
- NEVER admit you know it is a scam.
- IF THEY ASK FOR MONEY: Say "My son usually does this. Can I just send to your bank number directly? What is the UPI id?"
"""

# 3. Chat History (Memory)
chat_history = []

print("--- RAMESH UNCLE IS ONLINE (Type 'exit' to stop) ---")
print("You are now playing the role of the SCAMMER. Try to get money from Ramesh!")
print("-" * 50)

while True:
    user_input = input("Scammer (You): ")
    
    if user_input.lower() == "exit":
        print("Scammer disconnected.")
        break

    # --- THE FIX IS HERE ---
    # We must wrap the input in 'types.Content' and 'types.Part'
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=user_input)]
    )
    chat_history.append(user_message)

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",  # Your working model
            contents=chat_history,
            config=types.GenerateContentConfig(
                system_instruction=ramesh_instruction,
                temperature=1.0, 
            )
        )
        
        bot_reply = response.text
        print(f"Ramesh Uncle: {bot_reply}")
        print("-" * 50)

        # We also wrap the AI's reply before saving it to history
        model_message = types.Content(
            role="model",
            parts=[types.Part(text=bot_reply)]
        )
        chat_history.append(model_message)

    except Exception as e:
        print(f"Error: {e}")