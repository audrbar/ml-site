# Please write a script where 'gemini-2.0-flash' model describe your( upload your foto) appearance in Lithuanian.
import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["google_api_key"])

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)
