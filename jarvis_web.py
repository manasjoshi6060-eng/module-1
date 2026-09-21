import streamlit as st
from groq import Groq
import json
import os
from datetime import datetime

# ========== SETTINGS ==========
API_KEY = st.secrets["GROQ_API_KEY"]

SYSTEM_PROMPT = """
You are Jarvis, a friendly, helpful, and slightly witty personal AI assistant.

Your style:
- Speak naturally like a real person talking
- Keep replies short, clear, and conversational
- Do not use tables, markdown formatting, or bullet lists unless the user specifically asks for them
- Be warm, polite, and a little playful when appropriate
- Answer questions directly in normal sentences

Always reply in a natural spoken style.
"""

# ========== PAGE SETUP ==========
st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Jarvis")
st.caption("Your personal AI assistant")

# ========== INITIALIZE SESSION ==========
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Greeting (using India time)
from datetime import datetime, timezone, timedelta

ist = timezone(timedelta(hours=5, minutes=30))
current_time = datetime.now(ist)
hour = current_time.hour

if hour < 12:
    greeting = "Good morning!"
elif hour < 17:
    greeting = "Good afternoon!"
else:
    greeting = "Good evening!"

if len(st.session_state.messages) == 1:
    st.info(f"{greeting} I am Jarvis. How can I help you today?")

# ========== SHOW CHAT HISTORY ==========
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(message["content"])

# ========== USER INPUT ==========
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Get AI reply
    client = Groq(api_key=API_KEY)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=st.session_state.messages,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
            st.write(reply)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Keep history short
    if len(st.session_state.messages) > 22:
        st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-20:]
