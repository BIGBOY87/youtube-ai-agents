import os, json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

if __name__ == "__main__":
    if not os.path.exists("client_secret.json"):
        raise SystemExit("Missing client_secret.json")
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
    with open("token.json", "w", encoding="utf-8") as f:
        json.dump({"token":creds.token,"refresh_token":creds.refresh_token,"token_uri":creds.token_uri,"client_id":creds.client_id,"client_secret":creds.client_secret,"scopes":creds.scopes}, f, indent=2)
    print("token.json created. Do not upload it to GitHub.")
