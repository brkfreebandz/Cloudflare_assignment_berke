# Feedback Analyzer - Cloudflare Workers Project

A serverless feedback analysis dashboard built with Cloudflare Workers (Python), D1 Database, and Workers AI.

## 🚀 Live Demo

**Live Application:** https://feedback-analyzer.berkesoker.workers.dev

## 📋 Features

- Aggregates feedback from multiple sources (Discord, GitHub, Twitter, Support)
- Analyzes sentiment (positive, negative, neutral)
- Categorizes feedback (bugs, features, questions, etc.)
- Real-time dashboard with statistics
- Built entirely on Cloudflare's Developer Platform

## 🛠️ Tech Stack

- **Cloudflare Workers (Python)** - Serverless compute
- **D1 Database** - Serverless SQL database
- **Workers AI** - AI bindings (configured for future enhancements)
- **Tailwind CSS** - Styling

## 📦 Prerequisites

Before you begin, ensure you have:

1. **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
2. **Python** (v3.8 or higher)
3. **UV** - Python package manager
```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Or via Homebrew
   brew install uv
```
4. **Cloudflare Account** (free) - [Sign up here](https://dash.cloudflare.com/sign-up)
5. **Git** - For cloning the repository

## 🔧 Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/brkfreebandz/Cloudflare_assignment_berke.git
cd Cloudflare_assignment_berke/cloudflare-feedback-tool/feedback-analyzer
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Authenticate with Cloudflare
```bash
npx wrangler login
```

This will open a browser window to authenticate with your Cloudflare account.

### Step 4: Create Your D1 Database
```bash
npx wrangler d1 create feedback-db
```

**Important:** Copy the output! It will look like this:
```toml
[[d1_databases]]
binding = "feedback_db"
database_name = "feedback-db"
database_id = "YOUR-UNIQUE-DATABASE-ID"
```

### Step 5: Update Configuration

Open `wrangler.jsonc` and replace the database_id with YOUR database ID from Step 4:
```jsonc
{
  "d1_databases": [
    {
      "binding": "feedback_db",
      "database_name": "feedback-db",
      "database_id": "YOUR-UNIQUE-DATABASE-ID"  // ← Replace this
    }
  ]
}
```

### Step 6: Set Up Database Schema

Create the feedback table in your database:
```bash
npx wrangler d1 execute feedback-db --remote --file=./schema.sql
```

### Step 7: Seed Sample Data

Add sample feedback data:
```bash
npx wrangler d1 execute feedback-db --remote --file=./seed.sql
```

Verify the data was added:
```bash
npx wrangler d1 execute feedback-db --remote --command="SELECT COUNT(*) FROM feedback"
```

You should see: `COUNT(*) = 8`

### Step 8: Deploy to Cloudflare Workers
```bash
npx wrangler deploy
```

After deployment completes, you'll get a URL like:
```
https://feedback-analyzer.YOUR-SUBDOMAIN.workers.dev
```

Open this URL in your browser to see your live dashboard! 🎉

## 🧪 Local Development

To run locally (note: uses remote database):
```bash
npm run dev -- --remote
```

Then open: http://localhost:8787

**Note:** Python Workers require the `--remote` flag for D1 database access during local development.

## 📊 Project Structure
```
feedback-analyzer/
├── src/
│   └── entry.py          # Main Worker code (routes, API, dashboard)
├── schema.sql            # Database schema definition
├── seed.sql              # Sample data for testing
├── wrangler.jsonc        # Cloudflare Workers configuration
├── package.json          # Node dependencies
├── pyproject.toml        # Python dependencies
└── README.md            # This file
```

## 🔑 Key Files Explained

### `src/entry.py`
Main application file containing:
- Route handlers (`/`, `/api/feedback`, `/api/stats`)
- Database queries using D1
- HTML dashboard generation

### `wrangler.jsonc`
Configuration file that defines:
- Worker name and entry point
- D1 database binding
- Workers AI binding
- Python compatibility flags

### `schema.sql`
Defines the feedback table structure:
- `id` - Primary key
- `source` - Where feedback came from (discord, github, etc.)
- `content` - The actual feedback text
- `sentiment` - positive/negative/neutral
- `category` - bug/feature/question/etc.
- `created_at` - Timestamp

## 🌐 API Endpoints

### `GET /`
Returns the HTML dashboard interface

### `GET /api/feedback`
Returns all feedback entries as JSON

**Response:**
```json
[
  {
    "id": 1,
    "source": "discord",
    "content": "The new feature is amazing!",
    "sentiment": "positive",
    "category": "feature",
    "created_at": "2026-01-28T..."
  },
  ...
]
```

### `GET /api/stats`
Returns aggregated statistics

**Response:**
```json
{
  "sentiment": {
    "positive": 2,
    "negative": 4,
    "neutral": 2
  },
  "category": {
    "feature": 3,
    "bug": 2,
    "question": 1,
    "performance": 1,
    "documentation": 1
  }
}
```

## 🐛 Troubleshooting

### "Object of type JsProxy is not JSON serializable"
Make sure you're using `.to_py()` to convert D1 results to Python objects:
```python
data = result.results.to_py()
```

### "no such table: feedback"
Run the schema file on the remote database:
```bash
npx wrangler d1 execute feedback-db --remote --file=./schema.sql
```

### Workers.dev subdomain not set up
Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Workers & Pages and set up your subdomain.

### Local development not working
Always use `--remote` flag with Python Workers:
```bash
npm run dev -- --remote
```

## 📝 Adding Your Own Feedback Data

You can add custom feedback by inserting into the database:
```bash
npx wrangler d1 execute feedback-db --remote --command="
  INSERT INTO feedback (source, content, sentiment, category) 
  VALUES ('github', 'New bug report', 'negative', 'bug')
"
```

## 🔮 Future Enhancements

- Integrate Workers AI for automatic sentiment analysis
- Add filtering and search functionality
- Implement real-time updates with WebSockets
- Add authentication for admin features
- Create data visualization charts

## 📄 License

MIT License - feel free to use this project for learning and building!

## 👤 Author

Created by Berke Soker for Cloudflare Product Manager Intern Assignment (Summer 2026)

## 🙏 Acknowledgments

- Cloudflare Developer Platform Documentation
- Cloudflare Workers Python Runtime
- Tailwind CSS for styling
