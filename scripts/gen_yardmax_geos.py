#!/usr/bin/env python3
"""Generate YardMax landings + thank-you pages for all campaign geos."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHROME_KEYS = (
    "submitting",
    "cookie_text",
    "cookie_accept",
    "cookie_learn",
    "form_note_hero",
    "hours",
    "mins",
    "secs",
    "stock_l",
    "stock_r",
    "label_name",
    "label_phone",
    "label_addr",
    "ph_name",
    "ph_phone",
    "ph_addr",
    "form_note",
    "footer_blurb",
    "info",
    "about",
    "contact",
    "privacy",
    "terms",
    "cookie",
    "ship",
    "refund",
    "contacts",
    "rights",
    "ty_title",
    "ty_desc",
    "ty_h1",
    "ty_sub",
    "ty_alt",
    "ty_eyebrow",
    "ty_action_title",
    "ty_action_body",
    "ty_action_warn",
    "ty_hours_h",
    "ty_hours",
    "ty_next_h",
    "ty_steps",
    "ty_badges",
)

FORM_NOTES = {
    "it": "🔒 Nessun anticipo · Nessuna carta · Paghi solo alla consegna",
    "pl": "🔒 Bez zaliczki · Bez karty · Płacisz dopiero przy odbiorze",
    "de": "🔒 Keine Vorauszahlung · Keine Karte · Sie zahlen erst bei Lieferung",
    "hu": "🔒 Nincs előleg · Nincs kártya · Csak átvételkor fizetsz",
    "es": "🔒 Sin anticipo · Sin tarjeta · Pagas solo a la entrega",
    "pt": "🔒 Sem adiantamento · Sem cartão · Paga só na entrega",
    "ro": "🔒 Fără avans · Fără card · Plătești doar la livrare",
    "lt": "🔒 Be avanso · Be kortelės · Mokate tik pristatymo metu",
    "cz": "🔒 Bez zálohy · Bez karty · Platíte až při doručení",
    "sk": "🔒 Bez zálohy · Bez karty · Platíte až pri doručení",
    "lv": "🔒 Bez priekšapmaksas · Bez kartes · Maksājat tikai saņemot",
}

PHONES = {
    "it": "+39 333 123 4567",
    "pl": "+48 512 345 678",
    "hu": "+36 30 123 4567",
    "de": "+49 170 1234567",
    "ro": "+40 721 123 456",
    "lt": "+370 612 34567",
    "cz": "+420 601 123 456",
    "pt": "+351 912 345 678",
    "es": "+34 612 345 678",
    "sk": "+421 901 123 456",
    "lv": "+371 21 234 567",
}


def load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_product() -> dict:
    tr = load_mod("_yardmax_i18n", Path(__file__).with_name("_yardmax_i18n.py")).TRANSLATIONS
    tr.update(
        load_mod(
            "_yardmax_i18n_part2", Path(__file__).with_name("_yardmax_i18n_part2.py")
        ).TRANSLATIONS
    )
    return tr


def load_chrome() -> dict:
    chrome: dict = {}
    for name in ("_ga_i18n_part1", "_ga_i18n_part2", "_ga_i18n_part3"):
        chrome.update(load_mod(name, Path(__file__).with_name(f"{name}.py")).TRANSLATIONS)
    dream = load_mod("_dreamora_i18n", Path(__file__).with_name("_dreamora_i18n.py")).TRANSLATIONS
    out: dict[str, dict] = {}
    langs = set(chrome) | set(dream)
    for lang in langs:
        merged: dict = {}
        if lang in chrome:
            merged.update({k: chrome[lang][k] for k in CHROME_KEYS if k in chrome[lang]})
        if lang in dream:
            merged.update({k: dream[lang][k] for k in CHROME_KEYS if k in dream[lang]})
        out[lang] = merged
    return out


def rebrand(value):
    if isinstance(value, (list, tuple)):
        return type(value)(rebrand(x) for x in value)
    if not isinstance(value, str):
        return value
    return (
        value.replace("Dreamora™", "YardMax™")
        .replace("GlacierAir™", "YardMax™")
        .replace("Dreamora", "YardMax")
        .replace("GlacierAir", "YardMax")
    )


def merge_tr(lang: str, product: dict, chrome: dict) -> dict:
    t = {k: rebrand(v) for k, v in chrome[lang].items()}
    t.update(product[lang])
    t["form_note"] = FORM_NOTES[lang]
    t["form_note_hero"] = FORM_NOTES[lang]
    t["ph_phone"] = PHONES[lang]
    return t


def was_price(now: float) -> float:
    raw = now / 0.4
    if abs(now - round(now)) < 0.001:
        return float(int(raw + 0.5))
    return round(raw + 1e-8, 2)


def fmt_price(amount: float, currency: str) -> str:
    wholeish = abs(amount - round(amount)) < 0.001
    if currency == "HUF":
        whole = int(round(amount))
        return f"{whole:,}".replace(",", ".") + " Ft"
    if currency == "CZK":
        whole = int(round(amount))
        return f"{whole:,}".replace(",", ".") + " Kč"
    if currency == "PLN":
        if wholeish:
            return f"{int(round(amount))} zł"
        whole = int(amount)
        frac = int(round((amount - whole) * 100))
        return f"{whole},{frac:02d} zł"
    if currency == "RON":
        if wholeish:
            return f"{int(round(amount))} lei"
        whole = int(amount)
        frac = int(round((amount - whole) * 100))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s},{frac:02d} lei"
    if wholeish:
        return f"{int(round(amount))} €"
    return f"{amount:.2f}".replace(".", ",") + " €"


GEOS = {
    "1650": {"lang": "it", "price": 79.99, "currency": "EUR", "slug": "yardmax-1650", "tr": "it", "offer": "1650", "geo": "it"},
    "1745": {"lang": "pl", "price": 359.00, "currency": "PLN", "slug": "yardmax-1745", "tr": "pl", "offer": "1745", "geo": "pl"},
    "1746": {"lang": "hu", "price": 32999.00, "currency": "HUF", "slug": "yardmax-1746", "tr": "hu", "offer": "1746", "geo": "hu"},
    "1748": {"lang": "de", "price": 79.00, "currency": "EUR", "slug": "yardmax-1748", "tr": "de", "offer": "1748", "geo": "de"},
    "2653": {"lang": "hu", "price": 32990.00, "currency": "HUF", "slug": "yardmax-2653", "tr": "hu", "offer": "2653", "geo": "hu"},
    "2657": {"lang": "ro", "price": 397.00, "currency": "RON", "slug": "yardmax-2657", "tr": "ro", "offer": "2657", "geo": "ro"},
    "3188": {"lang": "de", "price": 86.00, "currency": "EUR", "slug": "yardmax-3188", "tr": "de", "offer": "3188", "geo": "de"},
    "3189": {"lang": "lt", "price": 69.00, "currency": "EUR", "slug": "yardmax-3189", "tr": "lt", "offer": "3189", "geo": "lt"},
    "3190": {"lang": "cs", "price": 1499.00, "currency": "CZK", "slug": "yardmax-3190", "tr": "cz", "offer": "3190", "geo": "cz"},
    "3191": {"lang": "pt", "price": 69.00, "currency": "EUR", "slug": "yardmax-3191", "tr": "pt", "offer": "3191", "geo": "pt"},
    "3192": {"lang": "es", "price": 69.00, "currency": "EUR", "slug": "yardmax-3192", "tr": "es", "offer": "3192", "geo": "es"},
    "4065": {"lang": "sk", "price": 79.00, "currency": "EUR", "slug": "yardmax-4065", "tr": "sk", "offer": "4065", "geo": "sk"},
    "4066": {"lang": "lv", "price": 79.00, "currency": "EUR", "slug": "yardmax-4066", "tr": "lv", "offer": "4066", "geo": "lv"},
}


LANDING_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18430324200"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'AW-18430324200');
  gtag('config', 'AW-18373055367');
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
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "YardMax™",
  "image": "https://homepickdock.com/assets/img/products/yardmax/hero.webp",
  "description": "{description}",
  "brand": {{ "@type": "Brand", "name": "YardMax" }},
  "offers": {{
    "@type": "Offer",
    "price": "{price_schema}",
    "priceCurrency": "{currency}",
    "availability": "https://schema.org/InStock",
    "url": "https://homepickdock.com/{geo}/{slug}/landing.html"
  }},
  "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "12847" }}
}}
</script>
<script>
window.SITE_CONFIG = {{
  GEO: '{geo}',
  PRODUCT_SLUG: '{slug}',
  CURRENCY: '{currency}',
  PRICE: {price_num},
  OFFER_NAME: 'YardMax {offer_name}',
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
      <img decoding="async" src="/assets/img/products/yardmax/hero.webp?v=2" alt="{alt_hero}" width="560" height="560" loading="eager" fetchpriority="high">
    </div>
    <div class="price-block">
      <span class="was">{was}</span>
      <span class="now">{now}</span>
      <span class="pct">-60%</span>
    </div>
    <a href="#order-form" class="cta-btn">{cta}</a>
    <p class="form-note">{form_note_hero}</p>
  </div>
  <div class="hero-image hero-image-desktop-only">
    <img decoding="async" src="/assets/img/products/yardmax/hero.webp?v=2" alt="{alt_hero}" width="560" height="560" loading="eager" fetchpriority="high">
  </div>
</section>

<div class="wrap">
  <div class="feature-row">
    <div class="feature-item"><div class="ico">🚚</div><h4>{f1_h}</h4><p>{f1_p}</p></div>
    <div class="feature-item"><div class="ico">💳</div><h4>{f2_h}</h4><p>{f2_p}</p></div>
    <div class="feature-item"><div class="ico">🛡️</div><h4>{f3_h}</h4><p>{f3_p}</p></div>
    <div class="feature-item"><div class="ico">↩️</div><h4>{f4_h}</h4><p>{f4_p}</p></div>
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
        <input name="subid" id="subid" type="hidden" value="" />
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
    <div class="why-img"><img decoding="async" src="/assets/img/products/yardmax/desc-1.webp?v=3" alt="{alt_d1}" loading="lazy"></div>
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
    <div class="why-img">
      <video width="720" height="720" autoplay muted loop playsinline preload="metadata" poster="/assets/img/products/yardmax/desc-2.webp?v=2" aria-label="{alt_d2}">
        <source src="/assets/img/products/yardmax/desc-2.mp4" type="video/mp4">
      </video>
    </div>
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
    <div class="why-img"><img decoding="async" src="/assets/img/products/yardmax/desc-3.webp?v=3" alt="{alt_d3}" loading="lazy"></div>
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
    <tr><th></th><th>{th_trad}</th><th class="highlight">YardMax™</th></tr>
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
        <img decoding="async" class="t-photo" src="/assets/img/reviews/yardmax/review-2.webp?v=3" alt="YardMax — {rev1_a}" loading="lazy">
        <div class="t-body">
          <div class="stars">★★★★★</div>
          <h4>{rev1_h}</h4>
          <p>{rev1_p}</p>
          <div class="author-row"><div class="author">{rev1_a}</div></div>
        </div>
      </div>
      <div class="testimonial">
        <img decoding="async" class="t-photo" src="/assets/img/reviews/yardmax/review-1.webp?v=3" alt="YardMax — {rev2_a}" loading="lazy">
        <div class="t-body">
          <div class="stars">★★★★★</div>
          <h4>{rev2_h}</h4>
          <p>{rev2_p}</p>
          <div class="author-row"><div class="author">{rev2_a}</div></div>
        </div>
      </div>
      <div class="testimonial">
        <img decoding="async" class="t-photo" src="/assets/img/reviews/yardmax/review-3.webp?v=2" alt="YardMax — {rev3_a}" loading="lazy">
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
    <img decoding="async" src="/assets/img/products/yardmax/kit.webp?v=3" alt="{alt_kit}" loading="lazy">
    <div class="kit-content">
      <div class="price-block" style="margin-bottom:16px;">
        <span class="was">{was}</span>
        <span class="now">{now}</span>
        <span class="pct">-60%</span>
      </div>
      <ul>
        <li>{li1}</li>
        <li>{li2}</li>
        <li>{li3}</li>
        <li>{li4}</li>
        <li>{li5}</li>
        <li>{li6}</li>
        <li>{li7}</li>
        <li>{li8}</li>
      </ul>
      <a href="#order-form" class="cta-btn">{kit_cta}</a>
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
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq6}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa6}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq7}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa7}</p></div></div>
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
<p><a href="/{geo}/{slug}/landing.html">YardMax™</a></p>
</body>
</html>
"""


