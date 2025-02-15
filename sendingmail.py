from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
import json
from email.mime.text import MIMEText


def create_message(to, subject, body):
    """Create a MIME message for sending an email."""
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_email():
    creds = Credentials.from_authorized_user_file("credentials1.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    to_email = "sharanhitam@gmail.com"  # Change to recipient's email
    subject = "Hello from Gmail API"
    body = "This is a test email sent using Python and the Gmail API."

    email_message = create_message(to_email, subject, body)

    try:
        send_result = (
            service.users().messages().send(userId="me", body=email_message).execute()
        )
        print(f"✅ Email sent successfully! Message ID: {send_result['id']}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")


if __name__ == "__main__":
    send_email()
