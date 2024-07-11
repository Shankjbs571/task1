import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def create_google_calendar_event(appointment):
  print("INSIDE CALENDAR FUCNTION")
  current_dir = os.path.dirname(os.path.abspath(__file__))
  json_path = os.path.join(current_dir, "token.json")
  creds = None
  if os.path.exists(json_path):
    print("TOKEN EXITS")
    creds = Credentials.from_authorized_user_file(json_path, SCOPES)
  else:
    print("token.json not found in current directory")

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Creating Appointment Event")
    
    # event = {
    #   'summary': 'Google I/O 2015',
    #   'location': '800 Howard St., San Francisco, CA 94103',
    #   'description': 'A chance to hear more about Google\'s developer products.',
    #   'start': {
    #     'dateTime': '2015-05-28T09:00:00-07:00',
    #     'timeZone': 'America/Los_Angeles',
    #     },
    #   'end': {
    #     'dateTime': '2015-05-28T17:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },
    #     'recurrence': [
    #         'RRULE:FREQ=DAILY;COUNT=2'
    #     ],
    #     'attendees': [
    #         {'email': 'lpage@example.com'},
    #         {'email': 'sbrin@example.com'},
    #     ],
    #     'reminders': {
    #         'useDefault': False,
    #         'overrides': [
    #         {'method': 'email', 'minutes': 24 * 60},
    #         {'method': 'popup', 'minutes': 10},
    #         ],
    #     },
    #     }
    event = {
        'summary': f'Appointment with Dr. {appointment.get('doctor').user.username}',
        'start': {
            'dateTime': f'{appointment.get('startdatetime')}',
            'timeZone': 'IST',
        },
        'end': {
            'dateTime': f'{appointment.get('enddatetime')}',
            'timeZone': 'IST',
        },
        'attendees': [
            {'email': appointment.get('patient').user.email},
            {'email': appointment.get('doctor').user.email},
        ],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: %s' % (event.get('htmlLink')))
    return event
  except HttpError as error:
    print(f"An error occurred: {error}")

