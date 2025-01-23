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

if st.button("Add one user"):
    json_data = json.loads(input_data)
    response = requests.post(f"{BASE_URL}/recipients/upload-recipient/", json=json_data)

if st.sidebar.button("Launch campaign"):
    response = requests.get(f"{BASE_URL}/campaign/launch/")

if st.sidebar.button("Delete all GP campaign data"):
    response = requests.delete(f"{BASE_URL}/campaign/delete-all/")

st.sidebar.link_button("Result analysis page", url="https://gophish-analysis.streamlit.app/")