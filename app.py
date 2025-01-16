import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
from typing import List, Tuple

# Load data
code_dir = os.path.dirname(os.path.realpath(__file__))  # Directory of the script
data_path = os.path.join(code_dir, "./test_results.csv")

@st.cache_data
def load_data(data_path):
    """Load and cache data from CSV."""
    data = pd.read_csv(data_path)
    return data

df = load_data(data_path)

# Calculate metrics
total_sent = len(df)  # All rows are counted
opened_emails = len(df[df["status"].isin(["Email Opened", "Clicked Link", "Submitted Data"])])
clicked_links = len(df[df["status"].isin(["Clicked Link", "Submitted Data"])])
submitted_data = len(df[df["status"] == "Submitted Data"])
reported_emails = len(df[df["status"] == "Email Reported"])

# Calculate percentages (relative to total_sent)
sent_percentage = (total_sent / total_sent) * 100 if total_sent > 0 else 0
opened_percentage = (opened_emails / total_sent) * 100 if total_sent > 0 else 0
clicked_percentage = (clicked_links / total_sent) * 100 if total_sent > 0 else 0
submitted_percentage = (submitted_data / total_sent) * 100 if total_sent > 0 else 0
reported_percentage = (reported_emails / total_sent) * 100 if total_sent > 0 else 0

# Centered title
st.markdown(
    """
    <div style="text-align: center;">
        <h2>Visualizing the Results of a Phishing Campaign</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

st.header("Summary Metrics")
st.write(f"**Total Sent Emails:** {total_sent} ({sent_percentage:.2f}%)")
st.write(f"**Opened Emails:** {opened_emails} ({opened_percentage:.2f}%)")
st.write(f"**Clicked Links:** {clicked_links} ({clicked_percentage:.2f}%)")
st.write(f"**Submitted Data:** {submitted_data} ({submitted_percentage:.2f}%)")
st.write(f"**Reported Emails:** {reported_emails} ({reported_percentage:.2f}%)")

# Prepare the data for the funnel chart
funnel_data = {
    "Status": [
        "Sent Emails",
        "Opened Emails",
        "Clicked Links",
        "Submitted Data",
        "Reported Emails"
    ],
    "Count": [
        total_sent,
        opened_emails,
        clicked_links,
        submitted_data,
        reported_emails
    ],
    "Percentage": [
        sent_percentage,
        opened_percentage,
        clicked_percentage,
        submitted_percentage,
        reported_percentage
    ]
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