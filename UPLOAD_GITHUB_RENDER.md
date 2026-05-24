# 📤 QUICK UPLOAD GUIDE - GitHub + Render

## Χρόνος: 5 λεπτά

---

## 📋 ΑΡΧΕΙΑ ΠΟΥ ΧΡΕΙΑΖΕΣΑΙ

### ✅ ΚΥΡΙΑ (8 αρχεία):
```
✓ youtube_ai_agents_advanced.py
✓ requirements_advanced.txt
✓ .env.advanced
✓ render.yaml
✓ render_start.py
✓ .gitignore
✓ README.md
✓ RENDER_GITHUB_SETUP.md
```

### ✅ ΠΡΟΣΘΕΤΑ (προαιρετικά):
```
○ SETUP_ADVANCED.md
○ Procfile
```

---

## 🎯 STEP-BY-STEP

### STEP 1️⃣: Δημιούργησε φάκελο
```bash
mkdir youtube-ai-agents
cd youtube-ai-agents
```

### STEP 2️⃣: Τοποθέτησε τα 8 αρχεία
- Κάνε copy-paste όλα τα αρχεία πάνω στο φάκελο

### STEP 3️⃣: Δημιούργησε .env
```bash
cp .env.advanced .env
```

### STEP 4️⃣: Συμπλήρωσε τα keys
Ανοίξε `.env` και βάλε τα API keys σου:
```
YOUTUBE_API_KEY=your_key_here
YOUTUBE_CHANNEL_ID=your_id_here
CLAUDE_API_KEY=your_key_here
... (κλπ)
```

### STEP 5️⃣: Ενεργοποίησε Git
```bash
git init
git add .
git commit -m "Initial commit - YouTube AI Agents"
git branch -M main
```

### STEP 6️⃣: Δημιούργησε GitHub Repo
1. Πήγαινε: https://github.com/new
2. Όνομα: `youtube-ai-agents`
3. Visibility: Public
4. Κάνε κλικ "Create repository"

### STEP 7️⃣: Σύνδεσε με GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/youtube-ai-agents.git
git push -u origin main
```

⚠️ Αντικατάστησε `YOUR_USERNAME` με το GitHub username σου!

### STEP 8️⃣: Deploy σε Render
1. Πήγαινε: https://render.com
2. Κάνε κλικ "New Web Service"
3. Σύνδεσε GitHub
4. Επίλεξε repo: `youtube-ai-agents`
5. Προσθήκη env vars (API keys)
6. Deploy!

---

## ⚠️ ΣΗΜΑΝΤΙΚΟ!

✅ **Το .env δεν θα uploads στο GitHub** (protected by .gitignore)
✅ **Τα API keys βάζονται στο Render environment**
✅ **Ο κώδικας είναι δημόσιος, τα secrets ιδιωτικά**

---

## ✅ ΕΤΟΙΜΟ!

Τώρα το σύστημα σου:
- ✓ Είναι στο GitHub
- ✓ Τρέχει στο Render 24/7
- ✓ Auto-redeploy on git push

---

Για λεπτομέρειες: Δες `RENDER_GITHUB_SETUP.md`
