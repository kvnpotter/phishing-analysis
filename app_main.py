import streamlit as st
import pandas as pd
from streamlit_app.data_loader import load_data
from streamlit_app.filters import display_sidebar, filter_data
from streamlit_app.kpi_calculations import calculate_kpis_abs
from streamlit_app.visualization import display_kpi_and_funnel, display_position_analysis, calculate_kpis_table, display_reported_analysis

st.set_page_config(
    page_title="Phishing Campaigns Dashboard",
    page_icon="mail.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    footer {visibility: hidden;} 
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.image("mail.png", width=50)
    st.title("Phishing Campaign Dashboard")

    # Load data
    data_path = "./generated_results_cleaned.csv"
    df = load_data(data_path)
    df['send_date'] = pd.to_datetime(df['send_date'])
    df['modified_date'] = pd.to_datetime(df['modified_date'])

    # Sidebar filters
    start_date, last_date, selected_positions, selected_templates, selected_statuses = display_sidebar(df)

    # Filter data
    filtered_data = filter_data(df, start_date, last_date, selected_positions, selected_templates, selected_statuses)

    # Calculate KPIs and visualize
    kpis = calculate_kpis_abs(filtered_data)
    kpi_names = ["Sent Emails", "Opened Emails", "Clicked Links", "Submitted Data", "Reported Emails"]
    display_kpi_and_funnel(filtered_data, kpis, kpi_names)
    display_position_analysis(filtered_data)

    # KPI Table
    status_order = ["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"]
    calculate_kpis_table(filtered_data, status_order)

    display_reported_analysis(filtered_data)

if __name__ == '__main__':
    main()