# 🔥 ContentForge

<div align="center">

**AI-powered content repurposing tool** — Transform one piece of content into posts optimized for every platform.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gemini API](https://img.shields.io/badge/Google%20Gemini-API-orange?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

</div>

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📖 Usage](#-usage)
- [💰 Monetization Ideas](#-monetization-ideas)
- [☁️ Deployment](#️-deployment)
- [🗺 Roadmap / Future Updates](#-roadmap--future-updates)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

| Platform | Output |
|---|---|
| 🐦 **Twitter / X** | Threaded tweets (5-10 tweets), hook + CTA, emoji-sparingly |
| 💼 **LinkedIn** | Professional post with hashtags & engagement question |
| 📸 **Instagram** | Casual caption with emojis and 20-30 hashtags |
| 📧 **Email Newsletter** | Subject line, structured sections, personal CTA |
| 🎬 **YouTube** | SEO description with timestamps & tags |

Additional controls available in the UI:
- 🎛 **Tone selector** — choose from formal, casual, humorous, and more
- 📏 **Length control** — short / medium / long output
- 😀 **Emoji density** — none / minimal / moderate / heavy
- #️⃣ **Hashtag count** — dial in the exact number you need
- ✅ **CTA toggle** — include or skip the call-to-action

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · Flask |
| AI | Google Gemini 2.5 Flash |
| Frontend | HTML · CSS · Vanilla JavaScript |
| Config | python-dotenv |

---

## 🚀 Quick Start

> **Prerequisites:** Python 3.8+, a free [Google Gemini API key](https://ai.google.dev/)

```bash
# 1. Clone the repo
git clone https://github.com/patilanupam/ContentForge.git
cd ContentForge

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Open .env and set:  GOOGLE_API_KEY=your-key-here

# 4. Start the server
python app.py
```

Then open **http://localhost:5050** in your browser. 🎉

---

## 📖 Usage

1. **Paste** your content (blog post, script, notes, article, etc.)
2. **Select** the target platform (Twitter, LinkedIn, Instagram, Newsletter, YouTube)
3. **Tweak** tone, length, emoji usage, and hashtag count with the optional controls
4. **Click** "Transform Content"
5. **Copy** the generated output and publish!

---

## 💰 Monetization Ideas

- **Freemium Model** — Free tier (5 transforms/month) + Pro tier ($9–19/month unlimited)
- **API Access** — Sell API access for developers building their own tools
- **White Label** — Offer to agencies as a fully branded white-label solution

---

## ☁️ Deployment

One-click deploy platforms:

| Platform | Notes |
|---|---|
| [Railway](https://railway.app/) | Easiest, zero-config |
| [Render](https://render.com/) | Free tier available |
| [Vercel](https://vercel.com/) | Requires WSGI adapter |

---

## 🗺 Roadmap / Future Updates

The following improvements are planned to make ContentForge even more powerful:

### 🔐 User Accounts & History
- [ ] User authentication (sign-up / login)
- [ ] Save and revisit past transformations
- [ ] Personal content library

### 🌐 More Platforms
- [ ] **TikTok** script / caption generator
- [ ] **Pinterest** pin descriptions
- [ ] **Threads (Meta)** post formatter
- [ ] **Reddit** post/comment styler

### 🤖 AI Enhancements
- [ ] Custom style fine-tuning (learn from your past posts)
- [ ] Brand voice profiles — define tone, vocabulary, and style once; reuse everywhere
- [ ] Batch processing — upload a CSV of content and transform all at once
- [ ] Auto-hashtag research with real-time trend data

### 🎨 UX / UI Improvements
- [ ] Live character/word count per platform limit
- [ ] Side-by-side comparison view (original vs transformed)
- [ ] Dark mode
- [ ] Export to PDF, Notion, or Google Docs

### 📊 Analytics & Insights
- [ ] Per-platform performance tips based on current best practices
- [ ] Readability score for generated content
- [ ] Suggested posting times per platform

### 🔗 Integrations & Automation
- [ ] Direct one-click publish to social platforms via OAuth
- [ ] Zapier / Make (formerly Integromat) webhook support
- [ ] Browser extension for transforming content on the fly
- [ ] Scheduling queue for planned posts

### 💳 Monetization Upgrades
- [ ] Stripe-powered subscription billing
- [ ] Usage-based billing dashboard
- [ ] Team / agency workspaces with shared brand profiles

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please open an issue first to discuss significant changes.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
Built with ❤️ using <a href="https://ai.google.dev/">Google Gemini API</a>
</div>
