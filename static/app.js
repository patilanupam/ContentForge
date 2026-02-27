// ContentForge – with Input Normalization, Multilingual support & UX upgrades

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
Try these for a week and let me know your results! Like and subscribe for more!`,

    hinglish: `Kal client meeting tha, bahut acha gaya. Unhone product demo dekha aur bahut impressed hue.
Unka feedback tha ki UI simple hai aur workflow smooth hai.
Next steps: onboarding call schedule karna hai aur pricing discuss karni hai.
Overall ek positive outcome tha.`,

    notes: `startup idea
ai + legal courts
data aggregation
something about reducing delays
maybe an app?
lawyers + clients + judges
transparency missing rn`
};

// Platform character limits (per-output limits for reference)
const PLATFORM_LIMITS = {
    twitter: 280,        // per tweet
    linkedin: 3000,
    instagram: 2200,
    newsletter: null,    // no hard limit
    youtube: 5000
};

const PLATFORM_LIMIT_LABELS = {
    twitter: '280 chars/tweet',
    linkedin: '3,000 chars',
    instagram: '2,200 chars',
    newsletter: 'No limit',
    youtube: '5,000 chars'
};

let selectedPlatform = 'twitter';
let lastOriginalInput = '';

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    setupListeners();
    setupAccessibility();
});

// ---------------------------------------------------------------------------
// Listeners
// ---------------------------------------------------------------------------

function setupListeners() {
    const input = document.getElementById('content-input');
    const transformBtn = document.getElementById('transform-btn');

    // Char counter & token estimate
    input.addEventListener('input', () => {
        const chars = input.value.length;
        document.getElementById('chars').textContent = chars.toLocaleString();
        const tokens = Math.ceil(chars / 4);
        document.getElementById('input-tokens').textContent = tokens.toLocaleString();
    });

    // Examples
    document.querySelectorAll('.example-tag[data-type]').forEach(btn => {
        btn.addEventListener('click', () => {
            input.value = EXAMPLES[btn.dataset.type] || '';
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
            document.querySelectorAll('.pill').forEach(p => {
                p.classList.remove('active');
                p.setAttribute('aria-checked', 'false');
            });
            pill.classList.add('active');
            pill.setAttribute('aria-checked', 'true');
            selectedPlatform = pill.dataset.platform;
        });
        // Keyboard: space/enter selects
        pill.addEventListener('keydown', e => {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                pill.click();
            }
        });
    });

    // Normalize toggle — show/hide options
    const normalizeToggle = document.getElementById('normalize-toggle');
    normalizeToggle.addEventListener('change', () => {
        const options = document.getElementById('norm-options');
        options.hidden = !normalizeToggle.checked;
    });

    // Reset parameters
    document.getElementById('reset-params')?.addEventListener('click', () => {
        document.getElementById('tone-select').value = 'professional';
        document.getElementById('length-select').value = 'medium';
        document.getElementById('emoji-select').value = 'moderate';
        document.getElementById('hashtag-select').value = '5';
        document.getElementById('output-lang-select').value = 'auto';
        document.getElementById('cta-checkbox').checked = true;
        document.getElementById('normalize-toggle').checked = false;
        document.getElementById('input-type-select').value = 'auto';
        document.getElementById('norm-options').hidden = true;
        toast('Parameters reset');
    });

    // Transform
    transformBtn.addEventListener('click', transform);

    // Result actions
    document.getElementById('copy-result')?.addEventListener('click', copyResult);
    document.getElementById('download-result')?.addEventListener('click', downloadResult);
    document.getElementById('regenerate-result')?.addEventListener('click', transform);
    document.getElementById('toggle-comparison')?.addEventListener('click', toggleComparison);
}

// ---------------------------------------------------------------------------
// Accessibility
// ---------------------------------------------------------------------------

function setupAccessibility() {
    // High contrast toggle
    document.getElementById('contrast-toggle')?.addEventListener('click', function () {
        const on = document.body.classList.toggle('high-contrast');
        this.setAttribute('aria-pressed', String(on));
        localStorage.setItem('cf_high_contrast', on ? '1' : '0');
    });

    // Larger text toggle
    document.getElementById('text-size-toggle')?.addEventListener('click', function () {
        const on = document.body.classList.toggle('large-text');
        this.setAttribute('aria-pressed', String(on));
        localStorage.setItem('cf_large_text', on ? '1' : '0');
    });

    // Restore saved preferences
    if (localStorage.getItem('cf_high_contrast') === '1') {
        document.body.classList.add('high-contrast');
        document.getElementById('contrast-toggle')?.setAttribute('aria-pressed', 'true');
    }
    if (localStorage.getItem('cf_large_text') === '1') {
        document.body.classList.add('large-text');
        document.getElementById('text-size-toggle')?.setAttribute('aria-pressed', 'true');
    }
}

// ---------------------------------------------------------------------------
// Parameters
// ---------------------------------------------------------------------------

function getParameters() {
    return {
        tone: document.getElementById('tone-select')?.value || 'professional',
        length: document.getElementById('length-select')?.value || 'medium',
        emoji: document.getElementById('emoji-select')?.value || 'moderate',
        hashtags: parseInt(document.getElementById('hashtag-select')?.value || '5'),
        includeCTA: document.getElementById('cta-checkbox')?.checked ?? true
    };
}

function getNormalizationOptions() {
    return {
        normalize: document.getElementById('normalize-toggle')?.checked || false,
        inputType: document.getElementById('input-type-select')?.value || 'auto',
        outputLanguage: document.getElementById('output-lang-select')?.value || 'auto'
    };
}

// ---------------------------------------------------------------------------
// Transform
// ---------------------------------------------------------------------------

async function transform() {
    const content = document.getElementById('content-input').value.trim();

    if (!content) {
        toast('Please add some content first! 📝', 'error');
        return;
    }

    const btn = document.getElementById('transform-btn');
    const loading = document.getElementById('loading-overlay');
    const params = getParameters();
    const normOpts = getNormalizationOptions();

    lastOriginalInput = content;

    btn.disabled = true;
    loading.style.display = 'flex';

    try {
        const response = await fetch('/transform', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content,
                platform: selectedPlatform,
                parameters: params,
                normalize: normOpts.normalize,
                inputType: normOpts.inputType,
                outputLanguage: normOpts.outputLanguage
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to transform');
        }

        showResult(data.result, data.normalizedInput || null);

        // Update output tokens
        document.getElementById('output-tokens').textContent =
            Math.ceil(data.result.length / 4).toLocaleString();

        updateStats();
        toast('✨ Transformed successfully!', 'success');

    } catch (error) {
        toast(error.message, 'error');
    } finally {
        btn.disabled = false;
        loading.style.display = 'none';
    }
}

// ---------------------------------------------------------------------------
// Result display
// ---------------------------------------------------------------------------

const PLATFORM_NAMES = {
    twitter: 'Twitter',
    linkedin: 'LinkedIn',
    instagram: 'Instagram',
    newsletter: 'Newsletter',
    youtube: 'YouTube'
};

function showResult(text, normalizedInput) {
    document.getElementById('result-content').textContent = text;
    document.getElementById('result-platform-name').textContent =
        PLATFORM_NAMES[selectedPlatform] || selectedPlatform;
    document.getElementById('result-card').style.display = 'block';

    // Platform character limit bar
    renderCharLimitBar(text);

    // Comparison view
    const comparisonBtn = document.getElementById('toggle-comparison');
    const comparisonView = document.getElementById('comparison-view');

    if (normalizedInput) {
        document.getElementById('original-content-display').textContent = lastOriginalInput;
        document.getElementById('normalized-content-display').textContent = normalizedInput;
        comparisonBtn.hidden = false;
        // Auto-show comparison when normalization was used
        comparisonView.hidden = false;
        comparisonBtn.setAttribute('aria-pressed', 'true');
    } else {
        comparisonBtn.hidden = true;
        comparisonView.hidden = true;
        comparisonBtn.setAttribute('aria-pressed', 'false');
    }

    window.currentResult = text;

    document.getElementById('result-card').scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
    });
}

function renderCharLimitBar(text) {
    const bar = document.getElementById('char-limit-bar');
    const limit = PLATFORM_LIMITS[selectedPlatform];
    const label = PLATFORM_LIMIT_LABELS[selectedPlatform];

    if (!limit) {
        bar.textContent = `Output: ${text.length.toLocaleString()} chars — ${label}`;
        bar.className = 'char-limit-bar';
        bar.hidden = false;
        return;
    }

    const ratio = text.length / limit;
    const pct = Math.min(100, Math.round(ratio * 100));
    let cls = 'char-limit-bar';
    if (ratio > 1) cls += ' over-limit';
    else if (ratio > 0.9) cls += ' near-limit';

    bar.innerHTML =
        `<span>${text.length.toLocaleString()} / ${limit.toLocaleString()} chars (${label})</span>` +
        `<div class="limit-progress" aria-hidden="true">` +
        `<div class="limit-fill" style="width:${pct}%"></div></div>`;
    bar.className = cls;
    bar.hidden = false;
}

function toggleComparison() {
    const view = document.getElementById('comparison-view');
    const btn = document.getElementById('toggle-comparison');
    const isHidden = view.hidden;
    view.hidden = !isHidden;
    btn.setAttribute('aria-pressed', String(isHidden));
}

// ---------------------------------------------------------------------------
// Copy / Download
// ---------------------------------------------------------------------------

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

// ---------------------------------------------------------------------------
// Stats
// ---------------------------------------------------------------------------

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

// ---------------------------------------------------------------------------
// Toast
// ---------------------------------------------------------------------------

function toast(message, type = 'success') {
    const toastEl = document.getElementById('toast');
    toastEl.textContent = message;
    toastEl.className = `toast ${type}`;
    toastEl.classList.add('show');

    setTimeout(() => {
        toastEl.classList.remove('show');
    }, 3000);
}
