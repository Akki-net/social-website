import os
import pickle
import datetime
import googleapiclient.discovery
import google_auth_oauthlib.flow
import google.auth.transport.requests
def create_event(appointment=None):
    # Load your previously saved credentials (if available)
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token_file:
            creds = pickle.load(token_file)
    # If no valid credentials are found, authenticate the user
    if not creds or not creds.valid:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            os.path.join('client_secret.json'), SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token_file:
            pickle.dump(creds, token_file)
    # Create a service object for the Calendar API
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    # Define event details (start time, end time, summary, etc.)
    startdate = datetime.datetime.combine(appointment.date_of_appointment, appointment.start_time)
    enddate = datetime.datetime.combine(appointment.date_of_appointment, appointment.end_time)
    time_to_add = datetime.timedelta(hours=5, minutes=30)
    startdate += time_to_add
    enddate += time_to_add
    event = {
        'summary': f"An appointment is scheduled with Dr. {appointment.doctor_name.first_name} regarding {appointment.get_required_speciality_display}",
        'start': {'dateTime': startdate.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': enddate.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    # Insert the event into the user’s primary calendar
    event = service.events().insert(calendarId='primary', body=event).execute()
    # return event.get("htmlLink")