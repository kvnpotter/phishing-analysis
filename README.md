# **Automated Phishing Awareness Campaign**


[Introduction](#introduction)     |     [Description](#description)     |       [Installation-Environment setup](#installation-environment-setup)    |       [Usage](#usage)    |[Contributors](#contributors)    |      [Timeline](#timeline)       |       [List of Improvements](#list-of-improvements)  

## **Introduction**

This repository contains the code and resources for an automated phishing awareness campaign for a Belgian telecommunications company, completed as a part of my AI and Data science bootcamp training at BeCode (Brussels, Belgium). The project aims to assess employee susceptibility to phishing attacks by using AI to generate fake phishing mails, based on available emplopyee information, and to analyze their response. Employees who fall for phishing attempts more than 50% of the time will receive targeted training content to improve their security awareness.

The campaign is fully automated, utilizing:
1. **GenAI** to generate relevant phishing emails.
2. **GoPhish**, an open source application to create and manage phishing campaigns.
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

This section describes the repo structure and working in detail

- /CampaignCreator/ : modules handling campaign creation, including generating phishing mail content and landing pages
* CampaignCreator.py : a function for creating a phishing campaign, used in local testing (defined as a collection of GoPhish campaigns, one per user in the specified user list)
* environment_setup.py : a number of utility functions to load environment variables (API keys etc.), prompts (for GenAI), topics (phishing mail topics per department), configuration (file paths, hosts, URLs, scheduler timing in seconds)
* 






## **Installation-Environment Setup**

### **Prerequisites**
Ensure you have the following installed:
- Python (>=3.8)
- GoPhish
- Streamlit
- FastAPI
- GenAI SDK
- Required Python packages (install using `requirements.txt`)

### **Setup Instructions**
1. Clone the repository:
   ```shell
   git clone https://github.com/proximus-ada/phishing-awareness.git
   cd phishing-awareness
   ```
2. Create a virtual environment and activate it:
   ```shell
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
   ```shell
   pip install -r requirements.txt
   ```
4. Set up GoPhish and configure phishing email templates.
5. Run the AI-based phishing email generator:
   ```shell
   python generate_emails.py
   ```
6. Start the API service:
   ```shell
   uvicorn api:app --reload
   ```
7. Start the Streamlit dashboard:
   ```shell
   streamlit run dashboard.py
   ```

## **Usage**

1. **Launch the phishing campaign:**
   - Upload target emails via API.
   - Configure and deploy phishing emails using GoPhish.
   - Schedule automatic or manual campaigns.
2. **Analyze responses:**
   - Run the AI model to assess phishing susceptibility.
   - Set up the [phishing campaign analysis dashboard](https://github.com/Miriam-Stoehr/phishing-campaign-analysis).
   - Retrieve email interaction data from GoPhish.
3. **Generate reports:**
   - Use the Streamlit dashboard to visualize employee engagement.
4. **Deliver training:**
   - Automatically assign training materials to high-risk employees.

## **Contributors**

- **Kevin** - [https://github.com/kvnpotter]
- **Celina Bolanos** - [https://github.com/Celina-Bolanos]
- **Frank** - (https://github.com/FraNnky96)
- **Stef** - [https://github.com/StefVandekerckhove1]
- **Olha** - [https://github.com/olhasl]
- **Miriam** - [https://github.com/Miriam-Stoehr]
- **fatemeh** - [https://github.com/Fatemeh992]


## **Timeline**

- **Phase 1:** Project Initiation & Tool Selection  
- **Phase 2:** Email Generation & Testing  
- **Phase 3:** API & Campaign Automation  
- **Phase 4:** AI Integration & Analysis  
- **Phase 5:** Dashboard Development  
- **Phase 6:** Testing & Deployment  
- **Phase 7:** Training Content Distribution & Final Report


## **List of Improvements**

- Add scraping and automate, to obtain more relevant data on the recipient. This was attempted using information from LinkedIn, however most profiles were private, therefore not providing any information. Due to time constraints, the per department solution was kept in the final product.
- Improve employee response analysis and sending training/congratulations. Due to time constraints, a temporary solution is implemented ; which obtains campaign data from GoPhish and sends emails with training data to all employees who clicked on the link in the email. Scheduler is put into place, two scenarios need to be implemented, one where an employee would automatically receive training as soon as they click on the link or give credentials, and another where periodically (ex. every 3 months) each employee's response to the phishing mails would be evaluated, and additional training sent if they clicked on the link f. ex. > 50% of cases.
- Get tracking working. As of now, GoPhish does identify cases where the recipient clicked the phishing link, and can obtain credentials, however it does not detect when recipients simply open the email.
- Allow for user admin on GoPhish instance.




