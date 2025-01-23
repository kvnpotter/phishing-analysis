# Imports

import os
from dotenv import load_dotenv
import json

# Loading API keys, prompts and topics

def load_env() -> str|None:
    """
    Load the API keys from the .env file.

    :return: tuple(str): The Google API key, Gmail username, and Gmail app password.
    """

    env_file = ".env"
    if os.path.exists(env_file):
        load_dotenv(env_file)
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        gmail_username = os.environ.get("gmail_username")
        gmail_app_password = os.environ.get("gmail_app_password")
        return (GOOGLE_API_KEY, gmail_username, gmail_app_password)
    else:
        raise FileNotFoundError(f"Environment file '{env_file}' not found.")
    
def load_config() -> str:
    """ 
    Load the configuration from the config.json file.
    """

    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, "r", encoding='utf-8') as file:
            config = json.load(file)
            return config
    else:
        raise FileNotFoundError(f"Topics file '{config_file}' not found.")
    
def load_topics(path: str) -> str|None:
    """
    Load the topics from the topics.json file.

    :param path: str: The path to the topics.json file.

    :return: dict: The topics dictionary.
    """

    # Load the JSON file
    topics_file = path
    if os.path.exists(topics_file):
        with open(topics_file, "r", encoding='utf-8') as file:
            topics = json.load(file)
            return topics
    else:
        raise FileNotFoundError(f"Topics file '{topics_file}' not found.")
    
def load_prompts(path: str) -> str|None:
    """
    Load the prompts from the prompts.json file.

    :param path: str: The path to the prompts.json file.

    :return: dict: The prompts dictionary.
    """

    # Load the JSON file
    prompts_file = path 
    if os.path.exists(prompts_file):
        with open(prompts_file, "r") as file:
            prompts = json.load(file)
            return prompts
    else:
        raise FileNotFoundError(f"Prompts file '{prompts_file}' not found.")