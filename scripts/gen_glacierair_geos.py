#!/usr/bin/env python3
"""Generate GlacierAir landings + thank-you pages for all campaign geos."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_translations() -> dict:
    tr: dict = {}
    for name in ("_ga_i18n_part1", "_ga_i18n_part2", "_ga_i18n_part3"):
        path = Path(__file__).with_name(f"{name}.py")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        tr.update(mod.TRANSLATIONS)
    return tr


def was_price(now: float) -> float:
    return round(now / 0.3, 2)


def fmt_price(amount: float, currency: str) -> str:
    if currency == "RON":
        whole = int(amount)
        frac = int(round((amount - whole) * 100))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s},{frac:02d} lei"
    if currency == "CZK":
        whole = int(round(amount))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s},00 Kč"
    if currency == "HUF":
        whole = int(round(amount))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s} Ft"
    if currency == "PLN":
        whole = int(amount)
        frac = int(round((amount - whole) * 100))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s},{frac:02d} zł"
    # EUR
    s = f"{amount:.2f}".replace(".", ",")
    return f"{s} €"


GEOS = {
    # key: offer id; geo = country path; slug = glacierair-{offer_id}
    "1274": {"lang": "it", "price": 99.99, "currency": "EUR", "slug": "glacierair-1274", "tr": "it", "offer": "1274", "geo": "it"},
    "1278": {"lang": "de", "price": 109.00, "currency": "EUR", "slug": "glacierair-1278", "tr": "de", "offer": "1278", "geo": "de"},
    "1298": {"lang": "ro", "price": 549.00, "currency": "RON", "slug": "glacierair-1298", "tr": "ro", "offer": "1298", "geo": "ro"},
    "1414": {"lang": "pt", "price": 99.00, "currency": "EUR", "slug": "glacierair-1414", "tr": "pt", "offer": "1414", "geo": "pt"},
    "1415": {"lang": "es", "price": 99.00, "currency": "EUR", "slug": "glacierair-1415", "tr": "es", "offer": "1415", "geo": "es"},
    "1695": {"lang": "es", "price": 99.00, "currency": "EUR", "slug": "glacierair-1695", "tr": "es", "offer": "1695", "geo": "es"},
    "1726": {"lang": "pt", "price": 99.00, "currency": "EUR", "slug": "glacierair-1726", "tr": "pt", "offer": "1726", "geo": "pt"},
    "3062": {"lang": "pt", "price": 96.00, "currency": "EUR", "slug": "glacierair-3062", "tr": "pt", "offer": "3062", "geo": "pt"},
    "3063": {"lang": "de", "price": 109.00, "currency": "EUR", "slug": "glacierair-3063", "tr": "de", "offer": "3063", "geo": "de"},
    "3067": {"lang": "cs", "price": 2390.00, "currency": "CZK", "slug": "glacierair-3067", "tr": "cz", "offer": "3067", "geo": "cz"},
    "3292": {"lang": "sk", "price": 99.00, "currency": "EUR", "slug": "glacierair-3292", "tr": "sk", "offer": "3292", "geo": "sk"},
    "3293": {"lang": "sl", "price": 99.00, "currency": "EUR", "slug": "glacierair-3293", "tr": "si", "offer": "3293", "geo": "si"},
    "3294": {"lang": "hr", "price": 109.00, "currency": "EUR", "slug": "glacierair-3294", "tr": "hr", "offer": "3294", "geo": "hr"},
    "3295": {"lang": "hu", "price": 38999.00, "currency": "HUF", "slug": "glacierair-3295", "tr": "hu", "offer": "3295", "geo": "hu"},
    "3296": {"lang": "cs", "price": 2390.00, "currency": "CZK", "slug": "glacierair-3296", "tr": "cz", "offer": "3296", "geo": "cz"},
    "3297": {"lang": "pl", "price": 419.00, "currency": "PLN", "slug": "glacierair-3297", "tr": "pl", "offer": "3297", "geo": "pl"},
    "3344": {"lang": "pt", "price": 89.00, "currency": "EUR", "slug": "glacierair-3344", "tr": "pt", "offer": "3344", "geo": "pt"},
    "3345": {"lang": "es", "price": 99.00, "currency": "EUR", "slug": "glacierair-3345", "tr": "es", "offer": "3345", "geo": "es"},
    "3356": {"lang": "pl", "price": 419.00, "currency": "PLN", "slug": "glacierair-3356", "tr": "pl", "offer": "3356", "geo": "pl"},
    "4242": {"lang": "sk", "price": 99.00, "currency": "EUR", "slug": "glacierair-4242", "tr": "sk", "offer": "4242", "geo": "sk"},
    "4243": {"lang": "lv", "price": 99.00, "currency": "EUR", "slug": "glacierair-4243", "tr": "lv", "offer": "4243", "geo": "lv"},
}


LANDING_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18360404200"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'AW-18360404200');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="contact" content="info@homepickdock.com">
<meta name="theme-color" content="#14181f">
<link rel="canonical" href="https://homepickdock.com/{geo}/{slug}/landing.html">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/glacierair-landing.css">
<script>
window.SITE_CONFIG = {{
  GEO: '{geo}',
  PRODUCT_SLUG: '{slug}',
  CURRENCY: '{currency}',
  PRICE: {price_num},
  OFFER_NAME: 'GlacierAir {offer_name}',
  LP_ID: '{geo}-{offer_name}',
  FORM_ENDPOINT: 'https://TODO-network-endpoint.com/api/lead',
  SUBMITTING_LABEL: '{submitting}',
  COOKIE_TEXT: '{cookie_text}',
  COOKIE_ACCEPT: '{cookie_accept}',
  COOKIE_LEARN: '{cookie_learn}'
}};
</script>
<script src="/assets/js/tracking.js" defer></script>
</head>
<body>

<div class="topbar">{topbar}</div>

<div class="rating-strip wrap">
  <div class="stars">★★★★★</div>
  <div class="rating-text">{rating}</div>
</div>

<section class="hero wrap">
  <div class="hero-copy">
    <span class="gift-strip">{gift}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="hero-image hero-image-mobile-only">
      <img decoding="async" src="/assets/img/products/glacierair/hero.png?v=2" alt="{alt_hero}" width="560" height="560" loading="eager" fetchpriority="high">
    </div>
    <div class="price-block">
      <span class="was">{was}</span>
      <span class="now">{now}</span>
      <span class="pct">-70%</span>
    </div>
    <a href="#order-form" class="cta-btn">{cta}</a>
    <p class="form-note">{form_note_hero}</p>
  </div>
  <div class="hero-image hero-image-desktop-only">
    <img decoding="async" src="/assets/img/products/glacierair/hero.png?v=2" alt="{alt_hero}" width="560" height="560" loading="eager" fetchpriority="high">
  </div>
</section>

<div class="wrap">
  <div class="feature-row">
    <div class="feature-item"><div class="ico">❄️</div><h4>{f1_h}</h4><p>{f1_p}</p></div>
    <div class="feature-item"><div class="ico">🚫</div><h4>{f2_h}</h4><p>{f2_p}</p></div>
    <div class="feature-item"><div class="ico">🔇</div><h4>{f3_h}</h4><p>{f3_p}</p></div>
    <div class="feature-item"><div class="ico">💳</div><h4>{f4_h}</h4><p>{f4_p}</p></div>
  </div>
</div>

<section class="order-section" id="order-form">
  <div class="wrap">
    <div class="urgency-strip">
      <div class="countdown-row">
        <div class="countdown-label">{countdown}</div>
        <div class="countdown-timer" id="countdownTimer">
          <div class="box"><div class="num" id="cd-h">00</div><div class="lbl">{hours}</div></div>
          <div class="sep">:</div>
          <div class="box"><div class="num" id="cd-m">14</div><div class="lbl">{mins}</div></div>
          <div class="sep">:</div>
          <div class="box"><div class="num" id="cd-s">59</div><div class="lbl">{secs}</div></div>
        </div>
      </div>
      <div class="stock-row">
        <div class="stock-label"><span class="left">{stock_l}</span><span class="right">{stock_r}</span></div>
        <div class="stock-bar"><div class="stock-bar-fill"></div></div>
      </div>
      <div class="live-row">
        <span class="dot"></span>
        <span id="liveCount" data-live="{live}">{live0}</span>
      </div>
    </div>

    <div class="order-card">
      <h2>{form_h2}</h2>
      <p>{form_p}</p>
      <form class="tm-order-form order-form" action="{form_action}" method="post">
        <label for="name">{label_name}</label>
        <input id="name" type="text" name="name" autocomplete="name" placeholder="{ph_name}" required><br>
        <label for="tel">{label_phone}</label>
        <input id="tel" type="tel" name="tel" autocomplete="tel" placeholder="{ph_phone}" required><br>
        <label for="street-address">{label_addr}</label>
        <input id="street-address" type="text" name="street-address" autocomplete="street-address" placeholder="{ph_addr}" required><br>
        <input name="uid" type="hidden" value="{form_uid}" />
        <input name="offer" type="hidden" value="{offer_name}" />
        <input name="lp" type="hidden" value="{form_lp}" />
        <input name="thankyoupage" type="hidden" value="https://homepickdock.com/{geo}/{slug}/thank-you.html"/>
        <input name="webhook" type="hidden" value="{form_webhook}"/>
        <input name="_key" type="hidden" value="{form_key}" />
        <div style="margin-top: 10px; text-align: center">
          <button name="submit" type="submit">{btn}</button>
        </div>
        <p class="form-note">{form_note}</p>
        <script src="{form_script}" async></script>
      </form>
    </div>
  </div>
</section>

<section class="why-block wrap">
  <div class="why-grid">
    <div class="why-img"><img decoding="async" src="/assets/img/products/glacierair/desc-1.png?v=2" alt="{alt_d1}" loading="lazy"></div>
    <div>
      <div class="num-eyebrow">{ey1}</div>
      <h3>{h3_1}</h3>
      <div class="tag-row"><span class="tag">{tag1a}</span><span class="tag">{tag1b}</span><span class="tag">{tag1c}</span></div>
      <p>{p1}</p>
      <p class="italic">{i1}</p>
    </div>
  </div>
</section>

<section class="why-block wrap">
  <div class="why-grid">
    <div class="why-img"><img decoding="async" src="/assets/img/products/glacierair/desc-2.png?v=2" alt="{alt_d2}" loading="lazy"></div>
    <div>
      <div class="num-eyebrow">{ey2}</div>
      <h3>{h3_2}</h3>
      <div class="tag-row"><span class="tag">{tag2a}</span><span class="tag">{tag2b}</span><span class="tag">{tag2c}</span></div>
      <p>{p2}</p>
      <p class="italic">{i2}</p>
    </div>
  </div>
</section>

<section class="why-block wrap" style="border-bottom:none;">
  <div class="why-grid">
    <div class="why-img"><img decoding="async" src="/assets/img/products/glacierair/desc-3.png?v=2" alt="{alt_d3}" loading="lazy"></div>
    <div>
      <div class="num-eyebrow">{ey3}</div>
      <h3>{h3_3}</h3>
      <div class="tag-row"><span class="tag">{tag3a}</span><span class="tag">{tag3b}</span><span class="tag">{tag3c}</span></div>
      <p>{p3}</p>
      <p class="italic">{i3}</p>
    </div>
  </div>
</section>

<section class="compare wrap">
  <div class="section-label">{cmp_label}</div>
  <h2>{cmp_h2}</h2>
  <table>
    <tr><th></th><th>{th_trad}</th><th class="highlight">GlacierAir™</th></tr>
    <tr><td>{r1a}</td><td>{r1b}</td><td class="win">{r1c}</td></tr>
    <tr><td>{r2a}</td><td>{r2b}</td><td class="win">{r2c}</td></tr>
    <tr><td>{r3a}</td><td>{r3b}</td><td class="win">{r3c}</td></tr>
    <tr><td>{r4a}</td><td>{r4b}</td><td class="win">{r4c}</td></tr>
    <tr><td>{r5a}</td><td>{r5b}</td><td class="win">{r5c}</td></tr>
    <tr><td>{r6a}</td><td>{r6b}</td><td class="win">{r6c}</td></tr>
    <tr><td>{r7a}</td><td>{was}</td><td class="win">{now_only}</td></tr>
  </table>
</section>

<section class="testimonials">
  <div class="wrap">
    <div class="section-heading">
      <h2>{rev_h2}</h2>
      <span class="eyebrow" style="display:block;margin-top:8px;color:#5b6472;font-weight:600;text-transform:none;letter-spacing:0;font-size:14px;">{rev_sub}</span>
    </div>
    <div class="t-grid">
      <div class="testimonial">
        <img decoding="async" class="t-photo" src="/assets/img/reviews/glacierair/review-1.png?v=2" alt="GlacierAir — {rev1_a}" loading="lazy">
        <div class="t-body">
          <div class="stars">★★★★★</div>
          <h4>{rev1_h}</h4>
          <p>{rev1_p}</p>
          <div class="author-row"><div class="author">{rev1_a}</div></div>
        </div>
      </div>
      <div class="testimonial">
        <img decoding="async" class="t-photo" src="/assets/img/reviews/glacierair/review-2.png?v=2" alt="GlacierAir — {rev2_a}" loading="lazy">
        <div class="t-body">
          <div class="stars">★★★★★</div>
          <h4>{rev2_h}</h4>
          <p>{rev2_p}</p>
          <div class="author-row"><div class="author">{rev2_a}</div></div>
        </div>
      </div>
      <div class="testimonial">
        <img decoding="async" class="t-photo" src="/assets/img/reviews/glacierair/review-3.png?v=3" alt="GlacierAir — {rev3_a}" loading="lazy">
        <div class="t-body">
          <div class="stars">★★★★★</div>
          <h4>{rev3_h}</h4>
          <p>{rev3_p}</p>
          <div class="author-row"><div class="author">{rev3_a}</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="kit-section wrap">
  <div class="section-heading">
    <span class="eyebrow">{kit_eye}</span>
    <h2>{kit_h2}</h2>
  </div>
  <div class="kit-box">
    <img decoding="async" src="/assets/img/products/glacierair/kit.png?v=3" alt="{alt_kit}" loading="lazy">
    <div class="kit-content">
      <div class="price-block" style="margin-bottom:16px;">
        <span class="was">{was}</span>
        <span class="now">{now}</span>
        <span class="pct">-70%</span>
      </div>
      <ul>
        <li>{li1}</li>
        <li>{li2}</li>
        <li>{li3}</li>
        <li>{li4}</li>
        <li>{li5}</li>
        <li>{li6}</li>
      </ul>
      <a href="#order-form" class="cta-btn">{cta}</a>
    </div>
  </div>
</section>

<section class="faq wrap">
  <div class="section-heading">
    <h2>{faq_h2}</h2>
  </div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq1}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa1}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq2}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa2}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq3}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa3}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq4}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa4}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq5}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa5}</p></div></div>
</section>

<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a href="/" class="site-logo" aria-label="homepickdock.com home">
          <span class="site-logo__text"><span class="site-logo__text-primary">homepickdock</span><span class="site-logo__text-accent">.com</span></span>
        </a>
        <p class="site-footer__blurb">{footer_blurb}</p>
      </div>
      <div>
        <h4 class="site-footer__heading">{info}</h4>
        <ul class="site-footer__list">
          <li><a href="/{geo}/about-us.html">{about}</a></li>
          <li><a href="/{geo}/contact-us.html">{contact}</a></li>
          <li><a href="/{geo}/privacy-policy.html">{privacy}</a></li>
          <li><a href="/{geo}/terms-conditions.html">{terms}</a></li>
          <li><a href="/{geo}/cookie-policy.html">{cookie}</a></li>
          <li><a href="/{geo}/shipping-policy.html">{ship}</a></li>
          <li><a href="/{geo}/refund-policy.html">{refund}</a></li>
        </ul>
      </div>
      <div>
        <h4 class="site-footer__heading">{contacts}</h4>
        <ul class="site-footer__list">
          <li><strong>Netmart LLC</strong></li>
          <li>County of Sussex 16192 Coastal Hwy</li>
          <li>Lewes, DE 19958-3608, United States</li>
          <li><a href="mailto:info@homepickdock.com">info@homepickdock.com</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__bottom">
      © <span data-year>2026</span> <strong>Netmart LLC</strong> — {rights}
      <a href="/">homepickdock.com</a>
    </div>
  </div>
</footer>

<script src="/assets/js/glacierair-landing.js" defer></script>
<script>
  document.querySelectorAll('[data-year]').forEach(function (el) {{
    el.textContent = String(new Date().getFullYear());
  }});
</script>
</body>
</html>
"""


