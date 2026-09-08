// ============================================================
// COUNTDOWN — sets a 24h countdown stored in localStorage
// Add data-countdown attribute to any element to render HH:MM:SS
// ============================================================

(function () {
  document.addEventListener('DOMContentLoaded', function () {
    const targets = document.querySelectorAll('[data-countdown]');
    if (!targets.length) return;

    const KEY = 'df_countdown_end';
    let end = parseInt(localStorage.getItem(KEY), 10);
    if (!end || end < Date.now()) {
      end = Date.now() + 24 * 60 * 60 * 1000;
      localStorage.setItem(KEY, String(end));
    }

    function pad(n) { return String(n).padStart(2, '0'); }

    function tick() {
      const ms = Math.max(0, end - Date.now());
      const h = Math.floor(ms / 3_600_000);
      const m = Math.floor((ms % 3_600_000) / 60_000);
      const s = Math.floor((ms % 60_000) / 1000);
      const text = pad(h) + ':' + pad(m) + ':' + pad(s);
      targets.forEach((t) => (t.textContent = text));
    }

    tick();
    setInterval(tick, 1000);
  });
})();
