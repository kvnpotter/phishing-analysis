# Imports

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
import urllib3
import logging
from contextlib import asynccontextmanager

from GoPhishConnector import gp_connect, gp_post_campaign, gp_delete_campaign
from CampaignCreator import PhishingCampaign, load_env, load_topics, load_prompts, load_config
from EmailScheduler import run_email_scheduler_in_background
from CampaignScheduler import run_campaign_scheduler_in_background

# Disable SSL warnings for development environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define User and UserList data models
class User(BaseModel):
    first_name: str 
    last_name: str 
    email: str 
    department: str 

class UserList(BaseModel):
    recipients: List[User] 

# In-memory "database" to store user data (for simplicity)
recipient_database: list[dict[str:str]] = []

# Load the environment variables and create the GoPhish API connection
config = load_config()
topics = load_topics(config["topics_path"])
prompts = load_prompts(config["prompts_path"])
GEMINI_API_KEY, gmail_username, gmail_app_password = load_env()
gp_api = gp_connect()

# Define the lifespan function to handle startup and shutdown events

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Set up logging to track background task errors
    logging.basicConfig(level=logging.INFO)

    # Setup and start the email scheduler in the background
    try:
        run_email_scheduler_in_background()
        logging.info("Email scheduler started successfully in the background.")
    except Exception as e:
        logging.error(f"Failed to start email scheduler: {e}")

    # Setup and start the campaign scheduler in the background
    try:
        run_campaign_scheduler_in_background(gp_api=gp_api,
                                             topics=topics,
                                             prompts=prompts,
                                             gmail_username=gmail_username,
                                             gmail_app_password=gmail_app_password)
        logging.info("Campaign scheduler started successfully in the background.")
    except Exception as e:
        logging.error(f"Failed to start campaign scheduler: {e}")

    # Yield the application
    yield

    # Shutdown logic
    logging.info("FastAPI app is shutting down...")

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
    lifespan=lifespan
)

# @app.on_event("startup")
# async def startup_event():
#     """Start the email scheduler in the background when the FastAPI app starts"""


# @app.on_event("shutdown")
# async def shutdown_event():
#     """Handle graceful shutdown of FastAPI app"""
    

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
