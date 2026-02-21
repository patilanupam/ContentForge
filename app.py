from flask import Flask, render_template, request, jsonify
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Google Gemini Configuration - using new SDK
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

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
    - Max 1300 characters""",
    
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
    - Add 5-10 relevant tags at bottom"""
}

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/tool')
def tool():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('index.html')

@app.route('/templates')
def templates():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    try:
        data = request.json
        content = data.get('content', '')
        platform = data.get('platform', 'twitter')
        params = data.get('parameters', {})
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        if platform not in PLATFORM_PROMPTS:
            return jsonify({'error': 'Invalid platform'}), 400
        
        # Build enhanced prompt with parameters
        base_prompt = PLATFORM_PROMPTS[platform]
        
        # Add parameter instructions
        param_instructions = []
        if params.get('tone'):
            param_instructions.append(f"Tone: {params['tone']}")
        if params.get('length'):
            length_map = {'short': 'concise', 'medium': 'moderate length', 'long': 'detailed'}
            param_instructions.append(f"Length: {length_map.get(params['length'], 'moderate length')}")
        if params.get('emoji'):
            emoji_map = {'none': 'no emojis', 'minimal': '1-2 emojis', 'moderate': '3-5 emojis', 'heavy': '8-10 emojis'}
            param_instructions.append(f"Emoji usage: {emoji_map.get(params['emoji'], 'moderate')}")
        if params.get('hashtags'):
            hashtags = params['hashtags']
            if hashtags > 0:
                param_instructions.append(f"Include {hashtags} relevant hashtags")
        if not params.get('includeCTA', True):
            param_instructions.append("Do not include call-to-action")
        
        additional_params = "\n".join([f"- {p}" for p in param_instructions]) if param_instructions else ""
        
        system_prompt = f"""You are an expert content repurposing specialist. Transform content for different social media platforms while maintaining the core message and value.

{f'Additional Requirements:{chr(10)}{additional_params}' if additional_params else ''}"""
        
        prompt = f"{system_prompt}\n\n{base_prompt}\n\nOriginal Content:\n{content}"
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        transformed = response.text
        return jsonify({'result': transformed, 'platform': platform})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting server on http://localhost:5050")
    app.run(debug=False, host='127.0.0.1', port=5050, threaded=True)
