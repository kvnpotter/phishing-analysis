# Imports

from .environment_setup import load_env, load_topics, load_prompts
from .PhishingCampaign import PhishingCampaign

# Global variables

topics = {}
prompts = {}
GEMINI_API_KEY = ""
gmail_username = ""
gmail_app_password = ""

# Create campaign

def create_campaign():
    """
    Create a phishing campaign
    """

    # Initialize the environment

    GEMINI_API_KEY, gmail_username, gmail_app_password = load_env()
    topics = load_topics("input_data_prompts_topics/Emailtopics.json")
    prompts = load_prompts("input_data_prompts_topics/prompts.json")

    # Create phishing campaign and load recipient data from CSV file with path specified in config.json

    campaign = PhishingCampaign(topics=topics,
                                prompts=prompts,
                                username=gmail_username,
                                password=gmail_app_password)
    campaign.load_data()

    # Setup the phishing campaigns using the supplied data

    campaign.setup_campaigns()

    return campaign



