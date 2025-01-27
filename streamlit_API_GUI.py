# Imports

import streamlit as st
import requests
import json

from CampaignCreator import load_config

# Set base URL for requests to API

config = load_config()
BASE_URL = config["API_base_url"]  # from the .env

# App Code

st.title("Upload data and launch campaigns")

# Multiline text input for JSON data
input_data = st.text_area(label="The input field for JSON recipients")

#  Buttons to upload JSON data and add one user
if st.button("Upload JSON recipients"):
    json_data = json.loads(input_data)
    response = requests.post(f"{BASE_URL}/recipients/upload-json/", json=json_data)

if st.button("Add one user"):
    json_data = json.loads(input_data)
    response = requests.post(f"{BASE_URL}/recipients/upload-recipient/", json=json_data)

# Sidebar buttons to launch campaign and delete all data - link to result analysis page
if st.sidebar.button("Launch campaign"):
    response = requests.get(f"{BASE_URL}/campaign/launch/")

if st.sidebar.button("Delete all GP campaign data"):
    response = requests.delete(f"{BASE_URL}/campaign/delete-all/")

st.sidebar.link_button("Result analysis page", url=config["analysis_url"])
