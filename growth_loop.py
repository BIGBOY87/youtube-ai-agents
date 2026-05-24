
import datetime

def _int(v):
    try:
        return int(v)
    except Exception:
        return 0

def analyze_video_performance(video):
    s = video.get("snippet", {})
    st = video.get("statistics", {})
    status = video.get("status", {})
    views = _int(st.get("viewCount"))
    likes = _int(st.get("likeCount"))
    comments = _int(st.get("commentCount"))
    title = s.get("title", "Untitled")
    video_id = video.get("id")

    actions = []

    if views < 50:
        actions.append({
            "priority": "high",
            "type": "create_short",
            "reason": "Low views. Create 2 Shorts from this source MP4 to create new entry points.",
            "recommended_cut": {"start": 30, "duration": 20},
        })
        actions.append({
            "priority": "medium",
            "type": "seo_refresh",
            "reason": "Low discovery. Test stronger title and hashtags.",
            "title_variant": f"{title[:70]} | Dark Tech House #BANGITUPMUSIC"
        })
    elif views < 500:
        actions.append({
            "priority": "medium",
            "type": "create_short",
            "reason": "Moderate reach. Create one Short and repost with stronger hook.",
            "recommended_cut": {"start": 45, "duration": 18},
        })
    else:
        actions.append({
            "priority": "scale",
            "type": "scale_format",
            "reason": "This format has traction. Create a similar follow-up upload.",
        })

    if likes == 0 and views > 30:
        actions.append({
            "priority": "medium",
            "type": "community_prompt",
            "reason": "Views exist but low engagement. Ask audience what style they want next.",
        })

    return {
        "video_id": video_id,
        "title": title,
        "views": views,
        "likes": likes,
        "comments": comments,
        "privacy_status": status.get("privacyStatus"),
        "analyzed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "recommended_actions": actions
    }
