/* Demo data for updates (you can replace with API data) */
    const demoUpdates = [
      { id: 1, date: '2025-09-24', place: 'Chennai', summary: 'Heavy morning downpour; waterlogging in low-lying areas.', img: '' },
      { id: 2, date: '2025-09-24', place: 'Kochi', summary: 'Intermittent showers with cool breeze; river levels steady.', img: '' },
      { id: 3, date: '2025-09-23', place: 'Goa', summary: 'Light showers; skies clearing in the afternoon.', img: '' },
      { id: 4, date: '2025-09-22', place: 'Mumbai', summary: 'Showers with gusty winds near the coast.', img: '' }
    ];

    // Insert updates into the grid
    function renderUpdates() {
      const updatesEl = document.getElementById('updates');
      updatesEl.innerHTML = '';
      demoUpdates.forEach(u => {
        const card = document.createElement('article');
        card.className = 'update-card';
        card.innerHTML = `
        <div class="update-meta">${u.date} • <strong>${u.place}</strong></div>
        <h3>${u.summary}</h3>
        <div style="margin-top:8px; color:var(--muted); font-size:13px;">Share your local note below.</div>
      `;
        updatesEl.appendChild(card);
      });
    }

    // Simple in-memory comments store for demo
    const comments = [
      { name: 'Anita', text: 'Heavy rain in my neighborhood around 7 AM. Streets flooded near the market.' },
      { name: 'Ramesh', text: 'Light drizzle here. Nice cool weather.' }
    ];

    function renderComments() {
      const list = document.getElementById('comment-list');
      list.innerHTML = '';
      if (comments.length === 0) {
        list.innerHTML = '<div class="comment">No observations yet — be the first to post!</div>';
        return;
      }
      comments.slice().reverse().forEach(c => { // newest first
        const el = document.createElement('div');
        el.className = 'comment';
        el.innerHTML = `<small>${escapeHtml(c.name)} • ${new Date().toLocaleString()}</small><div>${escapeHtml(c.text)}</div>`;
        list.appendChild(el);
      });
    }

    // Escape to avoid XSS in demo
    function escapeHtml(s) {
      return s.replace(/[&<>"']/g, function (m) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m];
      });
    }

    // Hook up the comment form
    document.getElementById('comment-form').addEventListener('submit', function (e) {
      e.preventDefault();
      const name = document.getElementById('cname').value.trim();
      const text = document.getElementById('ctext').value.trim();
      if (!name || !text) return;
      comments.push({ name, text });
      renderComments();
      // reset & focus for accessibility
      e.target.reset();
      document.getElementById('cname').focus();
      // update stats (demo)
      document.getElementById('count-comments').textContent = parseInt(document.getElementById('count-comments').textContent) + 1;
    });

    // New observation button scrolls to the comment form and focuses input
    document.getElementById('new-observation').addEventListener('click', function () {
      const target = document.getElementById('cname');
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => target.focus(), 450);
    });

    // Ensure anchor focus for keyboard users when arriving via link
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', (ev) => {
        const id = a.getAttribute('href').slice(1);
        const target = document.getElementById(id);
        if (target) {
          // Allow browser's smooth scroll (CSS) then set focus
          setTimeout(() => target.focus({ preventScroll: true }), 500);
        }
      });
    });

    // Init render
    renderUpdates();
    renderComments();

    // OPTIONAL: Replace demo data with a fetch to your API:
    // fetch('/api/updates').then(r=>r.json()).then(data=>{ demoUpdates = data; renderUpdates(); });

