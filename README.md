# 🕵️‍♂️ Agentic AI Scam Honey-Pot ("Ranjeet Uncle")

**Submitted for:** India AI Impact Hackathon  
**Problem Statement:** Agentic Honey-Pot for Scam Detection & Intelligence Extraction

## 📜 Overview
This project is an **Autonomous AI Agent** designed to waste scammers' time while extracting their financial details. 

The agent adopts the persona of **"Ranjeet Sehgal"**, a 65-year-old retired Railway employee from Gorakhpur, UP. He speaks in a specific **East Uttar Pradesh dialect** (using "Hum" instead of "Mai") and acts technically illiterate to bait scammers into revealing their UPI IDs and phone numbers.

## 🚀 Key Features
* **Active Persona:** Roleplays as a confused, talkative elderly man who constantly talks about his pension and nephew.
* **Dialect Engineering:** Uses "Hinglish" and regional grammar (East UP style) to sound authentic.
* **Stealth Intelligence Extraction:** A background "Spy" script uses **Regex** to capture UPI IDs, phone numbers, and links from the scammer's messages automatically.
* **JSON Output:** Returns structured data for every interaction, flagging scams and listing captured details.

## 🛠️ Tech Stack
* **Brain:** Google Gemini 2.5 Flash (Generative AI)
* **Backend:** FastAPI (Python)
* **Server:** Uvicorn
* **Logic:** Regular Expressions (Regex)

## ⚙️ How to Run Locally
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/AI-Scam-HoneyPot.git](https://github.com/YOUR_USERNAME/AI-Scam-HoneyPot.git)
    cd AI-Scam-HoneyPot
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup API Key:**
    * Open `main.py`.
    * Replace `PASTE_YOUR_API_KEY_HERE` with your actual Google Gemini API Key.

4.  **Run the Server:**
    ```bash
    python -m uvicorn main:app --reload
    ```

5.  **Test the Agent:**
    * Open your browser to: `http://127.0.0.1:8000/docs`
    * Send a POST request to `/chat` with a scam message.

## 📸 Example Output
**Input:** "Send 500rs registration fee to 9876543210"

**Agent Reply:** > "Arre babu, humara net nahi chal raha... hum station road wale office gaye the pichle hafte. Hum paytm kar de? Number do apna. 🙏"

**Captured Data:** `{'phone_numbers': ['9876543210']}`

---
*Created by Lala for the India AI Impact Hackathon 2026*