BANG IT UP MUSIC AI Agents v20 CLEAN FIXED

Δεν περιέχει client_secret.json ούτε token.json. Αυτά είναι μυστικά και μπαίνουν μόνο τοπικά.

Τοπικά:
1. Βάλε το δικό σου client_secret.json σε αυτόν τον φάκελο.
2. Τρέξε:
   python connect_upload_oauth.py
3. Θα δημιουργηθεί token.json.
4. Άνοιξε token.json και αντέγραψε όλο το JSON στο Render:
   YOUTUBE_TOKEN_JSON

Render Environment:
YOUTUBE_TOKEN_JSON=ολόκληρο token JSON
DRIVE_SOURCE_FOLDER_ID=1ZExCXK1dXS_S8GBWXs__YHSSlv0tDmOV
YOUTUBE_UPLOAD_ENABLED=true
AUTO_PUBLIC_MODE=true
AUTO_APPROVE_UPLOADS=true
MAX_UPLOAD_SOURCE_MB=250

Tests:
https://youtube-ai-agents.onrender.com/health
https://youtube-ai-agents.onrender.com/api/channel
https://youtube-ai-agents.onrender.com/api/drive/status
https://youtube-ai-agents.onrender.com/api/drive/scan
https://youtube-ai-agents.onrender.com/api/source/registry

Scopes:
youtube.upload
youtube.readonly
yt-analytics.readonly
drive.file

Δεν χρησιμοποιεί drive.readonly.
