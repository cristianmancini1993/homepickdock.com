// ============================================================
// FORM HANDLER — validation, submit, redirect to thank-you page
// ============================================================

(function () {
  function getURLParam(name) {
    const u = new URL(window.location.href);
    return u.searchParams.get(name) || '';
  }

  function getTrackingContext() {
    if (window.getMeersmartTrackingContext) {
      return window.getMeersmartTrackingContext();
    }

    const urlSubid = getURLParam('subid');
    const campaignId = getURLParam('utm_campaign') || getURLParam('campaignid') || getURLParam('campaign_id') || urlSubid;
    return {
      campaign_id: campaignId,
      subid: urlSubid,
      gclid: getURLParam('gclid'),
      gbraid: getURLParam('gbraid'),
      wbraid: getURLParam('wbraid'),
      utm_source: getURLParam('utm_source'),
      utm_medium: getURLParam('utm_medium'),
      utm_campaign: getURLParam('utm_campaign') || campaignId,
      utm_term: getURLParam('utm_term'),
      utm_content: getURLParam('utm_content'),
    };
  }

  function appendTrackingParams(url, context) {
    if (window.appendMeersmartTrackingParams) {
      return window.appendMeersmartTrackingParams(url, context);
    }

    const out = new URL(url, window.location.origin);
    if (context.campaign_id) out.searchParams.set('campaign_id', context.campaign_id);
    if (context.subid) out.searchParams.set('subid', context.subid);
    if (context.utm_campaign) out.searchParams.set('utm_campaign', context.utm_campaign);
    if (context.utm_source) out.searchParams.set('utm_source', context.utm_source);
    if (context.utm_medium) out.searchParams.set('utm_medium', context.utm_medium);
    if (context.utm_term) out.searchParams.set('utm_term', context.utm_term);
    if (context.utm_content) out.searchParams.set('utm_content', context.utm_content);
    return out.pathname + out.search;
  }

  function generateFingerprint() {
    return [
      navigator.userAgent,
      navigator.language,
      screen.width + 'x' + screen.height,
      new Date().getTimezoneOffset(),
    ].join('|').split('').reduce((h, c) => ((h << 5) - h + c.charCodeAt(0)) | 0, 0).toString(36);
  }

  function validateField(field) {
    const input = field.querySelector('.cod-form__input');
    if (!input) return true;
    const value = input.value.trim();
    let valid = true;

    if (input.required && !value) valid = false;

    if (input.name === 'name' && value) {
      // Min 3 chars, no digits, must contain at least 2 words ideally
      if (value.length < 3 || /\d/.test(value)) valid = false;
    }
    if (input.name === 'phone' && value) {
      // Allow + and digits, min 7 digits
      const digits = value.replace(/\D/g, '');
      if (digits.length < 7 || digits.length > 16) valid = false;
    }
    if (input.name === 'address' && value) {
      if (value.length < 10) valid = false;
    }

    field.classList.toggle('has-error', !valid);
    input.classList.toggle('is-invalid', !valid);
    return valid;
  }

  function validateForm(form) {
    const fields = form.querySelectorAll('.cod-form__field');
    let allValid = true;
    fields.forEach((f) => {
      if (!validateField(f)) allValid = false;
    });
    return allValid;
  }

  function applyOrderDisabled(form) {
    const C = window.SITE_CONFIG || {};
    if (!C.ORDER_DISABLED) return false;
    form.classList.add('cod-form--order-disabled');
    const noteText = C.ORDER_DISABLED_NOTE
      || 'Ordering is temporarily unavailable for this product.';
    const subtitle = form.querySelector('.cod-form__subtitle');
    const note = document.createElement('p');
    note.className = 'cod-form__order-disabled-note';
    note.setAttribute('role', 'alert');
    note.textContent = noteText;
    if (subtitle) subtitle.insertAdjacentElement('afterend', note);
    else form.insertAdjacentElement('afterbegin', note);

    form.querySelectorAll('input, textarea, select, button[type="submit"]').forEach(function (el) {
      el.disabled = true;
    });
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.textContent = C.ORDER_DISABLED_CTA_LABEL || 'Unavailable — out of stock';
    return true;
  }

  async function submitOrderForm(form) {
    const C = window.SITE_CONFIG || {};
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const trackingContext = getTrackingContext();

    const payload = {
      ...data,
      id_offerta: getURLParam('offer_id'),
      offer: C.OFFER_NAME || '',
      lp: C.LP_ID || '',
      campaign_id: trackingContext.campaign_id,
      subid: trackingContext.subid || trackingContext.campaign_id,
      sub_id: trackingContext.subid || trackingContext.campaign_id,
      utm_source: trackingContext.utm_source,
      utm_campaign: trackingContext.utm_campaign || trackingContext.campaign_id,
      utm_medium: trackingContext.utm_medium,
      utm_term: trackingContext.utm_term,
      utm_content: trackingContext.utm_content,
      fingerprint: generateFingerprint(),
      geo: C.GEO || '',
      product: C.PRODUCT_SLUG || '',
      timestamp: new Date().toISOString(),
    };

    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.dataset.originalText = submitBtn.innerHTML;
      submitBtn.innerHTML = '⏳ ' + (C.SUBMITTING_LABEL || 'Invio in corso...');
    }

    const tyURL = appendTrackingParams('/' + C.GEO + '/' + C.PRODUCT_SLUG + '/thank-you.html', trackingContext);

    try {
      if (C.FORM_ENDPOINT && !C.FORM_ENDPOINT.includes('TODO')) {
        await fetch(C.FORM_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          mode: 'no-cors',
        });
      } else {
        // No endpoint configured: log payload for debugging
        console.log('[form-handler] FORM_ENDPOINT not configured. Payload:', payload);
      }
      if (window.trackLead) window.trackLead();
      window.location.href = tyURL;
    } catch (err) {
      console.error('[form-handler] submit error', err);
      // Fallback: still redirect, do not lose the lead
      if (window.trackLead) window.trackLead();
      window.location.href = tyURL;
    }
  }

  // ---- WIRE UP ----
  document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.cod-form');
    forms.forEach(function (form) {
      const disabledEarly = applyOrderDisabled(form);

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if ((window.SITE_CONFIG || {}).ORDER_DISABLED) return;
        if (!validateForm(form)) {
          const firstError = form.querySelector('.cod-form__field.has-error');
          if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
          return;
        }
        submitOrderForm(form);
      });

      if (disabledEarly) return;

      // Live validation
      form.querySelectorAll('.cod-form__field').forEach(function (field) {
        const input = field.querySelector('.cod-form__input');
        if (!input) return;
        input.addEventListener('blur', () => validateField(field));
        input.addEventListener('input', () => {
          if (field.classList.contains('has-error')) validateField(field);
        });
      });

      // Click on CTA -> InitiateCheckout fired before submit
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.addEventListener('click', function () {
          if (window.trackInitiateCheckout) window.trackInitiateCheckout();
        });
      }

    });
  });
})();
