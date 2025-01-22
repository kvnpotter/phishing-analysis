import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def generate_queries(file):
    """ 
    Reads json file and generates a list of "queries" to be passed to 
    Google API

    PARAMS
    file json- containing the employees information

    RETURNS
    queries list - of the first name + last name + proximus
    """
    queries = []
    #file = pd.read_json(file)
    target = zip(file['first_name'], file['last_name'])
    for name, last in target:
        queries.append(f'{name} {last} proximus')
        # Could modify here to call get_link function
        # with the created query instead
    return queries


def get_info(query: str):
    """ 
    Gathers target basic information via online search.

    PARAMS:
    quere -str: name of the target person 

    RETURNS
    profile_link -str: url to the LinkedIn profile (if found)
    photo_link -str: url to the profile picture (if any)
    """
    # Set url, api key and engine id
    url = 'https://www.googleapis.com/customsearch/v1'  
    api_key = '****************'
    engine_id = '**************'

    # set params for connections
    params = {'key': api_key,
        'cx': engine_id,
        'q': query,
        'num': 1}

    # Connect to Google custom search API
    req = requests.get(url, params=params)

    # Get results
    try:
        results = req.json()['items']
    
    except KeyError:
        return print(f'No results for {query}')
    
    else:
        title = [item['title'] for item in results][0]
        profile_link = [item['link'] for item in results][0]
        basic_data = [item['snippet'] for item in results][0]

        pagemap = [item['pagemap'] for item in results][0]
        pagemap = pagemap['cse_thumbnail'][0]
        photo_link = pagemap['src']

        return (title, profile_link, basic_data, photo_link)


def get_details(url: str):
    """ 
    Scraps target's information if Linked in profile is public

    PARAMS
    url -str: link to the target's linkedIn profile

    RETURNS
    location -str: city name
    school -str: school or university name 
    languages -str: spoken languages
    posts
    """
    # Instantiate webDriver
    driver = webdriver.Edge()
    # Open LinkedIn profile
    driver.get(url)

    time.sleep(10)
    # test if profile is accessible (not private)
    try:
        popup = driver.find_element(By.CSS_SELECTOR, '#base-contextual-sign-in-modal > div > section > button > icon > svg')
        popup.click()
    # Print message if profile is not accessible:
    except:
        driver.close()
        return print('Private profile')

    # Otherwise, get the information.
    else:
        # Get location
        location = driver.find_element(By.CLASS_NAME, 'not-first-middot')
        location = location.text.split(',')[0]
        try: 
            # Get school name
            school = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[2]/div/div[2]/a/span')
            # Get languages
            main = driver.find_element(By.CSS_SELECTOR, r'#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section > section.core-section-container.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.py-4.languages')
            # Get latest posts they liked
            posts = driver.find_elements(By.TAG_NAME, 'h3')
        except:
            school = None
            languages = None
            posts = None
        else:
            school = school.text
            languages = main.find_elements(By.TAG_NAME, 'h3')
            languages = [lang.text for lang in languages]
            posts = [post.text for post in posts if len(post.text) > 100 ]

        driver.close()
    return (location, school, languages, posts)
