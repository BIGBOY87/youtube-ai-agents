BANG IT UP MUSIC AI Agents v10 - REAL UPLOAD LAYER

ΑΥΤΟ ΤΟ ΠΑΚΕΤΟ ΠΡΟΣΘΕΤΕΙ:
- YouTube OAuth upload connector
- connect_upload_oauth.py για δημιουργία token.json
- youtube_uploader.py για πραγματικό videos.insert upload
- public_publish_agent.py για upload με safety checks
- upload-ready endpoints για Flask/Render
- οδηγίες για ασφαλή χρήση χωρίς να βάλεις secrets στο GitHub

ΤΙ ΚΑΝΕΙ ΠΡΑΚΤΙΚΑ:
Ο agent μπορεί να πάρει ένα ήδη έτοιμο MP4 αρχείο, να του βάλει title/description/tags/privacy και να το ανεβάσει στο YouTube μέσω OAuth.

ΤΙ ΔΕΝ ΚΑΝΕΙ ΑΚΟΜΑ:
Δεν δημιουργεί μόνο του MP4 από το μηδέν. Για αυτό χρειάζεται video generation layer:
- Suno / δικό σου audio
- εικόνες/thumbnails
- ffmpeg composition

ΣΗΜΑΝΤΙΚΟ:
ΜΗΝ ΑΝΕΒΑΣΕΙΣ ΠΟΤΕ ΣΤΟ GITHUB:
- client_secret.json
- token.json
- .env
- API keys

RENDER ENVIRONMENT:
YOUTUBE_UPLOAD_ENABLED=true
AUTO_PUBLIC_MODE=true
AUTO_APPROVE_UPLOADS=false
PUBLIC_PUBLISH_LIMIT_PER_DAY=1
PUBLIC_POSTS_REQUIRE_OWN_CONTENT=true

ΓΙΑ ΠΡΩΤΗ ΣΥΝΔΕΣΗ:
1. Βάλε το νέο client_secret.json τοπικά στον υπολογιστή σου, όχι στο GitHub.
2. Τρέξε:
   pip install -r requirements.txt
   python connect_upload_oauth.py
3. Θα ανοίξει Google login.
4. Θα δημιουργηθεί token.json.
5. Για Render, το token πρέπει να μπει ως secret/environment, όχι σε δημόσιο repo.
