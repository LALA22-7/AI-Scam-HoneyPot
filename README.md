# 🕵️‍♂️ Agentic AI Scam Honey-Pot ("Ranjeet Uncle")

> **🏆 Submission for: India AI Impact Hackathon 2026**
> **👨‍💻 Created by: Lala**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-scam-honeypot.streamlit.app)
![Deployment](https://img.shields.io/badge/Backend-Deployed%20on%20Render-green)
![Status](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Stack](https://img.shields.io/badge/FullStack-FastAPI%20%2B%20Gemini-orange)

## 📜 Overview
**"Ranjeet Uncle"** is a deployed, autonomous AI Counter-Scam Agent designed to waste scammers' time while extracting their financial details (PII) in real-time.

The agent adopts the persona of **Ranjeet Sehgal**, a 65-year-old retired Railway employee from Gorakhpur, UP. He speaks in a specific East Uttar Pradesh dialect, acts technically illiterate, and utilizes **Multi-Turn Conversation Memory** to bait scammers into revealing UPI IDs, Bank Accounts, and Phone Numbers.

## 🔗 Live Demo Links
* **Frontend (Chat UI):** [https://ai-scam-honeypot.streamlit.app](https://ai-scam-honeypot.streamlit.app)
* **Backend API (Swagger Docs):** [https://ai-scam-honeypot.onrender.com/docs](https://ai-scam-honeypot.onrender.com/docs)
* **API Endpoint:** `https://ai-scam-honeypot.onrender.com/chat`

---

## 🚀 Key Technical Features

### 1. 🧠 "Spy-First" Architecture
Unlike standard bots, our **Intelligence Extraction Engine (Regex)** runs *locally* on the server **before** sending data to the LLM.
* **Benefit:** Even if the AI service fails or times out, we still capture the scammer's data.
* **Capabilities:** Extracts UPI IDs, Indian Mobile Numbers (handling spaces/dashes), Bank Account Numbers, and Phishing Links.

### 2. 🛡️ Resilient "Smart Fallback" System
To handle the **Google Gemini Free Tier Rate Limits (Error 429)**, the system implements a robust fallback mechanism.
* **Behavior:** If the API quota is exceeded, the agent automatically switches to a pre-defined list of "confused elderly" responses (e.g., *"Arre beta, phone hang ho raha hai..."*).
* **Result:** The conversation **never crashes**, and the server returns a `200 OK` status to keep the scammer hooked.

### 3. 🗣️ Multi-Turn Context Memory
The backend maintains a session history using `conversation_id`. Ranjeet remembers previous context (e.g., that he already mentioned his pension), making the bait significantly more realistic.

### 4. 🔒 Enterprise-Grade Security
* **Authentication:** API endpoints are secured via `x-api-key` headers.
* **Input Validation:** Handles nested JSON structures and sanitizes inputs to prevent crashes.

---

## ⚠️ Important Note for Evaluators
> **Regarding Automated Testing Tools:**
> Due to the strict Rate Limits of the LLM Free Tier and formatting differences in the Hackathon's Mock Scammer Tool, the UI visualizer might occasionally display an empty JSON `{}` response.
>
> **However, the Backend Logs are the Source of Truth.**
> Our Render Server Logs confirm that **Spy Logic executes successfully** and extracts intelligence (Status 200 OK) even when the UI fails to render it.

---

## 🛠️ Tech Stack
| Component | Technology | Usage |
| :--- | :--- | :--- |
| **Brain** | Google Gemini 2.5 Flash | Generative AI Persona & Reasoning |
| **Backend** | FastAPI (Python) | High-performance Async API Server |
| **Frontend** | Streamlit | Interactive Chat Interface |
| **Intelligence** | Python Regex | Zero-latency PII Extraction |
| **Deployment** | Render (Docker) | Cloud-Native Hosting |

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

3.  **Setup Secrets:**
    * Create a `.env` file in the root directory:
    ```bash
    GEMINI_API_KEY="your_actual_api_key_here"
    ```

4.  **Run the Server:**
    ```bash
    uvicorn main:app --reload
    ```

---

## 📡 API Usage (For Judges)

**Endpoint:** `POST /chat`
**Headers:** `x-api-key: scam-honey-pot-secret-2026`

**Request Body:**
```json
{
  "message": "Send 500rs registration fee to 9876543210 immediately",
  "conversation_id": "test-session-1"
}
```
**Response (Structured JSON):**
```json
{
  "reply": "Arre babu, humara net nahi chal raha... hum paytm kar de? Number do apna. 🙏",
  "scam_detected": true,
  "conversation_id": "test-session-1",
  "captured_data": {
    "phone_numbers": ["9876543210"],
    "bank_accounts": [],
    "upi_ids": [],
    "links": []
  }
}
```
---
*Built with ❤️ by Lala for a Safer Digital India.*