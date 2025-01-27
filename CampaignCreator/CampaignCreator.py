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


def create_campaign(recipients: list[dict[str, str]]) -> PhishingCampaign:
    """
    Create a phishing campaign

    :param recipients: List of recipient data stored in dictionaries.
    """

    # Initialize the environment

    GOOGLE_API_KEY, gmail_username, gmail_app_password = load_env()
    topics = load_topics("input_data_prompts_topics/Emailtopics.json")
    prompts = load_prompts("input_data_prompts_topics/prompts.json")

    # Create phishing campaign and load recipient data

    campaign = PhishingCampaign(
        topics=topics,
        prompts=prompts,
        username=gmail_username,
        password=gmail_app_password,
        recipients=recipients,
    )

    # Setup the phishing campaigns using the supplied data

    campaign.setup_campaigns()

    return campaign
