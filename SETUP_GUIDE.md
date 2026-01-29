# Complete Setup Guide - Cloudflare Feedback Analyzer

This guide walks you through recreating this project from scratch with detailed explanations.

## ⏱️ Estimated Time: 20-30 minutes

---

## Prerequisites Check

Before starting, ensure you have:

- [ ] **Node.js** (v16+) - Run `node --version`
- [ ] **Python** (v3.8+) - Run `python3 --version`
- [ ] **UV** - Run `uv --version`
- [ ] **Git** - Run `git --version`
- [ ] **Cloudflare Account** - Free signup at dash.cloudflare.com

---

## Part 1: Install Prerequisites

### Install Node.js

**macOS:**
```bash
brew install node
```

**Windows:** Download from https://nodejs.org/

**Verify:**
```bash
node --version  # Should be v16 or higher
npm --version   # Should be v8 or higher
```

### Install UV (Python Package Manager)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Or via Homebrew:**
```bash
brew install uv
```

**Verify:**
```bash
uv --version
```

### Create Cloudflare Account

1. Visit: https://dash.cloudflare.com/sign-up
2. Sign up with email
3. Verify email
4. Complete onboarding

---

## Part 2: Clone Repository
```bash
# Clone the project
git clone https://github.com/brkfreebandz/Cloudflare_assignment_berke.git

# Navigate to project directory
cd Cloudflare_assignment_berke

# Verify structure
ls -la
# You should see: src/, wrangler.jsonc, schema.sql, seed.sql, etc.
```

---

## Part 3: Install Dependencies
```bash
# Install Node packages (including Wrangler CLI)
npm install

# This installs:
# - wrangler (Cloudflare CLI)
# - Python Workers dependencies
# - Other required packages
```

---

## Part 4: Cloudflare Authentication

### Login to Cloudflare
```bash
npx wrangler login
```

- Browser window will open
- Click **"Allow"** to authorize
- Return to terminal

**Verify login:**
```bash
npx wrangler whoami
```

Should show your account email.

### Set Up workers.dev Subdomain

If you haven't already:

1. Go to https://dash.cloudflare.com
2. Navigate to **Workers & Pages**
3. Follow prompts to choose subdomain (e.g., `yourname.workers.dev`)

---

## Part 5: Create D1 Database

### Create Database
```bash
npx wrangler d1 create feedback-db
```

**CRITICAL:** Copy the entire output! It looks like:
```toml
[[d1_databases]]
binding = "feedback_db"
database_name = "feedback-db"
database_id = "abc123-def456-ghi789-jkl012"
```

### Update Configuration

Open `wrangler.jsonc` and find:
```jsonc
"d1_databases": [
  {
    "binding": "feedback_db",
    "database_name": "feedback-db",
    "database_id": "7b5d74df-39be-4dae-9e3a-64165fed1bfb"  // ← REPLACE THIS
  }
]
```

**Replace** the `database_id` with YOUR ID from the create command.

**Save the file.**

---

## Part 6: Set Up Database

### Create Table Schema
```bash
npx wrangler d1 execute feedback-db --remote --file=./schema.sql
```

**Expected output:**
```
✔ 1 queries executed
```

This creates the `feedback` table with columns:
- `id` - Primary key
- `source` - Where feedback came from
- `content` - Feedback text
- `sentiment` - positive/negative/neutral
- `category` - bug/feature/question/etc.
- `created_at` - Timestamp

### Load Sample Data
```bash
npx wrangler d1 execute feedback-db --remote --file=./seed.sql
```

**Expected output:**
```
✔ 1 queries executed (8 rows written)
```

### Verify Data
```bash
npx wrangler d1 execute feedback-db --remote --command="SELECT COUNT(*) FROM feedback"
```

**Expected output:**
```
┌──────────┐
│ COUNT(*) │
├──────────┤
│ 8        │
└──────────┘
```

If you see `8`, you're ready to deploy! ✅

---

## Part 7: Deploy to Production

### Deploy Worker
```bash
npx wrangler deploy
```

**Expected output:**
```
✨ Deployed feedback-analyzer
🌍 https://feedback-analyzer.YOUR-SUBDOMAIN.workers.dev
```

### Test Deployment

1. **Open the URL** from the deploy output
2. You should see:
   - ✅ "Feedback Analyzer" dashboard
   - ✅ Total count: 8
   - ✅ Sentiment breakdown
   - ✅ Category breakdown
   - ✅ Table with 8 feedback items

