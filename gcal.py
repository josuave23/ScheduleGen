from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def getService():
    creds = None

    # token.json stores the user's credentials after first login
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # if no valid credentials, prompt login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

#Check this one, might be reason for not viewing events far enough ahead
def getEvents(service, daysAhead):
    now = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(days=daysAhead)).isoformat() + "Z"

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        timeMax=end,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = []
    for e in result.get("items", []):
        start = e["start"].get("dateTime")
        end   = e["end"].get("dateTime")
        if start and end:  # skip all-day events for now
            events.append({
                "start": datetime.fromisoformat(start).replace(tzinfo=None),
                "end":   datetime.fromisoformat(end).replace(tzinfo=None),
                "title": e.get("summary", "Busy")
            })
    return events

#This might be the problem with pushing: Start = slot[0] might have to be start = timeline[0]
def pushEvents(service, timeline):
    already_pushed = set()

    for slot in timeline:
        if slot[2] is not None and slot[2].n not in already_pushed:
            start = slot[0]
            end   = start + timedelta(minutes=slot[2].duration)

            event = {
                "summary": slot[2].n,
                "start":   {"dateTime": start.isoformat(), "timeZone": "America/Los_Angeles"},
                "end":     {"dateTime": end.isoformat(),   "timeZone": "America/Los_Angeles"},
            }

            service.events().insert(calendarId="primary", body=event).execute()
            already_pushed.add(slot[2].n)