def esc_js(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def render_landing(geo: str, cfg: dict, t: dict, netmod) -> str:
    was = fmt_price(was_price(cfg["price"]), cfg["currency"])
    now = fmt_price(cfg["price"], cfg["currency"])
    slug = cfg["slug"]
    ctx = dict(t)
    for k in ("submitting", "cookie_text", "cookie_accept", "cookie_learn"):
        ctx[k] = esc_js(ctx[k])
    ctx.update(
        {
            "lang": cfg["lang"],
            "geo": geo,
            "slug": slug,
            "offer_name": cfg["offer"],
            "currency": cfg["currency"],
            "price_num": cfg["price"],
            "price_schema": f"{cfg['price']:.2f}",
            "was": was,
            "now": now,
        }
    )
    ctx["now_only"] = t["now_only"].replace("{price}", now)
    ctx["form_h2"] = t["form_h2"].replace("{price}", now)
    ctx["fa1"] = t["fa1"].replace("{price}", now)
    ctx["fa6"] = t["fa6"].replace(
        "{refund_link}",
        f'<a href="/{geo}/refund-policy.html">{t["refund_link_label"]}</a>',
    )
    ctx["fa7"] = (
        t["fa7"]
        .replace("{privacy_link}", f'<a href="/{geo}/privacy-policy.html">{t["privacy_link_label"]}</a>')
        .replace("{cookie_link}", f'<a href="/{geo}/cookie-policy.html">{t["cookie_link_label"]}</a>')
    )
    offer_id = str(cfg["offer"])
    net = netmod.FORMS[offer_id]
    ctx.update(
        {
            "form_action": netmod.ACTION,
            "form_script": netmod.SCRIPT,
            "form_uid": netmod.UID,
            "form_webhook": netmod.WEBHOOK,
            "form_lp": net["lp"],
            "form_key": net["key"],
        }
    )
    return LANDING_TMPL.format(**ctx)


def render_thank_you(geo: str, cfg: dict, t: dict, base_ty: str) -> str:
    slug = cfg["slug"]
    html = base_ty
    html = html.replace('lang="it"', f'lang="{cfg["lang"]}"', 1)
    html = re.sub(r"PRODUCT_SLUG:\s*'[^']*'", f"PRODUCT_SLUG: '{slug}'", html)
    html = html.replace("GEO: 'it'", f"GEO: '{geo}'")
    html = re.sub(r"CURRENCY:\s*'[^']*'", f"CURRENCY: '{cfg['currency']}'", html)
    html = re.sub(r"PRICE:\s*[0-9.]+", f"PRICE: {cfg['price']}", html)
    html = re.sub(r"CONVERSION_VALUE:\s*[0-9.]+", f"CONVERSION_VALUE: {cfg['cpa']}", html)
    html = re.sub(
        r"COOKIE_TEXT:\s*'[^']*',\s*\n\s*COOKIE_ACCEPT:\s*'[^']*',\s*\n\s*COOKIE_LEARN:\s*'[^']*'",
        f"COOKIE_TEXT: '{esc_js(t['cookie_text'])}',\n  COOKIE_ACCEPT: '{esc_js(t['cookie_accept'])}',\n  COOKIE_LEARN: '{esc_js(t['cookie_learn'])}'",
        html,
    )
    html = re.sub(r"<title>.*?</title>", f"<title>{t['ty_title']}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content=".*?"\s*/?>',
        f'<meta name="description" content="{t["ty_desc"]}">',
        html,
        count=1,
    )
    html = html.replace("Il tuo ordine è stato registrato con successo!", t["ty_h1"])
    html = html.replace(
        "Perfetto — il tuo ordine <strong>YardMax™</strong> è in elaborazione. Manca solo <strong>un ultimo passaggio</strong> per completarlo e far partire la spedizione.",
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
    html = re.sub(r"value:\s*[0-9.]+", f"value: {cfg['cpa']}", html)
    return html


def main(only: set[str] | None = None) -> None:
    product = load_product()
    chrome = load_chrome()
    netmod = load_mod("yardmax_network_forms", Path(__file__).with_name("yardmax_network_forms.py"))
    base_ty = (ROOT / "it/yardmax/thank-you.html").read_text(encoding="utf-8")

    missing = sorted(set(cfg["tr"] for cfg in GEOS.values()) - set(product))
    if missing:
        raise SystemExit(f"Missing YardMax translations: {missing}")

    for offer_id, cfg in GEOS.items():
        if only is not None and offer_id not in only:
            continue
        geo = cfg["geo"]
        slug = cfg["slug"]
        t = merge_tr(cfg["tr"], product, chrome)
        cfg = dict(cfg)
        cfg["cpa"] = netmod.CPA[offer_id]
        out_dir = ROOT / geo / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "landing.html").write_text(render_landing(geo, cfg, t, netmod), encoding="utf-8")
        (out_dir / "index.html").write_text(
            INDEX_TMPL.format(lang=cfg["lang"], geo=geo, slug=slug), encoding="utf-8"
        )
        (out_dir / "thank-you.html").write_text(
            render_thank_you(geo, cfg, t, base_ty), encoding="utf-8"
        )
        print(
            f"Wrote {geo}/{slug}/ (#{offer_id}) — {fmt_price(cfg['price'], cfg['currency'])} · CPA €{cfg['cpa']:g}"
        )


if __name__ == "__main__":
    import sys

    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    main(only)
