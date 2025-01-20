from gophish import Gophish
import json
import io
import csv
import pandas as pd
import streamlit as st

class GophishClient:
    """Handles connection to the Gophish API and data fetching."""
    def __init__(self, api_key: str, host: str = "https://127.0.0.1:3333"):   #TODO: Replace with our Gophish host
        self.client = Gophish(api_key, host=host, verify=False)

    def fetch_campaigns(self):
        """Fetch all campaigns from the Gophish API."""
        return self.client.campaigns.get()

    def fetch_campaign_details(self, campaign_id: int):
        """Fetch detailed data for a specific campaign."""
        return self.client.campaigns.get(campaign_id)


class CampaignDataProcessor:
    """Processes campaign data into CSV format."""
    def __init__(self, campaigns):
        self.campaigns = campaigns

    def process_campaigns(self):
        """Generate CSV strings for results and events."""
        results_buffer = io.StringIO()
        events_buffer = io.StringIO()
        results_writer = csv.writer(results_buffer)
        events_writer = csv.writer(events_buffer)

        # CSV Headers
        results_headers = [
            "campaign_id", "campaign_name", "template_id", "template_name", "status", "ip",
            "latitude", "longitude", "send_date", "reported", "modified_date", "email",
            "first_name", "last_name", "position"
        ]
        events_headers = [
            "campaign_id", "campaign_name", "template_id", "template_name", "email",
            "time", "message", "details"
        ]
        results_writer.writerow(results_headers)
        events_writer.writerow(events_headers)

        # Process campaigns
        for campaign in self.campaigns:
            self._process_single_campaign(campaign, results_writer, events_writer)

        return results_buffer.getvalue(), events_buffer.getvalue()

    def _process_single_campaign(self, campaign, results_writer, events_writer):
        """Process a single campaign's data."""
        campaign_id = campaign.id
        campaign_name = campaign.name
        template_id = campaign.template.id if campaign.template else None
        template_name = campaign.template.name if campaign.template else None

        # Get campaign details
        results = campaign.results
        events = campaign.timeline

        # Process events
        send_dates = {e.email: e.time for e in events if e.message == "Email Sent"}
        reported_statuses = {e.email: True for e in events if e.message == "Email Reported"}

        # Write results
        for result in results:
            modified_date = max(
                (e.time for e in events if e.email == result.email), default=None
            )
            send_date = send_dates.get(result.email)
            reported = reported_statuses.get(result.email, False)
            results_writer.writerow([
                campaign_id, campaign_name, template_id, template_name,
                result.status, result.ip, result.latitude, result.longitude,
                send_date, reported, modified_date, result.email,
                result.first_name, result.last_name, result.position
            ])

        # Write events
        for event in events:
            events_writer.writerow([
                campaign_id, campaign_name, template_id, template_name,
                event.email, event.time, event.message, event.details
            ])


class CampaignApp:
    """Streamlit app for campaign data management."""
    def __init__(self, results_csv: str, events_csv: str):
        self.results_csv = results_csv
        self.events_csv = events_csv

    def run(self):
        """Run the Streamlit app."""
        # Provide CSV download options
        with st.expander("Export CSV"):
            st.download_button(
                label="Download Results CSV",
                data=self.results_csv,
                file_name="results.csv",
                mime="text/csv"
            )
            st.download_button(
                label="Download Events CSV",
                data=self.events_csv,
                file_name="events.csv",
                mime="text/csv"
            )

        # Load results CSV into a DataFrame and display
        results_df = pd.read_csv(io.StringIO(self.results_csv))
        st.write("Campaign Results Preview:")
        st.dataframe(results_df.head())


# Main Script
def main():
    # Load configuration
    with open("config.json") as file:
        config = json.load(file)

    # Load synthetic data
    with open("./generated_results/generated_results.csv", "r", encoding="utf-8") as file:
        synthetic_results_csv = file.read()
    with open("./generated_results/generated_events.csv", "r", encoding="utf-8") as file:
        synthetic_events_csv = file.read()
    
    # Add selection option for data source
    data_source = st.sidebar.radio(
        "Select Data Source",
        options=["Synthetic Data", "Real Data"],
        index=0
    )

    if data_source == "Real Data":
        # Initialize Gophish client and fetch campaigns
        client = GophishClient(api_key=config["GOPHISH_API_KEY"])
        campaigns = client.fetch_campaigns()

        # Process real campaign data
        processor = CampaignDataProcessor(campaigns)
        results_csv, events_csv = processor.process_campaigns()
    else:
        # Use synthetic data
        results_csv = synthetic_results_csv
        events_csv = synthetic_events_csv
    
    # Run the Streamlit app with the selected data
    app = CampaignApp(results_csv, events_csv)
    app.run()

if __name__ == "__main__":
    main()
