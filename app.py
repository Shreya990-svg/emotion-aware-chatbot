import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

# --- Streamlit page config ---
st.set_page_config(page_title="SoulTalk: Emotion-Aware Chatbot", layout="centered")

# --- Custom CSS for Dark Theme & Better Contrast ---
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
            background-color: #1e88e5;
            color: white;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 8px;
        }
        .bot-msg {
            background-color: #2e7d32;
            color: white;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 12px;
        }
        .stTextInput > div > div > input {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center;'>🧠 SoulTalk: Your Emotion-Aware Friend 🤗</h1>", unsafe_allow_html=True)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Emotion-Aware Prompt Template ---
system_prompt = """
You are SoulTalk, a kind, emotionally supportive chatbot. 
Your responses must feel like a comforting, empathetic conversation with a friend.

1. Detect the emotional tone of the user's message using valence and arousal.
2. Respond without naming emotions directly (no emotion labels).
3. Be supportive, understanding, and use calming or uplifting language.
4. Avoid repeating the same phrases in every response.
"""

# --- Chat Input ---
user_input = st.text_input("Type your message here 👇", key="input")

# --- Process Input ---
if user_input:
    # Append user message
    st.session_state.chat_history.append(("You", user_input))

    # Generate response from Gemini
    full_prompt = system_prompt + f"\nUser: {user_input}\nSoulTalk:"
    response = model.generate_content(full_prompt)
    bot_reply = response.text.strip()

    # Append bot reply
    st.session_state.chat_history.append(("SoulTalk", bot_reply))

# --- Display Chat ---
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"<div class='user-msg'><strong>{sender}:</strong> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><strong>{sender}:</strong> {message}</div>", unsafe_allow_html=True)
