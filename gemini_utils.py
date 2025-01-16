# Imports

import google.generativeai as genai
import random
import time

# Context manager for Gemini API client
class GeminiClient:
    """
    Context manager for the Gemini API client.
    Initialize the Gemini API client
    """
    def __init__(self, system_instruction: str) -> None:
        self.client = None
        self.system_instruction = system_instruction

    def __enter__(self) -> genai.GenerativeModel:
        self.client = genai.GenerativeModel(model_name="gemini-1.5-pro",
                                            system_instruction= self.system_instruction)
        return self.client
    
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        pass

# Functions
    
def random_topic(department: str, topics: dict[str:list[dict[str:str]]]) -> dict[str:str]:
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
    
def generate_mail_body_gemini(department: str,
                              topics: dict[str:list[dict[str:str]]],
                              prompts: dict[str:str],
                              api_key: str) -> str:
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
    user_prompt = prompts["user_prompt"]

    # Subject and sender setting

    subject = topic["Topic"]
    sender_name = topic["Sender"]
    sender_email = topic["sender_mail"]
    t = "{{.Tracker}}"

    # Generate the mail body
    # Use the Gemini API to generate the mail body
    with GeminiClient(system_instruction= developer_message) as client:
        mail_body = client.generate_content(contents = user_prompt.format(department=department,
                                                                          sender=sender_name,
                                                                          subject=subject,
                                                                          t=t))
    print("Mail body generated")
    print("Waiting 45 seconds")
    time.sleep(45) # Wait for 45 seconds to not go over alotted quota to Gemini free !
    return (mail_body.text, sender_email, subject, sender_name)

# def generate_mail_subject_gemini(mail_body: str) -> str:
#     """
#     Generate the phishing mail subject from the Gemini API.
# 
#     :param mail_body: str: The phishing mail body.
#     
#     :return: str: The generated phishing mail subject.
#     """
# 
#     # Globals
#     global prompts
#     developer_message_subject = prompts["developer_message_subject"]
# 
#     # Generate the mail subject
#     # Use the Gemini API to generate the mail subject
#     with GeminiClient(system_instruction= developer_message_subject) as client:
#         mail_subject = client.generate_content(contents = mail_body)
#     return mail_subject.text

# Main code block

if __name__ == "__main__":
    
    from environment_setup import load_env, load_prompts, load_topics
    load_env()
    topics = load_topics("Emailtopics.json")
    prompts = load_prompts("prompts.json")

    result = generate_mail_body_gemini(department="Telecommunication Services",
                                        topics=topics,
                                        prompts=prompts,
                                        api_key="")
    print(result)

    
