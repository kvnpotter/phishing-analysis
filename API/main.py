# Imports

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from CampaignCreator import create_campaign
from GoPhishConnector import gp_connect, gp_post_campaign

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
    for recipient in user_list.recipients:
        recipient_database.append({"first_name": recipient.first_name,
                                   "last_name": recipient.last_name,
                                   "email": recipient.email,
                                   "department": recipient.department})

    return {"message": "Recipients uploaded successfully!",
            "database": recipient_database}

# GET endpoint to retrieve all recipients
@app.get("/recipients/")
def get_recipients():
    if not recipient_database:
        raise HTTPException(status_code=404, detail="No recipients found.")
    return {"recipients": recipient_database}

# Get endpoint to launch a campaign
@app.get("/campaign/launch/")
def launch_campaign():
    campaign = create_campaign()
    gp_api = gp_connect()
    gp_post_campaign(campaign=campaign, gp_api=gp_api)

    return {"message": "Campaign launched successfully!",
            "campaign": campaign}
