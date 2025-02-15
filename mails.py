from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
import json
from email.mime.text import MIMEText


import base64


def get_emails(query):
    query = f"is:unread category:primary after:2025/02/14"
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    print(query)
    creds = Credentials.from_authorized_user_file("credentials.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", q=query).execute()

    messages = results.get("messages", [])
    mails = []

    if not messages:
        print("No new emails found.")
        return "No new emails found"
    print(messages)

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

    return mails


def create_message(to, subject, body):
    """Create a MIME message for sending an email."""
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_email(subject, body, to):
    creds = Credentials.from_authorized_user_file("credentials.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    email_message = create_message(subject, body, to)

    try:
        send_result = (
            service.users().messages().send(userId="me", body=email_message).execute()
        )
        print(f"✅ Email sent successfully! Message ID: {send_result['id']}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
