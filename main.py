# Imports

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import urllib3

from GoPhishConnector import gp_connect, gp_post_campaign, gp_delete_campaign
from CampaignCreator import PhishingCampaign, load_env, load_topics, load_prompts

# Disable SSL warnings for development environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global variables and GoPhish API connection

topics = load_topics("input_data_prompts_topics/Emailtopics.json")
prompts = load_prompts("input_data_prompts_topics/prompts.json")
GEMINI_API_KEY, gmail_username, gmail_app_password = load_env()
gp_api = gp_connect()

# Create the FastAPI app
app = FastAPI(title="Phishing Campaign API",
    description="This API allows you to upload recipients, launch phishing campaigns, and delete campaign data from GoPhish.",
    version="1.0.0",
    contact={
        "name": "Kevin Potter",
        "url": "https://github.com/kvnpotter/phishing-analysis",
        "email": "devmail.kvnpotter@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Define User and UserList data models

class User(BaseModel):
    first_name: str =Field(description="The first name of the recipient.")
    last_name: str =Field(description="The last name of the recipient.")
    email: str =Field(description="The email address of the recipient.")
    department: str =Field(description="The department of the recipient.")

class UserList(BaseModel):
    recipients: List[User] =Field(description="A list of User dictionaries.")
    
# In-memory "database" to store user data (for simplicity)
recipient_database: list[dict[str:str]] = []

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the testing API!"}

@app.post("/recipients/upload-json/")
def upload_recipients(user_list: UserList):
    """ 
    Clear the previous recipients and upload a new list of recipients to the recipient database in JSON format. Stores in a list of dictionaries.
    [{"first_name": "John", "last_name": "Doe", "email": "johndoe@example.com", "department": "IT"}]
    """
    global recipient_database
    recipient_database = []
    for recipient in user_list.recipients:
        recipient_database.append({"first_name": recipient.first_name,
                                   "last_name": recipient.last_name,
                                   "email": recipient.email,
                                   "department": recipient.department})

    return {"message": "Recipients uploaded successfully!",
            "database": recipient_database}

@app.post("/recipients/upload-recipient/")
def upload_recipient(user_list: UserList):
    """
    Add a single recipient to the recipient database (list of dicts).
    [{"first_name": "John", "last_name": "Doe", "email": "johndoe@example.com", "department": "IT"}]
    """
    global recipient_database
    for recipient in user_list.recipients:
        recipient_database.append({"first_name": recipient.first_name,
                                   "last_name": recipient.last_name,
                                   "email": recipient.email,
                                   "department": recipient.department})

    return {"message": "Recipient added successfully!",
            "database": recipient_database}

@app.delete("/recipients/delete-all/")
def delete_all_recipients():
    """
    Delete all recipients from the recipient database.
    """
    global recipient_database
    recipient_database = []
    return {"message": "All recipients deleted successfully!"}

# GET endpoint to retrieve all recipients
@app.get("/recipients/")
def get_recipients():
    """ Get all recipients from the recipient database. """
    if not recipient_database:
        raise HTTPException(status_code=404, detail="No recipients found.")
    return {"recipients": recipient_database}

# Get endpoint to launch a campaign
@app.get("/campaign/launch/")
def launch_campaign():
    """ Launch a phishing campaign using the recipient database. Creates and sets up the campaign, then posts the data to GoPhish. """

    global GEMINI_API_KEY, gmail_username, gmail_app_password, topics, prompts, recipient_database, gp_api

    # create and setup phishing campaign

    campaign = PhishingCampaign(topics=topics,
                            prompts=prompts,
                            username=gmail_username,
                            password=gmail_app_password,
                            recipients=recipient_database)
    
    campaign.setup_campaigns()

    # Post campaign data to GoPhish
    gp_post_campaign(campaign=campaign, gp_api=gp_api)

    return {"message": "Campaign launched successfully!"}

@app.delete("/campaign/delete-all/")
def delete_gp_data():
    """ Delete all campaign data from GoPhish. """

    gp_delete_campaign(gp_api)
    return {"message": "All campaign data deleted successfully!"}
