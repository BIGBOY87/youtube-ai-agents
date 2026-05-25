BANG IT UP MUSIC AI Agents v20 CLEAN

Καθαρό πακέτο μέχρι το σημείο που φτάσαμε.

Περιέχει:
- /health
- /dashboard
- /api/channel
- /api/upload/status
- /api/source/upload-private
- /api/source/registry
- /api/drive/status
- /api/drive/scan
- /api/source/growth-loop
- connect_upload_oauth.py

Σημαντικό:
Χρησιμοποιούμε drive.file, όχι drive.readonly.

Τοπικό OAuth:
1. Βάλε client_secret.json στον ίδιο φάκελο.
2. Τρέξε: python connect_upload_oauth.py
3. Διάλεξε σωστό Google account / YouTube channel.
4. Θα δημιουργηθεί token.json.
5. Αντέγραψε όλο το token.json στο Render Environment ως YOUTUBE_TOKEN_JSON.

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

Μην ανεβάσεις ποτέ στο GitHub:
- client_secret.json
- token.json