**If you see "Loading...":**
- Wait 30-60 seconds (bindings need to activate)
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)

---

## Part 8: Test API Endpoints

### Test Feedback API

Visit in browser:
```
https://feedback-analyzer.YOUR-SUBDOMAIN.workers.dev/api/feedback
```

Should return JSON with all feedback.

### Test Stats API

Visit:
```
https://feedback-analyzer.YOUR-SUBDOMAIN.workers.dev/api/stats
```

Should return sentiment and category counts.

---

## Part 9: Local Development (Optional)

### Run Locally
```bash
npm run dev -- --remote
```

**Note:** The `--remote` flag is required for Python Workers to access D1.

Open: http://localhost:8787

**To stop:** Press `Ctrl+C`

---

## 🎉 Success Checklist

- [ ] Node.js and UV installed
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Logged into Cloudflare
- [ ] D1 database created
- [ ] `wrangler.jsonc` updated with your database ID
- [ ] Schema applied
- [ ] Sample data loaded (8 rows)
- [ ] Worker deployed successfully
- [ ] Dashboard loads in browser
- [ ] All 8 feedback items visible
- [ ] API endpoints working

---

## 🐛 Troubleshooting

### "wrangler: command not found"

**Solution:**
```bash
npm install
# Or globally:
npm install -g wrangler
```

### "uv: command not found"

**Solution:**
```bash
brew install uv
# Or:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "no such table: feedback"

**Solution:**
```bash
# Re-run schema
npx wrangler d1 execute feedback-db --remote --file=./schema.sql
```

### Dashboard shows "Loading..." forever

**Solutions:**

1. **Check browser console** (F12 → Console)
2. **Verify data:**
```bash
   npx wrangler d1 execute feedback-db --remote --command="SELECT * FROM feedback"
```
3. **Hard refresh:** `Cmd+Shift+R` or `Ctrl+Shift+R`
4. **Wait 2 minutes** for bindings to fully activate

### API returns errors

**Check logs:**
```bash
npx wrangler tail feedback-analyzer
```

Then refresh your browser and see real-time errors.

---

## 📝 Adding Your Own Data

### Add Single Feedback
```bash
npx wrangler d1 execute feedback-db --remote --command="
  INSERT INTO feedback (source, content, sentiment, category) 
  VALUES ('github', 'Love the new UI!', 'positive', 'feature')
"
```

### Clear All Data
```bash
npx wrangler d1 execute feedback-db --remote --command="DELETE FROM feedback"
```

### Reload Sample Data
```bash
npx wrangler d1 execute feedback-db --remote --file=./seed.sql
```

---

## 🔄 Making Changes

### Update Code

1. Edit `src/entry.py`
2. Test locally: `npm run dev -- --remote`
3. Deploy: `npx wrangler deploy`

### Update Database Schema

1. Edit `schema.sql`
2. **Warning:** This will recreate the table (data loss!)
3. Run: `npx wrangler d1 execute feedback-db --remote --file=./schema.sql`

---

## 🔮 Next Steps

### Enhance Your Project

1. **Add real data sources:**
   - Integrate Discord webhook
   - Connect to GitHub Issues API
   - Pull from Twitter API

2. **Implement Workers AI:**
   - Automatic sentiment analysis
   - Smart categorization
   - Theme extraction

3. **Add features:**
   - Search and filtering
   - Date range selection
   - Export to CSV
   - Admin authentication

4. **Improve UI:**
   - Add charts (Chart.js)
   - Real-time updates
   - Dark mode
   - Mobile responsive

---

## 📚 Learn More

- **Cloudflare Workers:** https://developers.cloudflare.com/workers/
- **D1 Database:** https://developers.cloudflare.com/d1/
- **Workers AI:** https://developers.cloudflare.com/workers-ai/
- **Python Workers:** https://developers.cloudflare.com/workers/languages/python/

---

## 💬 Need Help?

1. Check troubleshooting section above
2. Review [Cloudflare Docs](https://developers.cloudflare.com)
3. Join [Cloudflare Discord](https://discord.cloudflare.com)
4. Check [GitHub Issues](https://github.com/brkfreebandz/Cloudflare_assignment_berke/issues)

---

**Happy building!** 🚀
