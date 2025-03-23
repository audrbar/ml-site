import streamlit as st
from google import genai
from google.genai import types

# Load Gemini model
client = genai.Client(api_key=st.secrets["google_api_key"])

# Session state to hold chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.title("💬 Gemini Chatbot")
st.divider()

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
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction='you are a story teller for kids under 5 years old',
                max_output_tokens= 400,
                top_k= 2,
                top_p= 0.5,
                temperature= 0.5,
                response_mime_type= 'application/json',
                stop_sequences= ['\n'],
                seed=42,
            ),

        )
        response = response.text
    except Exception as e:
        response = f"Error: {str(e)}"

    # Display response
    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "text": response})
