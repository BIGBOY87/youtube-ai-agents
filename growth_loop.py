
def _int(v):
    try: return int(v)
    except Exception: return 0
def analyze_video_performance(video):
    s=video.get("snippet",{}); st=video.get("statistics",{}); status=video.get("status",{})
    views=_int(st.get("viewCount")); likes=_int(st.get("likeCount")); comments=_int(st.get("commentCount"))
    title=s.get("title","Untitled")
    actions=[]
    if views<50:
        actions.append({"priority":"high","type":"create_short","reason":"Low views. Create Shorts from this source MP4.","recommended_cut":{"start":30,"duration":20}})
        actions.append({"priority":"medium","type":"seo_refresh","reason":"Low discovery. Test stronger title/description."})
    elif views<500:
        actions.append({"priority":"medium","type":"create_short","reason":"Moderate reach. Create one Short.","recommended_cut":{"start":45,"duration":18}})
    else:
        actions.append({"priority":"scale","type":"scale_format","reason":"This format has traction."})
    return {"video_id":video.get("id"),"title":title,"views":views,"likes":likes,"comments":comments,"privacy_status":status.get("privacyStatus"),"recommended_actions":actions}
