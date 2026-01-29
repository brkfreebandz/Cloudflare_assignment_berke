# Cloudflare Feedback Analyzer

A serverless feedback analysis dashboard built with Cloudflare Workers (Python), D1 Database, and Workers AI.

## 🚀 Live Demo

**Live Application:** https://feedback-analyzer.berkesoker.workers.dev

## 📊 Features

- Aggregates feedback from multiple sources (Discord, GitHub, Twitter, Support tickets)
- Analyzes sentiment (positive, negative, neutral)
- Categorizes feedback by type (bugs, features, questions, performance, documentation)
- Real-time statistics dashboard
- Built entirely on Cloudflare's serverless platform

## 🛠️ Tech Stack

- **Cloudflare Workers** (Python) - Serverless compute at the edge
- **D1 Database** - Serverless SQL database (SQLite)
- **Workers AI** - AI bindings for future enhancements
- **Tailwind CSS** - Styling framework

## 📂 Project Structure
```
Cloudflare_assignment_berke/
├── README.md                 # This file
├── SETUP_GUIDE.md           # Detailed setup instructions
├── src/
│   └── entry.py             # Main Worker code (routes, API, dashboard)
├── schema.sql               # Database table definition
├── seed.sql                 # Sample feedback data
├── wrangler.jsonc           # Cloudflare Workers configuration
├── package.json             # Node.js dependencies
└── pyproject.toml           # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- UV (Python package manager): `brew install uv`
- Cloudflare account (free): https://dash.cloudflare.com/sign-up

### Deploy Your Own
```bash
# 1. Clone the repository
git clone https://github.com/brkfreebandz/Cloudflare_assignment_berke.git
cd Cloudflare_assignment_berke

# 2. Install dependencies
npm install

# 3. Login to Cloudflare
npx wrangler login

# 4. Create your D1 database
npx wrangler d1 create feedback-db

# 5. Update wrangler.jsonc with your database ID
# (Copy the database_id from step 4 output)

# 6. Set up database schema
npx wrangler d1 execute feedback-db --remote --file=./schema.sql

# 7. Load sample data
npx wrangler d1 execute feedback-db --remote --file=./seed.sql

# 8. Deploy!
npx wrangler deploy
```

**For detailed step-by-step instructions, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)**

## 🌐 API Endpoints

### `GET /`
Returns the HTML dashboard interface with real-time statistics

### `GET /api/feedback`
Returns all feedback entries as JSON
```json
[
  {
    "id": 1,
    "source": "discord",
    "content": "The new feature is amazing!",
    "sentiment": "positive",
    "category": "feature",
    "created_at": "2026-01-28..."
  }
]
```

### `GET /api/stats`
Returns aggregated statistics
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
    "question": 1
  }
}
```

## 🎯 Assignment Context

This project was created for the **Cloudflare Product Manager Intern (Summer 2026)** assignment.

### Part 1: Build Challenge ✅
Built a feedback aggregation and analysis tool that:
- Aggregates feedback from multiple mock sources
- Uses Cloudflare Workers, D1 Database, and Workers AI
- Provides meaningful insights through a web dashboard
- Deployed on Cloudflare's global network

### Part 2: Product Insights ✅
Documented friction points and suggestions for improving the Cloudflare Developer Platform.

## 🔑 Key Implementation Details

### Database Schema
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    content TEXT NOT NULL,
    sentiment TEXT,
    category TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Cloudflare Products Used

1. **Cloudflare Workers (Python Runtime)**
   - Hosts entire application and API
   - Global edge deployment
   - Zero cold starts

2. **D1 Database** (binding: `feedback_db`)
   - Serverless SQLite database
   - Automatic replication
   - SQL queries with Python

3. **Workers AI** (binding: `AI`)
   - Configured for future sentiment analysis
   - Can automate categorization

## 🐛 Troubleshooting

### Local Development
Python Workers require remote database access:
```bash
npm run dev -- --remote
```

### Database Issues
Verify data exists:
```bash
npx wrangler d1 execute feedback-db --remote --command="SELECT COUNT(*) FROM feedback"
```

Should return: `COUNT(*) = 8`

### Deployment Issues
Make sure you're logged in:
```bash
npx wrangler whoami
```

## 📝 Adding Custom Feedback
```bash
npx wrangler d1 execute feedback-db --remote --command="
  INSERT INTO feedback (source, content, sentiment, category) 
  VALUES ('github', 'New feature request', 'neutral', 'feature')
"
```

## 🔮 Future Enhancements

- Integrate Workers AI for automatic sentiment detection
- Add real-time data from actual feedback sources
- Implement search and filtering
- Create data visualization charts
- Add authentication for admin features
- Build export functionality

## 📚 Resources

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [D1 Database Docs](https://developers.cloudflare.com/d1/)
- [Workers AI Docs](https://developers.cloudflare.com/workers-ai/)
- [Python Workers Guide](https://developers.cloudflare.com/workers/languages/python/)

## 👤 Author

**Berke Soker**  
Product Manager Intern Assignment - January 2026

GitHub: [@brkfreebandz](https://github.com/brkfreebandz)

## 📄 License

MIT License - Free to use for learning and building!

---

**Questions?** Check the [detailed setup guide](./SETUP_GUIDE.md) or Cloudflare's documentation.
