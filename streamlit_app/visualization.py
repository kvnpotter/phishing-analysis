import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List
from .kpi_calculations import calculate_kpis_abs, calculate_kpis_rel

def display_kpi_and_funnel(data: pd.DataFrame, kpis: List[float], kpi_names: List[str]):
    """
    Displays KPI metrics in the left column (1-column wide)
    and the funnel chart in the right column (4-columns wide).
    """
    # Insert whitespace
    st.write("")

    st.header("KPI Metrics")
    st.write("")

    # Create layout with 2 columns (1:4 ratio)
    col1, col2, col3 = st.columns([1, 0.5, 4])

    # KPI Metrics in the left column
    with col1:
        st.markdown(
            """
            <style>
            .kpi-card {
                background-color: rgba(90, 210, 170, 0.2);
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 1px;
                margin-bottom: 1px;
                text-align: center;
                box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
            }
            .kpi-card h1 {
                font-size: 1.2rem;
                margin: 0;
                color: #333;
            }
            .kpi-card p {
                font-size: 1.2rem;
                font-weight: bold;
                margin: 0;
                color: #555;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Render each KPI as a card
        for kpi_name, kpi_value in zip(kpi_names, kpis):
            st.markdown(
                f"""
                <div class="kpi-card">
                    <h1>{kpi_value}</h1>
                    <p>{kpi_name}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Funnel Chart in the right column
    with col3:
        # Calculate KPIs for funnel chart
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

        # Create a DataFrame and sort by 'Percentage' in descending order
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
            color_discrete_sequence=px.colors.sequential.Darkmint,
            height=500
        )

        # Remove the legend and adjust the layout
        fig_funnel.update_layout(
            showlegend=False,  # Remove the legend
            title={
                "text": "Phishing Campaign Funnel Chart",  # Title text
                "x": 0.5,  # Center the title (horizontal alignment)
                "xanchor": "center",  # Anchor the title to the center
                "yanchor": "top"  # Anchor the title to the top
            },
            font=dict(
                size=16,  # General font size for the chart
                family="Arial, sans-serif"  # Optional: Set font family
            ),
            xaxis=dict(
                title=dict(font=dict(size=16)),  # Font size for x-axis title
                tickfont=dict(size=12)  # Font size for x-axis ticks
            ),
            yaxis=dict(
                title=dict(font=dict(size=16)),  # Font size for y-axis title
                tickfont=dict(size=12)  # Font size for y-axis ticks
            )
        )
        
        # Add percentage sign to the labels
        fig_funnel.update_traces(
            texttemplate="%{x}%",  # Add '%' to the data labels
            textposition="inside",  # Place labels inside the funnel sections
            textfont=dict(
                size=16,  # Increase font size for data labels
                color="black"  # Optional: Change label color
            )
        )

        # Display the funnel chart
        st.plotly_chart(fig_funnel, use_container_width=True)

    # Insert whitespace
    st.write("")
    st.write("")

    # Insert a line break for better spacing
    st.divider()

def display_position_analysis(data: pd.DataFrame):
    """
    Display analysis of phishing campaign data by position.
    Includes bar charts and pie charts for position-based insights.
    """
    # Insert whitespace
    st.write("")

    st.header("Position Analysis")

    # Insert whitespace
    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    # Group data by position and calculate metrics
    position_counts = data["position_group"].value_counts().reset_index()
    position_counts.columns = ["Position", "Count"]

    # Bar chart for positions
    with col1:
        fig_position_bar = px.bar(
            position_counts,
            x="Position",
            y="Count",
            title="Email Count by Job Field",
            color="Position",
            color_discrete_sequence=px.colors.sequential.Bluyl[-5:],
            height=450
        )
        # Update layout to remove the legend and center the title
        fig_position_bar.update_layout(
            showlegend=False,  # Remove the legend
            title={
                "text": "Email Count by Job Field",  # Title text
                "x": 0.5,  # Center the title (horizontal alignment)
                "xanchor": "center",  # Anchor the title to the center
                "yanchor": "top"  # Anchor the title to the top
            }
        )
        st.plotly_chart(fig_position_bar, use_container_width=True)

    # Pie chart for positions
    with col2:
        fig_position_pie = px.pie(
            position_counts,
            names="Position",
            values="Count",
            title="Distribution of Emails by Job Field",
            color_discrete_sequence=px.colors.sequential.Bluyl[-6:],
            height=400
        )
        # Update layout to remove the legend and center the title
        fig_position_pie.update_layout(
            showlegend=False,  # Remove the legend
            title={
                "text": "Distribution of Emails by Job Field",  # Title text
                "x": 0.5,  # Center the title (horizontal alignment)
                "xanchor": "center",  # Anchor the title to the center
                "yanchor": "top"  # Anchor the title to the top
            }
        )
        # Add data labels to display the count and percentage
        fig_position_pie.update_traces(
            textinfo="label+percent",  # Add both label and percentage
            textposition="outside",  # Place the labels inside the pie slices
            hoverinfo="label+value+percent"  # Display value, label, and percentage on hover
        )
        st.plotly_chart(fig_position_pie, use_container_width=True)

