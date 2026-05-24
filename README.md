# BANG IT UP MUSIC AI Agents v2

Render-ready YouTube growth agent system.

Endpoints:
- `/health`
- `/dashboard`
- `/api/channel`
- `/api/videos`
- `/api/report`
- `/api/seo?title=...&genre=...`
- `/api/shorts?title=...&genre=...`
- `/api/calendar`
- `/api/competitors`

Required Render Environment Variables:
- `YOUTUBE_API_KEY`
- `YOUTUBE_CHANNEL_ID`

Render:
Build Command: `pip install -r requirements.txt`
Start Command: `gunicorn app:app`

This system does not create fake views, fake subscribers, spam comments, or bot engagement.
