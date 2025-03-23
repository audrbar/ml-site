import ollama # type: ignore
import streamlit as st

# Initialize the Ollama client
client = ollama.Client()

# Define the model and the input prompt
model = "llama2"  # Replace with your model name

with st.container():
    st.title(":seedling: Ollama Client")
    st.subheader("Enable Ollama models locally using Ollama Client.")
    st.divider()

with st.container():
    your_prompt = st.text_input("Write your prompt")
    st.write("Your promt is: ", your_prompt)

if your_prompt:
    # Send the query to the model
    response = client.generate(model=model, prompt=your_prompt)
    # Print the response from the model
    print("Response from Ollama:")
    print(response.response)
    st.write(response.response)
