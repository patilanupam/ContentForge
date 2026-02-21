// ContentForge - Simple & Creative with Parameters

const EXAMPLES = {
    blog: `Artificial Intelligence is transforming content creation. Here's how to use it effectively while maintaining your authentic voice.

Key benefits:
• Save 10+ hours per week on content repurposing
• Maintain consistency across all platforms
• Focus on strategy while AI handles formatting

The future is about humans + AI working together, not replacement.`,
    
    podcast: `Episode 25: Building Better Habits

Today's Key Points:
- Start with tiny habits (2 minutes or less)
- Stack new habits onto existing routines
- Focus on systems, not goals
- Track your progress visually
- Forgive yourself and start again

Remember: It's about progress, not perfection!`,
    
    video: `[Intro]
Hey everyone! Today I'm sharing 3 productivity tips that changed my life.

[Main Content]
Tip 1: Time block your calendar
Tip 2: Use the 2-minute rule
Tip 3: Batch similar tasks together

[Outro]
Try these for a week and let me know your results! Like and subscribe for more!`
};

let selectedPlatform = 'twitter';

// Init
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    setupListeners();
});

function setupListeners() {
    const input = document.getElementById('content-input');
    const transformBtn = document.getElementById('transform-btn');
    
    // Char counter & token estimate
    input.addEventListener('input', () => {
        const chars = input.value.length;
        document.getElementById('chars').textContent = chars;
        // Estimate tokens (rough: 1 token ≈ 4 chars)
        const tokens = Math.ceil(chars / 4);
        document.getElementById('input-tokens').textContent = tokens;
    });
    
    // Examples
    document.querySelectorAll('.example-tag[data-type]').forEach(btn => {
        btn.addEventListener('click', () => {
            input.value = EXAMPLES[btn.dataset.type];
            input.dispatchEvent(new Event('input'));
            toast('Example loaded! 🚀');
        });
    });
    
    // Clear
    document.getElementById('clear-all').addEventListener('click', () => {
        input.value = '';
        input.dispatchEvent(new Event('input'));
        document.getElementById('result-card').style.display = 'none';
    });
    
    // Platform selection
    document.querySelectorAll('.pill').forEach(pill => {
        pill.addEventListener('click', () => {
            document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            selectedPlatform = pill.dataset.platform;
        });
    });
    
    // Reset parameters
    document.getElementById('reset-params')?.addEventListener('click', () => {
        document.getElementById('tone-select').value = 'professional';
        document.getElementById('length-select').value = 'medium';
        document.getElementById('emoji-select').value = 'moderate';
        document.getElementById('hashtag-select').value = '5';
        document.getElementById('cta-checkbox').checked = true;
        toast('Parameters reset');
    });
    
    // Transform
    transformBtn.addEventListener('click', transform);
    
    // Result actions
    document.getElementById('copy-result')?.addEventListener('click', copyResult);
    document.getElementById('download-result')?.addEventListener('click', downloadResult);
    document.getElementById('regenerate-result')?.addEventListener('click', transform);
}

function getParameters() {
    return {
        tone: document.getElementById('tone-select')?.value || 'professional',
        length: document.getElementById('length-select')?.value || 'medium',
        emoji: document.getElementById('emoji-select')?.value || 'moderate',
        hashtags: parseInt(document.getElementById('hashtag-select')?.value || '5'),
        includeCTA: document.getElementById('cta-checkbox')?.checked || false
    };
}

async function transform() {
    const content = document.getElementById('content-input').value.trim();
    
    if (!content) {
        toast('Please add some content first! 📝', 'error');
        return;
    }
    
    const btn = document.getElementById('transform-btn');
    const loading = document.getElementById('loading-overlay');
    const params = getParameters();
    
    btn.disabled = true;
    loading.style.display = 'flex';
    
    try {
        const response = await fetch('/transform', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                content, 
                platform: selectedPlatform,
                parameters: params
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to transform');
        }
        
        showResult(data.result);
        
        // Update output tokens (estimate)
        const outputTokens = Math.ceil(data.result.length / 4);
        document.getElementById('output-tokens').textContent = outputTokens;
        
        updateStats();
        toast('✨ Transformed successfully!', 'success');
        
    } catch (error) {
        toast(error.message, 'error');
    } finally {
        btn.disabled = false;
        loading.style.display = 'none';
    }
}

function showResult(text) {
    const platformNames = {
        twitter: 'Twitter',
        linkedin: 'LinkedIn',
        instagram: 'Instagram',
        newsletter: 'Newsletter',
        youtube: 'YouTube'
    };
    
    document.getElementById('result-content').textContent = text;
    document.getElementById('result-platform-name').textContent = platformNames[selectedPlatform];
    document.getElementById('result-card').style.display = 'block';
    
    // Smooth scroll
    document.getElementById('result-card').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
    
    window.currentResult = text;
}

function copyResult() {
    const text = document.getElementById('result-content').textContent;
    navigator.clipboard.writeText(text)
        .then(() => toast('📋 Copied!', 'success'))
        .catch(() => toast('Failed to copy', 'error'));
}

function downloadResult() {
    const text = document.getElementById('result-content').textContent;
    const filename = `${selectedPlatform}_${Date.now()}.txt`;
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
    
    toast('⬇️ Downloaded!', 'success');
}

function updateStats() {
    const stats = JSON.parse(localStorage.getItem('cf_stats') || '{"count":0}');
    stats.count++;
    localStorage.setItem('cf_stats', JSON.stringify(stats));
    loadStats();
}

function loadStats() {
    const stats = JSON.parse(localStorage.getItem('cf_stats') || '{"count":0}');
    document.getElementById('total-count').textContent = stats.count;
    document.getElementById('total-transforms').textContent = stats.count;
}

function toast(message, type = 'success') {
    const toastEl = document.getElementById('toast');
    toastEl.textContent = message;
    toastEl.className = `toast ${type}`;
    toastEl.classList.add('show');
    
    setTimeout(() => {
        toastEl.classList.remove('show');
    }, 3000);
}
