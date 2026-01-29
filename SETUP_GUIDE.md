# Complete Setup Guide for Cloudflare Feedback Analyzer

This guide walks you through every single step to recreate this project from scratch.

## ⏱️ Estimated Time: 20-30 minutes

---

## Part 1: Install Prerequisites (10 mins)

### 1.1 Install Node.js

**macOS:**
```bash
# Using Homebrew
brew install node

# Or download from: https://nodejs.org/
```

**Windows:**
Download installer from: https://nodejs.org/

**Verify installation:**
```bash
node --version  # Should show v16 or higher
npm --version   # Should show 8.0 or higher
```

### 1.2 Install UV (Python Package Manager)

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

### 1.3 Create Cloudflare Account

1. Go to: https://dash.cloudflare.com/sign-up
2. Sign up with your email
3. Verify your email
4. Complete onboarding

---

## Part 2: Clone and Setup Project (5 mins)

### 2.1 Clone Repository
```bash
# Clone the repo
git clone https://github.com/brkfreebandz/Cloudflare_assignment_berke.git

# Navigate to project
cd Cloudflare_assignment_berke/cloudflare-feedback-tool/feedback-analyzer

# Verify you're in the right place
ls -la
# You should see: src/, wrangler.jsonc, package.json, etc.
```

### 2.2 Install Dependencies
```bash
npm install
```

This installs Wrangler CLI and other dependencies.

---

## Part 3: Cloudflare Setup (10 mins)

### 3.1 Login to Cloudflare
```bash
npx wrangler login
```

- A browser window will open
- Click "Allow" to authorize Wrangler
- Return to terminal

### 3.2 Set Up Workers.dev Subdomain (if needed)

If you haven't set up a subdomain yet:

1. Go to: https://dash.cloudflare.com
2. Click **Workers & Pages**
3. Follow prompts to choose your subdomain (e.g., `yourname.workers.dev`)

### 3.3 Create D1 Database
```bash
npx wrangler d1 create feedback-db
```

**IMPORTANT:** Copy the entire output! Example:
```toml
[[d1_databases]]
binding = "feedback_db"
database_name = "feedback-db"
database_id = "abc123-def456-ghi789"
```

### 3.4 Update Configuration

Open `wrangler.jsonc` in a text editor and find this section:
```jsonc
"d1_databases": [
  {
    "binding": "feedback_db",
    "database_name": "feedback-db",
    "database_id": "7b5d74df-39be-4dae-9e3a-64165fed1bfb"  // ← REPLACE THIS
  }
]
```

Replace the `database_id` with YOUR ID from step 3.3.

Save the file.

---

## Part 4: Database Setup (5 mins)

### 4.1 Create Table
```bash
npx wrangler d1 execute feedback-db --remote --file=./schema.sql
```

Expected output: `✔ 1 queries executed`

### 4.2 Add Sample Data
```bash
npx wrangler d1 execute feedback-db --remote --file=./seed.sql
```

Expected output: `✔ 1 queries executed` (8 rows written)

### 4.3 Verify Data
```bash
npx wrangler d1 execute feedback-db --remote --command="SELECT COUNT(*) FROM feedback"
```

Expected output: `COUNT(*) = 8`

If you see 8, you're good! ✅

---

## Part 5: Deploy (2 mins)

### 5.1 Deploy to Production
```bash
npx wrangler deploy
```

Expected output:
```
✨ Deployed feedback-analyzer
🌍 https://feedback-analyzer.YOUR-SUBDOMAIN.workers.dev
```

### 5.2 Test Your Deployment

Open the URL from step 5.1 in your browser.

You should see:
- ✅ Total feedback count: 8
- ✅ Sentiment breakdown
- ✅ Category breakdown  
- ✅ Table with 8 feedback entries

**If you see "Loading..."**: Wait 30 seconds and refresh. Sometimes it takes a moment for the database binding to activate.

---

## Part 6: Local Development (Optional)

To run locally:
```bash
npm run dev -- --remote
```

Open: http://localhost:8787

**Note:** The `--remote` flag is required for Python Workers to access D1 databases locally.

---

## 🎉 Success Checklist

- [ ] Node.js and UV installed
- [ ] Repository cloned
- [ ] Dependencies installed (`npm install`)
- [ ] Logged into Cloudflare (`wrangler login`)
- [ ] D1 database created
- [ ] `wrangler.jsonc` updated with your database ID
- [ ] Schema applied (`schema.sql`)
- [ ] Sample data loaded (`seed.sql`)
- [ ] Worker deployed successfully
- [ ] Dashboard loads in browser
- [ ] All 8 feedback items visible

---

## ❓ Common Issues

### Issue: "wrangler: command not found"

**Solution:**
```bash
npm install -g wrangler
```

### Issue: "uv: command not found"

**Solution:**
```bash
# macOS
brew install uv

# Or
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

### Issue: Database shows 0 rows

**Solution:**
```bash
# Re-run the seed file
npx wrangler d1 execute feedback-db --remote --file=./seed.sql

# Verify
npx wrangler d1 execute feedback-db --remote --command="SELECT * FROM feedback"
```

### Issue: Dashboard shows "Loading..." forever

**Solutions:**
1. Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. Check browser console for errors (F12 → Console)
3. Verify database has data (see above)
4. Wait 1-2 minutes for bindings to activate after first deploy

### Issue: "Repository not found" when pushing to GitHub

**Solution:**
You don't need to push - just deploy to Cloudflare. The original repo is already public.

---

## 🚀 Next Steps

Now that you have it running:

1. **Customize the data**: Edit `seed.sql` and re-run it
2. **Modify the code**: Edit `src/entry.py` and redeploy
3. **Add features**: Implement filtering, search, or real-time updates
4. **Integrate AI**: Use Workers AI for automatic sentiment analysis

---

## 📚 Resources

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [D1 Database Docs](https://developers.cloudflare.com/d1/)
- [Workers AI Docs](https://developers.cloudflare.com/workers-ai/)
- [Python Workers Guide](https://developers.cloudflare.com/workers/languages/python/)

---

## 💬 Questions?

If you run into issues:
1. Check the troubleshooting section above
2. Review Cloudflare's documentation
3. Check the [Cloudflare Discord](https://discord.cloudflare.com)

Happy building! 🎉
