import os
import requests
import json
from utils.convert_utc_to_manila import convert_utc_to_manila

def get_flagged_emails():
    """
    Retrieves the user's flagged emails.

    Returns:
        list of dict: A list of flagged email details in JSON format.

    Sample Output:
        [
            {
                "Email Number": "1",
                "Subject": "RE: HR Alignment Meeting",
                "Sender": "John Doe",
                "Sender Email": "john.doe@email.com"
                "Importance": "normal",
                "Sent Date": "2018-07-13 05:11:23 PM",
                "Message Preview": "Hi Stephen ..."
            },
            ... # Additional emails
        ]
    """
    access_token = os.getenv("MSGRAPH_ACCESS_TOKEN")
    url = "https://graph.microsoft.com/v1.0/me/messages?$filter=flag/flagStatus eq 'flagged'"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return json.dumps({'error': 'Failed to fetch emails', 'status_code': response.status_code})

    flagged_emails_data = response.json().get('value', [])
    emails_json = []

    for email in flagged_emails_data[:5]: # limit to 5 emails
        email_details = {
            "Email Number": str(flagged_emails_data.index(email) + 1),
            "Subject": email.get('subject', 'No Subject'),
            "Sender": email.get('sender', {}).get('emailAddress', {}).get('name', 'Unknown Sender'),
            "Sender Email": email.get('sender', {}).get('emailAddress', {}).get('address', 'Unknown Sender Email'),
            "Importance": email.get('importance', 'Normal'),
            "Sent Date": convert_utc_to_manila(email.get('sentDateTime', 'Unknown Date')),
            "Message Preview": email.get('bodyPreview', 'No Preview Available')
        }
        emails_json.append(email_details)

    return json.dumps(emails_json, indent=4)