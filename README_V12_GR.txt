BANG IT UP MUSIC AI Agents v12 - UPLOAD READY MP4 ONLY

Αυτό το πακέτο αφαιρεί το βαρύ MP4 rendering από το Render.

Τι κάνει:
- κρατά το OAuth upload ενεργό
- ανεβάζει έτοιμο MP4 από direct URL
- δεν φορτώνει numpy / imageio / ffmpeg
- δεν τρώει 512MB RAM στο free Render

Ανέβασε όλα τα αρχεία στο GitHub με Replace.
Μετά Render → Deploy latest commit.

Environment που πρέπει να έχεις:
YOUTUBE_UPLOAD_ENABLED=true
AUTO_PUBLIC_MODE=true
AUTO_APPROVE_UPLOADS=true
YOUTUBE_TOKEN_JSON=[το token σου]
DEFAULT_UPLOAD_PRIVACY=private

Δοκιμή status:
https://youtube-ai-agents.onrender.com/api/upload/status

Για upload έτοιμου MP4:
POST στο /api/upload/from-url με JSON:

{
  "video_url": "https://example.com/video.mp4",
  "title": "BANG IT UP MUSIC Test Upload",
  "description": "Private test upload",
  "tags": ["BANGITUPMUSIC", "TechHouse", "EDM"],
  "privacy_status": "private",
  "own_content_confirmed": true
}

Πρώτο upload πάντα private.
