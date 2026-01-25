import streamlit as st
import asyncio
from main import chat  # <--- Imports the 2.5 Flash Brain from main.py

# Page Config
st.set_page_config(page_title="Ranjeet Uncle", page_icon="👴", layout="centered")

# Custom CSS
st.markdown("""
<style>
    .stTextInput > div > div > input { background-color: #f0f2f6; }
    .chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex }
    .chat-message.user { background-color: #2b313e }
    .chat-message.bot { background-color: #475063 }
</style>
""", unsafe_allow_html=True)

st.title("👴 Ranjeet Uncle vs Scammers")
st.caption("He is old. He is slow. And he wastes scammers' time.")

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize a place to store the LATEST scam intel so it doesn't disappear
if "latest_intel" not in st.session_state:
    st.session_state.latest_intel = None

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- HANDLE NEW INPUT ---
if prompt := st.chat_input("Type a scam message..."):
    # 1. Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get Bot Reply
    with st.spinner("Ranjeet Uncle is finding his glasses..."):
        try:
            # Call the AI
            response_data = asyncio.run(chat(prompt))
            bot_reply = response_data["reply"]
            
            # SAVE the intel to Session State (So the sidebar can see it later!)
            st.session_state.latest_intel = response_data
            
        except Exception as e:
            bot_reply = f"Arre beta... net issue hai... (Error: {str(e)})"
            st.session_state.latest_intel = None
    
    # 3. Show Bot Reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# --- SIDEBAR (SAFE MODE) ---
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("⚡ Model: Gemini 2.5 Flash")
    st.info("🟢 Agent Status: Online")
    
    st.divider()
    
    st.header("🕵️‍♂️ Intel Captured")
    
    # Check the SESSION STATE, not the local variable
    data = st.session_state.latest_intel
    
    if data and data.get("scam_detected"):
        st.error("🚨 SCAM DETECTED!")
        st.json(data["captured_data"])
    else:
        st.info("No scam data in latest message.")