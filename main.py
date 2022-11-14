from googleapiclient.discovery import build

import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Can only retrieve 50 playlists with 50 videos per playlist
# To use application:
#   - must add email address for testing in Google developer console
#   - requires client_screts.json - downloaded from Google OAuth, this should be kept secret

def main():
    credentials = None

    # load credentials from previous successful logins
    if os.path.exists("token.pickle"):
        print("Loading Credentials From File...")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
    
    # no credentials or invalid
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request()) # refresh invalid token
        else:
            print("Fetching New Tokens...")
            scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes) # loading credentials

            flow.run_local_server(port=8080, promt="consent") # ask to consent with built in server host
            credentials = flow.credentials

            # save the credentials for the next run
            with open("token.pickle", "wb") as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)

    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.playlists().list(part="snippet,contentDetails", mine=True, maxResults=50) # maxResult default is 5, can be 0 to 50
    response = request.execute()

    # study / troubleshoot purposes
    # print("RESPONSE")
    # print(response)
    
    # for each playlist, retrieve title 
    for item in response["items"]:
        print("Playlist:", item["snippet"]["title"])

        # find videos from playlistId
        videoRequest = youtube.playlistItems().list(part="snippet,contentDetails", playlistId=item["id"], maxResults=50) # maxResult default is 5, can be 0 to 50
        videoResponse = videoRequest.execute()

        # study / troubleshoot purposes
        # print("VIDEORESPONSE")
        # print(videoResponse)

        # for each video
        for video in videoResponse["items"]:
            print(video["snippet"]["title"])

    youtube.close()

if __name__ == "__main__":
    main()
