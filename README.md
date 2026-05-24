# BANG IT UP MUSIC AI Agents v5 - Initiative Engine

Render-ready Flask app for a safer autonomous YouTube growth dashboard.

## What is new in v5

- Initiative Engine: creates campaigns/tasks automatically when the channel needs action.
- Auto Schedule: daily autonomous draft workflow.
- Safety Policy: clear separation between safe auto-drafts, approval-required public actions, and blocked actions.
- Premium dashboard with Channel, Videos, Reports, SEO, Shorts, Distribution, Calendar, Approval Queue, Initiative Engine, Auto Schedule, Safety Policy.

## Required environment variables

- `YOUTUBE_API_KEY`
- `YOUTUBE_CHANNEL_ID`

Optional:

- `AUTO_MODE=true` or `false`

`AUTO_MODE=true` only changes dashboard/report behavior. It does not perform uploads, public posts, comments, fake views, fake subscribers, spam, or title edits. Those stay approval-required or blocked.

## Render deploy

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

## Endpoints

- `/dashboard`
- `/health`
- `/api/channel`
- `/api/videos`
- `/api/report`
- `/api/seo?title=Track&genre=EDM`
- `/api/shorts?title=Track&genre=EDM`
- `/api/distribution?title=Track&genre=EDM`
- `/api/calendar`
- `/api/approval-queue`
- `/api/initiatives`
- `/api/automation-schedule`
- `/api/safety-policy`

## Safety

This system is designed for organic growth only. It does not create fake views/subscribers, spam comments, mass DMs, or artificial engagement. Uploads, public posts, title edits, and comment replies should require explicit owner approval.
