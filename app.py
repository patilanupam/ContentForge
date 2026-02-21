import streamlit as st
from google import genai
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="ContentForge - AI Content Transformation",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .platform-pill {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 20px;
        background-color: #f0f2f6;
        cursor: pointer;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        margin: 1rem 0;
    }
    .stTextArea textarea {
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'transform_count' not in st.session_state:
    st.session_state.transform_count = 0
if 'input_tokens' not in st.session_state:
    st.session_state.input_tokens = 0
if 'output_tokens' not in st.session_state:
    st.session_state.output_tokens = 0
if 'result' not in st.session_state:
    st.session_state.result = None
if 'platform' not in st.session_state:
    st.session_state.platform = 'twitter'

# Google Gemini Configuration
@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY not found! Please add it to Streamlit secrets.")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_gemini_client()

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

PLATFORM_EMOJIS = {
    "twitter": "🐦",
    "linkedin": "💼",
    "instagram": "📸",
    "newsletter": "📧",
    "youtube": "🎬"
}

EXAMPLES = {
    "blog": """Artificial Intelligence is transforming content creation. Here's how to use it effectively while maintaining your authentic voice.

Key benefits:
• Save 10+ hours per week on content repurposing
• Maintain consistency across all platforms
• Focus on strategy while AI handles formatting

The future is about humans + AI working together, not replacement.""",
    
    "podcast": """Episode 25: Building Better Habits

Today's Key Points:
- Start with tiny habits (2 minutes or less)
- Stack new habits onto existing routines
- Focus on systems, not goals
- Track your progress visually
- Forgive yourself and start again

Remember: It's about progress, not perfection!""",
    
    "video": """[Intro]
Hey everyone! Today I'm sharing 3 productivity tips that changed my life.

[Main Content]
Tip 1: Time block your calendar
Tip 2: Use the 2-minute rule
Tip 3: Batch similar tasks together

[Outro]
Try these for a week and let me know your results! Like and subscribe for more!"""
}

# Sidebar - Parameters
with st.sidebar:
    st.markdown("### 🔥 ContentForge")
    st.markdown("---")
    
    st.markdown("### 📊 Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem;">Input Tokens</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{st.session_state.input_tokens}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem;">Output Tokens</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{st.session_state.output_tokens}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 0.8rem;">Total Transformations</div>
        <div style="font-size: 1.5rem; font-weight: bold;">{st.session_state.transform_count}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Parameters")
    
    tone = st.selectbox(
        "Tone",
        ["professional", "casual", "friendly", "enthusiastic"],
        index=0
    )
    
    length = st.selectbox(
        "Length",
        ["short", "medium", "long"],
        index=1
    )
    
    emoji = st.selectbox(
        "Emoji Usage",
        ["none", "minimal", "moderate", "heavy"],
        index=2
    )
    
    hashtags = st.selectbox(
        "Hashtags",
        [0, 3, 5, 10],
        index=2
    )
    
    include_cta = st.checkbox("Include Call-to-Action", value=True)
    
    st.markdown("---")
    if st.button("🔄 Reset Parameters", use_container_width=True):
        st.rerun()

# Main content
st.markdown('<div class="main-header">🔥 ContentForge</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Transform your content for any platform with AI</p>', unsafe_allow_html=True)

st.markdown("---")

# Platform selection
st.markdown("### 📱 Select Platform")
cols = st.columns(5)

platforms = ["twitter", "linkedin", "instagram", "newsletter", "youtube"]
platform_names = ["Twitter", "LinkedIn", "Instagram", "Newsletter", "YouTube"]

for idx, (col, platform, name) in enumerate(zip(cols, platforms, platform_names)):
    with col:
        if st.button(
            f"{PLATFORM_EMOJIS[platform]} {name}",
            key=f"platform_{platform}",
            use_container_width=True,
            type="primary" if st.session_state.platform == platform else "secondary"
        ):
            st.session_state.platform = platform

st.markdown("---")

# Content input
st.markdown("### ✍️ Your Content")

# Example buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
with col1:
    if st.button("📝 Blog Example"):
        st.session_state.example_content = EXAMPLES["blog"]
with col2:
    if st.button("🎙️ Podcast Example"):
        st.session_state.example_content = EXAMPLES["podcast"]
with col3:
    if st.button("🎥 Video Example"):
        st.session_state.example_content = EXAMPLES["video"]

# Get example content if set
default_content = st.session_state.get('example_content', '')

content = st.text_area(
    "Paste your content here",
    value=default_content,
    height=200,
    placeholder="Paste your blog post, video script, podcast notes, or any content you want to repurpose...",
    key="content_input"
)

# Character count
if content:
    chars = len(content)
    tokens = chars // 4
    st.session_state.input_tokens = tokens
    st.caption(f"📊 {chars:,} characters • ~{tokens:,} tokens")

# Transform button
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    transform_button = st.button("✨ Transform", type="primary", use_container_width=True)

# Clear button
if st.button("🗑️ Clear All"):
    st.session_state.result = None
    st.session_state.example_content = ""
    st.rerun()

# Transform logic
if transform_button:
    if not content.strip():
        st.error("⚠️ Please add some content first!")
    else:
        with st.spinner(f"🔄 Transforming for {platform_names[platforms.index(st.session_state.platform)]}..."):
            try:
                # Build parameters
                params = {
                    'tone': tone,
                    'length': length,
                    'emoji': emoji,
                    'hashtags': hashtags,
                    'includeCTA': include_cta
                }
                
                # Build prompt
                base_prompt = PLATFORM_PROMPTS[st.session_state.platform]
                
                param_instructions = []
                if params.get('tone'):
                    param_instructions.append(f"Tone: {params['tone']}")
                if params.get('length'):
                    length_map = {'short': 'concise', 'medium': 'moderate length', 'long': 'detailed'}
                    param_instructions.append(f"Length: {length_map.get(params['length'], 'moderate length')}")
                if params.get('emoji'):
                    emoji_map = {'none': 'no emojis', 'minimal': '1-2 emojis', 'moderate': '3-5 emojis', 'heavy': '8-10 emojis'}
                    param_instructions.append(f"Emoji usage: {emoji_map.get(params['emoji'], 'moderate')}")
                if params.get('hashtags') and params['hashtags'] > 0:
                    param_instructions.append(f"Include {params['hashtags']} relevant hashtags")
                if not params.get('includeCTA', True):
                    param_instructions.append("Do not include call-to-action")
                
                additional_params = "\n".join([f"- {p}" for p in param_instructions]) if param_instructions else ""
                
                system_prompt = f"""You are an expert content repurposing specialist. Transform content for different social media platforms while maintaining the core message and value.

{f'Additional Requirements:{chr(10)}{additional_params}' if additional_params else ''}"""
                
                prompt = f"{system_prompt}\n\n{base_prompt}\n\nOriginal Content:\n{content}"
                
                # Generate content
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=prompt
                )
                
                st.session_state.result = response.text
                st.session_state.output_tokens = len(response.text) // 4
                st.session_state.transform_count += 1
                
                st.success("✨ Transformation complete!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display result
if st.session_state.result:
    st.markdown("---")
    st.markdown(f"### 🎯 Result for {PLATFORM_EMOJIS[st.session_state.platform]} {platform_names[platforms.index(st.session_state.platform)]}")
    
    st.markdown(f'<div class="result-box">{st.session_state.result}</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "⬇️ Download",
            st.session_state.result,
            file_name=f"{st.session_state.platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col2:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.code(st.session_state.result, language=None)
            st.info("👆 Click the copy icon in the code block above")
    with col3:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.session_state.result = None
            st.rerun()
