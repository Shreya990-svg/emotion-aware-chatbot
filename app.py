import streamlit as st
import google.generativeai as genai
import os

# Securely configure Gemini API key from Streamlit secrets
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Emotion mapping using valence-arousal model
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

# Enhanced emotion detection
def get_emotion(text):
    text = text.lower()
    if any(word in text for word in ["happy", "glad", "joy", "smile", "excited"]): return "joy"
    if any(word in text for word in ["sad", "cry", "upset", "depressed", "down"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious", "annoyed"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous", "anxious"]): return "fear"
    if any(word in text for word in ["surprised", "shocked", "wow"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "nasty"]): return "disgust"
    if any(word in text for word in ["stress", "tense", "tired", "burned out"]): return "stress"
    return "neutral"

# Gemini-powered empathetic reply
def friendly_reply(history, user_text, emotion_label):
    convo = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in history])
    prompt = f"""
You're a warm, caring chatbot friend. The user is feeling '{emotion_label}'.

Your tone:
- Uplifting and casual
- Comforting and kind
- Speak like a best friend trying to help

Respond to what the user just said in 1–2 lines (no long paragraphs).

Conversation:
{convo}
You: {user_text}
Bot:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Streamlit UI ---
st.set_page_config(page_title="Emotion Chatbot", page_icon="💬")
st.markdown("<h1 style='color:#4b8bbe;'>💬 Chat with Your Friendly Bot</h1>", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input
user_input = st.text_input("You 👤:", key="user_input_field")

if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0.0, 0.0))
    bot_response = friendly_reply(st.session_state.chat_history, user_input, emotion)

    # Update chat memory
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion,
        "valence": valence,
        "arousal": arousal
    })

# Show entire chat log
for msg in st.session_state.chat_history:
    st.markdown(f"**👤 You:** {msg['user']}")
    st.markdown(f"**🤖 Bot:** {msg['bot']}")
    st.caption(f"_Emotion: {msg['emotion']} → Valence: {msg['valence']}, Arousal: {msg['arousal']}_")
    st.markdown("---")
