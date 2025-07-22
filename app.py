import streamlit as st
import google.generativeai as genai
import os

# Load the API key from Streamlit Secrets
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "neutral": (0.0, 0.0)
}

def get_emotion(text):
    text = text.lower()
    if "happy" in text: return "joy"
    if "sad" in text: return "sadness"
    if "angry" in text: return "anger"
    if "scared" in text: return "fear"
    return "neutral"

def friendly_reply(user_text, emotion_label):
    prompt = f"""
You are a friendly chatbot. The user is feeling '{emotion_label}' right now.
Respond like a buddy in just 1-2 lines. Be warm and casual.
Avoid long paragraphs. Just a kind and short sentence.
User said: "{user_text}"
You reply:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.set_page_config(page_title="Friendly Chatbot 😊", page_icon="💬")
st.title("Emotion-Aware Friendly Chatbot 🤗")

user_input = st.text_input("You 👤:")

if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0, 0))

    st.write(f"🧠 Emotion: `{emotion}` (Valence: {valence}, Arousal: {arousal})")

    bot_response = friendly_reply(user_input, emotion)
    st.success(f"🤖 {bot_response}")
