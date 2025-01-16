# Imports

import random
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError

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
    
def generate_mail_body_openai(department: str,
                              topics: dict[str:list[dict[str:str]]],
                              prompts: dict[str:str]) -> str:
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
                messages=[{"role": "developer", "content": developer_message},
                {"role": "user", "content": user_prompt.format(department=department,
                                                               sender=sender_name,
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

    return mail_body.choices[0].message.content, sender_email, subject, sender_name

#def generate_mail_subject_openai(mail_body: str) -> str:
#    """
#    Generate the phishing mail subject from the OpenAI API using mail body.
#
#    :param mail_body: str: The phishing mail body to use for subject generation.
#    
#    :return: str: The generated phishing mail subject.
#    """
#
#    # Globals
#    global prompts
#    developer_message_subject = prompts["developer_message_subject"]
#
#    # Generate Subject
#    with OpenAI() as client:
#        try:
#            mail_subject = client.chat.completions.create(
#                model="gpt-4o-mini",
#                messages=[{"role": "developer", "content": developer_message_subject},
#                {"role": "user", "content": mail_body}],
#                temperature=0.7,
#                max_tokens=300
#            )
#        except APIConnectionError as e:
#            print("The server could not be reached")
#            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
#        except RateLimitError as e:
#            print("A 429 status code was received; we should back off a bit.")
#        except APIStatusError as e:
#            print("Another non-200-range status code was received")
#            print(e.status_code)
#            print(e.response)
#
#    return mail_subject.choices[0].message.content

# Main code block

if __name__ == "__main__":
    
    # Load the environment variables
    #load_env()
    #load_prompts()
    #load_topics()

    # Set department and topic
    department = "HR"
    #topic = random_topic(department)

    # Generate mail body
    mail_body = generate_mail_body_openai(department= department)

    # Generate mail subject
    #mail_subject = generate_mail_subject_openai(mail_body)

    # Print the generated mail body and subject
    
    #print(mail_subject)
    print(mail_body)