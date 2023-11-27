import requests
import json
import os

def reply_to_email(subject, body, recipient):
    """
    Sends a reply to an email using the Microsoft Graph API.
    
    :param subject: The subject of the email.
    :param body: The body of the email.
    :param recipient: The recipient of the email.
    
    Example:
    subject = "RE: Hello"
    body = "Hello World!"
    recipient = "john.doe@email.com"

    Returns:
        dict: A dictionary containing the status of the reply.

    Sample Output:
        {
            "message": "Reply sent successfully!",
            "status_code": 202
        }

    """   
    
    access_token = os.getenv("MSGRAPH_ACCESS_TOKEN")
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers = {'Authorization': f'Bearer {access_token}'}
    body = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "Text",
                        "content": body
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": recipient
                            }
                        }
                    ]
                }
            }


    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 202:
        return json.dumps({'error': 'Failed to send reply', 'status_code': response.status_code})
    
    return json.dumps({'message': 'Reply sent successfully!', 'status_code': response.status_code, }) 