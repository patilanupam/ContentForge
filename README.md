# 🔥 ContentForge

**AI-powered content repurposing tool** - Transform one piece of content into posts optimized for every platform.

## Features

- 🐦 **Twitter/X Threads** - Convert long-form content into engaging tweet threads
- 💼 **LinkedIn Posts** - Professional, engagement-optimized posts
- 📸 **Instagram Captions** - Casual, emoji-rich captions with hashtags
- 📧 **Email Newsletters** - Well-structured email content
- 🎬 **YouTube Descriptions** - SEO-optimized video descriptions

## Tech Stack

- **Framework:** Streamlit
- **AI:** Google Gemini API
- **Language:** Python

## Local Setup

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
   - Create `.streamlit/secrets.toml` file:
     ```bash
     mkdir .streamlit
     cp .streamlit/secrets.toml.example .streamlit/secrets.toml
     ```
   - Add your API key to `.streamlit/secrets.toml`:
     ```toml
     GOOGLE_API_KEY = "your-key-here"
     ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser:**
   - Streamlit will automatically open the app in your default browser
   - Default URL: `http://localhost:8501`

## Deploy to Streamlit Cloud

1. **Push your code to GitHub** (already done!)

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**

3. **Click "New app"**

4. **Configure your app:**
   - Repository: `your-username/contentforge`
   - Branch: `main` or `master`
   - Main file path: `app.py`

5. **Add your API key in Secrets:**
   - Click on "Advanced settings"
   - In the "Secrets" section, add:
     ```toml
     GOOGLE_API_KEY = "your-google-api-key-here"
     ```

6. **Click "Deploy"!**

Your app will be live at: `https://your-app-name.streamlit.app`

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
