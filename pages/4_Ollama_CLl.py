import ollama # type: ignore
import streamlit as st

# Initialize the Ollama client
client = ollama.Client()

# Define the model and the input prompt
model = "llama2"  # Replace with your model name

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title(":seedling: Ollama Client")
st.write("Chat with local models using the Ollama Client (CLI).")
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
your_prompt = st.chat_input("Ask something...")

if your_prompt:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": your_prompt})
    with st.chat_message("user"):
        st.write(your_prompt)

    # Send the query to the model
    response = client.generate(model=model, prompt=your_prompt)
    reply = response.response
    # Append AI response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
