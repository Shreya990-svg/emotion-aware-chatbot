import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API key securely (using Streamlit secrets)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Emotion mapping with valence and arousal values
emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "stress": (-0.7, 0.7),
    "neutral": (0.0, 0.0)
}

# Detect basic emotion from text
def get_emotion(text):
    text = text.lower()
    if any(word in text for word in ["happy", "glad", "joy", "smile", "excited"]): return "joy"
    if any(word in text for word in ["sad", "cry", "upset", "depressed", "down"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious", "annoyed"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous", "anxious"]): return "fear"
    if any(word in text for word in ["surprised", "shocked", "wow"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "nasty"]): return "disgust"
    if any(word in text for word in ["stress", "tired", "tense", "burned out"]): return "stress"
    return "neutral"

# Generate friendly emotionally aware response
def friendly_reply(history, user_text, emotion_label):
    convo = "\n".join([f"You: {msg['user']}\nFriend: {msg['bot']}" for msg in history])
    prompt = f"""
You're a kind, emotionally intelligent friend. The user is feeling '{emotion_label}'.

Tone:
- Friendly and natural
- Supportive, comforting
- Keep it to just 1–2 lines max
- Make them feel better, not robotic

Chat history:
{convo}
You: {user_text}
Friend:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Streamlit App ---
st.set_page_config(page_title="Friendly Chat", page_icon="💬")
st.markdown("<h1 style='color:#4b8bbe;'>💬 Chat with Your Emotional Buddy</h1>", unsafe_allow_html=True)

# Session state for conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_input("You 👤:", key="user_input_field")

# On message sent
if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0.0, 0.0))  # used internally
    bot_response = friendly_reply(st.session_state.chat_history, user_input, emotion)

    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion,  # still stored if needed later
        "valence": valence,
        "arousal": arousal
    })

# Display conversation only (no emotion stats shown)
for msg in st.session_state.chat_history:
    st.markdown(f"**👤 You:** {msg['user']}")
    st.markdown(f"**💬 {msg['bot']}**")
    st.markdown("---")
