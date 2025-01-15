# Imports

import os
from dotenv import load_dotenv
import json
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError

# Global variables

config = {}

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
    
def load_config() -> None:
    """
    Load the configuration from the config.json file.
    """
    # Globals
    global config
    # Load the JSON file
    config_file = "config.json"  # Replace with your JSON file's name if different
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config = json.load(file)
            #developer_message = config["developer_message"]
            #user_prompt = config["user_prompt"]
            #developer_message_subject = config["developer_message_subject"]
    else:
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    
def generate_mail_body_openai(department: str) -> str:
    """
    Generate the phishing mail body from the OpenAI API.

    :param department: str: The department to target.
    
    :return: str: The generated phishing mail body.
    """
    # Globals
    global config
    developer_message = config["developer_message"]
    user_prompt = config["user_prompt"]
    # Load the environment variables
    #load_env()

    # Load the configuration
    #load_config()

    # Generate the mail body
    with OpenAI() as client:
        try:
            mail_body = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "developer", "content": developer_message},
                {"role": "user", "content": user_prompt.format(department=department)}],
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
    global config
    developer_message_subject = config["developer_message_subject"]

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
    load_config()

    # Set department
    department = "HR"

    # Generate mail body
    mail_body = generate_mail_body_openai(department)

    # Generate mail subject
    mail_subject = generate_mail_subject_openai(mail_body)

    # Print the generated mail body and subject
    print(mail_subject)
    print(mail_body)