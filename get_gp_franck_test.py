import os
from dotenv import load_dotenv
from gophish import Gophish
import urllib3

# Disable SSL warnings for development environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_env() -> None:
    """
    Load the API keys from the .env file.
    """
    env_file = ".env"
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        raise FileNotFoundError(f"Environment file '{env_file}' not found.")

def gp_connect() -> Gophish:
    """
    Creates a connection with GoPhish via API.

    RETURNS api: connection object
    """
    host = 'https://127.0.0.1:3333/'  # GoPhish API server
    api_key = os.environ.get("GOPHISH_API_KEY")  # API key from the .env file
    if not api_key:
        raise ValueError("API Key is missing in the environment variables.")
    try:
        api = Gophish(api_key, host=host, verify=False)
        return api
    except Exception as e:
        raise ConnectionError(f"Failed to connect to GoPhish API: {e}")
def fetch_campaign_data(api: Gophish):
    """
    Fetches and prints all campaign data from the GoPhish API.
    """
    try:
        campaigns = api.campaigns.get()
        for campaign in campaigns:
            print(f"Campaign Name: {campaign.name}")
            print(f"Campaign ID: {campaign.id}")
            print(f"Status: {campaign.status}")
            print(f"Launch Date: {campaign.launch_date}")
            print(f"Finish Date: {campaign.completed_date}") #finish_date doesn't exist
            print(f"Template ID: {campaign.template.id}") # Access template object and get relevant information from there
            #print(f"List ID: {campaign.list_id}") # What is list_id ?
            #print(f"Sent Emails: {campaign.sent}") # In results

    except Exception as e:
        print(f"Error fetching campaigns: {e}")

# Access campaign statistics

    try:
        summaries = api.campaigns.summary()
        for summary in summaries.campaigns:
            result = summary.stats
            print(f"Opened: {result.opened}")
            print(f"Clicked: {result.clicked}")
            print(f"Submitted data: {result.submitted_data}")

    except Exception as e:
        print(f"Error fetching campaigns: {e}")

# Load environment and establish API connection
load_env()
gp_api = gp_connect()

#Fetch and display campaign data
fetch_campaign_data(gp_api)