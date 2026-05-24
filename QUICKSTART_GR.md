# Γρήγορη εκκίνηση στα Ελληνικά

## 1. Μην στείλεις credentials σε κανέναν
Μην στείλεις API key, client_secret.json ή token.json στο chat.

## 2. Τι χρειάζεσαι
- Python 3.10+
- Google Cloud project
- YouTube Data API v3 enabled
- YouTube Analytics API enabled
- OAuth 2.0 Desktop Client JSON αρχείο με όνομα `client_secret.json`

## 3. Εγκατάσταση

```bash
pip install -r requirements.txt
cp .env.example .env
```

Βάλε το `client_secret.json` μέσα στον φάκελο του project.

## 4. Σύνδεση με YouTube

```bash
python main.py setup
```

Θα ανοίξει browser και θα κάνεις login στο Google account που έχει το κανάλι.

## 5. Δημιουργία campaign για νέο τραγούδι

```bash
python main.py campaign --title "ΟΝΟΜΑ ΤΡΑΓΟΥΔΙΟΥ" --genre "Trap / Dance" --mood "high energy"
```

Το report αποθηκεύεται στον φάκελο `outputs/`.

## 6. Analytics report

```bash
python main.py report --days 28
```

## Νόμιμη χρήση
Το σύστημα βοηθά σε SEO, περιγραφές, Shorts, social captions, community posts και analytics. Δεν κάνει fake views, fake subscribers, bot comments ή spam.
