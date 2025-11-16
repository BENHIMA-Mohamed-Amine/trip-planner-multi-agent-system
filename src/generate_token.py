from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Define the scopes you need
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def generate_token():
    creds = None

    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    print("token.json has been generated successfully!")

    # Test the connection
    service = build("calendar", "v3", credentials=creds)
    print("Testing connection...")
    calendars = service.calendarList().list().execute()
    print(f"Successfully connected! Found {len(calendars.get('items', []))} calendars.")


if __name__ == "__main__":
    generate_token()
