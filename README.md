
# **Proximus ADA Phishing Awareness Campaign**


[Introduction](#Introduction)     |     [Description](#Description)     |       [Installation-Environment setup](#Installation-Environment-setup)    |       [Usage](#Usage)    |[Contributors](#Contributors)    |      [Timeline](#Timeline)       |       [List of Improvements](#list-of-improvements)  

## **Introduction**

This repository contains the code and resources for an automated phishing awareness campaign at Proximus ADA done as a part of Data Science and AI training course at Becode in 2025. The project aims to assess employees' susceptibility to phishing attacks by using AI to analyze their responses to simulated phishing emails. Employees who fall for phishing attempts more than 50% of the time will receive targeted training content to improve their security awareness.

The campaign is fully automated, utilizing:
1. **GenAI** to generate relevant phishing emails.
2. **GoPhish** to send and manage phishing campaigns.
3. **Streamlit/FastAPI** for API and campaign management.
4. **Automated Scheduling** for regular and manual phishing simulations.
5. **Training Resources** to educate employees.
6. **Data Analysis & Insights** to evaluate employee engagement and effectiveness.

## **Description**

The phishing campaign operates in a structured workflow:

### **Data Analysis:**
- **Generate Emails:** Using GenAI to create phishing emails dynamically.
- **Send Emails:** Testing and deployment through GoPhish.
- **Dashboarding:** Visualization and monitoring of phishing campaigns.
- **Training Resource:** educational content is provided based on the output.
- **Align with DE:** Ensure proper data format and API compatibility.
- **Data Analysis & Insights:** Extract meaningful statistics on phishing responses.

### **Data Engineering:**
- **API Development:** Create an API (FastAPI or Streamlit) to upload target email lists and trigger campaigns.
- **Campaign Scheduling:** Support both planned (automated) and manual campaigns.
- **Follow-up Data Processing:** Retrieve email response data from GoPhish and store it for analysis.
- **Security & Roles:** Implement access control and secure data handling.
- **Scheduling:** Automate recurring phishing campaigns.

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
   - Retrieve email interaction data from GoPhish.
3. **Generate reports:**
   - Use the Streamlit dashboard to visualize employee engagement.
4. **Deliver training:**
   - Automatically assign training materials to high-risk employees.

## **Contributors**

- **[Kevin]** - [https://github.com/kvnpotter]
- **[Celina Bolanos]** - [https://github.com/Celina-Bolanos]
- **[Frank]** - (https://github.com/FraNnky96)
- **[Stef]** - [https://github.com/StefVandekerckhove1]
- **[Olha]** - [https://github.com/olhasl]
- **[Miria]** - [(https://github.com/Miriam-Stoehr)]
- **[fatemeh]** - [(https://github.com/Fatemeh992)]


## **Timeline**

- **Phase 1:** Project Initiation & Tool Selection  
- **Phase 2:** Email Generation & Testing  
- **Phase 3:** API & Campaign Automation  
- **Phase 4:** AI Integration & Analysis  
- **Phase 5:** Dashboard Development  
- **Phase 6:** Testing & Deployment  
- **Phase 7:** Training Content Distribution & Final Report  

## **List of Improvements**

- Enhance AI model accuracy for phishing detection.
- Improve dashboard UI/UX.
- Expand phishing scenarios for a more comprehensive assessment.
- Automate feedback and reporting mechanisms further.
- Strengthen security and role-based access control.

---
This project is an ongoing effort to strengthen cybersecurity awareness at Proximus ADA through innovative AI-driven automation.
````
