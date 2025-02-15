from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
import json

CREDENTIALS_FILE = "credentials.json"

# Load credentials from file
with open(CREDENTIALS_FILE, "r") as token_file:
    creds_data = json.load(token_file)
    credentials = Credentials.from_authorized_user_info(creds_data)

# Build the Google Calendar API service
service = build("calendar", "v3", credentials=credentials)


def get_meetings_for_date(date_str):
    """
    Fetches all meetings (events with attendees) for a given date.

    :param date_str: Date in "YYYY-MM-DD" format
    """
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    start_time = date.strftime("%Y-%m-%dT00:00:00Z")  # Start of the day
    end_time = date.strftime("%Y-%m-%dT23:59:59Z")  # End of the day

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    # Filter only meetings (events with attendees)
    meetings = [event for event in events if "attendees" in event]

    if not meetings:
        print(f"No meetings found on {date_str}")
        return

    print(f"Meetings on {date_str}:")
    for meeting in meetings:
        start = meeting["start"].get("dateTime", meeting["start"].get("date"))
        attendees = ", ".join([a["email"] for a in meeting.get("attendees", [])])
        print(f"- {meeting['summary']} at {start} with {attendees}")


# Example Usage: Get meetings for a specific date
date_to_check = "2025-02-15"  # Change this to your desired date
get_meetings_for_date(date_to_check)
