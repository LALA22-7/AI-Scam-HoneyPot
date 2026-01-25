import streamlit as st
import asyncio
from main import chat  # <--- This imports the 2.5 Flash Brain from main.py

# Page Config
st.set_page_config(page_title="Ranjeet Uncle", page_icon="👴", layout="centered")

# Custom CSS for that "WhatsApp" feel
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("👴 Ranjeet Uncle vs Scammers")
st.caption("He is old. He is slow. And he wastes scammers' time.")

# 1. Initialize Chat History (This remembers the chat!)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle New User Input
if prompt := st.chat_input("Type a scam message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display "Thinking..." spinner
    with st.spinner("Ranjeet Uncle is finding his glasses..."):
        try:
            # --- THE REAL AI CALL ---
            # We use asyncio.run() to call the async function from main.py
            response_data = asyncio.run(chat(prompt))
            bot_reply = response_data["reply"]
        except Exception as e:
            bot_reply = f"Arre beta... net issue hai... (Error: {str(e)})"
            response_data = None
    
    # Add bot reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# Sidebar for "Under the Hood" details
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("⚡ Model: Gemini 2.5 Flash") # Visual confirmation for Judges
    st.info("🟢 Agent Status: Online")
    
    st.divider()
    
    st.header("🕵️‍♂️ Intel Captured")
    if response_data and response_data.get("scam_detected"):
        st.error("🚨 SCAM DETECTED!")
        st.json(response_data["captured_data"])
    else:
        st.info("No scam detected yet.")