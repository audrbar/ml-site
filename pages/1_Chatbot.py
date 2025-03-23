import streamlit as st
from openai import OpenAI # type: ignore

# Ensure API key is set correctly
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def header():
    with st.container():
        st.title(":clown_face: OpenAI Chatbot")
        st.subheader("Just ask what you care about.")

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

def user_input():
    # User input
    user_input = st.chat_input("Ask something...")
    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Get AI response
        response = client.chat.completions.create(  # Correct API call
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content  # Correct response parsing

        # Append AI response
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

if __name__ == "__main__":
    header()
    user_input()
