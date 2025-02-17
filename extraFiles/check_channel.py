import google_auth_oauthlib.flow
import googleapiclient.discovery

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES
    )
    credentials = flow.run_local_server(port=0, open_browser=False)  # Prevents the browser error
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)


def get_channel_info():
    youtube = get_authenticated_service()
    
    request = youtube.channels().list(
        part="snippet",
        mine=True  # Get info for the authenticated user
    )
    response = request.execute()

    if "items" in response and len(response["items"]) > 0:
        channel = response["items"][0]
        print(f"Channel Name: {channel['snippet']['title']}")
        print(f"Channel ID: {channel['id']}")
        print(f"Channel Description: {channel['snippet']['description']}")
    else:
        print("No YouTube channel linked to this account.")

if __name__ == "__main__":
    get_channel_info()
