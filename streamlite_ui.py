import streamlit as st
import os
import ollama_testing

st.set_page_config('Appollo ChatBot')
st.header("Sona - Appollo ChatBot")
image_path = r"C:\Users\augus\PycharmProjects\image_captioning\RAG DEMO\static\appollo_name.jpg"

st.image(image_path, width=300)

container = st.container(height=500, border=True, key=None)

with st.form(key="user_form"):
    user_input = st.text_input(label="", placeholder="Message to Sona...", key='user_input')
    retrieved_data = st.text_input(label="", placeholder="Paste data here...", key='data')

    submit_button = st.form_submit_button(label="Get Response")

    if submit_button:
        result = ollama_testing.generate_response(user_input, retrieved_data)
        container.write(result)
        print(result)

