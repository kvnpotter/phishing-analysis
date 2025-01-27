# Imports

from .CampaignElements import GoPhishCampaign

# Classes


class PhishingCampaign:
    """ """

    def __init__(
        self,
        topics: dict[str : list[dict[str:str]]],
        prompts: dict[str:str],
        username: str,
        password: str,
        recipients: list[dict[str, str]],
    ) -> None:
        """
        Create complete campaign, containing instances of all required classes.

        :param topics: dict[str:list[dict[str:str]]]: The topics for the departments.
        :param prompts: dict[str:str]: The prompts for the phishing mail generation.
        :param username: str: The username for the sender email.
        :param password: str: The password for the sender email
        :param recipients: list[dict[str, str]]: The recipient data.
        """
        self.topics = topics
        self.prompts = prompts
        self.username = username
        self.password = password
        self.recipients = recipients
        self.campaigns = []

    def setup_campaigns(self) -> None:
        """
        Setup the phishing campaigns using supplied data.

        """
        index = 0  # PLACEHOLDER
        for recipient in self.recipients:

            campaign = GoPhishCampaign(
                id=index,
                first_name=recipient["first_name"],
                last_name=recipient["last_name"],
                recipient_email=recipient["email"],
                department=recipient["department"],
                topics=self.topics,
                prompts=self.prompts,
                username=self.username,
                password=self.password,
            )
            campaign.setup_campaign()
            campaign.generate_gp_campaign()
            self.campaigns.append(campaign)
            index += 1  # PLACEHOLDER


if __name__ == "__main__":

    campaign = PhishingCampaign()
    campaign.load_data()
    print(campaign.data.head())
