import pandas as pd
from typing import List

def calculate_kpis_abs(data: pd.DataFrame) -> List[float]:
    total_sent = len(data[data["status"].isin(["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"])])
    opened_emails = len(data[data["status"].isin(["Email Opened", "Clicked Link", "Submitted Data"])])
    clicked_links = len(data[data["status"].isin(["Clicked Link", "Submitted Data"])])
    submitted_data = len(data[data["status"] == "Submitted Data"])
    reported_emails = len(data[data["status"] == "Email Reported"])
    return [total_sent, opened_emails, clicked_links, submitted_data, reported_emails]

def calculate_kpis_rel(data: pd.DataFrame) -> List[float]:
    total_sent = len(data[data["status"].isin(["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"])])
    if total_sent == 0:
        return [0, 0, 0, 0, 0]
    opened_emails = len(data[data["status"].isin(["Email Opened", "Clicked Link", "Submitted Data"])])
    clicked_links = len(data[data["status"].isin(["Clicked Link", "Submitted Data"])])
    submitted_data = len(data[data["status"] == "Submitted Data"])
    reported_emails = len(data[data["status"] == "Email Reported"])
    return [
        100,  # 100% sent
        round((opened_emails / total_sent) * 100, 2),
        round((clicked_links / total_sent) * 100, 2),
        round((submitted_data / total_sent) * 100, 2),
        round((reported_emails / total_sent) * 100, 2)
    ]