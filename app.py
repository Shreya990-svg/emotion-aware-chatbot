import streamlit as st
import google.generativeai as genai

# --- Configure Gemini API Key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Emotion Valence-Arousal Mapping ---
emotion_valence_arousal = {
    "joy": (0.9, 0.7),
    "anger": (-0.8, 0.8),
    "sadness": (-0.9, -0.5),
    "fear": (-0.7, 0.6),
    "surprise": (0.2, 0.9),
    "disgust": (-0.6, 0.3),
    "neutral": (0.0, 0.0)
}

# --- Basic Emotion Detection ---
def get_emotion(text):
    text = text.lower()
    if any(word in text for word in ["happy", "glad", "joy", "smile", "excited"]): return "joy"
    if any(word in text for word in ["sad", "cry", "upset", "down", "unhappy"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious", "annoyed"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous", "anxious"]): return "fear"
    if any(word in text for word in ["surprised", "wow", "unexpected"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "nasty"]): return "disgust"
    return "neutral"

# --- Generate Friendly Response ---
def generate_reply(history, user_text, emotion):
    context = "\n".join([f"You: {h['user']}\nFriend: {h['reply']}" for h in history])
    
    prompt = f"""
You are SoulTalk, a deeply empathetic, emotionally intelligent AI friend.
Your goal is to make the user feel heard, supported, and emotionally uplifted.
You always reply in a calming, kind, and friendly tone, using emotionally soothing language.

The user currently feels: {emotion}
(Use this to guide how gentle, cheerful, or supportive you should be.)

Here's your chat history:
{context}

Now the user says:

You: {user_text}
Friend:"""

    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Streamlit UI Setup ---
st.set_page_config(page_title="SoulTalk - Emotion-Aware Chatbot", page_icon="💬")
st.title("🧠 SoulTalk: Your Emotion-Aware Friend 🤗")

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display Chat History (Styled like ChatGPT) ---
st.markdown("## 💬 Conversation")
for msg in st.session_state.chat_history:
    with st.container():
        st.markdown(
            f"<div style='background-color:#f0f2f6; padding:10px; border-radius:10px;'><b>👤 You:</b> {msg['user']}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='background-color:#d0f0c0; padding:10px; border-radius:10px; margin-top:5px;'><b>🧠 SoulTalk:</b> {msg['reply']}</div>",
            unsafe_allow_html=True
        )
        st.markdown("<hr>", unsafe_allow_html=True)

# --- User Input Field ---
user_input = st.text_input("Type your message here 👇", key="user_input_field")

# --- Handle User Input ---
if user_input:
    # 1. Emotion Detection
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0.0, 0.0))

    # 2. Generate Reply
    reply = generate_reply(st.session_state.chat_history, user_input, emotion)

    # 3. Update History
    st.session_state.chat_history.append({
        "user": user_input,
        "reply": reply,
        "emotion": emotion,
        "valence": valence,
        "arousal": arousal
    })

    # 4. Clear input after submission
    st.experimental_rerun()
