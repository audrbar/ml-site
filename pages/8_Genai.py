# Create a simple Streamlit chatbot which uses Python Google google.genai library.

import streamlit as st
import google.generativeai as genai
import os

# Set your API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# Session state to hold chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.title("💬 Gemini Chatbot")

# Chat display
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "text": prompt})

    # Get response from Gemini
    try:
        response = model.generate_content(prompt)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    # Display response
    st.chat_message("assistant").markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "text": reply})
