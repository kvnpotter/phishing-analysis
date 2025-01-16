import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from gophish import Gophish
from gophish.models import Group, Campaign, User, Result, Page, Template, SMTP
import pandas as pd
import json

def connect():
    """
    Creates a connection with GoPhish via API.
    
    RETURNS api: connection object
    """
    host = 'https://127.0.0.1:3333/'
    api_key =  '44c7ffff7bedccb22a88c409ed411cfd7c27bb9fb2a4efdd35df46eaa711d302' # from the settings page
    api = Gophish(api_key, host=host, verify=False)
    return api


def create_groups(file, api):
    """
    Iterates over the received json file and creates one GoPhish
    group per individual.

    PARAMS
    file json: 
    """
    # Convert string to json
    file = json.loads(file)
    # create a row for each person (index) and key (column)
    rows = [{key: file[key][index] for key in file} for index in file['email'].keys()]
    # Create gophish targets
    target = [User(first_name=row['first_name'], last_name=row['last_name'], email=row['email'], position=row['position']) for row in rows]
    for user in target:
        group = Group(name=user.first_name, targets=[user])
        #Send to GoPhish
        api.groups.post(group)
        return group


html_code = '<html lang="eng"><header><h1>You have been hacked!</h1></header><html>'

page = Page(
    id=1,
    html=html_code,
    name='Hacked Page'
)

temp = Template(
    name='First Template'
)

def new_campaign(group):
    campaign = Campaign(
    name="Password Reset Campaign",
    groups=[group],
    page=page,
    template=temp,
    smtp=smtp,
    url='https://celinab23.wixsite.com/phiishing-awareness',
    # Set launch date and time
    #launch_date=launch_date_iso 
    )
    return campaign


def create_campaign(file):
    """
    Calls all required functions to trigger a campaign.

    PARAMS:
    file - json: of the target employees to send the emails to.
    """
    # Connect to GoPhish
    api = connect()
    # Call func to create individual groups
    create_groups(file, api)