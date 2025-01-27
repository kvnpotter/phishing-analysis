# Imports

import random
import os
from CampaignCreator.genai_utils import (
    generate_mail_body_gemini,
    generate_mail_body_openai,
    generate_landing_page_openAI,
    generate_landing_page_gemini,
)
from datetime import datetime
from gophish.models import User, Group, SMTP, Page, Campaign, Template

# Classes


class PhishingMail:
    """ """

    def __init__(
        self,
        id: int,
        department: str,
        topics: dict[str : list[dict[str:str]]],
        prompts: dict[str:str],
    ) -> None:
        """
        Initialize the Template object to contain phishing email for the recipient.

        :param id: int: The ID of the template, row index of the recipient employee in supplied CSV file.
        :param department: str: The department to target.
        :param topics: dict[str:list[dict[str:str]]]: The topics for the departments.
        :param prompts: dict[str:str]: The prompts for the phishing mail generation.
        """
        self.id = id
        self.department = department
        self.topics = topics
        self.prompts = prompts
        self.model = None
        self.mail_body = None
        self.sender_email = None
        self.sender_name = None
        self.subject = None
        self.template = None

    def random_select_model(self) -> None:
        """
        Randomly select an AI model for mail generation.
        """
        self.model = random.choice(["OpenAI", "Gemini"])

    def select_email_generator(self) -> None:
        """
        Select the email generator based on the model.
        """
        if self.model == "OpenAI":
            self.generate_OpenAI_email()
        elif self.model == "Gemini":
            self.generate_Gemini_email()
        else:
            raise ValueError("Invalid model selected.")

    def generate_OpenAI_email(self) -> None:
        """
        Generate an email using OpenAI.
        """
        print("Generating OpenAI email...")
        result = generate_mail_body_openai(
            department=self.department, topics=self.topics, prompts=self.prompts
        )

        self.mail_body, self.sender_email, self.subject, self.sender_name = result

    def generate_Gemini_email(self) -> None:
        """
        Generate an email using Gemini.
        """
        print("Generating Gemini email...")
        result = generate_mail_body_gemini(
            department=self.department,
            topics=self.topics,
            prompts=self.prompts,
            api_key=os.environ.get("GOOGLE_API_KEY"),
        )

        self.mail_body, self.sender_email, self.subject, self.sender_name = result

    def generate_gp_template(self) -> None:
        """
        Generate a GoPhish template object.
        """
        envelope_sender = f"{self.sender_name} <{self.sender_email}>"
        self.template = Template(
            id=self.id,
            name=self.subject,
            html=self.mail_body,  # EDIT
            subject=self.subject,
            envelope_sender=envelope_sender,
        )


