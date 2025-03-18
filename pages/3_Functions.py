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

with st.container():
    st.title(":seedling: Function calling")
    st.subheader("Enable models to fetch data and take other actions.")
    st.write("Function calling provides a powerful and flexible way for OpenAI models to interface with\
        your code or external services.")
    st.link_button("More information...", "https://platform.openai.com/docs/guides/function-calling?api-mode=chat&example=get-weather")
    st.divider()

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

messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]

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

footer_section()
