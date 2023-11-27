import os
import requests
import json
from utils.convert_utc_to_manila import convert_utc_to_manila

def get_emails_with_specific_content_from_sender(search_term, sender):
    """
    Retrieves emails with specific content from a specific sender and returns them as JSON.
    
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
    url = f"https://graph.microsoft.com/v1.0/me/messages?$search=\"{search_term}\""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        emails = response.json().get('value', [])
        emails_json = []
        count = 0

        for email in emails:
            if email.get('sender', {}).get('emailAddress', {}).get('name') == sender:
                if count < 5:  # Limit to first 5 matching emails
                    email_details = {
                        "Email Number": str(emails.index(email) + 1),
                        "Subject": email.get('subject', 'No Subject'),
                        "Sender": email.get('sender', {}).get('emailAddress', {}).get('name', 'Unknown Sender'),
                        "Sender Email": email.get('sender', {}).get('emailAddress', {}).get('address', 'Unknown Sender Email'),
                        "Importance": email.get('importance', 'Normal'),
                        "Sent Date": convert_utc_to_manila(email.get('sentDateTime', 'Unknown Date')),
                        "Message Preview": email.get('bodyPreview', 'No Preview Available')
                    }
                    emails_json.append(email_details)
                    count += 1
                else:
                    break

        return json.dumps(emails_json, indent=4)
    else:
        return json.dumps({'error': f"Error fetching emails: {response.status_code}, {response.text}"})