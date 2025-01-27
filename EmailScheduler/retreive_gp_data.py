# Imports

import os
import json
from dotenv import load_dotenv
from gophish import Gophish
import urllib3

from GoPhishConnector import gp_connect

# Disable SSL warnings for development environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_campaign_data(api: Gophish, output_file: str) -> None:
    """
    Fetches campaign data from GoPhish API and saves it to a JSON file.

    :param api: The GoPhish API connection object
    :param output_file: The output file path to save the campaign data
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
                first_name = result.first_name
                last_name = result.last_name

            summary = api.campaigns.summary(campaign_id=campaign_id)
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

            data_campaign = {
                "Campaign ID": campaign_id,
                "Campaign Name": campaign_name,
                "Email": recipient_email,
                "Sent": sent,
                "Opened": opened,
                "Clicked": clicked,
                "Submitted": submitted_data,
                "first_name": first_name,
                "last_name": last_name,
            }

            campaign_data.append(data_campaign)

        # Save the collected data to a JSON file
        with open(output_file, "w") as json_file:
            json.dump(campaign_data, json_file, indent=4)

        print(f"Campaign data has been saved to {output_file}")

    except Exception as e:
        print(f"Error fetching campaigns: {e}")


def retreive_data():
    """Retrieve campaign data from GoPhish and save to a JSON file."""
    # Establish API connection

    gp_api = gp_connect()

    # Define the output file for the campaign data
    output_file = "gophish_campaign_results.json"

    # Fetch campaign data and save to a JSON file
    fetch_campaign_data(gp_api, output_file)
