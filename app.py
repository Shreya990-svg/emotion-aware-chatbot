import streamlit as st
import google.generativeai as genai

# --- Configuration ---
st.set_page_config(page_title="SoulTalk: Emotion-Aware Chatbot 🤗", page_icon="🧠")

# Setup Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Emotion valence-arousal mapping
emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "neutral": (0.0, 0.0)
}

# --- Emotion Detection ---
def get_emotion(text):
    text = text.lower()
    if any(word in text for word in ["happy", "glad", "joy", "smile", "excited"]): return "joy"
    if any(word in text for word in ["sad", "cry", "upset", "down", "unhappy"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious", "annoyed"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous", "anxious", "stressed"]): return "fear"
    if any(word in text for word in ["surprised", "wow", "unexpected"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "nasty"]): return "disgust"
    return "neutral"

# --- Gemini Response Generation ---
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

# --- Initialize Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- UI: Title & Styling ---
st.markdown("<h1 style='text-align: center; color: #ff66c4;'>🧠 SoulTalk: Your Emotion-Aware Friend 🤗</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>💬 Conversation</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- Input Form ---
with st.form("chat_form"):
    user_input = st.text_input("Type your message here 👇", key="user_input", placeholder="How are you feeling today?")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
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

    # Clear input field by resetting state
    st.session_state.user_input = ""

    # Optional: st.experimental_rerun() if you want the screen to scroll down

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    st.markdown(f"<b>👤 You:</b> {msg['user']}", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#252525;padding:10px;border-radius:10px;color:#f0f0f0;'>🧠 <b>SoulTalk:</b> {msg['reply']}</div>", unsafe_allow_html=True)
    st.markdown("---")
