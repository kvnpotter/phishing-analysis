# **Automated Phishing Awareness Campaign**


[Introduction](#introduction)     |     [Description](#description)     |       [Installation-Environment setup](#installation-environment-setup)    |       [Usage](#usage)    |[Contributors](#contributors)    |      [Timeline](#timeline)       |       [List of Improvements](#list-of-improvements)  

## **Introduction**

This repository contains the code and resources for an automated phishing awareness campaign for a Belgian telecommunications company, completed as a part of my AI and Data science bootcamp training at BeCode (Brussels, Belgium). The project aims to assess employee susceptibility to phishing attacks by using AI to generate fake phishing mails, based on available emplopyee information, and to analyze their response. Employees who fall for phishing attempts more than 50% of the time will receive targeted training content to improve their security awareness.

The campaign is fully automated, utilizing:
1. **GenAI** to generate relevant phishing emails.
2. [**GoPhish**](https://getgophish.com/), an open source application to create and manage phishing campaigns.
3. **FastAPI** for recipient upload and campaign management, and interaction with GoPhish.
4. **Streamlit** for API frontend (GUI) and data reporting.
5. **Automated Scheduling** for phishing simulations and sending training content.
6. **Training Resources** to educate employees.
7. **Data Analysis & Insights** to evaluate employee engagement and effectiveness.

Specifications for the final project/client expectations:
1. Fully automated tool which creates campaigns.
2. Based on provided target info : first and last name, email address and position at the company.
3. Find information on the person online, and choose a relevant topic for the phishing mail.
4. Generate a phishing mail about the topic using GenAI.
5. Create GoPhish objects and submit the data to send campaigns.
6. Ensure appropriate training for employees, based on their response to phishing mails. (Congratulate employees correctly reporting the mails)

In addition:
- [**Dashboarding:** Visualization and monitoring of phishing campaigns.](https://github.com/Miriam-Stoehr/phishing-campaign-analysis)

## **Description**

This section describes the repo structure in detail

- /CampaignCreator/ : modules handling campaign creation, including generating phishing mail content and landing pages
   * CampaignCreator.py : a function for creating a phishing campaign, used in local testing (defined as a collection of GoPhish campaigns, one per user in the specified user list).
   * environment_setup.py : a number of utility functions to load environment variables (API keys etc.), prompts (for GenAI), topics (phishing mail topics per department), configuration (file paths, hosts, URLs, scheduler timing in seconds).
   * genai_utils.py : functions to select a random topic (of 5), given the department where the employee works, on which to base the phishing email, and to generate phishing email/landing page content in HTML.
   * PhishingCampaign.py : set up a phishing campaign (defined as a collection of GoPhish campaigns, one per user in the specified user list), based on provided recipient data, topics and prompts. Setup a GoPhish campaign for each user.

- /CampaignScheduler/ : implement scheduling for sending the campaigns, based on user information stored in the API. Periodicity can be set in the config file.
- /EmailScheduler/ : to implement scheduling for sending the training emails, based on user response stored in GoPhish. Periodicity can be set in the config file.

- /GoPhishConnector/ : module to connect to an instance of GoPhish and interact with the application (send campaigns, delete data).

- /input_data_prompts_topics/ : Directory containing provided user data, prompts written for GenAI, training materual, and some possible topics.

- campaign_script.py : testing script to create campaigns and upload to GoPhish.
- config.json : specifies the path for prompt and topic files, adresses for API and GoPhish instances and intervals for scheduler.
- del_gophish.py : manually delete all information from GoPhish
- gophish_campaign_results.json : stores information on campaigns, used to select users to send training information to

- main.py : main API code
- streamlit_API_GUI.py : main code for streamlit-based API GUI


## **Installation-Environment Setup**

### **Prerequisites**
Ensure you have the following installed:
- Python
- Streamlit
- FastAPI
- GenAI SDK for Gemini and OpenAPI
- GoPhish (available from the [website](https://getgophish.com/)) and the API

### **Setup Instructions**
1. Clone the repository
   ```shell
   git clone https://github.com/kvnpotter/phishing-analysis.git
   cd phishing-analysis
   ```
2. Launch an instance of GoPhish, setup admin user, reporting mail, retrieve API key
3. Setup OpenAI and Gemini API keys
4. Get app passwords for necessary email accounts
5. Create a .env file with following structure
   ```Python
   GOPHISH_API_KEY = "YOUR_KEY_HERE"
   OPENAI_API_KEY = "YOUR_KEY_HERE"
   GOOGLE_API_KEY = "YOUR_KEY_HERE"
   gmail_username = "sender_email_address"
   gmail_app_password = "YOUR_KEY_HERE"
   smtp_reporting_mail = "smtp host for reporting"
   smtp_reporting_port = 587
   reporting_mail_username = "reporting_email_address"
   reporting_mail_password = "YOUR_KEY_HERE"
   SUBJECT="Feedback from our phishing campaign"
   ```
6. Setup recipient JSON and config file appropriately
5. Launch the API
   ```shell
   fastapi dev main.py
   ```
6. Startup streamlit GUI
   ```shell
   streamlit run streamlit_API_GUI.py
   ```

## **Usage**

1. **Uploading recipient data:**
   - Target information can be uploaded using the API GUI.
   - Copy the contents of the Employee.json file (after adding recipient emails) and paste in text box in GUI.
   - Clicking "Upload JSON recipients" will empty the user database and store the provided information.
   - To add one user, without deleting user database, repeat previous steps but click on "Add one user" instead.
2. **Launching campaign:**
   - Campaigns can be launched manually by clicking the button on the GUI. Stored user data will then be used to create the campaign, the content and upload to GoPhish to send the campaign
   - From API startup, a scheduler is instantiated, regularly (interval set in config) checking the recipient database, and sending campaigns to users in the db.
   - Launching a campaign will create all the necessary content for GoPhish per user.
   - Based on the provided department/position, a random selection will be made of 5 possible topics for phishing mails.
   - The subject is then sent to GenAI, randomly OpenAI or Gemini (disabled at the moment due to rate limitation errors, code is present and can be enabled) to create email content in HTML.
   - The email content is used to generate the landing page HTML.
   - Appropriate information on recipient, sender, phishing mail, landing page etc. is used to create the data for GoPhish
   - The data is posted to GoPhish and automatically launched
3. **Analyze responses and deliver training:**
   - Recipient responses are tracked by GoPhish
   - From API startup, a scheduler is instantiated, regularly (interval set in config) checking the GoPhish database, and retrieving necessary information.
   - Recipients who clicked on the phishing link will be sent an automated response for training purposes.
5. **Analyze data and generate reports:**
   - Set up the [phishing campaign analysis dashboard](https://github.com/Miriam-Stoehr/phishing-campaign-analysis). (Or click on the button in the API GUI)
   - Use the Streamlit dashboard to visualize employee engagement.

## **Contributors**

- **Kevin** - [https://github.com/kvnpotter] (Creation of API, GUI, modules interacting with GenAI and GoPhish, prompt engineering, integration of other parts including scheduling and email sending)
- **Celina Bolanos** - [https://github.com/Celina-Bolanos] (Contributions to API, GoPhish integration, possible deployment options)
- **Frank** - (https://github.com/FraNnky96) (Campaign and training scheduling)
- **Stef** - [https://github.com/StefVandekerckhove1] (Data analysis and Dashboard)
- **Olha** - [https://github.com/olhasl] (Data analysis and Dashboard)
- **Miriam** - [https://github.com/Miriam-Stoehr] (Contributions to the API, GoPhish integration, Data analysis and Dashboard)
- **fatemeh** - [https://github.com/Fatemeh992] (Creation of topics and employee files, writing training content, contribution to README)


## **Timeline**

Start project: 13/01/2025 09:30
End project: 24/01/2025 16:30


## **List of Improvements**

- Add scraping and automate, to obtain more relevant data on the recipient. This was attempted using information from LinkedIn, however most profiles were private, therefore not providing any information. Due to time constraints, the per department solution was kept in the final product.
- Improve employee response analysis and sending training/congratulations. Due to time constraints, a temporary solution is implemented ; which obtains campaign data from GoPhish and sends emails with training data to all employees who clicked on the link in the email. Scheduler is put into place, two scenarios need to be implemented, one where an employee would automatically receive training as soon as they click on the link or give credentials, and another where periodically (ex. every 3 months) each employee's response to the phishing mails would be evaluated, and additional training sent if they clicked on the link f. ex. > 50% of cases.
- Get tracking working. As of now, GoPhish does identify cases where the recipient clicked the phishing link, and can obtain credentials, however it does not detect when recipients simply open the email.
- Allow for user admin on GoPhish instance, and setting reporting email automatically (however, from the source code of GoPhish, it does not seem possible to do so, and has to be set mmanually via the GUI).
- Integrate data reporting with actual campaign data. As of now, dummy data is being used, due to time constraints.
- Improve user data storage in SQL database (instead of a list of dictionaries as a variable in the API).




