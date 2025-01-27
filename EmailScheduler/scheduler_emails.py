# Imports

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import threading
import logging
from fastapi import BackgroundTasks

from .feedback import send_emails_periodically
from CampaignCreator import load_config

# Setting up logging for the background task
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create a scheduler class to handle email tasks
class EmailScheduler:
    def __init__(self):
        """
        Initialize the scheduler"""
        self.scheduler = BackgroundScheduler()

    def add_email_job(self, task, **kwargs):
        """Add a job to the scheduler to send emails periodically

        :param task: The function to run
        :param kwargs: Additional keyword arguments for the job - e.g., interval
        """
        self.scheduler.add_job(task, "interval", **kwargs)

    def start(self):
        """Start the scheduler"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Email scheduler started at {now}")
        self.scheduler.start()
        print(f"Email scheduler started at {now}")

    def stop(self):
        """Stop the scheduler if needed"""
        self.scheduler.shutdown()


# Create an instance of the EmailScheduler class
email_scheduler = EmailScheduler()


def setup_email_scheduler() -> None:
    """
    Setup the email scheduler and add a job to send emails periodically.
    """
    config = load_config()
    interval_phishing_feedback = config["interval_phishing_feedback"]
    email_scheduler = EmailScheduler()
    email_scheduler.start()
    email_scheduler.add_email_job(
        send_emails_periodically, seconds=interval_phishing_feedback
    )


# Run the email scheduler in the background using a threading mechanism
def run_email_scheduler_in_background() -> None:
    """Run the email scheduler in a separate thread."""
    scheduler_thread = threading.Thread(target=setup_email_scheduler)
    scheduler_thread.daemon = (
        True  # Allow the program to exit even if the thread is running
    )
    scheduler_thread.start()
