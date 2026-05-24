BANG IT UP MUSIC AI Agents v13 - REPURPOSE EXISTING YOUTUBE VIDEOS

Τι προσθέτει:
- /api/repurpose-existing?max=10
- /api/repurpose-video/<video_id>
- /api/auto-run πλέον φτιάχνει repurpose plan για τα υπάρχοντα videos
- Δημιουργεί Shorts hooks, captions, hashtags, SEO refresh και distribution posts
- Δεν κόβει το υπάρχον YouTube video σε MP4. Για πραγματικό Short χρειάζεται το αρχικό MP4 ή direct MP4 URL.

Ανέβασε όλα τα αρχεία στο GitHub με Replace.
Μετά Render → Deploy latest commit.

Δοκιμές:
https://youtube-ai-agents.onrender.com/health
https://youtube-ai-agents.onrender.com/api/repurpose-existing?max=10
https://youtube-ai-agents.onrender.com/dashboard

Το upload σύστημα παραμένει σε ready MP4 URL mode:
POST /api/upload/from-url
