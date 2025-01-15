# Imports

import os
from dotenv import load_dotenv
import json
import google.generativeai as genai

# Global variables

prompts = {}
GEMINI_API_KEY = ""

# Functions

def load_env() -> None:
    """
    Load the environment variables from the .env file.
    """

    # Globals
    global GEMINI_API_KEY

    env_file = ".env"
    if os.path.exists(env_file):
        load_dotenv(env_file)
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    else:
        raise FileNotFoundError(f"Environment file '{env_file}' not found.")
    
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
    
def generate_mail_body_gemini(department: str) -> str:
    """
    Generate the phishing mail body from the Gemini API.

    :param department: str: The department to target.
    
    :return: str: The generated phishing mail body.
    """
    # Globals
    global prompts, GEMINI_API_KEY
    developer_message = prompts["developer_message"]
    user_prompt = prompts["user_prompt"]

    # Generate the mail body
    # Use the Gemini API to generate the mail body
    model=genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=developer_message)
    mail_body = model.generate_content(user_prompt.format(department=department))

    return mail_body.text

def generate_mail_subject_gemini(mail_body: str) -> str:
    """
    Generate the phishing mail subject from the Gemini API.

    :param mail_body: str: The phishing mail body.
    
    :return: str: The generated phishing mail subject.
    """

    # Globals
    global prompts
    developer_message_subject = prompts["developer_message_subject"]

    # Generate the mail subject
    # Use the Gemini API to generate the mail subject
    model=genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=developer_message_subject)
    mail_subject = model.generate_content(mail_body)

    return mail_subject.text

# Main code block

if __name__ == "__main__":
    
    # Load the environment variables
    load_env()
    load_prompts()

    # Set department
    department = "HR"

    # Generate mail body
    mail_body = generate_mail_body_gemini(department)

    # Generate mail subject
    mail_subject = generate_mail_subject_gemini(mail_body)

    # Print the generated mail body and subject
    print(mail_subject)
    print(mail_body)

    
