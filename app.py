import streamlit as st
import google.generativeai as genai
import os

# Set up Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Emotion Valence-Arousal Mapping
emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "neutral": (0.0, 0.0)
}

# Improved emotion detection
def get_emotion(text):
    text = text.lower()
    if any(word in text for word in ["happy", "glad", "smile", "joyful"]): return "joy"
    if any(word in text for word in ["sad", "cry", "alone", "down"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious", "annoyed"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous", "anxious"]): return "fear"
    if any(word in text for word in ["wow", "shocked", "surprised"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "yuck"]): return "disgust"
    return "neutral"

# Friendly, relaxing reply prompt
def friendly_reply(history, user_text, emotion_label):
    full_convo = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in history])
    prompt = f"""
You're a warm, supportive chatbot friend. You remember the conversation and respond kindly.
The user is currently feeling '{emotion_label}' — respond like a caring buddy.
Your goal is to help them feel heard, emotionally lighter, and less stressed.
Keep your replies short (1–2 lines), friendly, casual, and comforting. Avoid robotic language.

Conversation so far:
{full_convo}
You: {user_text}
Bot:"""

    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.set_page_config(page_title="Emotion-Aware Chatbot 🤗", page_icon="💬")
st.title("Talk to a Friendly Chatbot 💬")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input with unique key to avoid duplicate error
user_input = st.text_input("You 👤:", key="user_input")

# Handle user message
if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0, 0))
    bot_response = friendly_reply(st.session_state.chat_history, user_input, emotion)

    # Save conversation
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion
    })

# Show full conversation history
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**🤖 Bot:** {chat['bot']}")
    st.caption(f"_Emotion: {chat['emotion']} → Valence: {emotion_valence_arousal[chat['emotion']][0]}, Arousal: {emotion_valence_arousal[chat['emotion']][1]}_")
    st.markdown("---")
