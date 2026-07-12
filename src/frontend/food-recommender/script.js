// Reads message from the optional input, hits POST {API_RECOMMENDER}/display/recommendations,
// and renders the response.

const API_RECOMMENDER =
    (window.ORDERLY_CONFIG && window.ORDERLY_CONFIG.API_RECOMMENDER) || "";

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('get-recs-btn');
    if (btn) btn.addEventListener('click', loadRecommendations);
    loadRecommendations();
});

async function loadRecommendations() {
    const spinner = document.getElementById('loading-spinner');
    const container = document.getElementById('recommendations-container');
    const error = document.getElementById('error-message');
    const noRecs = document.getElementById('no-recommendations');
    const errorText = document.getElementById('error-message-text');

    spinner.style.display = 'block';
    container.style.display = 'none';
    error.style.display = 'none';
    noRecs.style.display = 'none';

    try {
        const msgEl = document.getElementById('user-message');
        const message = msgEl && msgEl.value ? msgEl.value.trim() : "";
        const menu = readStoredMenu();

        const url = API_RECOMMENDER + '/display/recommendations';
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message || "Recommend a dish", menu }),
        });

        if (!response.ok) {
            let detail = 'HTTP ' + response.status;
            try {
                const body = await response.json();
                if (body && body.detail) detail = body.detail;
            } catch (_) { /* keep generic */ }
            throw new Error(detail);
        }

        const data = await response.json();
        spinner.style.display = 'none';

        if (!data.recommendations || data.recommendations.length === 0) {
            noRecs.style.display = 'block';
            return;
        }

        container.style.display = 'block';
        renderDishes(data.recommendations);

    } catch (err) {
        console.error('Error loading the recommendations:', err);
        spinner.style.display = 'none';
        error.style.display = 'block';
        if (errorText) errorText.textContent = err.message || String(err);
    }
}

// Menu uploaded via the photo-upload page (photo_from_gallery/script.js),
// stashed in localStorage since that's a separate page load. Falls back to
// [] (backend's FALLBACK_POOL) if no menu was ever uploaded this session.
function readStoredMenu() {
    try {
        const raw = localStorage.getItem('orderly_menu');
        const parsed = raw ? JSON.parse(raw) : [];
        return Array.isArray(parsed) ? parsed : [];
    } catch (_) {
        return [];
    }
}

function renderDishes(dishes) {
    const grid = document.getElementById('dishes-grid');
    grid.innerHTML = '';

    dishes.forEach(dish => {
        const card = document.createElement('div');
        card.className = 'dish-card';

        const price = (dish.price === null || dish.price === undefined)
            ? ''
            : `<div class="price">${escapeHtml(dish.price)} $</div>`;

        card.innerHTML = `
            <div class="card-content">
                <h3>${escapeHtml(dish.name || '')}</h3>
                ${price}
                <div class="description">${escapeHtml(dish.description || '')}</div>
                ${dish.ingredients && dish.ingredients.length
                    ? `<div class="ingredients"> ${dish.ingredients.map(escapeHtml).join(' • ')}</div>`
                    : ''}
                ${dish.reason
                    ? `<div class="reason"> ${escapeHtml(dish.reason)}</div>`
                    : ''}
            </div>
        `;
        grid.appendChild(card);
    });
}

// Tiny HTML escaper to avoid XSS via AI-generated text.
function escapeHtml(s) {
    if (s === null || s === undefined) return '';
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}