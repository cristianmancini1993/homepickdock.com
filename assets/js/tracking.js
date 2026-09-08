// ============================================================
// TRACKING PIXELS — Centralizes Meta Pixel + Google Tag events
// ============================================================
// Configure IDs in window.SITE_CONFIG (set in <head> of every page).

(function () {
  const C = window.SITE_CONFIG || {};
  const CLICK_ID_KEYS = ['gclid', 'gbraid', 'wbraid'];
  const DEFAULT_GOOGLE_ADS_SEND_TO = 'AW-18373055367/cCCpCM3jueAcEIen-rhE';
  const CASHBOLT_SUBMIT_SESSION_KEY = 'df_cashbolt_submit';

  function getURLParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name) || '';
  }

  function getStoredParam(name) {
    try {
      return window.localStorage.getItem('df_' + name) || '';
    } catch (e) {
      return '';
    }
  }

  function setStoredParam(name, value) {
    if (!value) return;
    try {
      window.localStorage.setItem('df_' + name, value);
    } catch (e) {
      // Storage may be blocked; URL parameters still cover the active session.
    }
  }

  function captureClickIds() {
    CLICK_ID_KEYS.forEach(function (key) {
      const value = getURLParam(key);
      if (value) setStoredParam(key, value);
    });
  }

  function getTrackingContext() {
    captureClickIds();

    const utmCampaign = getURLParam('utm_campaign') || getURLParam('campaignid') || getURLParam('campaign_id');
    const urlSubid = getURLParam('subid');
    const context = {
      campaign_id: utmCampaign || urlSubid || getStoredParam('campaign_id'),
      subid: urlSubid || getStoredParam('subid'),
      gclid: getURLParam('gclid') || getStoredParam('gclid'),
      gbraid: getURLParam('gbraid') || getStoredParam('gbraid'),
      wbraid: getURLParam('wbraid') || getStoredParam('wbraid'),
      utm_source: getURLParam('utm_source') || getStoredParam('utm_source'),
      utm_medium: getURLParam('utm_medium') || getStoredParam('utm_medium'),
      utm_campaign: utmCampaign || getStoredParam('utm_campaign'),
      utm_term: getURLParam('utm_term') || getStoredParam('utm_term'),
      utm_content: getURLParam('utm_content') || getStoredParam('utm_content'),
    };

    Object.keys(context).forEach(function (key) {
      if (context[key]) setStoredParam(key, context[key]);
    });

    return context;
  }

  function hasCashboltSubmitCookie() {
    return document.cookie.split(';').some(function (part) {
      return part.trim() === 'df_cashbolt_submit=1';
    });
  }

  function setCashboltSubmitCookie() {
    document.cookie = 'df_cashbolt_submit=1;path=/;max-age=7200;SameSite=Lax';
  }

  function clearCashboltSubmitCookie() {
    document.cookie = 'df_cashbolt_submit=;path=/;max-age=0;SameSite=Lax';
  }

  function markCashboltFormSubmitted() {
    try {
      sessionStorage.setItem(CASHBOLT_SUBMIT_SESSION_KEY, '1');
    } catch (e) {
      // ignore
    }
    setStoredParam('cashbolt_submit', '1');
    setCashboltSubmitCookie();
  }

  function shouldFireThankYouConversion() {
    try {
      if (sessionStorage.getItem(CASHBOLT_SUBMIT_SESSION_KEY) === '1') return true;
    } catch (e) {
      // ignore
    }
    if (getStoredParam('cashbolt_submit') === '1') return true;
    if (hasCashboltSubmitCookie()) return true;

    const p = new URLSearchParams(window.location.search);
    if (p.get('order_id') || p.get('transaction_id') || p.get('tid')) return true;

    return false;
  }

  function clearCashboltSubmitMarkers() {
    try {
      sessionStorage.removeItem(CASHBOLT_SUBMIT_SESSION_KEY);
    } catch (e) {
      // ignore
    }
    try {
      localStorage.removeItem('df_cashbolt_submit');
    } catch (e) {
      // ignore
    }
    clearCashboltSubmitCookie();
  }

  function isCashboltOrderForm(form) {
    const action = form.action || '';
    return form.classList.contains('tm-order-form')
      || action.indexOf('supertrendaffiliateprogram.com') !== -1
      || action.indexOf('unbreakable-offers.com') !== -1;
  }

  function bindCashboltSubmitTracking(form) {
    if (form.dataset.dfCashboltSubmitBound === '1') return;
    form.dataset.dfCashboltSubmitBound = '1';

    form.addEventListener('submit', function () {
      markCashboltFormSubmitted();
    }, true);

    form.addEventListener('click', function (event) {
      const target = event.target;
      if (!target || target.type !== 'submit') return;
      if (!form.checkValidity()) return;
      markCashboltFormSubmitted();
    }, true);
  }

  function setHiddenField(form, name, value) {
    if (!value) return;
    let input = form.querySelector('input[name="' + name + '"]');
    if (!input) {
      input = document.createElement('input');
      input.type = 'hidden';
      input.name = name;
      form.appendChild(input);
    }
    input.value = value;
  }

  function appendTrackingParams(url, context) {
    if (!url) return url;
    try {
      const out = new URL(url, window.location.origin);
      if (context.campaign_id) out.searchParams.set('campaign_id', context.campaign_id);
      if (context.subid) out.searchParams.set('subid', context.subid);
      if (context.gclid) out.searchParams.set('gclid', context.gclid);
      if (context.gbraid) out.searchParams.set('gbraid', context.gbraid);
      if (context.wbraid) out.searchParams.set('wbraid', context.wbraid);
      if (context.utm_campaign) out.searchParams.set('utm_campaign', context.utm_campaign);
      if (context.utm_source) out.searchParams.set('utm_source', context.utm_source);
      if (context.utm_medium) out.searchParams.set('utm_medium', context.utm_medium);
      if (context.utm_term) out.searchParams.set('utm_term', context.utm_term);
      if (context.utm_content) out.searchParams.set('utm_content', context.utm_content);
      return out.toString();
    } catch (e) {
      return url;
    }
  }

  function wireCashboltForms(context) {
    document.querySelectorAll('form').forEach(function (form) {
      setHiddenField(form, 'subid', context.subid || context.campaign_id);
      setHiddenField(form, 'sub_id', context.subid || context.campaign_id);
      setHiddenField(form, 'campaign_id', context.campaign_id);
      setHiddenField(form, 'gclid', context.gclid);
      setHiddenField(form, 'gbraid', context.gbraid);
      setHiddenField(form, 'wbraid', context.wbraid);
      setHiddenField(form, 'utm_campaign', context.utm_campaign || context.campaign_id);
      setHiddenField(form, 'utm_source', context.utm_source);
      setHiddenField(form, 'utm_medium', context.utm_medium);
      setHiddenField(form, 'utm_term', context.utm_term);
      setHiddenField(form, 'utm_content', context.utm_content);

      const thankYouInput = form.querySelector('input[name="thankyoupage"]');
      if (thankYouInput) {
        thankYouInput.value = appendTrackingParams(thankYouInput.value, context);
      }

      if (isCashboltOrderForm(form)) {
        bindCashboltSubmitTracking(form);
      }
    });
  }

  window.getMeersmartTrackingContext = getTrackingContext;
  window.appendMeersmartTrackingParams = appendTrackingParams;
  window.markMeersmartCashboltSubmit = markCashboltFormSubmitted;
  // Legacy aliases
  window.getDevicegroveTrackingContext = getTrackingContext;
  window.appendDevicegroveTrackingParams = appendTrackingParams;
  window.markDevicegroveCashboltSubmit = markCashboltFormSubmitted;

  window.fireMeersmartThankYouConversion = function (options) {
    options = options || {};
    const cfg = window.SITE_CONFIG || {};

    if (!shouldFireThankYouConversion()) {
      if (cfg.DEBUG_TRACKING) {
        console.log('[tracking] Thank-you conversion skipped (no Cashbolt submit proof).');
      }
      return false;
    }

    if (!window.gtag) return false;

    const T = getTrackingContext();
    const p = new URLSearchParams(window.location.search);
    const transactionId = p.get('order_id') || p.get('transaction_id') || p.get('tid')
      || T.subid || T.campaign_id || ('df_' + Date.now());
    const dedupeKey = 'df_gads_conv_' + transactionId;

    try {
      if (localStorage.getItem(dedupeKey) === '1') return false;
      localStorage.setItem(dedupeKey, '1');
    } catch (e) {
      // ignore
    }

    const sendTo = options.send_to || cfg.GOOGLE_ADS_CONVERSION_SEND_TO || DEFAULT_GOOGLE_ADS_SEND_TO;
    // Conversion value = product CPA (CONVERSION_VALUE), fallback to PRICE
    const cpaValue = options.value != null
      ? options.value
      : (cfg.CONVERSION_VALUE != null ? cfg.CONVERSION_VALUE : (cfg.PRICE != null ? cfg.PRICE : 1.0));
    const payload = {
      send_to: sendTo,
      value: cpaValue,
      currency: options.currency || cfg.CONVERSION_CURRENCY || 'EUR',
      transaction_id: transactionId,
      campaign_id: T.campaign_id || '',
      subid: T.subid || T.campaign_id || '',
      utm_campaign: p.get('utm_campaign') || T.utm_campaign || T.campaign_id || '',
      utm_source: p.get('utm_source') || T.utm_source || '',
      utm_medium: p.get('utm_medium') || T.utm_medium || '',
      utm_term: p.get('utm_term') || T.utm_term || '',
      utm_content: p.get('utm_content') || T.utm_content || '',
    };

    if (T.gclid) payload.gclid = T.gclid;
    if (T.gbraid) payload.gbraid = T.gbraid;
    if (T.wbraid) payload.wbraid = T.wbraid;

    window.gtag('event', 'conversion', payload);
    clearCashboltSubmitMarkers();
    return true;
  };
  window.fireDevicegroveThankYouConversion = window.fireMeersmartThankYouConversion;

  captureClickIds();

  // ---- META PIXEL bootstrap ----
  if (C.META_PIXEL_ID) {
    !(function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', C.META_PIXEL_ID);
    window.fbq('track', 'PageView');
  }

  // ---- GOOGLE TAG bootstrap ----
  if (C.GOOGLE_TAG_ID) {
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + C.GOOGLE_TAG_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', C.GOOGLE_TAG_ID);
  }

  // ---- NETWORK PIXEL (Adrice / ClickFlare / Voluum) ----
  if (C.NETWORK_PIXEL_URL) {
    const pixelContext = getTrackingContext();
    const img = new Image();
    img.src = appendTrackingParams(C.NETWORK_PIXEL_URL, {
      subid: pixelContext.subid || pixelContext.campaign_id,
      gclid: pixelContext.gclid,
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    wireCashboltForms(getTrackingContext());
  });
})();

