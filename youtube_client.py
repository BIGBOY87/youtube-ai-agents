
import os, requests
class YouTubeClient:
    def __init__(self):
        self.api_key=os.getenv("YOUTUBE_API_KEY","")
        self.base="https://www.googleapis.com/youtube/v3"
    def _get(self,path,params):
        if not self.api_key: raise RuntimeError("Missing YOUTUBE_API_KEY")
        params=dict(params); params["key"]=self.api_key
        r=requests.get(self.base+path,params=params,timeout=20); r.raise_for_status(); return r.json()
    def videos_by_ids(self,ids):
        if isinstance(ids,str): ids=[ids]
        return self._get("/videos",{"part":"snippet,statistics,contentDetails,status","id":",".join(ids)}).get("items",[])
