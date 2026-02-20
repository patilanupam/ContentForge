# 🔥 ContentForge

**AI-powered content repurposing tool** - Transform one piece of content into posts optimized for every platform.

## Features

- 🐦 **Twitter/X Threads** - Convert long-form content into engaging tweet threads
- 💼 **LinkedIn Posts** - Professional, engagement-optimized posts
- 📸 **Instagram Captions** - Casual, emoji-rich captions with hashtags
- 📧 **Email Newsletters** - Well-structured email content
- 🎬 **YouTube Descriptions** - SEO-optimized video descriptions

## Tech Stack

- **Backend:** Flask (Python)
- **AI:** Google Gemini API
- **Frontend:** HTML, CSS, JavaScript (vanilla)

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd contentforge
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   - Get a free Google Gemini API key from [Google AI Studio](https://ai.google.dev/)
   - Copy `.env.example` to `.env`
   - Add your API key to `.env`:
     ```
     GOOGLE_API_KEY=your-key-here
     ```

4. **Run the app:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   ```
   http://localhost:5050
   ```

## Usage

1. Paste your content (blog post, script, notes, etc.)
2. Select the target platform
3. Click "Transform Content"
4. Copy and use!

## Monetization Ideas

- **Freemium Model:** Free tier (5 transforms/month) + Pro tier ($9-19/month unlimited)
- **API Access:** Sell API access for developers
- **White Label:** Offer to agencies as a white-label solution

## Deployment

Deploy to:
- [Railway](https://railway.app/)
- [Render](https://render.com/)
- [Vercel](https://vercel.com/) (with Flask)

## License

MIT

---

Built with ❤️ using Google Gemini API
