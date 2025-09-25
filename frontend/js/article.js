
// Simple JS to toggle appearance controls
document.querySelectorAll('.controls .row .btn').forEach(btn => {
    btn.addEventListener('click', e => {
        const group = btn.closest('.row');
        group.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Apply effects
        if (btn.dataset.size) {
            const size = btn.dataset.size;
            if (size === 'small') document.documentElement.style.setProperty('--text', '#e6eef8'), document.body.style.fontSize = '13px';
            if (size === 'standard') document.body.style.fontSize = '15px';
            if (size === 'large') document.body.style.fontSize = '17px';
        }
        if (btn.dataset.width) {
            const w = btn.dataset.width;
            if (w === 'standard') document.querySelector('.container').style.maxWidth = '1200px';
            if (w === 'wide') document.querySelector('.container').style.maxWidth = '1600px';
        }
        if (btn.dataset.color) {
            const c = btn.dataset.color;
            if (c === 'dark') document.documentElement.style.setProperty('--bg', '#081018');
            if (c === 'light') document.documentElement.style.setProperty('--bg', '---text', '#f6f7fb');
            if (c === 'auto') document.documentElement.style.setProperty('--bg', '#0f1720');
        }
    })
})

function openImage() {
    // try to open included image file (may not be available in all environments)
    const path = '/mnt/data/1670ccff-ff26-45f8-8745-09f71f2b1625.jpg';
    window.open(path, '_blank');
}