INDEX_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>Redirect…</title>
<script>
(function () {{
  var path = '/{geo}/{slug}/landing.html';
  window.location.replace(path + window.location.search + window.location.hash);
}})();
</script>
<meta http-equiv="refresh" content="0;url=/{geo}/{slug}/landing.html">
<link rel="canonical" href="https://homepickdock.com/{geo}/{slug}/landing.html">
</head>
<body>
<p><a href="/{geo}/{slug}/landing.html">GlacierAir™</a></p>
</body>
</html>
"""


def esc_js(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def render_landing(geo: str, cfg: dict, t: dict) -> str:
    was = fmt_price(was_price(cfg["price"]), cfg["currency"])
    now = fmt_price(cfg["price"], cfg["currency"])
    slug = cfg.get("slug", "glacierair")
    ctx = dict(t)
    # escape JS string fields
    for k in ("submitting", "cookie_text", "cookie_accept", "cookie_learn"):
        ctx[k] = esc_js(ctx[k])
    ctx.update(
        {
            "lang": cfg["lang"],
            "geo": geo,
            "slug": slug,
            "offer_name": cfg.get("offer", geo.upper()),
            "geo_upper": geo.upper(),
            "currency": cfg["currency"],
            "price_num": cfg["price"],
            "was": was,
            "now": now,
        }
    )
    # localized "only {price}" for compare row
    only_map = {
        "de": f"Nur {now}",
        "es": f"Solo {now}",
        "pt": f"Apenas {now}",
        "ro": f"Doar {now}",
        "cz": f"Jen {now}",
        "sk": f"Len {now}",
        "si": f"Le {now}",
        "hr": f"Samo {now}",
        "it": f"Solo {now}",
        "hu": f"Csak {now}",
        "pl": f"Tylko {now}",
        "lv": f"Tikai {now}",
    }
    ctx["now_only"] = only_map.get(geo, now)
    ctx["fa4"] = t["fa4"].replace("{price}", now)
    import importlib.util as _ilu

    _nf = Path(__file__).with_name("glacierair_network_forms.py")
    _spec = _ilu.spec_from_file_location("glacierair_network_forms", _nf)
    _mod = _ilu.module_from_spec(_spec)
    assert _spec.loader is not None
    _spec.loader.exec_module(_mod)
    offer_id = str(cfg.get("offer", ""))
    net = _mod.FORMS.get(offer_id, {"lp": "", "key": ""})
    ctx.update(
        {
            "form_action": _mod.ACTION,
            "form_script": _mod.SCRIPT,
            "form_uid": _mod.UID,
            "form_webhook": _mod.WEBHOOK,
            "form_lp": net["lp"],
            "form_key": net["key"],
        }
    )
    return LANDING_TMPL.format(**ctx)


def patch_thank_you(geo: str, cfg: dict, t: dict, it_ty: str) -> str:
    """Clone IT thank-you structure and fully localize + price/geo."""
    import re

    slug = cfg.get("slug", "glacierair")
    html = it_ty
    html = html.replace('lang="it"', f'lang="{cfg["lang"]}"', 1)
    html = html.replace("GEO: 'it'", f"GEO: '{geo}'")
    if "PRODUCT_SLUG:" in html:
        import re as _re

        html = _re.sub(r"PRODUCT_SLUG:\s*'[^']*'", f"PRODUCT_SLUG: '{slug}'", html)
    else:
        html = html.replace(f"GEO: '{geo}'", f"GEO: '{geo}',\n  PRODUCT_SLUG: '{slug}'")
    html = html.replace("CURRENCY: 'EUR'", f"CURRENCY: '{cfg['currency']}'")
    html = html.replace("PRICE: 99.99", f"PRICE: {cfg['price']}")
    html = html.replace(
        "trackPurchase(99.99, 'EUR')",
        f"trackPurchase({cfg['price']}, '{cfg['currency']}')",
    )
    html = html.replace(
        "COOKIE_TEXT: 'Usiamo cookie tecnici e di terze parti per migliorare la tua esperienza e per analisi.',\n  COOKIE_ACCEPT: 'Accetta',\n  COOKIE_LEARN: 'Scopri di più'",
        f"COOKIE_TEXT: '{t['cookie_text']}',\n  COOKIE_ACCEPT: '{t['cookie_accept']}',\n  COOKIE_LEARN: '{t['cookie_learn']}'",
    )
    html = re.sub(r"<title>.*?</title>", f"<title>{t['ty_title']}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content=".*?"\s*/?>',
        f'<meta name="description" content="{t["ty_desc"]}">',
        html,
        count=1,
    )
    if "ty_h1" in t:
        html = html.replace("Il tuo ordine è stato registrato con successo!", t["ty_h1"])
        html = html.replace(
            "Perfetto — il tuo ordine è in elaborazione. Manca solo <strong>un ultimo passaggio</strong> per completarlo e far partire la spedizione.",
            t["ty_sub"],
        )
        html = html.replace(
            "Il team homepickdock al lavoro: call center e logistica COD", t["ty_alt"]
        )
        html = html.replace("👇 Cosa devi fare adesso", t["ty_eyebrow"])
        html = html.replace("📞 Rispondi alla chiamata di conferma", t["ty_action_title"])
        html = html.replace(
            "Un nostro operatore ti contatterà <strong>nelle prossime ore</strong> per confermare il tuo ordine.",
            t["ty_action_body"],
        )
        html = html.replace(
            "Se non rispondi alla chiamata, l'ordine verrà automaticamente annullato.",
            t["ty_action_warn"],
        )
        html = html.replace("🕒 Orari di contatto", t["ty_hours_h"])
        html = html.replace("<strong>Lunedì – Sabato</strong> · 9:00 – 18:00", t["ty_hours"])
        html = html.replace("📋 Cosa succede dopo", t["ty_next_h"])
        it_steps = [
            "Rispondi alla chiamata e <strong>conferma i tuoi dati</strong>",
            "Il tuo ordine verrà spedito entro <strong>24–48 ore</strong>",
            "Consegna a domicilio e <strong>pagamento alla consegna</strong>",
        ]
        for ii, li in zip(it_steps, t["ty_steps"]):
            html = html.replace(f"<li>{ii}</li>", f"<li>{li}</li>")
        it_badges = ("🔒 Pagamento alla consegna", "🛡️ Garanzia 24 mesi", "🔐 Protezione SSL")
        for ib, lb in zip(it_badges, t["ty_badges"]):
            html = html.replace(ib, lb)
        footer_it = (
            "    <div>\n"
            '      <h4 class="site-footer__heading">Informazioni</h4>\n'
            '      <ul class="site-footer__list">\n'
            '        <li><a href="/it/about-us.html">Chi siamo</a></li>\n'
            '        <li><a href="/it/contact-us.html">Contattaci</a></li>\n'
            '        <li><a href="/it/privacy-policy.html">Privacy Policy</a></li>\n'
            '        <li><a href="/it/terms-conditions.html">Termini e Condizioni</a></li>\n'
            '        <li><a href="/it/cookie-policy.html">Cookie Policy</a></li>\n'
            '        <li><a href="/it/shipping-policy.html">Politica di Spedizione</a></li>\n'
            '        <li><a href="/it/refund-policy.html">Politica di Rimborso</a></li>\n'
            "      </ul>\n"
            "    </div>\n"
            "    <div>\n"
            '      <h4 class="site-footer__heading">Contatti</h4>'
        )
        footer_geo = (
            "    <div>\n"
            f'      <h4 class="site-footer__heading">{t["info"]}</h4>\n'
            '      <ul class="site-footer__list">\n'
            f'        <li><a href="/{geo}/about-us.html">{t["about"]}</a></li>\n'
            f'        <li><a href="/{geo}/contact-us.html">{t["contact"]}</a></li>\n'
            f'        <li><a href="/{geo}/privacy-policy.html">{t["privacy"]}</a></li>\n'
            f'        <li><a href="/{geo}/terms-conditions.html">{t["terms"]}</a></li>\n'
            f'        <li><a href="/{geo}/cookie-policy.html">{t["cookie"]}</a></li>\n'
            f'        <li><a href="/{geo}/shipping-policy.html">{t["ship"]}</a></li>\n'
            f'        <li><a href="/{geo}/refund-policy.html">{t["refund"]}</a></li>\n'
            "      </ul>\n"
            "    </div>\n"
            "    <div>\n"
            f'      <h4 class="site-footer__heading">{t["contacts"]}</h4>'
        )
        html = html.replace(footer_it, footer_geo)
        html = html.replace("Tutti i diritti riservati.", t["rights"] + ".")
    html = html.replace("/it/", f"/{geo}/")
    # Google Ads conversion value = CPA/CPL EUR for this offer
    import importlib.util as _ilu

    _nf = Path(__file__).with_name("glacierair_network_forms.py")
    _spec = _ilu.spec_from_file_location("glacierair_network_forms", _nf)
    _mod = _ilu.module_from_spec(_spec)
    assert _spec.loader is not None
    _spec.loader.exec_module(_mod)
    offer_id = str(cfg.get("offer", ""))
    cpa = _mod.CPA.get(offer_id)
    if cpa is not None:
        html = re.sub(r"'value':\s*[0-9.]+", f"'value': {cpa}", html)
        html = re.sub(
            r"<!-- Google Ads Purchase conversion — value = CPA/CPL EUR for offer #\d+ -->",
            f"<!-- Google Ads Purchase conversion — value = CPA/CPL EUR for offer #{offer_id} -->",
            html,
        )
    return html

def update_italian_prices() -> None:
    path = ROOT / "it/glacierair-1274/landing.html"
    text = path.read_text(encoding="utf-8")
    was = fmt_price(was_price(99.99), "EUR")
    now = fmt_price(99.99, "EUR")
    text = text.replace("PRICE: 74.99", "PRICE: 99.99")
    text = text.replace("74,99 €", now)
    text = text.replace("249,99 €", was)
    # compare row old was might already be updated
    path.write_text(text, encoding="utf-8")
    ty = ROOT / "it/glacierair-1274/thank-you.html"
    ty_t = ty.read_text(encoding="utf-8")
    ty_t = ty_t.replace("PRICE: 74.99", "PRICE: 99.99")
    ty_t = ty_t.replace("trackPurchase(74.99, 'EUR')", "trackPurchase(99.99, 'EUR')")
    ty.write_text(ty_t, encoding="utf-8")
    print("Updated IT prices →", was, now)


def main(only: set[str] | None = None) -> None:
    tr_all = load_translations()
    update_italian_prices()
    it_ty = (ROOT / "it/glacierair-1274/thank-you.html").read_text(encoding="utf-8")

    for offer_id, cfg in GEOS.items():
        if only is not None and offer_id not in only:
            continue
        geo = cfg["geo"]
        slug = cfg["slug"]
        tr_key = cfg["tr"]
        if tr_key == "it":
            # Italian source pages are maintained separately; only ensure paths/prices
            continue
        t = tr_all[tr_key]
        out_dir = ROOT / geo / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        landing = render_landing(geo, cfg, t)
        (out_dir / "landing.html").write_text(landing, encoding="utf-8")
        (out_dir / "index.html").write_text(
            INDEX_TMPL.format(lang=cfg["lang"], geo=geo, slug=slug), encoding="utf-8"
        )
        (out_dir / "thank-you.html").write_text(
            patch_thank_you(geo, cfg, t, it_ty), encoding="utf-8"
        )
        print(f"Wrote {geo}/{slug}/ (#{offer_id}) — {fmt_price(cfg['price'], cfg['currency'])}")


if __name__ == "__main__":
    import sys

    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    main(only)
