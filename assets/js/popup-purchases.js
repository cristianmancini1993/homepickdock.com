// ============================================================
// POPUP PURCHASES — rotates fake-purchase notifications
// Reads list from window.POPUP_PURCHASES (set by content JSON)
// Timing:
//   FIRST_DELAY_MS  → wait before showing the first popup
//   VISIBLE_MS      → how long each popup stays fully visible
//   GAP_MS          → pause (no popup on screen) before the next one
// ============================================================

(function () {
  const FIRST_DELAY_MS = 4000;
  const VISIBLE_MS = 4000;
  const GAP_MS = 1000;
  const FADE_MS = 400;

  document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.popup-purchases');
    if (!container) return;

    if ((window.SITE_CONFIG || {}).ORDER_DISABLED) return;

    const items = window.POPUP_PURCHASES || [];
    if (!items.length) return;

    let index = 0;
    let card = null;
    let scheduled = null;

    function escapeHtml(s) {
      return String(s).replace(/[&<>"']/g, (c) => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
      })[c]);
    }

    function hideCurrent(cb) {
      if (!card) { if (cb) cb(); return; }
      const stale = card;
      card = null;
      stale.classList.remove('is-visible');
      setTimeout(() => {
        if (stale && stale.parentNode) stale.parentNode.removeChild(stale);
        if (cb) cb();
      }, FADE_MS);
    }

    function avatarHtml(item) {
      if (item.image) {
        const alt = escapeHtml(item.name || '');
        return `<div class="popup-purchase-card__avatar popup-purchase-card__avatar--photo">`
          + `<img src="${escapeHtml(item.image)}" alt="${alt}" width="40" height="40" loading="lazy" decoding="async">`
          + `</div>`;
      }
      return `<div class="popup-purchase-card__avatar">${escapeHtml(item.initial || '🛒')}</div>`;
    }

    function showOne() {
      const item = items[index % items.length];
      index++;

      card = document.createElement('div');
      card.className = 'popup-purchase-card';
      card.innerHTML = `
        ${avatarHtml(item)}
        <div class="popup-purchase-card__text">
          <span class="popup-purchase-card__name">${escapeHtml(item.name || '')}</span>
          ${escapeHtml(item.message || '')}
          <div class="popup-purchase-card__time">${escapeHtml(item.time || '')}</div>
        </div>
      `;
      container.appendChild(card);
      requestAnimationFrame(() => card && card.classList.add('is-visible'));

      // After VISIBLE_MS, fade out, then wait GAP_MS, then show next
      scheduled = setTimeout(() => {
        hideCurrent(() => {
          scheduled = setTimeout(showOne, GAP_MS);
        });
      }, VISIBLE_MS);
    }

    // Pause rotation when the tab is hidden, resume when visible again
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        if (scheduled) { clearTimeout(scheduled); scheduled = null; }
        hideCurrent();
      } else if (!scheduled && !card) {
        scheduled = setTimeout(showOne, GAP_MS);
      }
    });

    setTimeout(showOne, FIRST_DELAY_MS);
  });
})();
