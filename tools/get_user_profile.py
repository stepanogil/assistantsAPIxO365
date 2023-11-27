import os
from dotenv import load_dotenv

load_dotenv()

# MS Graph env
access_token = os.getenv("MSGRAPH_ACCESS_TOKEN")
client_id = os.getenv("MSGRAPH_CLIENT_ID")
tenant_id = os.getenv("MSGRAPH_TENANT_ID")
scopes = os.getenv("MSGRAPH_SCOPES")


import requests
import json


def get_user_profile():
    """
    Get user profile from Microsoft Graph.
    
    Returns:
        dict: A dictionary containing user profile details.
    
    Sample Output:
        {
            "Name": "John Doe",
            "Location": "Manila"
        }
    
    """
    access_token = os.getenv("MSGRAPH_ACCESS_TOKEN")
    if not access_token:
        return json.dumps({'error': 'Access token not found'})

    url = "https://graph.microsoft.com/v1.0/me"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return json.dumps({'error': 'Failed to fetch user profile', 'status_code': response.status_code})

    user_data = response.json()
    profile_data = {
        "Name": user_data.get('displayName', 'No Name'),
        "Position": user_data.get('jobTitle', 'No Position'),
        "Location": user_data.get('officeLocation', 'No Location')
    }

    return json.dumps(profile_data, indent=4)

