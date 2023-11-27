import os
import requests
import json
from utils.convert_utc_to_manila import convert_utc_to_manila
from datetime import datetime, timedelta

def get_events_for_week():
    """
    Retrieves the user's calendar events for the next 7 days.

    Returns:
        list of dict: A list of events with details in JSON format. 

    Sample Output:
        [
            {
                "Event Number": "1",
                "Subject": "HR Alignment Meeting",
                "Importance": "normal",
                "Organizer": "John Doe",
                "Start": "2023-11-28 10:30:00 AM",
                "End": "2023-11-28 11:30:00 AM",
                "Location": "Microsoft Teams Meeting",
                "Response": "accepted"
            },
            ... # Additional events
        ]
    """
    access_token = os.getenv("MSGRAPH_ACCESS_TOKEN")
    if not access_token:
        return json.dumps({'error': 'Access token not found'})

    now = datetime.now()
    end_date = now + timedelta(days=7)

    start_datetime = now.isoformat()
    end_datetime = end_date.isoformat()

    url = f"https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={start_datetime}&enddatetime={end_datetime}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return json.dumps({'error': 'Failed to fetch events', 'status_code': response.status_code})

    cal_events_data = response.json().get('value', [])
    events_json = []

    # for event in [cal_events_data[1], cal_events_data[2], cal_events_data[4]]: # display only non-confi events
    for event in cal_events_data[:5]: # limit to 5 events
        organizer = event.get('organizer', {}).get('emailAddress', {})
        location = event.get('location', {})
        response_status = event.get('responseStatus', {})

        event_details = {
            "Event Number": str(cal_events_data.index(event) + 1),
            "Subject": event.get('subject', 'No Subject'),
            "Importance": event.get('importance', 'Normal'),
            "Organizer": organizer.get('name', 'Unknown Organizer'),
            "Start": convert_utc_to_manila(event['start']['dateTime']),
            "End": convert_utc_to_manila(event['end']['dateTime']),
            "Location": location.get('displayName', 'No Location'),
            "Response": response_status.get('response', 'Unknown')
        }
        events_json.append(event_details)

    return json.dumps(events_json, indent=4)