# Cloudflare Product Manager Intern Assignment

## Feedback Analyzer Dashboard

A serverless feedback analysis tool built with Cloudflare Workers, D1 Database, and Workers AI.

![Screenshot](https://feedback-analyzer.berkesoker.workers.dev)

## 🚀 Live Demo

**Live Application:** https://feedback-analyzer.berkesoker.workers.dev

## 📂 Project Structure
```
Cloudflare_assignment_berke/
└── cloudflare-feedback-tool/
    └── feedback-analyzer/          # Main application
        ├── src/                    # Python Worker code
        ├── schema.sql              # Database schema
        ├── seed.sql                # Sample data
        ├── wrangler.jsonc          # Cloudflare configuration
        ├── README.md               # Detailed project documentation
        └── SETUP_GUIDE.md          # Step-by-step setup instructions
```

## 📖 Documentation

For complete documentation and setup instructions, see:

- **[Main README](./cloudflare-feedback-tool/feedback-analyzer/README.md)** - Project overview and quick start
- **[Setup Guide](./cloudflare-feedback-tool/feedback-analyzer/SETUP_GUIDE.md)** - Detailed step-by-step instructions

## 🔗 Quick Links

- **GitHub Repository:** https://github.com/brkfreebandz/Cloudflare_assignment_berke
- **Live Dashboard:** https://feedback-analyzer.berkesoker.workers.dev

## 🛠️ Technology Stack

- **Cloudflare Workers** (Python) - Serverless compute
- **D1 Database** - Serverless SQL database  
- **Workers AI** - AI bindings
- **Tailwind CSS** - Styling

## �� Assignment Deliverables

This project was created for the Cloudflare Product Manager Intern (Summer 2026) assignment.

### Part 1: Build Challenge ✅
Built a feedback aggregation and analysis tool that:
- Aggregates feedback from multiple sources
- Analyzes sentiment and categorizes feedback
- Displays insights in a dashboard

### Part 2: Product Insights ✅
Documented friction points and suggestions for Cloudflare Developer Platform products.

## 🚀 Quick Start

To run this project locally or deploy your own version:
```bash
cd cloudflare-feedback-tool/feedback-analyzer
npm install
npx wrangler login
npx wrangler deploy
```

For detailed instructions, see the [Setup Guide](./cloudflare-feedback-tool/feedback-analyzer/SETUP_GUIDE.md).

## �� Author

**Berke Soker**  
Cloudflare PM Intern Assignment - January 2026

---

For questions or issues, please refer to the documentation in the feedback-analyzer directory.
