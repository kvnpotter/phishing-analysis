# Imports

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

#from CampaignCreator import create_campaign
from GoPhishConnector import gp_connect, gp_post_campaign
from CampaignCreator import PhishingCampaign, load_env, load_topics, load_prompts

# Global variables

topics = {}
prompts = {}
GEMINI_API_KEY = ""
gmail_username = ""
gmail_app_password = ""

# Create the FastAPI app
app = FastAPI()

# Define User and UserList data models

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str

class UserList(BaseModel):
    recipients: List[User]
    
# In-memory "database" to store user data (for simplicity)
recipient_database = []

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the testing API!"}

@app.post("/recipients/upload-json/")
def upload_recipients(user_list: UserList):
    global recipient_database
    recipient_database = []
    for recipient in user_list.recipients:
        recipient_database.append({"first_name": recipient.first_name,
                                   "last_name": recipient.last_name,
                                   "email": recipient.email,
                                   "department": recipient.department})

    return {"message": "Recipients uploaded successfully!",
            "database": recipient_database}

@app.delete("/recipients/delete-all/")
def delete_all_recipients():
    global recipient_database
    recipient_database = []
    return {"message": "All recipients deleted successfully!"}

# GET endpoint to retrieve all recipients
@app.get("/recipients/")
def get_recipients():
    if not recipient_database:
        raise HTTPException(status_code=404, detail="No recipients found.")
    return {"recipients": recipient_database}

# Get endpoint to launch a campaign
@app.get("/campaign/launch/")
def launch_campaign():

    # Initialize the environment

    global GEMINI_API_KEY, gmail_username, gmail_app_password, topics, prompts, recipient_database

    GEMINI_API_KEY, gmail_username, gmail_app_password = load_env()
    topics = load_topics("input_data_prompts_topics/Emailtopics.json")
    prompts = load_prompts("input_data_prompts_topics/prompts.json")

    # create and setup phishing campaign

    campaign = PhishingCampaign(topics=topics,
                            prompts=prompts,
                            username=gmail_username,
                            password=gmail_app_password,
                            recipients=recipient_database)
    
    campaign.setup_campaigns()

    # Connect to GoPhish and post campaign data
    gp_api = gp_connect()
    gp_post_campaign(campaign=campaign, gp_api=gp_api)

    # Empty user database

    recipient_database = []

    return {"message": "Campaign launched successfully!"}
