import os
import json
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

def _credentials():
    raw = os.getenv("YOUTUBE_TOKEN_JSON", "").strip()
    if raw:
        return Credentials.from_authorized_user_info(json.loads(raw), SCOPES)
    if os.path.exists("token.json"):
        return Credentials.from_authorized_user_file("token.json", SCOPES)
    raise RuntimeError("Missing OAuth token. Set YOUTUBE_TOKEN_JSON or create token.json.")

def _drive():
    return build("drive", "v3", credentials=_credentials())

def _folder_id():
    fid = os.getenv("DRIVE_SOURCE_FOLDER_ID", "").strip()
    if not fid:
        raise RuntimeError("Missing DRIVE_SOURCE_FOLDER_ID.")
    return fid

def direct_download_url(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def title_from_filename(name):
    name = re.sub(r"\.(mp4|mov|m4v|webm)$", "", name, flags=re.I)
    name = name.replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", name).strip()

def list_source_videos(max_results=100):
    fid = _folder_id()
    q = f"'{fid}' in parents and trashed=false and (mimeType contains 'video/' or name contains '.mp4' or name contains '.mov' or name contains '.m4v')"
    res = _drive().files().list(
        q=q,
        pageSize=max_results,
        fields="files(id,name,mimeType,size,createdTime,modifiedTime,webViewLink)"
    ).execute()

    out = []
    for f in res.get("files", []):
        out.append({
            "drive_file_id": f.get("id"),
            "name": f.get("name"),
            "title_guess": title_from_filename(f.get("name", "")),
            "mimeType": f.get("mimeType"),
            "size": f.get("size"),
            "createdTime": f.get("createdTime"),
            "modifiedTime": f.get("modifiedTime"),
            "webViewLink": f.get("webViewLink"),
            "source_mp4_url": direct_download_url(f.get("id")),
        })
    return out
