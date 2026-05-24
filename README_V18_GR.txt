BANG IT UP MUSIC AI Agents v18 - Source Registry + Growth Loop

Τι κάνει:
1. Εσύ δίνεις MP4 direct URL στον agent.
2. Agent το ανεβάζει στο YouTube ως PRIVATE.
3. Agent αποθηκεύει mapping:
   source_mp4_url ↔ youtube_video_id
4. Growth loop ελέγχει πώς πάει το video στο κανάλι.
5. Agent δημιουργεί recommended actions:
   - create_short
   - seo_refresh
   - community_prompt
   - scale_format

Endpoints:
POST /api/source/upload-private
GET  /api/source/registry
GET  /api/source/analyze/<video_id>
GET  /api/source/growth-loop

Παράδειγμα PowerShell για private source upload:

$body = @{
  source_mp4_url = "DIRECT_MP4_URL"
  title = "MIDNIGHT RUN | Dark Melodic Techno"
  description = "Private source upload for AI workflow."
  tags = @("BANGITUPMUSIC","TechHouse","EDM")
  own_content_confirmed = $true
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "https://youtube-ai-agents.onrender.com/api/source/upload-private" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

Μετά:
https://youtube-ai-agents.onrender.com/api/source/registry
https://youtube-ai-agents.onrender.com/api/source/growth-loop
