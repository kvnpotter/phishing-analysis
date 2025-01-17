# Imports

import os
from gophish import Gophish

# Globals

GOPHISH_API_KEY = os.environ.get("GOPHISH_API_KEY")

# Functions

def gp_connect() -> None:
    """
    Creates a connection with GoPhish via API.
    
    RETURNS api: connection object
    """
    global GOPHISH_API_KEY
    
    host = 'https://127.0.0.1:3333/'
    api_key =  GOPHISH_API_KEY # from the settings page
    api = Gophish(api_key, host=host, verify=False)
    return api

def gp_post_campaign(campaign, gp_api) -> None:
    """
    Posts a campaign to GoPhish.
    
    :param campaign: PhishingCampaign object: Wrapper object containing list of individual GoPhish campaigns.
    :param gp_api: gophish.client.Gophish object: Connection object to GoPhish API.
    """
    for gp_campaign in campaign.campaigns:
        gp_api.smtp.post(gp_campaign.smtp)
        print (f"Posted sender {gp_campaign.id} to GP")
        gp_api.pages.post(gp_campaign.landing_page)
        print (f"Posted landing page {gp_campaign.id} to GP")
        gp_api.templates.post(gp_campaign.template)
        print (f"Posted template {gp_campaign.id} to GP")
        gp_api.groups.post(gp_campaign.group)
        print (f"Posted group {gp_campaign.id} to GP")
        gp_api.campaigns.post(gp_campaign.campaign)
        print (f"Posted campaign {gp_campaign.id} to GP")

def gp_delete_campaign(gp_api) -> None:
    """
    Deletes all data from GoPhish.
    """
    smtp = gp_api.smtp.get()
    for sender in smtp:
        gp_api.smtp.delete(sender.id)

    campaigns = gp_api.campaigns.get()
    for camp in campaigns:
        gp_api.campaigns.delete(camp.id)

    groups = gp_api.groups.get()
    for group in groups:
        gp_api.groups.delete(group.id)

    templates = gp_api.templates.get()
    for template in templates:
        gp_api.templates.delete(template.id)

    pages = gp_api.pages.get()
    for page in pages:
        gp_api.pages.delete(page.id)