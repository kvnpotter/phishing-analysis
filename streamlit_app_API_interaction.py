# Imports

import streamlit as st
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

# Code

st.title("Upload data and launch campaigns")

input_data = st.text_area(label= "The input field for JSON recipients")

if st.button("Upload JSON recipients"):
    json_data = json.loads(input_data)
    response = requests.post(f"{BASE_URL}/recipients/upload-json/", json=json_data)

if st.sidebar.button("Launch campaign"):
    response = requests.get(f"{BASE_URL}/campaign/launch/")