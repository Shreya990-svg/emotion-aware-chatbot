import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API key securely from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Emotion mapping with valence-arousal (internal use only)
emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "stress": (-0.6, 0.6),
    "neutral": (0.0, 0.0)
}

# Improved emotion detection with continuity
def get_emotion(text, prev_emotion=None):
    text = text.lower()
    emotion = "neutral"
    if any(word in text for word in ["happy", "glad", "joy", "smile", "excited"]): emotion = "joy"
    elif any(word in text for word in ["sad", "cry", "upset", "depressed", "down"]): emotion = "sadness"
    elif any(word in text for word in ["angry", "mad", "furious", "annoyed"]): emotion = "anger"
    elif any(word in text for word in ["scared", "afraid", "nervous", "anxious"]): emotion = "fear"
    elif any(word in text for word in ["surprised", "shocked", "wow"]): emotion = "surprise"
    elif any(word in text for word in ["disgusted", "gross", "nasty"]): emotion = "disgust"
    elif any(word in text for word in ["stress", "tired", "tense", "burned out"]): emotion = "stress"

    # If follow-up short message, carry emotion forward
    if emotion == "neutral" and prev_emotion and len(text.split()) <= 5:
        emotion = prev_emotion

    return emotion

# Generate friendly response using Gemini API
def friendly_reply(history, user_text, emotion_label):
    convo = "\n".join([f"You: {msg['user']}\nFriend: {msg['bot']}" for msg in history])
    prompt = f"""
You're a caring, emotionally intelligent friend helping someone through tough or confusing emotions.

The user is currently feeling '{emotion_label}'.

Respond in a short, comforting, warm tone (1–3 lines).
Your goal is to:
- Make them feel understood
- Be gentle, hopeful, and human-like
- Offer real, small ideas or emotional comfort (not general positivity)
- If they ask for help or 'what to do', give creative, thoughtful suggestions

Here's your friendly conversation so far:
{convo}
You: {user_text}
Friend:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Streamlit App Setup ---
st.set_page_config(page_title="Emotion-Aware Chatbot 🫲", page_icon="💬")
st.title("Talk to Your Emotion-Aware Chatbot 💬")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input (use key to avoid duplicate ID errors)
user_input = st.text_input("You 👤:", key="user_input_field")

# Handle message
if user_input:
    prev_emotion = st.session_state.chat_history[-1]["emotion"] if st.session_state.chat_history else None
    emotion = get_emotion(user_input, prev_emotion)
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
    st.markdown(f"{msg['bot']}")
    st.markdown("---")
