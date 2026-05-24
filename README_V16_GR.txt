BANG IT UP MUSIC AI Agents v16 - Scheduler

Ανέβασε όλα τα αρχεία στο GitHub με Replace.
Render → Deploy latest commit.

Render Environment:
AUTO_SCHEDULER_ENABLED=true
PUBLIC_BASE_URL=https://youtube-ai-agents.onrender.com
SCHEDULER_SECRET=βαλε-ενα-δικο-σου-secret

Δοκιμές:
https://youtube-ai-agents.onrender.com/api/scheduler/status
https://youtube-ai-agents.onrender.com/api/scheduler/run?secret=ΤΟ_SECRET_ΣΟΥ
https://youtube-ai-agents.onrender.com/api/scheduler/log

Για καθημερινή εκτέλεση:
φτιάξε free cron στο cron-job.org που καλεί το /api/scheduler/run?secret=...
