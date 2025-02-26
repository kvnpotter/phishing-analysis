# Imports

from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError
import google.generativeai as genai
import random
import time


# Context manager for Gemini API client
class GeminiClient:
    """
    Context manager for the Gemini API client.
    Initialize the Gemini API client
    """

    def __init__(self, system_instruction: str, api_key: str) -> None:
        self.client = None
        self.system_instruction = system_instruction
        self.api_key = api_key

    def __enter__(self) -> genai.GenerativeModel:
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(
            model_name="gemini-1.5-flash", system_instruction=self.system_instruction
        )
        return self.client

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        pass


# Functions


def random_topic(
    department: str, topics: dict[str : list[dict[str:str]]]
) -> dict[str:str]:
    """
    Get a random topic from the topics for the specified department.

    :param department: str: The department to target.
    :param topics: dict[str:list[dict[str:str]]]: The topics for the departments.

    :return: dict[str:str]: The random topic for the department.
    """

    # Get the topics for the department
    department_topics = topics[department]

    # Select a random topic
    random_topic = random.choice(department_topics)

    return random_topic


def generate_mail_body_gemini(
    department: str,
    topics: dict[str : list[dict[str:str]]],
    prompts: dict[str:str],
    api_key: str,
) -> str:
    """
    Generate the phishing mail body from the Gemini API.

    :param department: str: The department to target.
    :param topics: dict[str:list[dict[str:str]]]: The topics for the departments.
    :param prompts: dict[str:str]: The prompts for the phishing mail generation.
    :param api_key: str: The API key for the Gemini API.

    :return: str: The generated phishing mail body.
    """
    # Get a random topic for the department
    topic = random_topic(department, topics)

    # Get prompts
    developer_message = prompts["developer_message"]
    tracker = '"<img src="{{.TrackingURL}}" style="display:none"/>"'  # EDIT TRACKER
    developer_message = developer_message.format(
        tracker=tracker,
        FirstName="{{.FirstName}}",
        LastName="{{.LastName}}",
        Position="{{.Position}}",
        Email="{{.Email}}",
        From="{{.From}}",
        URL="{{.URL}}",
    )
    user_prompt = prompts["user_prompt"]

    # Subject and sender setting

    subject = topic["Topic"]
    sender_name = topic["Sender"]
    sender_email = topic["sender_mail"]

    # Generate the mail body
    # Use the Gemini API to generate the mail body
    with GeminiClient(system_instruction=developer_message, api_key=api_key) as client:
        mail_body = client.generate_content(
            contents=user_prompt.format(
                department=department, sender=sender_name, subject=subject
            )
        )
    mail_with_tracker = mail_body.text  # + "\n{{.Tracker}}" # Add tracker EDIT
    print("Mail body generated")
    # print("Waiting 45 seconds") #Only used to stop rate limitation for gemini-1.5-pro free
    # time.sleep(45) # Wait for 45 seconds to not go over alotted quota to Gemini free !
    return (mail_with_tracker, sender_email, subject, sender_name)


def generate_mail_body_openai(
    department: str, topics: dict[str : list[dict[str:str]]], prompts: dict[str:str]
) -> str:
    """
    Generate the phishing mail body from the OpenAI API.

    :param department: str: The department to target.
    :param topics: dict[str:list[dict[str:str]]]: The topics for the departments.
    :param prompts: dict[str:str]: The prompts for the phishing mail generation.

    :return: str: The generated phishing mail body.
    """

    # Get a random topic for the department
    topic = random_topic(department, topics)

    # Get prompts
    developer_message = prompts["developer_message"]
    tracker = '"<img src="{{.TrackingURL}}" style="display:none"/>"'  # EDIT TRACKER
    developer_message = developer_message.format(
        tracker=tracker,
        FirstName="{{.FirstName}}",
        LastName="{{.LastName}}",
        Position="{{.Position}}",
        Email="{{.Email}}",
        From="{{.From}}",
        URL="{{.URL}}",
    )
    user_prompt = prompts["user_prompt"]

    # Subject and sender setting

    subject = topic["Topic"]
    sender_name = topic["Sender"]
    sender_email = topic["sender_mail"]

    # Generate the mail body
    with OpenAI() as client:
        try:
            mail_body = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "developer", "content": developer_message},
                    {
                        "role": "user",
                        "content": user_prompt.format(
                            department=department, sender=sender_name, subject=subject
                        ),
                    },
                ],
                temperature=0.7,
                max_tokens=300,
            )
        except APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
    mail_body.choices[0].message.content  # += "\n{{.Tracker}}" #Add tracker EDIT
    return mail_body.choices[0].message.content, sender_email, subject, sender_name


def generate_landing_page_gemini(
    phishing_mail_body: str, prompts: dict[str:str], api_key: str
) -> str:
    """
    Generate the phishing landing page from the Gemini API.

    :param phishing_mail_body: str: The phishing mail body.
    :param prompts: dict[str:str]: The prompts for the phishing landing page generation.
    :param api_key: str: The API key for the Gemini API.

    :return: str: The generated phishing landing page in HTML format.
    """

    # Get prompts
    developer_message_landing_page = prompts["developer_message_landing_page"]
    user_prompt_landing_page = prompts["user_prompt_landing_page"]

    # Generate the page
    # Use the Gemini API to generate the mail body
    with GeminiClient(
        system_instruction=developer_message_landing_page, api_key=api_key
    ) as client:
        landing_page = client.generate_content(
            contents=user_prompt_landing_page.format(email_body=phishing_mail_body)
        )
    # print("Waiting 45 seconds") #Only used to stop rate limitation for gemini-1.5-pro free
    # time.sleep(45) # Wait for 45 seconds to not go over alotted quota to Gemini free !
    print("Generated landing page")
    return landing_page.text


def generate_landing_page_openAI(
    phishing_mail_body: str, prompts: dict[str:str]
) -> str:
    """
    Generate the phishing landing page from the OpenAI API.

    :param phishing_mail_body: str: The phishing mail body.
    :param prompts: dict[str:str]: The prompts for the phishing landing page generation.

    :return: str: The generated phishing landing page in HTML format.
    """

    # Get prompts
    developer_message_landing_page = prompts["developer_message_landing_page"]
    user_prompt_landing_page = prompts["user_prompt_landing_page"]

    # Generate the page HTML
    with OpenAI() as client:
        try:
            landing_page_html = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "developer", "content": developer_message_landing_page},
                    {
                        "role": "user",
                        "content": user_prompt_landing_page.format(
                            email_body=phishing_mail_body
                        ),
                    },
                ],
                temperature=0.7,
                max_tokens=300,
            )
        except APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)

    print("Generated landing page")

    return landing_page_html.choices[0].message.content


# Main code block

if __name__ == "__main__":

    from CampaignCreator.environment_setup import load_env, load_prompts, load_topics

    load_env()
    topics = load_topics("Emailtopics.json")
    prompts = load_prompts("prompts.json")

    result = generate_mail_body_gemini(
        department="Telecommunication Services",
        topics=topics,
        prompts=prompts,
        api_key="",
    )
    print(result)
