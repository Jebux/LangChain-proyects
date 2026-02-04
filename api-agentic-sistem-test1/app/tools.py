from langchain.tools import tool
from typing import Optional
import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

# Scopes required for Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def get_calendar_service():
    """Authenticates and returns the Google Calendar service resource."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists(CREDENTIALS_FILE):
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            else:
                print("Warning: credentials.json not found. Calendar functionality will not work.")
                return None
    
    service = build('calendar', 'v3', credentials=creds)
    return service

@tool
def schedule_event(summary: str, start_datetime: str, end_datetime: str, description: Optional[str] = ""):
    """
    Schedules an event on Google Calendar.
    Args:
        summary: Title of the event.
        start_datetime: Start time in ISO 8601 format (e.g., '2023-10-27T09:00:00-07:00').
        end_datetime: End time in ISO 8601 format (e.g., '2023-10-27T10:00:00-07:00').
        description: Description of the event (optional).
    """
    service = get_calendar_service()
    if not service:
        return "Error: Google Calendar credentials not configured. Please ensure credentials.json is present."

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'UTC', # Or flexible timezone
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'UTC',
        },
    }

    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event_result.get('htmlLink')}"
    except Exception as e:
        return f"Failed to create event: {str(e)}"
