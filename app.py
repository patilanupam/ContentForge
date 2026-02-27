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
if 'normalized_input' not in st.session_state:
    st.session_state.normalized_input = None

# Google Gemini Configuration
@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GOOGLE_API_KEY")
        except:
            pass
    
    if api_key and api_key != "your_google_api_key_here":
        return genai.Client(api_key=api_key)
    return None

client = get_gemini_client()

# Check if running in demo mode
DEMO_MODE = client is None

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

# Demo mode responses (used when no API key is provided)
DEMO_RESPONSES = {
    "twitter": """1/ 🚀 Just discovered how AI is revolutionizing content creation!

Here's what I learned about using AI tools effectively while keeping your authentic voice... 🧵

2/ The biggest game-changer? Time savings. We're talking 10+ hours saved per week on content repurposing alone. That's an entire workday back in your schedule! ⏰

3/ But it's not just about speed. AI helps maintain consistency across all platforms while you focus on the big picture - strategy, creativity, and connecting with your audience. 🎯

4/ Here's the key insight: It's not about AI replacing humans. It's about humans + AI working together. You bring the strategy and authenticity, AI handles the formatting. 💡

5/ Think of AI as your content assistant, not your replacement. You're still the creative director - AI just helps execute your vision faster. 🎨

Ready to 10x your content output? The future is collaborative. 🤝""",
    
    "linkedin": """AI is transforming content creation, and here's how to use it effectively while maintaining your authentic voice 🚀

After spending months testing various AI tools, I've discovered something crucial: the best results come from collaboration, not automation.

Here's what's working:

✅ Save 10+ hours per week on content repurposing
✅ Maintain consistency across all platforms
✅ Focus on strategy while AI handles formatting

The real power isn't in replacing human creativity—it's in augmenting it. Think of AI as your content assistant that never sleeps, helping you scale your message without losing your unique voice.

The future of content creation is about humans + AI working together. You bring the strategic thinking and authentic perspective. AI brings speed and consistency.

What's your experience with AI content tools? Are you seeing similar time savings?

#ContentCreation #AITools #ProductivityHacks #DigitalMarketing #ContentStrategy""",
    
    "instagram": """✨ AI is changing the content game and I'm HERE for it! 🚀

Picture this: You spend hours creating one amazing piece of content... and then you have to manually adapt it for Twitter, LinkedIn, Instagram, YouTube, your newsletter... 😰

That was me. Until I discovered the power of AI-assisted content repurposing! 🤖💖

Now I'm saving 10+ HOURS every week (yes, you read that right!) and maintaining consistency across ALL platforms. 🎯✨

The secret? 👇

It's not about replacing your creativity—it's about amplifying it! You bring the authentic voice and strategic thinking, AI handles the tedious formatting work. 🎨⚡

Think of it as having a 24/7 content assistant who never gets tired! 💪

The future is collaborative. Humans + AI = Content magic! ✨🤝

Who else is using AI to level up their content game? Drop a 🙋‍♀️ in the comments!

#ContentCreation #AItools #ProductivityHacks #SocialMediaTips #ContentStrategy #DigitalMarketing #CreatorEconomy #AIforCreators #ContentMarketing #SocialMediaMarketing #MarketingTips #SmallBusinessTips #EntrepreneurLife #ContentCreator #SocialMediaStrategy #MarketingStrategy #DigitalCreator #OnlineBusiness #ContentTips #CreativeEntrepreneur #BusinessGrowth #MarketingAutomation #ContentRepurposing #TimeManagement #ProductivityTips #WorkSmarterNotHarder #CreatorTips #SocialMediaGrowth #ContentIdeas""",
    
    "newsletter": """Subject: The AI Content Tool That Gave Me Back 10 Hours Per Week ⏰

Hey there!

Remember last month when I told you I was drowning in content creation? Creating posts for every platform was eating up my entire week, and I was starting to burn out.

Well, I found a solution that's been absolutely game-changing.

**The Problem We All Face**

You create one great piece of content—a blog post, video, podcast episode—and then you need to share it everywhere. But each platform has different requirements:
- Twitter needs threads with character limits
- LinkedIn wants professional, long-form posts
- Instagram needs casual captions with lots of hashtags
- YouTube needs detailed descriptions

Manually adapting content for each platform? That's easily 10+ hours per week. 😰

**Enter: AI-Assisted Content Repurposing**

Here's what I discovered: AI tools can transform your content while maintaining your authentic voice and core message. Think of it as having a content assistant who understands each platform's best practices.

The key benefits I'm seeing:
• Save 10+ hours per week (seriously!)
• Maintain consistency across all platforms
• Focus on strategy instead of formatting
• Never miss an opportunity to share your message

**The Future: Humans + AI**

Here's what's important to understand: this isn't about replacing human creativity. It's about augmentation, not automation.

You bring: Strategy, authenticity, unique insights
AI brings: Speed, consistency, platform optimization

Together? Content magic. ✨

**Your Turn**

Are you spending too much time on content repurposing? Hit reply and let me know your biggest content challenge. I'd love to hear from you!

To your success,
[Your Name]

P.S. If you're interested in learning more about the specific tools I'm using, let me know! I'm thinking of putting together a detailed guide.""",
    
    "youtube": """🚀 AI is Transforming Content Creation - Here's How to Use It Effectively

Discover how AI tools can save you 10+ hours per week on content repurposing while maintaining your authentic voice. In this video, I share my complete process for using AI to scale content across multiple platforms.

⏱️ TIMESTAMPS:
00:00 - Introduction
01:30 - The Content Repurposing Problem
03:45 - How AI Can Help (Without Replacing You)
06:20 - Real Results: 10+ Hours Saved Per Week
09:15 - The Human + AI Collaboration Model
12:30 - Best Practices for Maintaining Authenticity
15:45 - Tools I'm Using
18:00 - Common Mistakes to Avoid
20:30 - Final Thoughts & Action Steps

🔑 KEY TAKEAWAYS:
✅ Save 10+ hours per week on content repurposing
✅ Maintain consistency across all platforms
✅ Focus on strategy while AI handles formatting
✅ Keep your authentic voice with AI assistance

📱 CONNECT WITH ME:
Instagram: [Your Handle]
Twitter: [Your Handle]
LinkedIn: [Your Profile]
Newsletter: [Your Link]

💡 RESOURCES MENTIONED:
• AI Content Tools Guide: [Link]
• Platform-Specific Best Practices: [Link]
• My Complete Content System: [Link]

🎯 If this video helped you, don't forget to:
• Hit that LIKE button 👍
• SUBSCRIBE for more content creation tips
• Drop a COMMENT with your biggest content challenge
• SHARE with a creator friend who needs this!

#AIContentCreation #ContentStrategy #ProductivityHacks #ContentMarketing #SocialMediaTips #AITools #CreatorEconomy #DigitalMarketing #ContentRepurposing #MarketingAutomation"""
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
    
    # Demo mode indicator
    if DEMO_MODE:
        st.warning("⚠️ **DEMO MODE**\n\nNo API key detected. Using example transformations.\n\nTo use real AI transformations, add your Google API key to Streamlit secrets.")
        with st.expander("📖 How to add API key"):
            st.markdown("""
            **For Streamlit Cloud:**
            1. Go to app settings
            2. Click "Secrets"
            3. Add:
            ```toml
            GOOGLE_API_KEY = "your-key"
            ```
            
            **Get free API key:**
            [Google AI Studio](https://ai.google.dev/)
            """)
    else:
        st.success("✅ **AI ACTIVE**\n\nGoogle Gemini connected")
    
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
    st.markdown("### 🌐 Language")
    
    output_language = st.selectbox(
        "Output Language",
        ["Same as input", "English", "Hindi", "Spanish", "French", "Portuguese", "Arabic", "Japanese", "Chinese"],
        index=0,
        help="Select the language for the generated output"
    )
    output_lang_value = "auto" if output_language == "Same as input" else output_language
    
    st.markdown("---")
    if st.button("🔄 Reset Parameters", use_container_width=True):
        st.rerun()

# Main content
st.markdown('<div class="main-header">🔥 ContentForge</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Transform your content for any platform with AI</p>', unsafe_allow_html=True)

# Show demo mode banner at top
if DEMO_MODE:
    st.info("ℹ️ **Running in Demo Mode** - Example transformations are shown below. Add your Google API key in the sidebar for real AI-powered transformations based on your content.")

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
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    if st.button("📝 Blog Example"):
        st.session_state.example_content = EXAMPLES["blog"]
with col2:
    if st.button("🎙️ Podcast Example"):
        st.session_state.example_content = EXAMPLES["podcast"]
with col3:
    if st.button("🎥 Video Example"):
        st.session_state.example_content = EXAMPLES["video"]
with col4:
    if st.button("🌐 Hinglish Example"):
        st.session_state.example_content = """Kal client meeting tha, bahut acha gaya. Unhone product demo dekha aur impressed hue.
Next steps: onboarding call schedule karna hai aur pricing discuss karni hai."""
with col5:
    if st.button("📋 Rough Notes"):
        st.session_state.example_content = """startup idea
ai + legal courts
data aggregation
reducing delays
app for lawyers + clients + judges"""

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

# Normalization controls
st.markdown("#### 🧹 Input Normalization")
col_norm1, col_norm2 = st.columns([1, 2])
with col_norm1:
    normalize_input = st.checkbox(
        "Clean my input first",
        help="Auto-fix grammar, structure, and mixed-language content before transforming"
    )
with col_norm2:
    input_type = st.selectbox(
        "Input type",
        ["Auto detect", "Bullet Notes", "Transcript", "Rough Ideas", "Full Paragraph"],
        index=0,
        disabled=not normalize_input,
        label_visibility="visible"
    )
    input_type_value = "auto" if input_type == "Auto detect" else input_type.lower().replace(" ", "_")

# Transform button
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    transform_button = st.button("✨ Transform", type="primary", use_container_width=True)

# Clear button
if st.button("🗑️ Clear All"):
    st.session_state.result = None
    st.session_state.example_content = ""
    st.rerun()

def _build_normalize_prompt(content, input_type, output_language):
    language_instruction = (
        f"Write/translate the output in {output_language}."
        if output_language and output_language != "auto"
        else ""
    )
    input_type_hint = (
        f"The user has indicated this content is: {input_type}."
        if input_type and input_type != "auto"
        else ""
    )
    return (
        "You are an intelligent content preprocessor.\n\n"
        "Tasks:\n"
        "1. Detect the input type (bullet notes / transcript / rough ideas / paragraph / mixed-language).\n"
        "2. Fix grammar, repair fragmented ideas, reconstruct into coherent content.\n"
        "3. Preserve ALL original meaning, intent, and facts — do NOT add new information.\n"
        "4. For mixed-language input (e.g., Hinglish), normalise while preserving meaning.\n"
        "5. If input is only emojis or completely unusable, return it unchanged.\n"
        f"{language_instruction}\n"
        f"{input_type_hint}\n\n"
        f"Input:\n{content}\n\n"
        "Return ONLY the cleaned content with no explanations."
    )


# Transform logic
if transform_button:
    if not content.strip():
        st.error("⚠️ Please add some content first!")
    else:
        platform_name = platform_names[platforms.index(st.session_state.platform)]
        
        # Demo mode - use pre-generated responses
        if DEMO_MODE:
            with st.spinner(f"🔄 Generating demo transformation for {platform_name}..."):
                import time
                time.sleep(1.5)  # Simulate processing time
                
                st.session_state.result = DEMO_RESPONSES[st.session_state.platform]
                st.session_state.output_tokens = len(st.session_state.result) // 4
                st.session_state.transform_count += 1
                
                st.info("ℹ️ This is a demo transformation. Add your Google API key for real AI-powered transformations based on your content!")
                st.rerun()
        
        # Real API mode
        else:
            with st.spinner(f"🔄 Transforming for {platform_name}..."):
                try:
                    # Step 1: Normalize input if requested
                    content_to_transform = content
                    if normalize_input:
                        with st.spinner("🧹 Cleaning your input..."):
                            norm_prompt = _build_normalize_prompt(
                                content, input_type_value, output_lang_value
                            )
                            norm_response = client.models.generate_content(
                                model="gemini-2.0-flash-exp",
                                contents=norm_prompt
                            )
                            content_to_transform = norm_response.text.strip()
                            st.session_state.normalized_input = content_to_transform
                    else:
                        st.session_state.normalized_input = None
                    
                    # Step 2: Build platform prompt with parameters
                    params = {
                        'tone': tone,
                        'length': length,
                        'emoji': emoji,
                        'hashtags': hashtags,
                        'includeCTA': include_cta
                    }
                    
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
                    if output_lang_value != "auto":
                        param_instructions.append(f"Write the output in {output_lang_value}")
                    
                    additional_params = "\n".join([f"- {p}" for p in param_instructions]) if param_instructions else ""
                    
                    system_prompt = f"""You are an expert content repurposing specialist. Transform content for different social media platforms while maintaining the core message and value.

{f'Additional Requirements:{chr(10)}{additional_params}' if additional_params else ''}"""
                    
                    prompt = f"{system_prompt}\n\n{base_prompt}\n\nOriginal Content:\n{content_to_transform}"
                    
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
    
    # Side-by-side comparison when normalization was used
    if st.session_state.normalized_input:
        st.markdown("#### 🔍 Side-by-side Comparison")
        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            st.markdown("**📝 Original Input**")
            st.text_area("original", value=st.session_state.get('example_content', content), height=150, disabled=True, label_visibility="collapsed")
        with comp_col2:
            st.markdown("**🧹 Cleaned Input**")
            st.text_area("normalized", value=st.session_state.normalized_input, height=150, disabled=True, label_visibility="collapsed")
        st.markdown("---")
    
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
