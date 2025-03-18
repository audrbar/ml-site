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

def write_chat_to_file(filename, messages):
    with open(filename, 'w') as f:
        json.dump(messages, f, indent=4)

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

with st.container():
    st.title(":seedling: Function calling")
    st.subheader("Enable models to fetch data and take other actions.")
    st.write("Function calling provides a powerful and flexible way for OpenAI models to interface with\
        your code or external services.")
    st.link_button("More information...", "https://platform.openai.com/docs/guides/function-calling?api-mode=chat&example=get-weather")
    st.divider()

with st.container():
    your_city = st.text_input("Choose your city and get a wether data:")
    st.write("Your city is", your_city)

if your_city:
    client = OpenAI(api_key=st.secrets["openai_api_key"])
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
    }]

    messages = [{"role": "user", "content": "What's the weather like in {your_city} today?"}]

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

    # Serialize messages before writing to file
    serializable_messages = [serialize_message(msg) for msg in messages]

    # Example usage
    write_chat_to_file("data/chat_history.json", serializable_messages)

footer_section()
