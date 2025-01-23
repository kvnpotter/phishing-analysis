# Imports

import json
from CampaignCreator import create_campaign

import urllib3

# Disable SSL warnings for development environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Main function
def main():
    from GoPhishConnector import gp_connect, gp_post_campaign

    # Read recipient data from JSON file

    with open("input_data_prompts_topics/Employee_one.json", "r") as file:
        recipients_dict = json.load(file)
    recipients_list = recipients_dict["recipients"]

    # Set up campaign

    campaign = create_campaign(recipients=recipients_list)

    # Instantiate GoPhish 

    gp_api = gp_connect()

    # Post campaign data to GoPhish

    gp_post_campaign(campaign=campaign, gp_api=gp_api)

if __name__ == "__main__":
    main()

