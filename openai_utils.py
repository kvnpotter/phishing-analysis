# Imports

import os
from dotenv import load_dotenv
import json
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError
import random

# Global variables

topics = {}
prompts = {}

# Functions

def load_env() -> None:
    """
    Load the environment variables from the .env file.
    """

    env_file = ".env"
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        raise FileNotFoundError(f"Environment file '{env_file}' not found.")
    
def load_topics() -> None:
    """
    Load the topics from the topics.json file.
    """
    # Globals
    global topics
    # Load the JSON file
    topics_file = "topics.json"  # Replace with your JSON file's name if different
    if os.path.exists(topics_file):
        with open(topics_file, "r") as file:
            topics = json.load(file)
    else:
        raise FileNotFoundError(f"Topics file '{topics_file}' not found.")
    
def load_prompts() -> None:
    """
    Load the prompts from the prompts.json file.
    """
    # Globals
    global prompts
    # Load the JSON file
    prompts_file = "prompts.json"  # Replace with your JSON file's name if different
    if os.path.exists(prompts_file):
        with open(prompts_file, "r") as file:
            prompts = json.load(file)
    else:
        raise FileNotFoundError(f"Prompts file '{prompts_file}' not found.")

def random_topic(department: str) -> dict[str:str]:
    """
    Get a random topic from the topics for the specified department.

    :param department: str: The department to target.

    :return: dict[str:str]: The random topic for the department.	
    """

    # Globals
    global topics

    # Get the topics for the department
    department_topics = topics[department]

    # Select a random topic
    random_topic = random.choice(department_topics)

    return random_topic
    
def generate_mail_body_openai(department: str, topic: dict[str, str]) -> str:
    """
    Generate the phishing mail body from the OpenAI API.

    :param department: str: The department to target.
    :param topic: dict[str, str]: The random topic for the department as a dictionary containing email subject, sender name and sender email as str.
    
    :return: str: The generated phishing mail body.
    """
    # Globals
    global prompts
    developer_message = prompts["developer_message"]
    user_prompt = prompts["user_prompt"]

    # Subject and sender setting

    subject = topic["topic"]
    sender = topic["sender"]

    # Generate the mail body
    with OpenAI() as client:
        try:
            mail_body = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "developer", "content": developer_message},
                {"role": "user", "content": user_prompt.format(department=department,
                                                               sender=sender,
                                                               subject=subject)}],
                temperature=0.7,
                max_tokens=300
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

    return mail_body.choices[0].message.content

def generate_mail_subject_openai(mail_body: str) -> str:
    """
    Generate the phishing mail subject from the OpenAI API using mail body.

    :param mail_body: str: The phishing mail body to use for subject generation.
    
    :return: str: The generated phishing mail subject.
    """

    # Globals
    global prompts
    developer_message_subject = prompts["developer_message_subject"]

    # Generate Subject
    with OpenAI() as client:
        try:
            mail_subject = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "developer", "content": developer_message_subject},
                {"role": "user", "content": mail_body}],
                temperature=0.7,
                max_tokens=300
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

    return mail_subject.choices[0].message.content

# Main code block

if __name__ == "__main__":
    
    # Load the environment variables
    load_env()
    load_prompts()
    load_topics()

    # Set department and topic
    department = "HR"
    topic = random_topic(department)

    # Generate mail body
    mail_body = generate_mail_body_openai(department= department,
                                          topic= topic)

    # Generate mail subject
    #mail_subject = generate_mail_subject_openai(mail_body)

    # Print the generated mail body and subject
    
    #print(mail_subject)
    print(mail_body)