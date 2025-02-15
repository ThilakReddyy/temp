from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

CREDENTIALS_FILE = "credentials1.json"

# Load credentials from file
with open(CREDENTIALS_FILE, "r") as token_file:
    creds_data = json.load(token_file)
    credentials = Credentials.from_authorized_user_info(creds_data)

# Build the Google Calendar API service
service = build("calendar", "v3", credentials=credentials)


def create_meeting(
    summary, start_time, end_time, attendees_emails, location=None, description=None
):
    """
    Creates a meeting in Google Calendar.

    :param summary: Meeting title
    :param start_time: Start time in 'YYYY-MM-DDTHH:MM:SS' format (UTC)
    :param end_time: End time in 'YYYY-MM-DDTHH:MM:SS' format (UTC)
    :param attendees_emails: List of emails of attendees
    :param location: Meeting location (optional)
    :param description: Meeting description (optional)
    """
    event = {
        "summary": summary,
        "location": location,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
        "attendees": [{"email": email} for email in attendees_emails],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 30},  # Email reminder before 30 minutes
                {"method": "popup", "minutes": 10},  # Popup reminder before 10 minutes
            ],
        },
    }

    event_result = service.events().insert(calendarId="primary", body=event).execute()
    print(event_result)

    print(f"Meeting '{summary}' created successfully!")
    print("Meeting Link:", event_result.get("htmlLink"))


# Example Usage: Creating a Meeting
create_meeting(
    summary="Project Discussion",
    start_time="2025-02-15T10:00:00Z",  # Change to your date-time
    end_time="2025-02-15T11:00:00Z",  # Change to your date-time
    attendees_emails=["alice@example.com", "bob@example.com"],
    location="Google Meet",
    description="Discussing project updates and next steps.",
)
