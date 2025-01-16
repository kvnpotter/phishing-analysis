# Imports

import random
from gemini_utils import generate_mail_body_gemini
from openai_utils import generate_mail_body_openai
from datetime import datetime
from gophish.models import User, Group, SMTP, Page, Campaign, Template

# Classes

class PhishingMail():
    """

    """
    def __init__(self,id: int,
                 department: str,
                 topics,
                 prompts) -> None:
        """
        Initialize the Template object to contain phishing email for the recipient.

        :param id: int: The ID of the template, row index of the recipient employee in supplied CSV file.
        :param department: str: The department to target.
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
        result = generate_mail_body_openai(department=self.department,
                                           topics=self.topics,
                                           prompts=self.prompts)

        self.mail_body, self.sender_email, self.subject, self.sender_name = result

    def generate_Gemini_email(self) -> None:
        """
        Generate an email using Gemini.
        """
        print("Generating Gemini email...")
        result = generate_mail_body_gemini(department=self.department,
                                           topics=self.topics,
                                           prompts=self.prompts,
                                           api_key=None) # PLACEHOLDER - can put own API key

        self.mail_body, self.sender_email, self.subject, self.sender_name = result

    def generate_gp_template(self) -> None:
        """
        Generate a GoPhish template object.
        """
        self.template = Template(id=self.id,
                                 name=self.subject,
                                 text=self.mail_body)

class UserGroup:
    """

    """
    def __init__(self, id: int, first_name: str, last_name: str, recipient_email: str, department: str) -> None:
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
        self.user = User(id= self.id, first_name=self.first_name, last_name=self.last_name, email=self.recipient_email, position=self.department)

    def generate_gp_group(self) -> None:
        """
        Generate a GoPhish group object.
        """
        self.group = Group(id= self.id, name=f"{self.last_name}_{self.first_name}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}", targets=[self.user])

class SenderProfile:
    """

    """
    def __init__(self, id: int, name: str, sender_email: str) -> None:
        """
        Initialize the SenderProfile object to contain sender information.

        :param id: int: The sender's ID obtained from the supplied CSV file with employee data, row index of the recipient employee.
        :param name: str: The sender's name.
        :param sender_email: str: The sender's email address.
        """
        self.id = id
        self.name = name
        self.sender_email = sender_email
        self.sender_profile = None

    def generate_gp_sender(self) -> None:
        """
        Generate a GoPhish sender object.
        """
        self.sender_profile = SMTP(id = self.id, 
                                   name=self.name,
                                   interface_type="SMTP",
                                   host = "host:port",
                                   from_address=self.sender_email, # PLACEHOLER - can put own email
                                   ignore_cert_errors=True)
        
class LandingPage:
    """

    """
    def __init__(self,
                 id: int,
                 html: str,
                 name: str,
                 redirect_url: str,
                 capture_credentials: bool = False,
                 capture_passwords: bool = False
                 ) -> None:
        """
        Initialize the LandingPage object to contain the phishing landing page information.

        :param id: int: The landing page's ID obtained from the supplied CSV file with employee data, row index of the recipient employee.
        :param html: str: The HTML content of the landing page.
        :param name: str: The name of the landing page.
        :capture_credentials: bool: (Optional) Whether to capture credentials.
        :capture_passwords: bool: (Optional) Whether to capture passwords.
        :redirect_url: str: The URL to redirect to after form submission.
        """
        self.id = id
        self.html = html
        self.name = name
        self.capture_credentials = capture_credentials
        self.capture_passwords = capture_passwords
        self.redirect_url = redirect_url
        self.page = None

    def generate_gp_page(self) -> None:
        """
        Generate a GoPhish page object.
        """
        self.page = Page(id=self.id,
                         name=self.name,
                         html=self.html,
                         capture_credentials=self.capture_credentials,
                         capture_passwords=self.capture_passwords,
                         redirect_url=self.redirect_url)
        
class GoPhishCampaign:
    """

    """
    def __init__(self,
                 id: int,
                 first_name: str,
                 last_name: str,
                 recipient_email: str,
                 department: str,
                 topics: dict[str:list[dict[str:str]]],
                 prompts: dict[str:str]) -> None:
        """
        Initialize the GoPhishCampaign object to contain individual campaign information.

        :param id: int: The campaign's ID obtained from the supplied CSV file with employee data, row index of the recipient employee.
        :param first_name: str: The first name of recipient of campaign.
        :param last_name: str: The last name of recipient of campaign.
        :param recipient_email: str: The email address of recipient of campaign.
        :param department: str: The department of recipient of campaign.
        :param topics: dict[str:list[dict[str:str]]]: The topics for the departments.
        :param prompts: dict[str:str]: The prompts for the phishing mail generation	
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.recipient_email = recipient_email
        self.department = department
        self.topics = topics
        self.prompts = prompts
        self.template = None
        self.model = None
        self.sender_name = None
        self.sender_email = None
        self.mail_subject = None
        self.user = None
        self.group = None
        self.smtp = None
        self.landing_page = None
        self.url = None ### PLACEHOLDER
        self.campaign = None

    def setup_campaign(self) -> None:
        """
        Setup the phishing campaign using supplied data. Retrieve the template, sender, and subject.
        """

        # Create the template
        template = PhishingMail(id=self.id,
                                department=self.department,
                                topics=self.topics,
                                prompts=self.prompts)
        template.random_select_model()
        template.select_email_generator()
        template.generate_gp_template()

        self.template = template.template
        self.sender_name = template.sender_name
        self.sender_email = template.sender_email
        self.mail_subject = template.subject
        self.model = template.model

        # Create user and user group

        recipient = UserGroup(id=self.id,
                              first_name=self.first_name,
                              last_name=self.last_name,
                              recipient_email=self.recipient_email,
                              department=self.department)
        recipient.generate_gp_user()
        recipient.generate_gp_group()

        self.user = recipient.user
        self.group = recipient.group

        # Create sender profile

        sender = SenderProfile(id=self.id, name=self.sender_name, sender_email=self.sender_email)
        sender.generate_gp_sender()

        self.smtp = sender.sender_profile

        # Create landing page

        page = LandingPage(id=self.id,
                           html="<html><body><h1>You failed the test!</h1></body></html>", #### PLACEHOLDER
                           name="Test Page", #### PLACEHOLDER
                           redirect_url="https://you_failed_the_test.com", #### PLACEHOLDER
                           capture_credentials=True,
                           capture_passwords=True)
        page.generate_gp_page()

        self.landing_page = page.page

    def generate_gp_campaign(self) -> None:
        """
        Generate a GoPhish campaign object.
        """
        self.campaign = Campaign(id=self.id,
                                 name=f"{self.last_name}_{self.first_name}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}",
                                 # send_by_date=self.send_by_date, PLACEHOLDER, HOW WORKS
                                 #launch_date=self.launch_date, PLACEHOLDER, HOW WORKS
                                 groups=[self.group],
                                 page=self.landing_page,
                                 template=self.template,
                                 smtp=self.smtp,
                                 url=self.url)

