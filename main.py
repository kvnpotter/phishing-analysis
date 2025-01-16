# Imports

from CampaignCreator import load_env, load_topics, load_prompts
from CampaignCreator import PhishingCampaign

# Global variables

topics = {}
prompts = {}
GEMINI_API_KEY = ""

# Main

if __name__ == "__main__":

    # Initialize the environment

    GEMINI_API_KEY = load_env()
    topics = load_topics("input_data_prompts_topics/Emailtopics.json")
    prompts = load_prompts("input_data_prompts_topics/prompts.json")

    # Create phishing campaign and load recipient data from CSV file with path specified in config.json

    campaign = PhishingCampaign(topics=topics,
                                prompts=prompts)
    campaign.load_data()

    # Setup the phishing campaigns using the supplied data

    campaign.setup_campaigns()

    #print(campaign.campaigns[0].template)

    print(f"""Phishing campaign id = {campaign.campaigns[2].id}\n
          Campaign name = {campaign.campaigns[2].campaign.name}\n
    First Name = {campaign.campaigns[2].first_name}\n
    Last Name = {campaign.campaigns[2].last_name}\n
    Recipient Email = {campaign.campaigns[2].recipient_email}\n
    Department = {campaign.campaigns[2].department}\n
    Mail generated with {campaign.campaigns[2].model}\n
    Mail sender = {campaign.campaigns[2].sender_name} <{campaign.campaigns[2].sender_email}>\n
    Mail subject = {campaign.campaigns[2].mail_subject}\n
    Mail body = {campaign.campaigns[2].template.text}\n
    To user group = {campaign.campaigns[2].group.name}\n
    Using SMTP {campaign.campaigns[2].smtp.name}, {campaign.campaigns[2].smtp.host}, {campaign.campaigns[2].smtp.from_address}\n
    Landing page {campaign.campaigns[2].landing_page.name}, {campaign.campaigns[2].landing_page.redirect_url}\n""")



