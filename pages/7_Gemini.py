import streamlit as st
from PIL import Image
from google import genai

# Load Gemini model
client = genai.Client(api_key=st.secrets["google_api_key"])

# Session state to hold chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.title("💬 Gemini IMG")
st.divider()

uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

# Chat display
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# User input
if prompt := st.chat_input("Ask describe the person's appearance in Lithuanian..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "text": prompt})

    # Get response from Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                prompt,
                Image.open(uploaded_file) # type: ignore
            ]
        )
        response = response.text
    except Exception as e:
        response = f"Error: {str(e)}"

    # Display response
    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "text": response})
