# YouTube AI Agents – Heroku Deployment

Αυτό το πακέτο είναι έτοιμο για GitHub + Heroku.

## Τι περιέχει

- `app.py`: web health endpoint για Heroku
- `worker.py`: background worker για agents
- `Procfile`: ορίζει web + worker dynos
- `.env.template`: μεταβλητές περιβάλλοντος
- `.gitignore`: προστασία μυστικών αρχείων
- τον υπάρχοντα BANG IT UP MUSIC agent κώδικα

## Ασφάλεια

ΜΗΝ ανεβάσεις ποτέ σε GitHub:

- `.env`
- `token.json`
- `client_secret.json`
- API keys

## Heroku Config Vars

Βάλε στο Heroku:

- `YOUTUBE_API_KEY`
- `YOUTUBE_CHANNEL_ID`
- `WORKER_INTERVAL_MINUTES=60`

Προαιρετικά:

- `TIKTOK_API_KEY`
- `INSTAGRAM_TOKEN`
- `TWITTER_API_KEY`
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`

## Heroku commands

```bash
heroku login
heroku create youtube-ai-agents-bangitup
heroku config:set YOUTUBE_API_KEY="YOUR_VALUE" YOUTUBE_CHANNEL_ID="YOUR_VALUE"
git push heroku main
heroku ps:scale web=1 worker=1
heroku logs --tail
```

## Health check

Άνοιξε:

```text
https://YOUR-HEROKU-APP.herokuapp.com/health
```

Πρέπει να δεις:

```json
{"status":"ok"}
```

## Σημαντικό

Το Heroku δεν είναι δωρεάν όπως παλιά. Για worker dyno χρειάζεται πληρωμένο dyno. Το Uptime Robot κρατά awake μόνο web endpoints, όχι πραγματικό worker dyno.

Το σύστημα δεν κάνει fake views, fake subscribers, spam comments ή μαζικό posting. Παράγει νόμιμες προτάσεις, drafts, reports και growth actions.
