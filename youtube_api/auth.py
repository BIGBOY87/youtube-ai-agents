from __future__ import annotations

from pathlib import Path
from typing import Sequence

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

ROOT = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = ROOT / "client_secret.json"
TOKEN_FILE = ROOT / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


def get_credentials(scopes: Sequence[str] | None = None) -> Credentials:
    requested_scopes = list(scopes or SCOPES)
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), requested_scopes)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not CLIENT_SECRET_FILE.exists():
            raise FileNotFoundError(
                f"Missing {CLIENT_SECRET_FILE}. Download OAuth Desktop client JSON from Google Cloud "
                "and save it as client_secret.json in the project root."
            )
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), requested_scopes)
        creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return creds
