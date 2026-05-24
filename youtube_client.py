import os, requests
class YoutubeClient:
    def __init__(self):
        self.key=os.getenv('YOUTUBE_API_KEY','')
        self.channel_id=os.getenv('YOUTUBE_CHANNEL_ID','')
        self.base='https://www.googleapis.com/youtube/v3'
    def _get(self,path,params):
        params=dict(params); params['key']=self.key
        r=requests.get(self.base+path,params=params,timeout=20)
        r.raise_for_status(); return r.json()
    def channel(self,channel_id=None):
        cid=channel_id or self.channel_id
        data=self._get('/channels',{'part':'snippet,statistics,brandingSettings,contentDetails','id':cid})
        return data.get('items',[{}])[0]
    def recent_videos(self,max_results=10,channel_id=None):
        cid=channel_id or self.channel_id
        search=self._get('/search',{'part':'snippet','channelId':cid,'order':'date','maxResults':max_results,'type':'video'})
        ids=','.join([x['id']['videoId'] for x in search.get('items',[]) if x.get('id',{}).get('videoId')])
        if not ids: return []
        vids=self._get('/videos',{'part':'snippet,statistics,contentDetails','id':ids})
        return vids.get('items',[])
