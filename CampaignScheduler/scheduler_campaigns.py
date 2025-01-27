# Imports
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import threading
import requests

from CampaignCreator import PhishingCampaign, load_config
from GoPhishConnector import gp_post_campaign


# Scheduler class to manage periodic tasks
class SchedulerCampaigns:
    def __init__(self):
        """Initialize the scheduler"""
        self.scheduler = BackgroundScheduler()

    def add_job(self, task, args, **kwargs):
        """Add a job to the scheduler with the given task and parameters

        :param task: The function to be executed
        :param args: The arguments to be passed to the function
        :param kwargs: Additional keyword arguments for the job - e.g., interval"""
        self.scheduler.add_job(task, "interval", args, **kwargs)

    def start(self):
        """Start the scheduler"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Scheduler for campaigns started... at {now}")
        self.scheduler.start()

    def stop(self):
        """Stop the scheduler if needed"""
        self.scheduler.shutdown()


# Functions
def create_and_launch_campaign(
    gp_api, topics, prompts, gmail_username, gmail_app_password
):
    """Create and launch a new phishing campaign on GoPhish.

    :param gp_api: The GoPhish API connection object
    :param topics: The file of phishing topics
    :param prompts: The prompts required for GenAI
    :param gmail_username: The Gmail username for sending emails
    :param gmail_app_password: The Gmail app password for sending"""
    # Get the updated recipient database
    config = load_config()
    API_base_url = config["API_base_url"]
    try:
        response = requests.get(f"{API_base_url}/recipients").json()
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 307:
            print("Temporary redirect error (Did you upload data yet?) : ", http_err)
        elif http_err.response.status_code == 404:
            print("Resource not found error (Did you upload data yet?) : ", http_err)
        else:
            print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    recipient_database = response["recipients"]

    print(f"recipient_database: {recipient_database}")
    print(f"gp_api: {gp_api}")
    print(f"gmail_username: {gmail_username}")
    campaign = PhishingCampaign(
        topics=topics,
        prompts=prompts,
        username=gmail_username,
        password=gmail_app_password,
        recipients=recipient_database,
    )

    campaign.setup_campaigns()

    # Post campaign data to GoPhish
    gp_post_campaign(campaign=campaign, gp_api=gp_api)
    print("Campaign launched successfully")


# Run the campaign scheduler in the background using a threading mechanism
def run_campaign_scheduler_in_background(
    gp_api, topics, prompts, gmail_username, gmail_app_password
) -> None:
    """Run the campaign scheduler in a separate thread.

    :param gp_api: The GoPhish API connection object
    :param topics: The file of phishing topics
    :param prompts: The prompts required for GenAI
    :param gmail_username: The Gmail username for sending emails
    :param gmail_app_password: The Gmail app password for sending"""
    scheduler_thread = threading.Thread(
        target=setup_campaign_scheduler,
        args=(gp_api, topics, prompts, gmail_username, gmail_app_password),
    )
    scheduler_thread.daemon = (
        True  # Allow the program to exit even if the thread is running
    )
    scheduler_thread.start()


def setup_campaign_scheduler(
    gp_api, topics, prompts, gmail_username, gmail_app_password
) -> None:
    """
    Setup the campaign scheduler and add a job to send emails periodically.

    :param gp_api: The GoPhish API connection object
    :param topics: The file of phishing topics
    :param prompts: The prompts required for GenAI
    :param gmail_username: The Gmail username for sending emails
    :param gmail_app_password: The Gmail app password for sending
    """
    config = load_config()
    interval_campaign_launch = config["interval_campaign_launch"]
    campaign_scheduler = SchedulerCampaigns()
    campaign_scheduler.start()
    campaign_scheduler.add_job(
        create_and_launch_campaign,
        args=(gp_api, topics, prompts, gmail_username, gmail_app_password),
        seconds=interval_campaign_launch,
    )
