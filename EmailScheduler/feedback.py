import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json
from collections import defaultdict
import logging

from .retreive_gp_data import retreive_data

# Load environment variables from .env file
load_dotenv()

# Set up logging for better error tracking
logging.basicConfig(
    filename="email_sending.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Feedback:
    def __init__(self):
        """
        Initialize the Feedback class to send emails to users who clicked on phishing links.
        """
        # Use environment variables for email configuration
        self.email_config = {
            "smtp_server": os.getenv("smtp_reporting_mail"),
            "smtp_port": int(os.getenv("smtp_reporting_port", 587)),
            "sender_email": os.getenv("reporting_mail_username"),
            "password": os.getenv("reporting_mail_password"),
            "subject": os.getenv("SUBJECT", "Phishing Simulation Campaign Results"),
        }

        # Check if all required environment variables are set
        if not all(self.email_config.values()):
            raise ValueError(
                "One or more email configuration values are missing in the environment variables."
            )

    def send_email(
        self,
        sender_email,
        user_email,
        first_name,
        last_name,
        pdf_path="input_data_prompts_topics/training_phishing.pdf",
    ):
        """Send an email to the user who clicked on the phishing link.

        :param sender_email: The sender's email address
        :param user_email: The recipient's email address
        :param first_name: The recipient's first name
        :param last_name: The recipient's last name
        :param pdf_path: The path to the PDF attachment (default: training_phishing.pdf)
        """
        try:
            # Set up the server
            with smtplib.SMTP(
                self.email_config["smtp_server"], self.email_config["smtp_port"]
            ) as s:
                s.starttls()
                s.login(
                    self.email_config["sender_email"], self.email_config["password"]
                )
                print(f"Logged in as {self.email_config['sender_email']}")
                # Create the email
                msg = MIMEMultipart()
                msg["From"] = sender_email  # Dynamic sender email
                msg["To"] = user_email
                msg["Subject"] = self.email_config["subject"]

                # Dynamically generate email content using first name and last name
                html_content = f"""
                                <html>
                                    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333;">
                                        <h1 style="color: #2c3e50;">Phishing Simulation Campaign Results</h1>
                                        <p>Dear {first_name} {last_name},</p>
                                        <p>Thank you for participating in our recent phishing simulation campaign. The results are as follows:</p>
                                        <ul>
                                            <li>You clicked on a phishing link during this campaign.</li>
                                        </ul>
                                        <p>We appreciate your efforts in helping us raise awareness about cybersecurity. To enhance your ability to recognize phishing attempts and protect yourself from potential threats, we strongly encourage you to complete our recommended training modules.</p>
                                        <p>If you have any questions or need further assistance, please don’t hesitate to reach out.</p>
                                        <footer style="margin-top: 20px; font-size: 12px; color: #7f8c8d;">
                                            <p>This email is part of a simulated phishing awareness campaign. Please remember to exercise caution and refrain from clicking on any suspicious links in real-life scenarios.</p>
                                        </footer>
                                    </body>
                                </html>
                                """
                msg.attach(MIMEText(html_content, "html"))

                # Adding the PDF attachment
                if pdf_path:
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_attachment = MIMEApplication(
                            pdf_file.read(), _subtype="pdf"
                        )
                        pdf_attachment.add_header(
                            "Content-Disposition",
                            "attachment",
                            filename="training_phishing.pdf",
                        )
                        msg.attach(pdf_attachment)

                # Send the email using msg.as_string() to get the MIME format
                s.sendmail(sender_email, user_email, msg.as_string())
                logging.info(f"Email sent to {user_email} successfully!")
                print(f"Email sent to {user_email} successfully!")
        except smtplib.SMTPException as e:
            logging.error(f"SMTP error occurred while sending to {user_email}: {e}")
            print(f"SMTP error occurred: {e}")
        except Exception as e:
            logging.error(
                f"Unexpected error occurred while sending to {user_email}: {e}"
            )
            print(f"An unexpected error occurred: {e}")


def load_campaign_data(json_file_path):
    """Load the campaign data from a JSON file

    :param json_file_path: The path to the JSON file containing campaign data"""
    try:
        with open(json_file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading campaign data from {json_file_path}: {e}")
        print(f"Error loading campaign data: {e}")
        return []


def send_emails_to_users(Feedback, campaign_data, sender_email):
    """Send emails to users who clicked on the phishing link

    :param Feedback: An instance of the Feedback class
    :param campaign_data: The campaign data containing user information
    :param sender_email: The sender's email address"""
    # Track users who clicked on links
    users_to_email = defaultdict(int)

    # Loop through the campaign data and filter users who clicked
    for user_data in campaign_data:
        if user_data.get("Clicked", 0) > 0:  # Check if the user clicked
            user_email = user_data.get("Email")
            first_name = user_data.get(
                "first_name", "User"
            )  # Default to 'User' if no name
            last_name = user_data.get("last_name", "")
            users_to_email[user_email] = (first_name, last_name)

    # Check if there are users to email
    if not users_to_email:
        print("No users to email (no one clicked the phishing link).")
        logging.info("No users to email (no one clicked the phishing link).")
        return

    # Send emails only to users who clicked at least once
    for user_email, (first_name, last_name) in users_to_email.items():
        try:
            # Send email to the user who clicked the link
            Feedback.send_email(sender_email, user_email, first_name, last_name)
        except Exception as e:
            logging.error(f"Failed to send email to {user_email}: {e}")
            print(f"Failed to send email to {user_email}: {e}")


def send_emails_periodically():
    """Example task to send emails periodically"""
    try:
        print("trying to retrieve data")
        retreive_data()  # Fetch GoPhish data
        print("data retrieved")
    except Exception as e:
        logging.error(f"Failed to retrieve GoPhish data: {e}")
        print(f"Failed to retrieve GoPhish data: {e}")
        return

    campaign_data_file = "gophish_campaign_results.json"

    # Load campaign data from the JSON file
    campaign_data = load_campaign_data(campaign_data_file)

    if not campaign_data:
        logging.warning("No campaign data found or failed to load.")
        print("No campaign data found or failed to load.")
        return

    if not campaign_data:
        print("No campaign data found or failed to load.")
        return

    # Create an instance of the Feedback class
    feedback = Feedback()

    # Get the sender email from environment variables
    sender_email = os.getenv("reporting_mail_username")

    if not sender_email:
        logging.error("Sender email is missing from environment variables.")
        print("Sender email is missing from environment variables.")
        return

    # Send emails to users who clicked on the phishing link
    send_emails_to_users(feedback, campaign_data, sender_email)
