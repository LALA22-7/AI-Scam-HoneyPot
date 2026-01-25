# 🕵️‍♂️ Agentic AI Scam Honey-Pot ("Ranjeet Uncle")

> **Submitted for: India AI Impact Hackathon 2026**
> **Created by: Lala**

![Project Status](https://img.shields.io/badge/Status-Active-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Stack](https://img.shields.io/badge/FullStack-Streamlit%20%2B%20FastAPI-orange)

## 📜 Overview
**"Ranjeet Uncle"** is an Autonomous AI Agent designed to waste scammers' time while extracting their financial details.

The agent adopts the persona of **Ranjeet Sehgal**, a 65-year-old retired Railway employee from Gorakhpur, UP. He speaks in a specific East Uttar Pradesh dialect (using "Hum" instead of "Mai"), acts technically illiterate, and constantly distracts scammers with stories about his pension and nephew to bait them into revealing UPI IDs and phone numbers.

## 🚀 Key Features
* **🎭 Active Persona:** Roleplays as a confused, talkative elderly man. He never breaks character.
* **🗣️ Dialect Engineering:** Uses "Hinglish" and regional grammar (East UP style) to sound authentic.
* **🕵️‍♂️ Stealth Intelligence Extraction:** A background "Spy" script uses **Regex** to automatically capture UPI IDs, phone numbers, and links from the scammer's messages in real-time.
* **🖥️ Dual Interface:**
    * **Web UI:** A WhatsApp-style chat interface for easy testing.
    * **REST API:** A full backend ready for integration with telecom networks.
* **🔒 Secure:** Uses Environment Variables for API key protection.

## 🛠️ Tech Stack
* **Brain:** Google Gemini 2.5 Flash (Generative AI)
* **Frontend:** Streamlit (Python Web Framework)
* **Backend:** FastAPI (High-performance API)
* **Server:** Uvicorn
* **Logic:** Regular Expressions (Regex) & Pydantic

---

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

3.  **Setup Security Crucial!**
    * Create a file named .env in the root folder and add your Google Gemini API Key. (Do not hardcode keys in the main script!)
    ```bash
    GEMINI_API_KEY="your_actual_api_key_here"
    ```
## ❓Choose Your Run Mode

A.  **Run the API Server Backend**

    ```bash
    python -m uvicorn main:app --reload
    ```

    * Open your browser to: `http://127.0.0.1:8000/docs`
    * Send a POST request to `/chat` with a scam message.

B.  **Run the Web App Frontend**

    ```bash
    python -m streamlit run app.py
    ```
    
    * Access at: `http://localhost:8501`

## 📸 Example Output
**Input:** "Send 500rs registration fee to 9876543210"

**Agent Reply:** > "Arre babu, humara net nahi chal raha... hum station road wale office gaye the pichle hafte. Hum paytm kar de? Number do apna. 🙏"



**Captured Intel[JSON]** `{
  "scam_detected": true,
  "captured_data": {
    "phone_numbers": ["9876543210"],
    "upi_ids": [],
    "links": []
  }
}`
## 📸 Screenshots

| Web Interface (Streamlit) | API Docs (Swagger UI) |
|:---:|:---:|
| ![Streamlit UI](PASTE_YOUR_STREAMLIT_IMAGE_LINK_HERE) | ![Swagger UI](PASTE_YOUR_SWAGGER_IMAGE_LINK_HERE) |
---
*Built with ❤️ by Lala for a Safer Digital India.*