import os
import streamlit as st
import json
from rich import print
from openai import OpenAI
from Home import footer_section
import requests

def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

def write_to_file(content: str, filename: str = "data/chat_history.txt"):
        with open(filename, 'w') as file:
            file.write(content)
        return os.path.abspath(filename)

client = OpenAI(api_key=st.secrets["openai_api_key"])

messages = []

# Convert message objects to serializable dictionaries
def serialize_message(message):
    if isinstance(message, dict):
        # Already a dictionary, return as is
        return message
    elif hasattr(message, 'to_dict'):
        # If the message has a to_dict method, use it
        return message.to_dict()
    elif hasattr(message, '__dict__'):
        # Convert object attributes to a dictionary
        return {key: serialize_message(value) for key, value in message.__dict__.items()}
    else:
        raise TypeError(f"Object of type {type(message).__name__} is not JSON serializable")

st.title(":seedling: Function calling")
st.subheader("Enable models to fetch data and take other actions.")
st.write("Function calling provides a powerful and flexible way for OpenAI models to interface with\
    your code or external services.")
st.link_button("More information...", "https://platform.openai.com/docs/guides/function-calling?api-mode=chat&example=get-weather")
st.divider()

your_city = st.chat_input("Choose your city and get a wether data:")

if your_city:
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False
            },
            "strict": True
        }
    }, {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Write content to a file and return the absolute path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"],
                "additionalProperties": False
            },
            "strict": True
        }
    }]

    messages = [{"role": "user", "content": f"What's the weather like in {your_city} today?"}]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages, # type: ignore
        tools=tools, # type: ignore
    )
    st.write("Completion:")
    st.write(completion.choices[0].message.tool_calls)

    tool_call = completion.choices[0].message.tool_calls[0] # type: ignore
    st.write("Tool Call:")
    st.write(tool_call)
    args = json.loads(tool_call.function.arguments)
    st.write("Args:")
    st.write(args)

    result = get_weather(args["latitude"], args["longitude"])
    st.write(f"Result: {result}")

    messages.append(completion.choices[0].message)  # type: ignore
    messages.append({                               # append result message
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    })

    completion_2 = client.chat.completions.create(
        model="gpt-4o",
        messages=messages, # type: ignore
        tools=tools, # type: ignore
    )

    st.write(f"Completion 2: {completion_2.choices[0].message.content}")

    # Add the model's response to the messages
    messages.append(completion_2.choices[0].message) # type: ignore

    # ------------------------------------------------------------

    # Ask to write the conversation to a file
    messages.append({
        "role": "user",
        "content": "Please write this conversation to a file."
    })

    completion_3 = client.chat.completions.create(
        model="gpt-4o",
        messages=messages, # type: ignore
        tools=tools, # type: ignore
    )

    st.write(completion_3.choices[0].message)

    # Execute the tool call if it's requesting to write to a file
    if completion_3.choices[0].message.tool_calls:
        tool_call = completion_3.choices[0].message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)

        if tool_call.function.name == "write_to_file":
            file_path = write_to_file(args["content"])
            print(f"Conversation written to: {file_path}")

footer_section()
