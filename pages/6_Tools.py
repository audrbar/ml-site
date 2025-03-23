import os
import streamlit as st
import json
from rich import print
from openai import OpenAI
from Home import footer_section
import requests

# Read from file
def read_from_file(file_path):
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' not found."
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"

# Write to file
def write_to_file(file_path, content):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return f"Successfully wrote to '{file_path}'."
    except Exception as e:
        return f"Error writing to file: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_from_file",
            "description": "Reads from file and answers questions about city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Writes contents to a specified file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["file_path", "content"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

client = OpenAI(api_key=st.secrets["openai_api_key"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.container():
    st.subheader(":seedling: Multiple Tools calling")
    st.write("Enable models to choose between few tools and take other actions.")
    st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# User input
user_input = st.chat_input("Enter your request (e.g., 'Tell me about your city')")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    messages = [{"role": "user", "content": f"Read from file and {user_input}"}]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages, # type: ignore
        tools=tools, # type: ignore
        tool_choice="auto"
    )

    with st.expander("Click to read Completion 1"):
        st.write(completion.choices[0].message)

    tool_call = completion.choices[0].message.tool_calls[0] # type: ignore

    with st.expander("Click to read Tool Call"):
        st.write(tool_call)

    args = json.loads(tool_call.function.arguments)

    with st.expander("Click to read Args"):
        st.write(args)

    city_story = read_from_file("data/city.txt")
    with st.chat_message("assistant"):
        st.write(city_story)

    messages.append(completion.choices[0].message)  # type: ignore
    messages.append({                               # append result message
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(city_story)
    })

    completion_2 = client.chat.completions.create(
        model="gpt-4o",
        messages=messages, # type: ignore
        tools=tools, # type: ignore
    )
    write_to_file("data/city_short.txt", completion_2.choices[0].message.content)

    with st.expander("Click to read Completion 2"):
        st.write(completion_2.choices[0].message.content)