class UserGroup:
    """ """

    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        recipient_email: str,
        department: str,
    ) -> None:
        """
        Initialize the User object to contain recipient information.

        :param id: int: The user's ID (row index) obtained from the supplied CSV file with employee data.
        :param first_name: str: The user's first name.
        :param last_name: str: The user's last name.
        :param recipient_email: str: The user's email address.
        :param department: str: The user's department.
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.recipient_email = recipient_email
        self.department = department
        self.user = None
        self.group = None

    def generate_gp_user(self) -> None:
        """
        Generate a GoPhish user object.
        """
        self.user = User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.recipient_email,
            position=self.department,
        )

    def generate_gp_group(self) -> None:
        """
        Generate a GoPhish group object.
        """
        self.group = Group(
            id=self.id,
            name=f"{self.last_name}_{self.first_name}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}",
            targets=[self.user],
        )


class SenderProfile:
    """ """

    def __init__(
        self, id: int, name: str, sender_email: str, username: str, password: str
    ) -> None:
        """
        Initialize the SenderProfile object to contain sender information.

        :param id: int: The sender's ID obtained from the supplied CSV file with employee data, row index of the recipient employee.
        :param name: str: The sender's name.
        :param sender_email: str: The sender's email address.
        :param username: str: The username for the sender's email account.
        :param password: str: The password for the sender's email account.
        """
        self.id = id
        self.name = name
        self.sender_email = sender_email
        self.username = username
        self.password = password
        self.sender_profile = None

    def generate_gp_sender(self) -> None:
        """
        Generate a GoPhish sender object.
        """
        self.sender_profile = SMTP(
            id=self.id,
            name=self.name,
            interface_type="SMTP",
            host="smtp.gmail.com:465",  # PLACEHOLDER - can put own SMTP server
            username=self.username,
            password=self.password,
            from_address=self.sender_email,  # PLACEHOLER - can put own email
            ignore_cert_errors=True,
        )


class LandingPage:
    """ """

    def __init__(
        self,
        id: int,
        phishing_mail_body: str,
        prompts: dict[str:str],
        name: str,
        capture_credentials: bool = False,
        capture_passwords: bool = False,
    ) -> None:
        """
        Initialize the LandingPage object to contain the phishing landing page information.

        :param id: int: The landing page's ID.
        :param phishing_mail_body: str: The phishing mail body to use for generation.
        :param prompts: dict[str:str]: The prompts for the phishing generation.
        :param name: str: The name of the landing page.
        :capture_credentials: bool: (Optional) Whether to capture credentials.
        :capture_passwords: bool: (Optional) Whether to capture passwords.
        """
        self.id = id
        self.phishing_mail_body = phishing_mail_body
        self.prompts = prompts
        self.name = name
        self.capture_credentials = capture_credentials
        self.capture_passwords = capture_passwords
        self.redirect_url = "https://r.mtdv.me/you-got-phished"
        self.html = None
        self.page = None
        self.model = None

    def random_select_model(self) -> None:
        """
        Randomly select an AI model for page generation.
        """
        self.model = random.choice(["OpenAI", "Gemini"])

    def select_page_generator(self) -> None:
        """
        Select the page generator based on the model.
        """
        if self.model == "OpenAI":
            self.generate_OpenAI_page()
        elif self.model == "Gemini":
            self.generate_Gemini_page()
        else:
            raise ValueError("Invalid model selected.")

    def generate_OpenAI_page(self) -> None:
        """
        Generate a landing page using OpenAI.
        """
        print("Generating OpenAI page...")
        result = generate_landing_page_openAI(
            phishing_mail_body=self.phishing_mail_body, prompts=self.prompts
        )

        self.html = result

    def generate_Gemini_page(self) -> None:
        """
        Generate a landing page using Gemini.
        """
        print("Generating Gemini page...")
        result = generate_landing_page_gemini(
            phishing_mail_body=self.phishing_mail_body,
            prompts=self.prompts,
            api_key=os.environ.get("GOOGLE_API_KEY"),
        )  # PLACEHOLDER - can put own API key

        self.html = result

    def generate_gp_page(self) -> None:
        """
        Generate a GoPhish page object.
        """
        self.page = Page(
            id=self.id,
            name=self.name,
            html=self.html,
            capture_credentials=self.capture_credentials,
            capture_passwords=self.capture_passwords,
            redirect_url=self.redirect_url,
        )


class GoPhishCampaign:
    """ """

    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        recipient_email: str,
        department: str,
        topics: dict[str : list[dict[str:str]]],
        prompts: dict[str:str],
        username: str,
        password: str,
    ) -> None:
        """
        Initialize the GoPhishCampaign object to contain individual campaign information.

        :param id: int: The campaign's ID obtained from the supplied CSV file with employee data, row index of the recipient employee.
        :param first_name: str: The first name of recipient of campaign.
        :param last_name: str: The last name of recipient of campaign.
        :param recipient_email: str: The email address of recipient of campaign.
        :param department: str: The department of recipient of campaign.
        :param topics: dict[str:list[dict[str:str]]]: The topics for the departments.
        :param prompts: dict[str:str]: The prompts for the phishing mail generation.
        :param username: str: The username for the sender's email account.
        :param password: str: The password for the sender's email account.
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.recipient_email = recipient_email
        self.department = department
        self.topics = topics
        self.prompts = prompts
        self.username = username
        self.password = password
        self.template = None
        self.model = None
        self.sender_name = None
        self.sender_email = None
        self.mail_subject = None
        self.user = None
        self.group = None
        self.smtp = None
        self.landing_page = None
        self.url = "http://127.0.0.1/"  ### PLACEHOLDER
        self.campaign = None

    def setup_campaign(self) -> None:
        """
        Setup the phishing campaign using supplied data. Retrieve the template, sender, and subject.
        """

        # Create the template
        template = PhishingMail(
            id=self.id,
            department=self.department,
            topics=self.topics,
            prompts=self.prompts,
        )
        # template.random_select_model() # PLACEHOLDER ISSUES WITH OPENAI RATE LIMIT...
        # template.select_email_generator()
        template.generate_Gemini_email()
        template.generate_gp_template()

        self.template = template.template
        self.sender_name = template.sender_name
        self.sender_email = template.sender_email
        self.mail_subject = template.subject
        self.model = template.model
        self.template.name = f"{self.last_name}_{self.first_name}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"

        print(f"Recipient: {self.first_name} {self.last_name}")
        print(f"Email: {self.recipient_email}")
        print(f"Department: {self.department}")
        print(f"Mail subject: {self.mail_subject}")
        print(f"Mail Body:\n{self.template.html}")

        # Create user and user group

        recipient = UserGroup(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            recipient_email=self.recipient_email,
            department=self.department,
        )
        recipient.generate_gp_user()
        recipient.generate_gp_group()

        self.user = recipient.user
        self.group = recipient.group

        # Create sender profile

        smtp_name = f"{self.last_name}_{self.first_name}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"
        sender = SenderProfile(
            id=self.id,
            name=smtp_name,
            sender_email=self.sender_email,
            username=self.username,
            password=self.password,
        )
        sender.generate_gp_sender()

        self.smtp = sender.sender_profile

        # Create landing page
        page_name = f"{self.last_name}_{self.first_name}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"

        page = LandingPage(
            id=self.id,
            phishing_mail_body=self.template.text,
            prompts=self.prompts,
            name=page_name,
            capture_credentials=True,
            capture_passwords=True,
        )
        # page.random_select_model() # ISSUES WITH OPENAI RATE LIMIT...
        # page.select_page_generator()
        page.generate_Gemini_page()
        page.generate_gp_page()

        self.landing_page = page.page

    def generate_gp_campaign(self) -> None:
        """
        Generate a GoPhish campaign object.
        """
        self.campaign = Campaign(
            id=self.id,
            name=f"{self.last_name}_{self.first_name}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}",
            # send_by_date=self.send_by_date, PLACEHOLDER, HOW WORKS
            # launch_date=self.launch_date, PLACEHOLDER, HOW WORKS
            groups=[self.group],
            page=self.landing_page,
            template=self.template,
            smtp=self.smtp,
            url=self.url,
        )

