import streamlit as st
import google.generativeai as genai
import os

# Set up Gemini
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
    if any(word in text for word in ["happy", "glad", "smile"]): return "joy"
    if any(word in text for word in ["sad", "cry", "alone"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous"]): return "fear"
    if any(word in text for word in ["wow", "shocked", "surprised"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "yuck"]): return "disgust"
    return "neutral"

# More supportive system prompt
def friendly_reply(history, user_text, emotion_label):
    full_convo = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in history])
    prompt = f"""
You're a warm, supportive chatbot friend. You remember the conversation and respond kindly.
The user feels '{emotion_label}' right now. Your job is to help them feel heard and relaxed.
Keep your replies short, casual, and comforting. Help them smile.

Conversation so far:
{full_convo}
You: {user_text}
Bot:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# UI Setup
st.set_page_config(page_title="Emotion-Aware Chatbot 🤗", page_icon="💬")
st.title("Talk to a Friendly Chatbot 💬")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You 👤:")

if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0, 0))

    # Get bot reply
    bot_response = friendly_reply(st.session_state.chat_history, user_input, emotion)

    # Save conversation
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion
    })

# Show full conversation
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**🤖 Bot:** {chat['bot']}")
    st.caption(f"_Emotion: {chat['emotion']} → Valence: {emotion_valence_arousal[chat['emotion']][0]}, Arousal: {emotion_valence_arousal[chat['emotion']][1]}_")
    st.markdown("---")
import streamlit as st
import google.generativeai as genai
import os

# Set up Gemini
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
    if any(word in text for word in ["happy", "glad", "smile"]): return "joy"
    if any(word in text for word in ["sad", "cry", "alone"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous"]): return "fear"
    if any(word in text for word in ["wow", "shocked", "surprised"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "yuck"]): return "disgust"
    return "neutral"

# More supportive system prompt
def friendly_reply(history, user_text, emotion_label):
    full_convo = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in history])
    prompt = f"""
You're a warm, supportive chatbot friend. You remember the conversation and respond kindly.
The user feels '{emotion_label}' right now. Your job is to help them feel heard and relaxed.
Keep your replies short, casual, and comforting. Help them smile.

Conversation so far:
{full_convo}
You: {user_text}
Bot:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# UI Setup
st.set_page_config(page_title="Emotion-Aware Chatbot 🤗", page_icon="💬")
st.title("Talk to a Friendly Chatbot 💬")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You 👤:")

if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0, 0))

    # Get bot reply
    bot_response = friendly_reply(st.session_state.chat_history, user_input, emotion)

    # Save conversation
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion
    })

# Show full conversation
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**🤖 Bot:** {chat['bot']}")
    st.caption(f"_Emotion: {chat['emotion']} → Valence: {emotion_valence_arousal[chat['emotion']][0]}, Arousal: {emotion_valence_arousal[chat['emotion']][1]}_")
    st.markdown("---")
import streamlit as st
import google.generativeai as genai
import os

# Set up Gemini
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
    if any(word in text for word in ["happy", "glad", "smile"]): return "joy"
    if any(word in text for word in ["sad", "cry", "alone"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous"]): return "fear"
    if any(word in text for word in ["wow", "shocked", "surprised"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "yuck"]): return "disgust"
    return "neutral"

# More supportive system prompt
def friendly_reply(history, user_text, emotion_label):
    full_convo = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in history])
    prompt = f"""
You're a warm, supportive chatbot friend. You remember the conversation and respond kindly.
The user feels '{emotion_label}' right now. Your job is to help them feel heard and relaxed.
Keep your replies short, casual, and comforting. Help them smile.

Conversation so far:
{full_convo}
You: {user_text}
Bot:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# UI Setup
st.set_page_config(page_title="Emotion-Aware Chatbot 🤗", page_icon="💬")
st.title("Talk to a Friendly Chatbot 💬")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You 👤:", key="user_input")
if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0, 0))

    # Get bot reply
    bot_response = friendly_reply(st.session_state.chat_history, user_input, emotion)

    # Save conversation
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion
    })

# Show full conversation
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**🤖 Bot:** {chat['bot']}")
    st.caption(f"_Emotion: {chat['emotion']} → Valence: {emotion_valence_arousal[chat['emotion']][0]}, Arousal: {emotion_valence_arousal[chat['emotion']][1]}_")
    st.markdown("---")
import streamlit as st
import google.generativeai as genai
import os

# Set up Gemini
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
    if any(word in text for word in ["happy", "glad", "smile"]): return "joy"
    if any(word in text for word in ["sad", "cry", "alone"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous"]): return "fear"
    if any(word in text for word in ["wow", "shocked", "surprised"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "yuck"]): return "disgust"
    return "neutral"

# More supportive system prompt
def friendly_reply(history, user_text, emotion_label):
    full_convo = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in history])
    prompt = f"""
You're a warm, supportive chatbot friend. You remember the conversation and respond kindly.
The user feels '{emotion_label}' right now. Your job is to help them feel heard and relaxed.
Keep your replies short, casual, and comforting. Help them smile.

Conversation so far:
{full_convo}
You: {user_text}
Bot:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# UI Setup
st.set_page_config(page_title="Emotion-Aware Chatbot 🤗", page_icon="💬")
st.title("Talk to a Friendly Chatbot 💬")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You 👤:")

if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0, 0))

    # Get bot reply
    bot_response = friendly_reply(st.session_state.chat_history, user_input, emotion)

    # Save conversation
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion
    })

# Show full conversation
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**🤖 Bot:** {chat['bot']}")
    st.caption(f"_Emotion: {chat['emotion']} → Valence: {emotion_valence_arousal[chat['emotion']][0]}, Arousal: {emotion_valence_arousal[chat['emotion']][1]}_")
    st.markdown("---")
import streamlit as st
import google.generativeai as genai
import os

# Set up Gemini
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
    if any(word in text for word in ["happy", "glad", "smile"]): return "joy"
    if any(word in text for word in ["sad", "cry", "alone"]): return "sadness"
    if any(word in text for word in ["angry", "mad", "furious"]): return "anger"
    if any(word in text for word in ["scared", "afraid", "nervous"]): return "fear"
    if any(word in text for word in ["wow", "shocked", "surprised"]): return "surprise"
    if any(word in text for word in ["disgusted", "gross", "yuck"]): return "disgust"
    return "neutral"

# More supportive system prompt
def friendly_reply(history, user_text, emotion_label):
    full_convo = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in history])
    prompt = f"""
You're a warm, supportive chatbot friend. You remember the conversation and respond kindly.
The user feels '{emotion_label}' right now. Your job is to help them feel heard and relaxed.
Keep your replies short, casual, and comforting. Help them smile.

Conversation so far:
{full_convo}
You: {user_text}
Bot:"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# UI Setup
st.set_page_config(page_title="Emotion-Aware Chatbot 🤗", page_icon="💬")
st.title("Talk to a Friendly Chatbot 💬")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You 👤:")

if user_input:
    emotion = get_emotion(user_input)
    valence, arousal = emotion_valence_arousal.get(emotion, (0, 0))

    # Get bot reply
    bot_response = friendly_reply(st.session_state.chat_history, user_input, emotion)

    # Save conversation
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion
    })

# Show full conversation
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**🤖 Bot:** {chat['bot']}")
    st.caption(f"_Emotion: {chat['emotion']} → Valence: {emotion_valence_arousal[chat['emotion']][0]}, Arousal: {emotion_valence_arousal[chat['emotion']][1]}_")
    st.markdown("---")
