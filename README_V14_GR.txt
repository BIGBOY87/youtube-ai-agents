BANG IT UP MUSIC AI Agents v14 - AUTO SHORTS WORKFLOW

Τι προσθέτει:
- /api/shorts/tasks?max=10
- /api/shorts/task/<video_id>
- /api/shorts/upload-from-url
- /api/auto-run δημιουργεί Shorts tasks από υπάρχοντα YouTube videos

Σημαντικό:
Το YouTube API δεν δίνει το αρχικό MP4 αρχείο από ένα υπάρχον YouTube video.
Για πραγματικό upload Short χρειάζεται direct MP4 URL από:
- το αρχικό σου αρχείο
- ένα ήδη κομμένο vertical Short MP4
- Drive/Dropbox/Cloudinary/direct hosting

Το endpoint /api/shorts/upload-from-url ανεβάζει ready Short MP4 στο YouTube.

Παράδειγμα:
POST https://youtube-ai-agents.onrender.com/api/shorts/upload-from-url

{
  "short_mp4_url": "https://example.com/my-short.mp4",
  "title": "Night Drive Tech House #Shorts",
  "description": "BANG IT UP MUSIC Short. #Shorts #BANGITUPMUSIC",
  "tags": ["BANGITUPMUSIC", "Shorts", "TechHouse", "EDM"],
  "privacy_status": "private",
  "own_content_confirmed": true
}

Πρώτο upload πάντα private.
