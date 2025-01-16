import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
from typing import List, Tuple

st.set_page_config(
    page_title="Phishing Campaigns Dashboard",
    page_icon="mail.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

@st.cache_data
def load_data(data_path):
    """Load and cache data from CSV."""
    data = pd.read_csv(data_path)
    return data

def filter_data(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    return data[data[column].isin(values)] if values else data

@st.cache_data
def calculate_kpis_abs(data: pd.DataFrame) -> List[float]:
    '''Calculate the absolute KPIs'''
    total_sent = len(data[data["status"].isin(["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"])])
    opened_emails = len(data[data["status"].isin(["Email Opened", "Clicked Link", "Submitted Data"])])
    clicked_links = len(data[data["status"].isin(["Clicked Link", "Submitted Data"])])
    submitted_data = len(data[data["status"] == "Submitted Data"])
    reported_emails = len(data[data["status"] == "Email Reported"])
    return [total_sent, opened_emails, clicked_links, submitted_data, reported_emails]

@st.cache_data
def calculate_kpis_rel(data: pd.DataFrame) -> List[float]:
    '''Calculate the relative KPIs - percentages (relative to total_sent)'''
    total_sent = len(data[data["status"].isin(["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"])])
    opened_emails = len(data[data["status"].isin(["Email Opened", "Clicked Link", "Submitted Data"])])
    clicked_links = len(data[data["status"].isin(["Clicked Link", "Submitted Data"])])
    submitted_data = len(data[data["status"] == "Submitted Data"])
    reported_emails = len(data[data["status"] == "Email Reported"])
    sent_percentage = (total_sent / total_sent) * 100 if total_sent > 0 else 0
    opened_percentage = (opened_emails / total_sent) * 100 if total_sent > 0 else 0
    clicked_percentage = (clicked_links / total_sent) * 100 if total_sent > 0 else 0
    submitted_percentage = (submitted_data / total_sent) * 100 if total_sent > 0 else 0
    reported_percentage = (reported_emails / total_sent) * 100 if total_sent > 0 else 0
    return [sent_percentage, opened_percentage, clicked_percentage, submitted_percentage, reported_percentage]

def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
    st.header("KPI Metrics")
    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(5), zip(kpi_names, kpis))):
        col.metric(label=kpi_name, value=kpi_value)

def display_sidebar(data: pd.DataFrame) -> Tuple[List[str], List[str], List[str], List[str], List[str]]:
    st.sidebar.header("Filters")
    
    # Convert pd.Timestamp to timezone-aware
    start_date = pd.Timestamp(st.sidebar.date_input("Start date", data['send_date'].min().date())).tz_localize("UTC")
    last_date = pd.Timestamp(st.sidebar.date_input("End date", data['send_date'].max().date())).tz_localize("UTC")

    position = sorted(data['position'].unique())
    selected_positions = st.sidebar.multiselect("Position", position, position)

    selected_campaigns = st.sidebar.multiselect("Select Campaign", data['campaign_name'].unique())

    selected_statuses = st.sidebar.multiselect("Select Status", data['status'].unique())

    return start_date, last_date, selected_positions, selected_campaigns, selected_statuses

def display_charts(data: pd.DataFrame):
    # Calculate KPIs once
    abs_values = calculate_kpis_abs(data)
    rel_values = calculate_kpis_rel(data)

    # Prepare the data for the funnel chart
    funnel_data = {
        "Status": [
            "Sent Emails",
            "Opened Emails",
            "Clicked Links",
            "Submitted Data",
            "Reported Emails"
        ],
        "Count": abs_values,
        "Percentage": rel_values
    }

    # Create a DataFrame and sort by 'Count' in descending order
    funnel_df = pd.DataFrame(funnel_data).sort_values("Percentage")

    funnel_df["Status"] = pd.Categorical(
        funnel_df["Status"],
        categories=funnel_df["Status"][::-1],  # Reverse the order
        ordered=True
    )

    # Create the funnel chart
    fig_funnel = px.funnel(
        funnel_df,
        x="Percentage",  # The size of the funnel sections
        y="Status",  # The labels for the sections
        title="Phishing Campaign Funnel Chart",
        color="Status",  # Optional: adds color to the sections
        color_discrete_sequence=px.colors.sequential.Darkmint
    )

    # Remove the legend
    fig_funnel.update_layout(showlegend=False)

    # Add percentage sign to the labels
    fig_funnel.update_traces(
        texttemplate="%{x}%",  # Add '%' to the data labels
        textposition="inside"  # Place labels inside the funnel sections
    )

    # Display the funnel chart in Streamlit
    st.plotly_chart(fig_funnel)

