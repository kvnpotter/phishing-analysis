# Imports

import random
from gemini_utils import generate_mail_body_gemini
from openai_utils import generate_mail_body_openai
from CampaignElements import PhishingMail, UserGroup, SenderProfile, LandingPage, GoPhishCampaign
import os
import json
import pandas as pd
from gophish import Gophish
from gophish.models import *
from datetime import datetime

# Classes

class PhishingCampaign:
    """

    """
    def __init__(self):
        self.config = None
        self.data = None
        self.campaigns = []

    def load_data(self) -> None:
        """
        Load the recipient data from the CSV file.

        """
        config_file = "config.json"  # Contains recipient employee data
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                self.config = json.load(file)
        else:
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
        
        data_path = self.config["employee_data_path"]

        if os.path.exists(data_path):
            self.data = pd.read_csv(data_path, sep=";")
        else:
            raise FileNotFoundError(f"Employee data file '{data_path}' not found.")
        
    def setup_campaigns(self) -> None:
        """
        Setup the phishing campaigns using supplied data.

        """
        for index, recipient in self.data.iterrows():

            campaign = GoPhishCampaign(id=index,
                                       first_name=recipient["First Name"],
                                       last_name=recipient["Last Name"],
                                       recipient_email=recipient["Email"],
                                       department= recipient["Team Unit"])
            self.campaigns.append(campaign)


        
if __name__ == "__main__":

    campaign = PhishingCampaign()
    campaign.load_data()
    print(campaign.data.head())