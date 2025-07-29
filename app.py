import streamlit as st
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Emotion-to-valence/arousal mapping
emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "neutral": (0.0, 0.0)
}

# Simple emotion detection
def get_emotion(text):
    text = text.lower()
    if any(w in text for w in ["happy", "glad", "joy", "smile", "excited"]): return "joy"
    if any(w in text for w in ["sad", "cry", "upset", "down", "unhappy"]): return "sadness"
    if any(w in text for w in ["angry", "mad", "furious", "annoyed"]): return "anger"
    if any(w in text for w in ["scared", "afraid", "nervous", "anxious"]): return "fear"
    if any(w in text for w in ["surprised", "wow", "unexpected"]): return "surprise"
    if any(w in text for w in ["disgusted", "gross", "nasty"]): return "disgust"
    return "neutral"

# Generate emotionally-aware reply
def generate_reply(history, user_text, emotion):
    context = "\n".join([f"You: {h['user']}\nSoulTalk: {h['reply']}" for h in history])

    prompt = f"""
You are SoulTalk, an emotionally intelligent AI friend.
Reply in a soothing, kind, and emotionally uplifting tone.
User currently feels: {emotion}

Chat so far:
{context}

User says:
You: {user_text}
SoulTalk:"""

    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# -- Streamlit UI setup --
st.set_page_config(page_title="🧠 SoulTalk", layout="centered")

# Improved dark theme colors
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #f5f5f5;
        }
        .chat-box {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 10px;
        }
        .user-msg {
            background-color: #0d47a1;
            color: #ffffff;
            border-left: 4px solid #42a5f5;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 8px;
            font-size: 15px;
        }
        .bot-msg {
            background-color: #2e7d32;
            color: #ffffff;
            border-left: 4px solid #81c784;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 12px;
            font-size: 15px;
        }
        h1 {
            color: #f48fb1;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🧠 SoulTalk: Your Emotion-Aware Friend 🤗")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("Type your message here...")

# Process message
if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0.0, 0.0))
    reply = generate_reply(st.session_state.chat_history, user_input, emotion)

    st.session_state.chat_history.append({
        "user": user_input,
        "reply": reply,
        "emotion": emotion,
        "valence": valence,
        "arousal": arousal
    })

# Show chat
for msg in st.session_state.chat_history:
    st.markdown(f"<div class='user-msg'><strong>You:</strong> {msg['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-msg'><strong>SoulTalk:</strong> {msg['reply']}</div>", unsafe_allow_html=True)