#if __name__ == "__main__":
#
#    # Testing template creation
#
#    template = PhishingMail(id=1, department="HR")
#    template.random_select_model()
#    template.select_email_generator()
#    template.generate_gp_template()
#    #print(template.subject)
#    #print(template.mail_body)
#    #print(template.sender)
#    #print(template.template.text)
#
#    # Testing user creation
#
#    user = UserGroup(id=1, first_name="John", last_name="Doe", email="john_doe@test.com", department="HR")
#    user.generate_gp_user()
#    user.generate_gp_group()
#    #print(user.group.name)
#
#    # Testing sender profile creation
#
#    sender = SenderProfile(id=1, name=template.sender, email="john_doe@test.com")
#    sender.generate_gp_sender()
#    #print(sender.sender_profile.name)
#
#    # Testing landing page creation
#
#    page = LandingPage(id=1,
#                       html="<html><body><h1>You failed the test!</h1></body></html>",
#                       name="Test Page",
#                       redirect_url="https://you_failed_the_test.com",
#                       capture_credentials=True,
#                       capture_passwords=True)
#    #print(page.html)
#
#    # Testing campaign creation
#
#    campaign = GoPhishCampaign(id=1,
#                               name="Test Campaign",
#                               send_by_date=datetime.now(),
#                               launch_date=datetime.now(),
#                               groups=[user.group],
#                               page=None,
#                               template=template.template,
#                               smtp=sender.sender_profile,
#                               url="https://you_failed_the_test.com")
#    campaign.generate_gp_campaign()
#    print(campaign.campaign)