import streamlit as st
import asyncio
import uuid
from main import chat  # Importing your Ranjeet logic

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ranjeet Uncle - Scam Detector",
    page_icon="👴",
    layout="centered"
)

# --- 1. SESSION ID MANAGEMENT ---
# We need a unique ID for the callback to work
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

# --- 2. MOCK BACKGROUND TASKS ---
# Streamlit doesn't have FastAPI's BackgroundTasks, so we make a fake one
class MockBackgroundTasks:
    def add_task(self, func, *args, **kwargs):
        # Just run the async function immediately in the background
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(func(*args, **kwargs))
        except Exception as e:
            print(f"Background task failed: {e}")

# --- HEADER ---
st.title("👴 Ranjeet Uncle")
st.caption("The AI that wastes scammers' time so you don't have to.")

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Say something (e.g., 'You won a lottery!')"):
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Get Ranjeet's Reply
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # --- THE FIX IS HERE ---
        # We pass the session_id and the mock_tasks object
        mock_tasks = MockBackgroundTasks()
        
        # Run async chat function
        full_response = asyncio.run(chat(prompt, st.session_state["session_id"], mock_tasks))
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- SIDEBAR (Optional) ---
with st.sidebar:
    st.header("🕵️ Spy Dashboard")
    st.write(f"Session ID: `{st.session_state['session_id']}`")
    st.info("Ranjeet is active. Any extracted data (Bank accounts, UPI) is being sent to the Hackathon server in the background.")