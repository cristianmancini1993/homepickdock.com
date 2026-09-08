// ============================================================
// MAIN — site-wide bootstrap (cookie banner, year, smooth scroll)
// ============================================================

(function () {
  document.addEventListener('DOMContentLoaded', function () {
    // Inject current year
    const years = document.querySelectorAll('[data-year]');
    const y = new Date().getFullYear();
    years.forEach((el) => (el.textContent = y));

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        const id = link.getAttribute('href');
        if (!id || id === '#') return;
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });

    // Cookie banner (simple consent, persisted in localStorage)
    const KEY = 'df_cookie_consent';
    if (!localStorage.getItem(KEY)) {
      const banner = document.createElement('div');
      banner.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#0f172a;color:#fff;padding:1rem;z-index:1000;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:1rem;font-size:0.875rem;box-shadow:0 -4px 12px rgba(0,0,0,0.2)';
      const cookieText = (window.SITE_CONFIG && window.SITE_CONFIG.COOKIE_TEXT) || 'We use cookies to improve your experience and for analytics.';
      const cookieAccept = (window.SITE_CONFIG && window.SITE_CONFIG.COOKIE_ACCEPT) || 'Accept';
      const cookieLearn = (window.SITE_CONFIG && window.SITE_CONFIG.COOKIE_LEARN) || 'Learn more';
      banner.innerHTML = '<span>' + cookieText + '</span>' +
        '<a href="/' + (window.SITE_CONFIG && window.SITE_CONFIG.GEO || 'it') + '/cookie-policy.html" style="color:#86efac;text-decoration:underline">' + cookieLearn + '</a>' +
        '<button id="df-cookie-ok" style="background:#16a34a;color:#fff;border:none;padding:0.5rem 1.25rem;border-radius:0.375rem;cursor:pointer;font-weight:700">' + cookieAccept + '</button>';
      document.body.appendChild(banner);
      document.getElementById('df-cookie-ok').addEventListener('click', function () {
        localStorage.setItem(KEY, '1');
        banner.remove();
      });
    }
  });
})();
