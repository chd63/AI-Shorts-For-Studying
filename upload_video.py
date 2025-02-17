import os
import google.auth
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None
    creds = Credentials.from_service_account_file(
        "service-account.json", scopes=SCOPES)

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)


def upload_video(file_path, title, description, tags, category_id="22", privacy_status="public", is_short=False):
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    if is_short:
        body["snippet"]["tags"].append("#Shorts")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    response = request.execute()

    print(f"Video uploaded! Video ID: {response['id']}")


