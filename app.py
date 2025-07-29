import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page config
st.set_page_config(page_title="SoulTalk: Your Emotion-Aware Friend", page_icon="🧠", layout="centered")

# Apply custom CSS for improved color contrast
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #f5f5f5;
        }
        .chat-box {
            margin-bottom: 10px;
        }
        .user-msg {
            background-color: #2196f3;  /* Brighter blue */
            color: #ffffff;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 8px;
            font-size: 16px;
        }
        .bot-msg {
            background-color: #66bb6a;  /* Soft green */
            color: #ffffff;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 12px;
            font-size: 16px;
        }
        h1 {
            color: #ffb6c1;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Gemini Pro model initialization
model = genai.GenerativeModel("gemini-pro")

# System prompt
system_prompt = """
You are SoulTalk, an emotion-aware, supportive AI friend.
Always respond in a warm, kind, emotionally uplifting, and stress-relieving way.
You analyze the emotional tone behind user input (valence-arousal), then respond supportively.
Do not mention valence/arousal or emotion detection.
Don't label or name any emotion.
Only offer comforting conversation that feels like a safe space.
Avoid therapist language or generic advice.
Sound like a caring friend who truly wants to help.

Tone: gentle, relaxed, empathetic.
Style: short paragraphs, soft conversational flow, no technical words.
"""

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown("## 🧠 <span style='color:#ffffff;'>SoulTalk: Your Emotion-Aware Friend 🤗</span>", unsafe_allow_html=True)

# User input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

    # Generate response
    convo = model.start_chat(history=[
        {"role": "user", "parts": [system_prompt]},
        *st.session_state.chat_history,
    ])
    response = convo.send_message(user_input)
    bot_reply = response.text

    # Add bot message
    st.session_state.chat_history.append({"role": "model", "parts": [bot_reply]})

# Display chat history
for i, msg in enumerate(st.session_state.chat_history):
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-box user-msg'>👤 <b>You:</b> {msg['parts'][0]}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-box bot-msg'>🧠 <b>SoulTalk:</b> {msg['parts'][0]}</div>", unsafe_allow_html=True)
