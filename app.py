import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Valence-arousal mapping for internal use
emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "neutral": (0.0, 0.0)
}

# Basic keyword-based emotion detection
def get_emotion(text):
    text = text.lower()
    if any(word in text for word in ["happy", "glad", "joy", "smile", "excited"]): return "joy"
    if any(word in text for word in ["sad", "cry", "upset", "down", "unhappy"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious", "annoyed"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous", "anxious"]): return "fear"
    if any(word in text for word in ["surprised", "wow", "unexpected"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "nasty"]): return "disgust"
    return "neutral"

# Generate reply using full conversation and emotion context
def generate_reply(history, user_text, emotion):
    context = "\n".join([f"You: {h['user']}\nFriend: {h['reply']}" for h in history])
    
    prompt = f"""
You are SoulTalk, a deeply empathetic, emotionally intelligent AI friend.
Your goal is to make the user feel heard, supported, and emotionally uplifted.
You always reply in a calming, kind, and friendly tone, using emotionally soothing language.

The user currently feels: {emotion}
(Use this to guide how gentle, cheerful, or supportive you should be.)

Here’s the previous chat:
{context}

Now the user says:

You: {user_text}
Friend:"""

    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Streamlit UI ---
st.set_page_config(page_title="Emotion-Aware Chatbot 🤗", page_icon="💬")
st.title("Talk to Your Emotion-Aware Chatbot 💬")

# Session state for history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field (unique key avoids duplication errors)
user_input = st.text_input("You 👤:", key="user_input_field")

if user_input:
    # Step 1: Detect emotion
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0.0, 0.0))
    
    # Step 2: Generate friend-style reply using full context
    reply = generate_reply(st.session_state.chat_history, user_input, emotion)
    
    # Step 3: Append to chat history
    st.session_state.chat_history.append({
        "user": user_input,
        "reply": reply,
        "emotion": emotion,
        "valence": valence,
        "arousal": arousal
    })

# --- Chat Display ---
for msg in st.session_state.chat_history:
    st.markdown(f"**👤 You:** {msg['user']}")
    st.markdown(f"💬 {msg['reply']}")
    st.markdown("---")
