
import os, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES=[
 "https://www.googleapis.com/auth/youtube.upload",
 "https://www.googleapis.com/auth/youtube.force-ssl",
 "https://www.googleapis.com/auth/youtube.readonly",
 "https://www.googleapis.com/auth/yt-analytics.readonly",
]

def _creds():
    raw=os.getenv("YOUTUBE_TOKEN_JSON","").strip()
    if raw: return Credentials.from_authorized_user_info(json.loads(raw),SCOPES)
    if os.path.exists("token.json"): return Credentials.from_authorized_user_file("token.json",SCOPES)
    raise RuntimeError("Missing OAuth token")

def upload_video(video_file,title,description,tags=None,category_id="10",privacy_status="private",publish_at=None):
    if not os.path.exists(video_file): raise FileNotFoundError(video_file)
    if privacy_status not in {"private","unlisted","public"}: privacy_status="private"
    body={"snippet":{"title":title[:100],"description":description[:5000],"tags":tags or [],"categoryId":category_id},
          "status":{"privacyStatus":privacy_status,"selfDeclaredMadeForKids":False}}
    if publish_at:
        body["status"]["publishAt"]=publish_at
        body["status"]["privacyStatus"]="private"
    yt=build("youtube","v3",credentials=_creds())
    media=MediaFileUpload(video_file,chunksize=-1,resumable=True,mimetype="video/mp4")
    req=yt.videos().insert(part="snippet,status",body=body,media_body=media)
    resp=None
    while resp is None:
        _,resp=req.next_chunk()
    return {"status":"uploaded","video_id":resp.get("id"),"youtube_url":f"https://www.youtube.com/watch?v={resp.get('id')}","privacy_status":privacy_status}
