import pandas as pd
import streamlit as st

@st.cache_data
def load_data(data_path: str) -> pd.DataFrame:
    """Load and cache data from CSV."""
    data = pd.read_csv(data_path)

    # Create grouping dictionary
    grouping_dict = {
        'Cloud Services': 'Technology and IT Services',
        'Technical Support': 'Technology and IT Services',
        'Data Management and Analytics': 'Data and Analytics',
        'IT Support Services': 'Technology and IT Services',
        'Customer Support': 'Customer and Client Management',
        'Infrastructure Management': 'Technology and IT Services',
        'Client Onboarding': 'Customer and Client Management',
        'Research & Development (R&D)': 'Research and Development (R&D)',
        'IoT (Internet of Things)': 'Technology and IT Services',
        'Cybersecurity': 'Technology and IT Services',
        'Cloud Computing': 'Technology and IT Services',
        'Digital Platforms Management': 'Technology and IT Services',
        'Telecommunication Services': 'Telecommunications',
        'Human Resources (HR)': 'Human Resources',
        'Hardware Integration': 'Technology and IT Services',
        'Content Creation': 'Media and Content Operations',
        'Digital Identity and Authentication': 'Technology and IT Services',
        'Media and Entertainment': 'Media and Content Operations',
        'Green Technology Initiatives': 'Sustainability and Corporate Responsibility',
        'Broadband and Mobile Services': 'Telecommunications',
        'Emerging Technologies': 'Research and Development (R&D)',
        'AI and Machine Learning': 'Data and Analytics',
        'Budgeting and Financial Analysis': 'Finance and Business Operations',
        'B2B and B2C Sales': 'Customer and Client Management',
        'Broadcasting & Media Operations': 'Media and Content Operations',
        'Revenue Management': 'Customer and Client Management',
        'Finance & Accounting': 'Finance and Business Operations',
        'IT Solutions': 'Technology and IT Services',
        'Brand Management': 'Brand Management',
        'Partnerships & Affiliations': 'Customer and Client Management',
        'Digital Transformation Strategies': 'Technology and IT Services',
        'Legal and Compliance': 'Legal',
        'Product Development': 'Research and Development (R&D)',
        'Digital Marketing': 'Finance and Business Operations',
        'Software Solutions': 'Technology and IT Services',
        'CPaaS (Communication Platform as a Service) Solutions': 'Technology and IT Services',
        'Sustainability & Corporate Social Responsibility (CSR)': 'Sustainability and Corporate Responsibility'
    }

    # Create a new column 'position_group' based on the 'position' column
    data['position_group'] = data['position'].map(grouping_dict)

    return data