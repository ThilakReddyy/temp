from google_auth_oauthlib.flow import Flow
import json

CREDENTIALS_FILE = "credentials.json"

# Load credentials from file
with open(CREDENTIALS_FILE, "r") as token_file:
    creds_data = json.load(token_file)

CLIENT_ID = creds_data["installed"]["client_id"]
CLIENT_SECRET = creds_data["installed"]["client_secret"]
REDIRECT_URI = "http://localhost"
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.app.created",
    "https://www.googleapis.com/auth/calendar.events.owned",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

CREDENTIALS_FILE = "credentials1.json"  # File to store tokens
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uris": [REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },
    scopes=SCOPES,
)

flow.redirect_uri = REDIRECT_URI

# Generate auth URL with access_type="offline" to get a refresh token
auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")


print("Authorize this app by visiting this URL:", auth_url)
auth_code = input("Enter the authorization code: ")

flow.fetch_token(code=auth_code)
credentials = flow.credentials

with open(CREDENTIALS_FILE, "w") as token_file:
    token_file.write(credentials.to_json())

print(credentials.token)

# AIzaSyDru1qtay6NSMmVoivDHcQzcmX3JG3aIuU
