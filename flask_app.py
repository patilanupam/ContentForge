"""ContentForge – Flask backend.

Pipeline: User Input → [Normalizer] → Platform Formatter → Output
"""

import os

from flask import Flask, jsonify, render_template, request
from google import genai

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Platform configuration
# ---------------------------------------------------------------------------

PLATFORM_PROMPTS = {
    "twitter": """Transform this content into a Twitter/X thread (5-10 tweets).
    Rules:
    - Each tweet max 280 characters
    - Start with a hook
    - Use line breaks between tweets
    - End with a call to action
    - Add relevant emojis sparingly
    Format: Number each tweet (1/, 2/, etc.)""",
    "linkedin": """Transform this content into a LinkedIn post.
    Rules:
    - Professional but conversational tone
    - Start with a compelling hook
    - Use short paragraphs and line breaks
    - Include 3-5 relevant hashtags at the end
    - End with a question to drive engagement
    - Max 3000 characters""",
    "instagram": """Transform this content into an Instagram caption.
    Rules:
    - Casual, engaging tone
    - Start with attention-grabbing first line
    - Use emojis throughout
    - Include a clear call to action
    - Add 20-30 relevant hashtags at the end
    - Max 2200 characters""",
    "newsletter": """Transform this content into an email newsletter.
    Rules:
    - Friendly, personal tone
    - Clear subject line suggestion at top
    - Well-structured with headers
    - Include a personal anecdote or insight
    - End with clear CTA
    - Easy to scan/skim""",
    "youtube": """Transform this content into a YouTube video description.
    Rules:
    - Compelling first 2 lines (shown in preview)
    - Include timestamps placeholder
    - Add relevant keywords naturally
    - Include social links placeholders
    - End with subscribe CTA
    - Add 5-10 relevant tags at bottom""",
}

DEMO_RESPONSES = {
    "twitter": (
        "1/ 🚀 AI is revolutionizing content creation!\n\n"
        "Here's what you need to know about using it effectively... 🧵\n\n"
        "2/ Save 10+ hours per week on content repurposing. "
        "That's an entire workday back in your schedule! ⏰\n\n"
        "3/ AI maintains consistency across all platforms while you focus on "
        "strategy, creativity, and audience connection. 🎯\n\n"
        "4/ Key insight: humans + AI working together, not replacement. "
        "You bring authenticity, AI handles formatting. 💡\n\n"
        "5/ Ready to 10x your content output? The future is collaborative. 🤝"
    ),
    "linkedin": (
        "AI is transforming content creation — here's how to use it without "
        "losing your authentic voice 🚀\n\n"
        "After months of testing, the secret is collaboration, not automation.\n\n"
        "✅ Save 10+ hours/week\n"
        "✅ Stay consistent across platforms\n"
        "✅ Focus on strategy, not formatting\n\n"
        "What's your experience with AI content tools?\n\n"
        "#ContentCreation #AITools #ProductivityHacks #DigitalMarketing"
    ),
    "instagram": (
        "✨ AI is changing the content game and I'm HERE for it! 🚀\n\n"
        "Saving 10+ HOURS every single week. No joke. 🎯\n\n"
        "Drop a 🙋 if you want the full breakdown!\n\n"
        "#ContentCreation #AItools #ProductivityHacks #SocialMediaTips "
        "#ContentStrategy #DigitalMarketing #CreatorEconomy"
    ),
    "newsletter": (
        "Subject: The tool that gave me 10 extra hours every week ⏰\n\n"
        "Hey there!\n\n"
        "AI-assisted content repurposing is a game-changer.\n\n"
        "Benefits:\n"
        "• Save 10+ hours/week\n"
        "• Stay consistent across every platform\n"
        "• Focus on strategy, not formatting\n\n"
        "Hit reply — what's your biggest content challenge?\n\n"
        "[Your Name]"
    ),
    "youtube": (
        "🚀 AI is Transforming Content Creation\n\n"
        "Learn how to save 10+ hours/week on content repurposing while "
        "keeping your authentic voice.\n\n"
        "⏱️ TIMESTAMPS:\n"
        "00:00 - Intro\n03:45 - How AI helps\n09:15 - Human + AI model\n\n"
        "🎯 Like, subscribe, and drop your biggest content challenge below!\n\n"
        "#AIContentCreation #ContentStrategy #ProductivityHacks"
    ),
}

# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------


def get_gemini_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key and api_key != "your_google_api_key_here":
        return genai.Client(api_key=api_key)
    return None


client = get_gemini_client()

# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------


def _build_normalize_prompt(content: str, input_type: str, output_language: str) -> str:
    language_instruction = (
        f"Write the output in {output_language}."
        if output_language and output_language != "auto"
        else ""
    )
    input_type_hint = (
        f"The user has indicated this content is: {input_type}."
        if input_type and input_type != "auto"
        else ""
    )
    return (
        "You are an intelligent content preprocessor for a content transformation tool.\n\n"
        "Tasks:\n"
        "1. Detect the input type (bullet notes / transcript / rough ideas / "
        "paragraph / mixed-language).\n"
        "2. Fix grammar, repair fragmented ideas, and reconstruct into coherent content.\n"
        "3. Preserve ALL original meaning, intent, and factual information — "
        "do NOT add new facts.\n"
        "4. For mixed-language input (e.g., Hinglish), normalise while preserving meaning.\n"
        "5. If the input is only emojis or completely unusable, return it unchanged.\n"
        f"{language_instruction}\n"
        f"{input_type_hint}\n\n"
        f"Input:\n{content}\n\n"
        "Return ONLY the cleaned content with no meta-commentary or explanations."
    )


def _normalize_content(content: str, input_type: str = "auto", output_language: str = "auto") -> str:
    prompt = _build_normalize_prompt(content, input_type, output_language)
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    return response.text.strip()


# ---------------------------------------------------------------------------
# Transform helper
# ---------------------------------------------------------------------------


def _transform_content(
    content: str, platform: str, parameters: dict, output_language: str = "auto"
) -> str:
    base_prompt = PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS["twitter"])

    tone = parameters.get("tone", "professional")
    length = parameters.get("length", "medium")
    emoji = parameters.get("emoji", "moderate")
    hashtags = parameters.get("hashtags", 5)
    include_cta = parameters.get("includeCTA", True)

    length_map = {"short": "concise", "medium": "moderate length", "long": "detailed"}
    emoji_map = {
        "none": "no emojis",
        "minimal": "1-2 emojis",
        "moderate": "3-5 emojis",
        "heavy": "8-10 emojis",
    }

    param_lines = [
        f"- Tone: {tone}",
        f"- Length: {length_map.get(length, 'moderate length')}",
        f"- Emoji usage: {emoji_map.get(emoji, 'moderate')}",
    ]
    if hashtags and int(hashtags) > 0:
        param_lines.append(f"- Include {hashtags} relevant hashtags")
    if not include_cta:
        param_lines.append("- Do not include a call-to-action")
    if output_language and output_language != "auto":
        param_lines.append(f"- Write the output in {output_language}")

    system_prompt = (
        "You are an expert content repurposing specialist.\n\n"
        "Requirements:\n" + "\n".join(param_lines)
    )
    prompt = f"{system_prompt}\n\n{base_prompt}\n\nOriginal Content:\n{content}"

    response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
    return response.text.strip()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/tool")
def tool():
    return render_template("index.html")


@app.route("/normalize", methods=["POST"])
def normalize_endpoint():
    data = request.get_json(silent=True) or {}
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "No content provided"}), 400

    if not client:
        return jsonify({"normalized": content, "demo": True})

    try:
        normalized = _normalize_content(
            content,
            data.get("inputType", "auto"),
            data.get("outputLanguage", "auto"),
        )
        return jsonify({"normalized": normalized})
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500


@app.route("/transform", methods=["POST"])
def transform_endpoint():
    data = request.get_json(silent=True) or {}
    content = data.get("content", "").strip()
    platform = data.get("platform", "twitter")
    parameters = data.get("parameters", {})
    should_normalize = data.get("normalize", False)
    input_type = data.get("inputType", "auto")
    output_language = data.get("outputLanguage", "auto")

    if not content:
        return jsonify({"error": "No content provided"}), 400

    if not client:
        return jsonify({"result": DEMO_RESPONSES.get(platform, ""), "demo": True})

    try:
        normalized_content = content
        if should_normalize:
            normalized_content = _normalize_content(content, input_type, output_language)

        result = _transform_content(normalized_content, platform, parameters, output_language)
        return jsonify(
            {
                "result": result,
                "normalizedInput": normalized_content if should_normalize else None,
            }
        )
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
