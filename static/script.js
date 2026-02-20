document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    const transformBtn = document.getElementById('transform-btn');
    const platformBtns = document.querySelectorAll('.platform-btn');
    const outputSection = document.getElementById('output-section');
    const result = document.getElementById('result');
    const platformName = document.getElementById('platform-name');
    const copyBtn = document.getElementById('copy-btn');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');

    let selectedPlatform = 'twitter';

    const platformNames = {
        twitter: 'Twitter/X Thread',
        linkedin: 'LinkedIn Post',
        instagram: 'Instagram Caption',
        newsletter: 'Email Newsletter',
        youtube: 'YouTube Description'
    };

    // Platform selection
    platformBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            platformBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedPlatform = btn.dataset.platform;
        });
    });

    // Transform content
    transformBtn.addEventListener('click', async () => {
        const contentText = content.value.trim();
        
        if (!contentText) {
            showError('Please paste some content first!');
            return;
        }

        // Show loading
        loading.style.display = 'block';
        outputSection.style.display = 'none';
        error.style.display = 'none';
        transformBtn.disabled = true;

        try {
            const response = await fetch('/transform', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: contentText,
                    platform: selectedPlatform
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Something went wrong');
            }

            // Show result
            result.textContent = data.result;
            platformName.textContent = platformNames[selectedPlatform];
            outputSection.style.display = 'block';

        } catch (err) {
            showError(err.message);
        } finally {
            loading.style.display = 'none';
            transformBtn.disabled = false;
        }
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(result.textContent);
            copyBtn.textContent = '✅ Copied!';
            setTimeout(() => {
                copyBtn.textContent = '📋 Copy';
            }, 2000);
        } catch (err) {
            showError('Failed to copy to clipboard');
        }
    });

    function showError(message) {
        error.textContent = message;
        error.style.display = 'block';
        setTimeout(() => {
            error.style.display = 'none';
        }, 5000);
    }
});
