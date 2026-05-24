BANG IT UP MUSIC AI Agents v16.1 - Scheduler Fix

Αυτό διορθώνει το Internal Server Error του /api/scheduler/run.
Η προηγούμενη έκδοση έκανε HTTP self-call στο ίδιο Render app.
Αυτή η έκδοση τρέχει εσωτερικά τον scheduler.

Ανέβασε όλα τα αρχεία στο GitHub με Replace.
Render → Deploy latest commit.

Test:
https://youtube-ai-agents.onrender.com/health
https://youtube-ai-agents.onrender.com/api/scheduler/status
https://youtube-ai-agents.onrender.com/api/scheduler/run?secret=ΤΟ_SECRET_ΣΟΥ
https://youtube-ai-agents.onrender.com/api/scheduler/log