// ---- PUBLIC API ----
window.trackInitiateCheckout = function () {
  const C = window.SITE_CONFIG || {};
  const T = window.getMeersmartTrackingContext ? window.getMeersmartTrackingContext() : {};
  if (window.fbq) window.fbq('track', 'InitiateCheckout');
  if (window.gtag && C.GOOGLE_ADS_CONVERSION_ID) {
    window.gtag('event', 'begin_checkout', {
      campaign_id: T.campaign_id || '',
      subid: T.subid || '',
      utm_campaign: T.utm_campaign || '',
      utm_content: T.utm_content || '',
      utm_term: T.utm_term || '',
    });
  }
};

window.trackLead = function () {
  const C = window.SITE_CONFIG || {};
  const T = window.getMeersmartTrackingContext ? window.getMeersmartTrackingContext() : {};
  if (window.fbq) window.fbq('track', 'Lead');
  if (window.gtag && C.GOOGLE_ADS_CONVERSION_ID && C.GOOGLE_ADS_CONVERSION_LABEL) {
    window.gtag('event', 'conversion', {
      send_to: C.GOOGLE_ADS_CONVERSION_ID + '/' + C.GOOGLE_ADS_CONVERSION_LABEL,
      campaign_id: T.campaign_id || '',
      subid: T.subid || '',
      gclid: T.gclid || '',
      utm_campaign: T.utm_campaign || '',
      utm_content: T.utm_content || '',
      utm_term: T.utm_term || '',
    });
  }
};

window.trackPurchase = function (value, currency) {
  if (window.fireMeersmartThankYouConversion) {
    return window.fireMeersmartThankYouConversion({ value: value, currency: currency });
  }

  const C = window.SITE_CONFIG || {};
  const T = window.getMeersmartTrackingContext ? window.getMeersmartTrackingContext() : {};
  if (window.fbq) {
    window.fbq('track', 'Purchase', {
      value: value || C.PRICE || 0,
      currency: currency || C.CURRENCY || 'EUR',
      campaign_id: T.campaign_id || '',
      subid: T.subid || '',
    });
  }
  if (window.gtag && C.GOOGLE_ADS_CONVERSION_ID && C.TY_CONVERSION_LABEL) {
    window.gtag('event', 'conversion', {
      send_to: C.GOOGLE_ADS_CONVERSION_ID + '/' + C.TY_CONVERSION_LABEL,
      value: value || C.PRICE || 0,
      currency: currency || C.CURRENCY || 'EUR',
      campaign_id: T.campaign_id || '',
      subid: T.subid || '',
      gclid: T.gclid || '',
      utm_campaign: T.utm_campaign || '',
      utm_content: T.utm_content || '',
      utm_term: T.utm_term || '',
    });
  }
};
