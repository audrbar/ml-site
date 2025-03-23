import streamlit as st
import ollama # type: ignore
import requests
import json

# Ollama API endpoint
url = "http://localhost:11434/api/chat"  # Replace with your Ollama endpoint if needed

# Initialize session state chat history
if "messages_api" not in st.session_state:
    st.session_state.messages_api = []

if "messages_cli" not in st.session_state:
    st.session_state.messages_cli = []

# 🌱 Header
def header():
    with st.container():
        st.title(":seedling: Ollama Chat")
        st.write("Chat with local models using the Ollama API or Python Client.")
        st.divider()

# Ollama API Chat
def ollama_api():

    for message in st.session_state.messages_api:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    api_user_prompt = st.chat_input("Send a message to Ollama API...", key="chat_input_api")

    if api_user_prompt:
        st.session_state.messages_api.append({"role": "user", "content": api_user_prompt})
        with st.chat_message("user"):
            st.write(api_user_prompt)

        payload = {
            "model": "llama2",
            "messages": [{"role": "user", "content": api_user_prompt}]
        }

        response = requests.post(url, json=payload, stream=True)

        if response.status_code == 200:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response_text = ""

                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            json_data = json.loads(line)
                            if "message" in json_data and "content" in json_data["message"]:
                                chunk = json_data["message"]["content"]
                                response_text += chunk
                                response_placeholder.markdown(response_text)
                        except json.JSONDecodeError:
                            st.warning(f"Failed to parse line: {line}")

            st.session_state.messages_api.append({"role": "assistant", "content": response_text})
        else:
            st.error(f"Request failed: {response.status_code}")

# Ollama Python Client Chat
def ollama_cli():
    client = ollama.Client()

    # Display chat history first (top-down)
    for message in st.session_state.messages_cli:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Show chat input LAST to keep it at the bottom
    cli_user_input = st.chat_input("Send a message to Ollama Client...", key="chat_input_cli")

    if cli_user_input:
        # Store and show user's message
        st.session_state.messages_cli.append({"role": "user", "content": cli_user_input})
        with st.chat_message("user"):
            st.write(cli_user_input)

        # Send to Ollama Client
        response = client.generate(model="gemma3", prompt=cli_user_input)

        # Show assistant response
        with st.chat_message("assistant"):
            st.write(response.response)

        # Save response
        st.session_state.messages_cli.append({"role": "assistant", "content": response.response})

# Main App
if __name__ == '__main__':
    header()

    tab1, tab2 = st.tabs(["Ollama API", "Ollama Client"])
    with tab1:
        ollama_api()
    with tab2:
        ollama_cli()
