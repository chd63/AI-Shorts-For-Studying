import os
import json
import google.auth
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload  # Correct import
import google_auth_oauthlib.flow

# SCOPES required to upload videos to YouTube
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Path to your saved refresh token and client secret JSON
TOKEN_FILE = 'token.json'
CLIENT_SECRETS_FILE = 'client_secret.json'


def get_credentials():
    """Get credentials using a refresh token."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token:
            creds_data = json.load(token)

            # Load client_id and client_secret from the client_secret.json file
            with open(CLIENT_SECRETS_FILE, 'r') as f:
                client_data = json.load(f)
                
                # Check if the structure contains 'installed' or 'web'
                if 'installed' in client_data:
                    client_id = client_data['installed']['client_id']
                    client_secret = client_data['installed']['client_secret']
                elif 'web' in client_data:
                    client_id = client_data['web']['client_id']
                    client_secret = client_data['web']['client_secret']
                else:
                    raise ValueError("Invalid client_secret.json structure. Neither 'installed' nor 'web' found.")

            creds = Credentials(
                None,
                refresh_token=creds_data.get('refresh_token'),
                client_id=client_id,  # Use the client ID from the file
                client_secret=client_secret,  # Use the client secret from the file
                token_uri="https://oauth2.googleapis.com/token"
            )

    if creds and creds.expired and creds.refresh_token:
        print("Refreshing credentials...")  # Debugging print
        creds.refresh(Request())
        with open(TOKEN_FILE, 'w') as token:
            json.dump({"refresh_token": creds.refresh_token}, token)
        print("Credentials refreshed.")  # Debugging print

    return creds


def upload_video(file_path, title, description, tags, category_id="22", privacy_status="public", is_short=False):
    """Upload a video to YouTube with optional Shorts tagging."""
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        },
        "madeForKids": False
    }

    # If this is a YouTube Short, add the hashtag to the tags
    if is_short:
        body["snippet"]["tags"].append("#Shorts")

    # Make the video upload request
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    response = request.execute()

    print(f"Video uploaded successfully! Video ID: {response['id']}")
    return response['id']


if __name__ == "__main__":
    upload_video(
        file_path="final_output.mp4",
        title="My YouTube Video",
        description="This is a description of my YouTube video",
        tags=["python", "YouTube API", "Automation"],
        is_short=True  # Set to True if you want to upload as a YouTube Short
    )