def display_position_analysis(data: pd.DataFrame):
    """
    Display analysis of phishing campaign data by position.
    Includes bar charts and pie charts for position-based insights.
    """
    st.header("Position Analysis")

    # Group data by position and calculate metrics
    position_counts = data["position"].value_counts().reset_index()
    position_counts.columns = ["Position", "Count"]

    # Bar chart for positions
    fig_position_bar = px.bar(
        position_counts,
        x="Position",
        y="Count",
        title="Email Count by Position",
        color="Position",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    st.plotly_chart(fig_position_bar)

    # Pie chart for positions
    fig_position_pie = px.pie(
        position_counts,
        names="Position",
        values="Count",
        title="Distribution of Emails by Position",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    st.plotly_chart(fig_position_pie)

    # Additional position-specific analysis
    status_order = ["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"]

    # Group data by position and count the statuses
    status_by_position = data.groupby("position")["status"].value_counts().unstack(fill_value=0)

    # Reorder the columns to match the desired order
    status_by_position = status_by_position.reindex(columns=status_order, fill_value=0)

    # Display the table
    st.write("The table below shows the breakdown of statuses for each position.")
    st.dataframe(status_by_position) 

@st.cache_data
def calculate_kpis_table(data: pd.DataFrame, status_order: List[str]) -> pd.DataFrame:
    """
    Calculate the KPIs (absolute counts) per position and return a DataFrame.
    """
    # Define KPI logic for the given statuses
    kpi_mapping = {
        "Email Sent": ["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"],
        "Email Opened": ["Email Opened", "Clicked Link", "Submitted Data"],
        "Clicked Link": ["Clicked Link", "Submitted Data"],
        "Submitted Data": ["Submitted Data"],
        "Email Reported": ["Email Reported"]
    }
    
    # Initialize an empty dictionary to store counts
    kpis_by_position = {}

    # Loop through each position
    for position, group in data.groupby("position"):
        kpis_by_position[position] = {}
        for status, related_statuses in kpi_mapping.items():
            # Count rows where the status matches the related statuses
            kpis_by_position[position][status] = len(group[group["status"].isin(related_statuses)])

    # Convert the dictionary to a DataFrame
    kpis_df = pd.DataFrame.from_dict(kpis_by_position, orient="index").reindex(columns=status_order, fill_value=0)

    # Calculate the KPIs table
    status_order = ["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"]
   
    # Display the table
    st.write("The table below shows the absolute KPIs for each position:")
    st.dataframe(kpis_df)

def main():
    st.image("mail.png", width=50)  # Displays the image (adjust the width if needed)
    st.title("Phishing Campaign Dashboard")  # Displays the title

    # Unpack all five returned values
    start_date, last_date, selected_positions, selected_campaigns, selected_statuses = display_sidebar(df)

    # Add one day to the last_date
    adjusted_last_date = last_date + pd.Timedelta(days=1)

    # Filter data with the adjusted last date
    filtered_data = df[(df['send_date'] >= start_date) & (df['send_date'] < adjusted_last_date)].copy()

    # Apply additional filters
    filtered_data = filter_data(filtered_data, 'position', selected_positions)
    filtered_data = filter_data(filtered_data, 'campaign_name', selected_campaigns)
    filtered_data = filter_data(filtered_data, 'status', selected_statuses)

    # Calculate KPIs and display metrics
    kpis = calculate_kpis_abs(filtered_data)
    kpi_names = ["Sent Emails", "Opened Emails", "Clicked Links", "Submitted Data", "Reported Emails"]
    display_kpi_metrics(kpis, kpi_names)

    # Display charts
    display_charts(filtered_data)

    # Display position-specific analysis
    display_position_analysis(filtered_data)
    calculate_kpis_table(filtered_data, kpi_names)

# Data path
code_dir = os.path.dirname(os.path.realpath(__file__))  # Directory of the script
data_path = os.path.join(code_dir, "./results.csv")

df = load_data(data_path)
df['send_date'] = pd.to_datetime(df['send_date'])
df['modified_date'] = pd.to_datetime(df['modified_date'])

if __name__ == '__main__':
    main()