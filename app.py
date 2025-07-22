import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Emotion mapping with valence-arousal
emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "neutral": (0.0, 0.0)
}

# Basic emotion detection using keywords
def get_emotion(text):
    text = text.lower()
    if any(word in text for word in ["happy", "glad", "joy", "smile", "excited"]): return "joy"
    if any(word in text for word in ["sad", "cry", "upset", "down", "unhappy"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious", "annoyed"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous", "anxious"]): return "fear"
    if any(word in text for word in ["surprised", "wow", "unexpected"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "nasty"]): return "disgust"
    return "neutral"

# Generate friendly response using Gemini API
def friendly_reply(history, user_text, emotion_label):
    convo = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in history])
    prompt = f"""
You're a kind and emotionally aware chatbot friend.
The user is feeling '{emotion_label}' right now.
Use a short, casual, warm tone. Make them feel understood and less stressed.
Respond in 1–2 friendly lines only.

Conversation so far:
{convo}
You: {user_text}
Bot:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Streamlit App Setup ---
st.set_page_config(page_title="Emotion-Aware Chatbot 🤗", page_icon="💬")
st.title("Talk to Your Emotion-Aware Chatbot 💬")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input (use key to avoid duplicate element error)
user_input = st.text_input("You 👤:", key="user_input_field")

# Handle message
if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0.0, 0.0))
    bot_reply = friendly_reply(st.session_state.chat_history, user_input, emotion)

    # Save to chat history
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_reply,
        "emotion": emotion,
        "valence": valence,
        "arousal": arousal
    })

# Display conversation history
for msg in st.session_state.chat_history:
    st.markdown(f"**You:** {msg['user']}")
    st.markdown(f"**🤖 Bot:** {msg['bot']}")
    st.caption(f"_Emotion: {msg['emotion']} → Valence: {msg['valence']}, Arousal: {msg['arousal']}_")
    st.markdown("---")
