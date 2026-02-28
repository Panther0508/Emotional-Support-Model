import streamlit as st
import os
import json
from chatbot import get_response

st.set_page_config(page_title="Emotional Support AI 💛", layout="centered")
st.title("Emotional Support AI 💛🤖")

# User input with default placeholder
username = st.text_input("Enter your name (for conversation tracking):", "")

if username.strip() == "":
    st.info("Please enter your username to start chatting!")
else:
    os.makedirs("users", exist_ok=True)
    user_file = f"users/{username}.json"
    
    # Load past conversation
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            chat_history = json.load(f)
    else:
        chat_history = []

    personality = st.selectbox("Choose AI personality:", ["empathetic","funny","motivational"])
    user_input = st.text_input("You:")

    if user_input:
        reply, emotion = get_response(user_input, personality)
        st.text(f"AI ({emotion}): {reply}")
        chat_history.append({"user": user_input, "ai": reply, "emotion": emotion})
        with open(user_file, "w") as f:
            json.dump(chat_history, f, indent=4)

    # Display past 10 messages
    if chat_history:
        st.subheader("Previous conversation:")
        for chat in chat_history[-10:]:
            st.write(f"**You:** {chat['user']}")
            st.write(f"**AI ({chat['emotion']}):** {chat['ai']}")