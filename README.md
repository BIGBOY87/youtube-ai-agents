# BANG IT UP MUSIC — Legal YouTube AI Agent System

Local Python system for organic YouTube growth using the official YouTube Data API and YouTube Analytics API.

## What it does

- Connects with Google OAuth locally.
- Reads your own channel and recent video metadata.
- Reads basic YouTube Analytics reports when your account has access.
- Generates SEO titles, descriptions, hashtags, tags, pinned comments, Shorts ideas and community posts.
- Generates a weekly organic promotion plan.
- Exports Markdown reports to `outputs/`.

## What it does not do

It does not create fake views, fake subscribers, bot comments, spam posts, or automated artificial engagement.

## Setup

1. Install Python 3.10+.
2. Create a Google Cloud project.
3. Enable:
   - YouTube Data API v3
   - YouTube Analytics API
4. Create OAuth 2.0 Client ID for a Desktop app.
5. Download the OAuth JSON and save it as:

```bash
client_secret.json
```

inside this project folder.

6. Install dependencies:

```bash
pip install -r requirements.txt
```

7. Copy environment file:

```bash
cp .env.example .env
```

8. Run:

```bash
python main.py setup
python main.py report
```

The first run opens a browser for Google OAuth permission. Do not share `client_secret.json` or `token.json`.

## Main commands

```bash
python main.py setup
python main.py channel
python main.py videos --max 10
python main.py analytics --days 28
python main.py campaign --title "MY NEW SONG" --genre "Trap / Dance" --mood "high energy"
python main.py report --days 28
```

## Files

- `main.py`: command line interface.
- `youtube_api/auth.py`: OAuth handling.
- `youtube_api/client.py`: YouTube Data + Analytics API calls.
- `agents/seo_agent.py`: titles, descriptions, tags.
- `agents/shorts_agent.py`: Shorts/reels ideas.
- `agents/promotion_agent.py`: posts and weekly plan.
- `agents/analytics_agent.py`: rule-based growth recommendations.

## Security

Never paste API keys, OAuth secrets or token files into ChatGPT or public websites. Keep credentials local.
