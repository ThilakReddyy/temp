from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
import json
from savetojson import save_to_json

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_emails(query):
    creds = Credentials.from_authorized_user_file("credentials1.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", q=query).execute()

    messages = results.get("messages", [])
    mails = []

    if not messages:
        print("No new emails found.")
        return

    for msg in messages:
        msg_id = msg["id"]
        email = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="full")
            .execute()
        )

        headers = email["payload"]["headers"]
        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
        )
        sender = next(
            (h["value"] for h in headers if h["name"] == "From"), "Unknown Sender"
        )
        date = next(
            (h["value"] for h in headers if h["name"] == "Date"), "Unknown Date"
        )

        # Get Email Body
        body = ""
        if "parts" in email["payload"]:
            for part in email["payload"]["parts"]:
                if part["mimeType"] == "text/plain":  # Fetch plain text emails
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode(
                        "utf-8"
                    )
        mails.append({"sender": sender, "date": date, "subject": subject})

    save_to_json(mails, "emails.json")


if __name__ == "__main__":
    query = "after:2025/02/15"  # Change date format as needed
    today = "2025/02/14"

    query = f"is:unread category:primary after:{today}"

    get_emails(query)
