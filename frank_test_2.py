import os
import json
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

def fetch_campaign_data(api: Gophish, output_file: str) -> None:
    """
    Fetches campaign data from GoPhish API and saves it to a JSON file.
    """
    try:
        campaigns = api.campaigns.get()  # Get all campaigns
        campaign_data = []  # This will hold our campaign data
        
        # Fetch campaign results and stats
        for campaign in campaigns:
            # Iterate over campaign results and create structured data
            for result in campaign.results:
                campaign_id = campaign.id
                campaign_name = campaign.name
                recipient_email = result.email

            summary = gp_api.campaigns.summary(campaign_id=campaign_id)
            stats = summary.stats
            if stats.sent:
                sent = True
            else:
                sent = False
            if stats.opened:
                opened = True
            else:
                opened = False
            if stats.clicked:
                clicked = True
            else:
                clicked = False
            if stats.submitted_data:
                submitted_data = True
            else:
                submitted_data = False

                data = {
                    "Campaign ID": campaign_id,
                    "Campaign Name": campaign_name,
                    "Email": recipient_email,
                    "Sent": sent,
                    "Opened": opened,
                    "Clicked": clicked,
                    "Submitted": submitted_data
                }
            campaign_data.append(data)
        
        # Save the collected data to a JSON file
        with open(output_file, 'w') as json_file:
            json.dump(campaign_data, json_file, indent=4)
        
        print(f"Campaign data has been saved to {output_file}")
    
    except Exception as e:
        print(f"Error fetching campaigns: {e}")

# Load environment and establish API connection
load_env()
gp_api = gp_connect()

# Define the output file for the campaign data
output_file = 'gophish_campaign_results.json'

# Fetch campaign data and save to a JSON file
fetch_campaign_data(gp_api, output_file)