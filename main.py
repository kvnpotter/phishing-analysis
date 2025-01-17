# Imports

from CampaignCreator import create_campaign

# Main function
def main():
    from GoPhishConnector import gp_connect, gp_post_campaign

    # Set up campaign

    campaign = create_campaign()

    # Instantiate GoPhish 

    gp_api = gp_connect()

    # Post campaign data to GoPhish

    gp_post_campaign(campaign=campaign, gp_api=gp_api)

if __name__ == "__main__":
    main()

