BANG IT UP MUSIC AI Agents v15

Render:
- ελαφρύ backend
- upload έτοιμου MP4/Short URL
- διαβάζει υπάρχοντα YouTube videos
- δημιουργεί Shorts tasks

Τοπικά στον υπολογιστή:
- local_short_factory.py κόβει δικά σου MP4 σε vertical Shorts
- δεν κατεβάζει YouTube videos
- χρησιμοποιεί μόνο δικά σου local source files

Deploy:
Ανέβασε όλα τα αρχεία στο GitHub με Replace.
Render → Deploy latest commit.

Test:
https://youtube-ai-agents.onrender.com/health
https://youtube-ai-agents.onrender.com/api/shorts/tasks?max=10