def calculate_kpis_table(data: pd.DataFrame, status_order: List[str]):
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
    for position, group in data.groupby("position_group"):
        kpis_by_position[position] = {}
        for status, related_statuses in kpi_mapping.items():
            # Count rows where the status matches the related statuses
            kpis_by_position[position][status] = len(group[group["status"].isin(related_statuses)])

        # Add count of reported emails
        kpis_by_position[position]["Email Reported"] = len(group[group["reported"] == True])    

    # Convert the dictionary to a DataFrame
    kpis_df = pd.DataFrame.from_dict(kpis_by_position, orient="index").reindex(columns=status_order, fill_value=0)
    
    # Sort the DataFrame by "Emails Sent" column in descending order
    kpis_df = kpis_df.sort_values(by="Email Sent", ascending=False)

    # Convert DataFrame to HTML with centered alignment
    kpis_df_html = kpis_df.style.set_table_styles(
        [
            {"selector": "th", "props": [("text-align", "left"), ("font-weight", "bold")]},
            {"selector": "td", "props": [("text-align", "center")]}
        ]
    ).to_html()

    # Clean up trailing whitespace
    kpis_df_html = kpis_df_html.strip()

    # Insert whitespace
    for i in range(4):
        st.write("")

    # Display the table
    st.write("")

    # Display the table
    st.markdown(
         f"""
        <div style="text-align: left; padding: 10px;">
            <h5 style="margin-bottom: 40px;">Absolute KPIs per Professional Field</h5>
            <div style="display: flex; justify-content: left; overflow-x: auto;">
                {kpis_df_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")

def display_reported_analysis(data: pd.DataFrame):
    """
    Display analysis of phishing campaign data by reporting.
    Includes bar charts for reported-based insights.
    """
    # Insert whitespace
    st.write("")
    st.title("Reported Emails by Status")
    st.write("")
    st.write("")

    # Define the desired order of statuses
    desired_order = ["Email Sent", "Email Opened", "Clicked Link", "Submitted Data"]

    # Calculate percentages of True and False for each status
    status_counts = data.groupby("status")["reported"].value_counts(normalize=True).unstack(fill_value=0)
    absolute_counts = data.groupby("status")["reported"].value_counts().unstack(fill_value=0)
    status_counts.columns = ["Not Reported", "Reported"]
    absolute_counts.columns = ["Not Reported", "Reported"]
    status_counts = status_counts * 100  # Convert to percentages

    # Reorder the data according to the desired order
    status_counts = status_counts.reindex(desired_order)
    absolute_counts = absolute_counts.reindex(desired_order)

    # Create a stacked bar chart using Plotly
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=status_counts.index,
            y=status_counts["Not Reported"],
            name="Not Reported",
            marker_color="#98DBC6",
        )
    )
    fig.add_trace(
        go.Bar(
            x=status_counts.index,
            y=status_counts["Reported"],
            name="Reported",
            marker_color="#028482",
        )
    )

    # Add annotations for absolute values
    for idx, status in enumerate(status_counts.index):
        # Not Reported
        fig.add_annotation(
            x=status,
            y=status_counts["Not Reported"][idx] / 2,
            text=f"{absolute_counts['Not Reported'][idx]}",
            showarrow=False,
            font=dict(color="black", size=16),
        )
        # Reported
        fig.add_annotation(
            x=status,
            y=status_counts["Not Reported"][idx] + (status_counts["Reported"][idx] / 2),
            text=f"{absolute_counts['Reported'][idx]}",
            showarrow=False,
            font=dict(color="black", size=16),
        )

    # Update layout for the stacked bar chart
    fig.update_layout(
        barmode="stack",
        title="Reported vs Not Reported Emails by Status",
        xaxis_title="Status",
        yaxis_title="Percentage (%)",
        legend_title="Reported Status",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)