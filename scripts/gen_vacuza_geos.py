#!/usr/bin/env python3
"""Generate Vacuza landings + thank-you pages for campaign geos."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OFFERS = {
    "1211": {
        "geo": "si",
        "lang": "sl",
        "price": 99.0,
        "currency": "EUR",
        "cpa": 20.0,
        "was_display": "330 €",
        "now_display": "99 €",
        "schema_price": "99",
    },
    "1777": {
        "geo": "hu",
        "lang": "hu",
        "price": 33999.0,
        "currency": "HUF",
        "cpa": 17.0,
        "was_display": "113.330 Ft",
        "now_display": "33.999 Ft",
        "schema_price": "33999",
    },
    "2771": {
        "geo": "sk",
        "lang": "sk",
        "price": 99.0,
        "currency": "EUR",
        "cpa": 20.0,
        "was_display": "330 €",
        "now_display": "99 €",
        "schema_price": "99",
    },
    "2772": {
        "geo": "hr",
        "lang": "hr",
        "price": 99.0,
        "currency": "EUR",
        "cpa": 20.0,
        "was_display": "330 €",
        "now_display": "99 €",
        "schema_price": "99",
    },
    "2773": {
        "geo": "ro",
        "lang": "ro",
        "price": 497.0,
        "currency": "RON",
        "cpa": 20.0,
        "was_display": "1.657 lei",
        "now_display": "497 lei",
        "schema_price": "497",
    },
    "2774": {
        "geo": "pl",
        "lang": "pl",
        "price": 419.0,
        "currency": "PLN",
        "cpa": 20.0,
        "was_display": "1.397 zł",
        "now_display": "419 zł",
        "schema_price": "419",
    },
    "2775": {
        "geo": "cz",
        "lang": "cs",
        "price": 2490.0,
        "currency": "CZK",
        "cpa": 20.0,
        "was_display": "8.300 Kč",
        "now_display": "2.490 Kč",
        "schema_price": "2490",
    },
    "3646": {
        "geo": "lt",
        "lang": "lt",
        "price": 89.0,
        "currency": "EUR",
        "cpa": 16.0,
        "was_display": "297 €",
        "now_display": "89 €",
        "schema_price": "89",
    },
    "3648": {
        "geo": "cz",
        "lang": "cs",
        "price": 2099.0,
        "currency": "CZK",
        "cpa": 20.0,
        "was_display": "6.997 Kč",
        "now_display": "2.099 Kč",
        "schema_price": "2099",
        "source_geo": "cz",
        "form_lp": "3685",
        "form_key": "9da17a263b89395049186ed230874a3790ea932d",
        "price_replacements": [
            ("2.490 Kč", "2.099 Kč"),
            ("8.300 Kč", "6.997 Kč"),
            ("2490", "2099"),
        ],
    },
    "4011": {
        "geo": "es",
        "lang": "es",
        "price": 99.0,
        "currency": "EUR",
        "cpa": 18.0,
        "was_display": "330 €",
        "now_display": "99 €",
        "schema_price": "99",
    },
    "4012": {
        "geo": "pt",
        "lang": "pt",
        "price": 99.0,
        "currency": "EUR",
        "cpa": 18.0,
        "was_display": "330 €",
        "now_display": "99 €",
        "schema_price": "99",
    },
    "4013": {
        "geo": "de",
        "lang": "de",
        "price": 104.0,
        "currency": "EUR",
        "cpa": 18.0,
        "was_display": "347 €",
        "now_display": "104 €",
        "schema_price": "104",
    },
    "4019": {
        "geo": "lv",
        "lang": "lv",
        "price": 104.0,
        "currency": "EUR",
        "cpa": 16.0,
        "was_display": "347 €",
        "now_display": "104 €",
        "schema_price": "104",
    },
}

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18430324200"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'AW-18430324200');
  gtag('config', 'AW-18373055367');
</script>"""

ACQUISTO_SNIPPET = """<!-- Event snippet for Acquisto conversion page -->
<script>
  gtag('event', 'conversion', {
      'send_to': 'AW-18430324200/IIsjCPyKrPEcEOjbodRE',
      'transaction_id': ''
      // 'new_customer': true /* calculate dynamically, populate with true/false */,
  });
</script>"""

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
<p><a href="/{geo}/{slug}/landing.html">Vacuza™</a></p>
</body>
</html>
"""


FORM_TMPL = """      <form class="cod-form tm-order-form order-form" action="https://offers.adricenetwork.com/forms/html/" method="post">
        <div class="cod-form__field">
          <label class="cod-form__label" for="name">{name_label}</label>
          <input id="name" class="cod-form__input" type="text" name="name" autocomplete="name" placeholder="{name_ph}" required>
        </div>
        <div class="cod-form__field">
          <label class="cod-form__label" for="street-address">{addr_label}</label>
          <input id="street-address" class="cod-form__input" type="text" name="street-address" autocomplete="street-address" placeholder="{addr_ph}" required>
        </div>
        <div class="cod-form__field">
          <label class="cod-form__label" for="tel">{phone_label}</label>
          <input id="tel" class="cod-form__input" type="tel" name="tel" autocomplete="tel" placeholder="{phone_ph}" required>
        </div>
        <input name="uid" type="hidden" value="{uid}" />
        <input name="offer" type="hidden" value="{offer}" />
        <input name="lp" type="hidden" value="{lp}" />
        <input name="thankyoupage" type="hidden" value="{thankyou}"/>
        <input name="webhook" type="hidden" value="{webhook}"/>
        <input name="_key" type="hidden" value="{key}" />
        <div style="margin-top:10px;text-align:center">
          <button name="submit" type="submit">{btn}</button>
        </div>
        <p class="form-note">{form_note}</p>
        <script src="https://offers.adricenetwork.com/forms/html/js-v2/" async></script>
      </form>"""


def extract_form_meta(html: str) -> dict:
    def pick_label(field_id: str) -> str:
        m = re.search(rf'<label[^>]*for="{field_id}"[^>]*>([^<]+)</label>', html, re.I)
        return m.group(1).strip() if m else ""

    def pick_ph(field_id: str) -> str:
        m = re.search(rf'id="{field_id}"[^>]*placeholder="([^"]*)"', html, re.I)
        return m.group(1).strip() if m else ""

    thank = re.search(r'name="thankyoupage"[^>]*value="([^"]+)"', html)
    btn = re.search(r'<button name="submit"[^>]*>([^<]+)</button>', html)
    note = re.search(r'<form[\s\S]*?<p class="form-note">([^<]+)</p>', html)

    def pick_hidden(name: str) -> str:
        m = re.search(rf'name="{name}"[^>]*value="([^"]*)"', html, re.I)
        return m.group(1) if m else ""

    addr_label = pick_label("street-address") or pick_label("address")
    addr_ph = pick_ph("street-address") or pick_ph("address")
    phone_label = pick_label("tel") or pick_label("phone")
    phone_ph = pick_ph("tel") or pick_ph("phone")

    return {
        "name_label": pick_label("name") or "Name*",
        "name_ph": pick_ph("name") or pick_label("name").rstrip("*"),
        "addr_label": addr_label or "Address*",
        "addr_ph": addr_ph or addr_label.rstrip("*"),
        "phone_label": phone_label or "Phone*",
        "phone_ph": phone_ph or phone_label.rstrip("*"),
        "thankyou": thank.group(1) if thank else "",
        "btn": btn.group(1).strip() if btn else "Order now",
        "form_note": note.group(1).strip() if note else "",
        "uid": pick_hidden("uid") or "018e3961-c73a-7965-8fc1-b1d91c869a42",
        "offer": pick_hidden("offer"),
        "lp": pick_hidden("lp"),
        "key": pick_hidden("_key"),
        "webhook": pick_hidden("webhook") or "https://hook.eu2.make.com/w4wq67derax4vcu8h25pjgbl5s8z4r9a",
    }


def apply_cod_form(html: str) -> str:
    meta = extract_form_meta(html)
    new_form = FORM_TMPL.format(**meta)
    html = re.sub(r'<form class="(?:cod-form )?tm-order-form order-form"[\s\S]*?</form>', new_form, html, count=1)
    html = re.sub(r'\n<script src="/assets/js/network-params.js"></script>', "", html)
    html = re.sub(r'\n<script src="/assets/js/form-handler.js" defer></script>', "", html)
    html = html.replace(
        "FORM_ENDPOINT: 'https://TODO-network-endpoint.com/api/lead'",
        "FORM_ENDPOINT: 'https://offers.adricenetwork.com/forms/html/'",
    )
    html = html.replace(
        'value="https://hook.eu2.make.com/26cau8ymvxr5w61ologw0yuhmrvx84ok"',
        'value="https://hook.eu2.make.com/w4wq67derax4vcu8h25pjgbl5s8z4r9a"',
    )
    html = html.replace(
        'value="https://hook.eu2.make.com/bnamxchry4osb6t3p2fgmer3krqreofj"',
        'value="https://hook.eu2.make.com/w4wq67derax4vcu8h25pjgbl5s8z4r9a"',
    )
    return html


def fetch(url: str) -> str:
    out = subprocess.check_output(["curl", "-sL", url], text=True)
    return out


def normalize_gtag(html: str) -> str:
    html = re.sub(r"<!-- Google tag \(gtag\.js\) -->[\s\S]*?</script>\s*", "", html)
    html = re.sub(
        r'<script async src="https://www.googletagmanager.com/gtag/js[^"]*"></script>\s*<script>[\s\S]*?</script>\s*',
        "",
        html,
    )
    return html.replace("<head>", "<head>\n" + GTAG + "\n", 1)


def strip_hreflang(html: str) -> str:
    return re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?', "", html)


def transform_landing(html: str, offer_id: str, cfg: dict) -> str:
    geo = cfg["geo"]
    slug = f"vacuza-{offer_id}"
    source_geo = cfg.get("source_geo", geo)

    html = normalize_gtag(html)
    html = html.replace("Sweevo™", "Vacuza™")
    html = html.replace("Sweevo", "Vacuza")
    html = html.replace("sweevo", "vacuza")
    html = html.replace("gbyteit.com", "homepickdock.com")
    html = html.replace("info@gbyteit.com", "info@homepickdock.com")
    html = html.replace("SUPERADS INTERNATIONAL TECHNOLOGY LIMITED", "Netmart LLC")
    html = html.replace("RM 1502-A EASEY COMM BLDG 253-261 HENNESSY RD", "County of Sussex 16192 Coastal Hwy")
    html = html.replace("Wan Chai, Hong Kong", "Lewes, DE 19958-3608, United States")
    html = html.replace('site-logo__text-primary">gby</span><span class="site-logo__text-accent">teit', 'site-logo__text-primary">homepickdock</span><span class="site-logo__text-accent">.com')
    html = html.replace('aria-label="gbyteit home"', 'aria-label="homepickdock.com home"')
    html = html.replace(f'href="/{geo}/"', 'href="/"')
    html = html.replace('href="https://homepickdock.com/"', 'href="/"')
    html = html.replace("/assets/css/sweevo-landing.css", "/assets/css/vacuza-landing.css")
    html = html.replace("/assets/js/sweevo-landing.js", "/assets/js/vacuza-landing.js")
    html = re.sub(r"/assets/img/products/vacuza/([a-z0-9-]+)\.jpg\?v=2", r"/assets/img/products/vacuza/\1.jpg?v=3", html)
    html = re.sub(r"/assets/img/reviews/vacuza/([a-z0-9-]+)\.jpg\?v=2", r"/assets/img/reviews/vacuza/\1.jpg?v=3", html)

    html = strip_hreflang(html)
    html = html.replace(f"/{source_geo}/vacuza/", f"/{geo}/{slug}/")
    html = html.replace(f"PRODUCT_SLUG: 'vacuza'", f"PRODUCT_SLUG: '{slug}'")
    html = re.sub(r"OFFER_NAME: '[^']+'", f"OFFER_NAME: 'Vacuza {offer_id}'", html)
    html = re.sub(r"LP_ID: '[^']+'", f"LP_ID: '{geo}-{offer_id}'", html)
    html = re.sub(r"OFFER_ID: '\d+'", f"OFFER_ID: '{offer_id}'", html)
    html = re.sub(r'<input name="offer" type="hidden" value="\d+"', f'<input name="offer" type="hidden" value="{offer_id}"', html)

    if offer_id == "3648":
        html = re.sub(r'<input name="lp" type="hidden" value="\d+"', f'<input name="lp" type="hidden" value="{cfg["form_lp"]}"', html)
        html = re.sub(r'<input name="_key" type="hidden" value="[^"]+"', f'<input name="_key" type="hidden" value="{cfg["form_key"]}"', html)

    html = re.sub(r'"price": "\d+"', f'"price": "{cfg["schema_price"]}"', html)
    html = re.sub(r'"priceCurrency": "[^"]+"', f'"priceCurrency": "{cfg["currency"]}"', html)
    html = re.sub(r"PRICE: [0-9.]+", f"PRICE: {cfg['price']}", html)
    html = re.sub(r"CURRENCY: '[^']+'", f"CURRENCY: '{cfg['currency']}'", html)

    html = re.sub(r'<span class="was">[^<]+</span>', f'<span class="was">{cfg["was_display"]}</span>', html)
    html = re.sub(r'<span class="now">[^<]+</span>', f'<span class="now">{cfg["now_display"]}</span>', html)

    for old, new in cfg.get("price_replacements", []):
        html = html.replace(old, new)

    # FAQ cash-on-delivery amount
    html = re.sub(
        r"(<div class=\"faq-a\"><p>[^<]*<strong>)[^<]+(</strong>)",
        lambda m: m.group(1) + cfg["now_display"] + m.group(2),
        html,
        count=1,
        flags=re.DOTALL,
    )

    return apply_cod_form(html)


def transform_thank_you(html: str, offer_id: str, cfg: dict) -> str:
    geo = cfg["geo"]
    slug = f"vacuza-{offer_id}"
    source_geo = cfg.get("source_geo", geo)

    html = normalize_gtag(html)
    html = html.replace("Sweevo™", "Vacuza™")
    html = html.replace("Sweevo", "Vacuza")
    html = html.replace("gbyteit", "homepickdock")
    html = html.replace("info@gbyteit.com", "info@homepickdock.com")
    html = html.replace("SUPERADS INTERNATIONAL TECHNOLOGY LIMITED", "Netmart LLC")
    html = html.replace("RM 1502-A EASEY COMM BLDG 253-261 HENNESSY RD — Wan Chai, Hong Kong", "County of Sussex 16192 Coastal Hwy, Lewes, DE 19958-3608, United States")
    html = html.replace('site-logo__text-primary">gby</span><span class="site-logo__text-accent">teit', 'site-logo__text-primary">homepickdock</span><span class="site-logo__text-accent">.com')
    html = html.replace(f'href="/{geo}/"', 'href="/"')
    html = re.sub(r"PRODUCT_SLUG: '[^']+'", f"PRODUCT_SLUG: '{slug}'", html)
    html = re.sub(r"GEO: '[^']+'", f"GEO: '{geo}'", html)
    html = re.sub(r"CURRENCY: '[^']+'", f"CURRENCY: '{cfg['currency']}'", html)
    html = re.sub(r"PRICE: [0-9.]+", f"PRICE: {cfg['price']}", html)
    html = html.replace(f"/{source_geo}/vacuza/", f"/{geo}/{slug}/")
    html = re.sub(r"gtag\('event', 'conversion'.*?</script>\s*", "", html, flags=re.DOTALL)
    if "IIsjCPyKrPEcEOjbodRE" not in html:
        html = html.replace(GTAG, GTAG + "\n" + ACQUISTO_SNIPPET, 1)
    html = html.replace(
        "</body>",
        f"""<script>
  window.addEventListener('load', function () {{
    if (window.trackPurchase) window.trackPurchase({cfg['price']}, '{cfg['currency']}');
  }});
</script>
</body>""",
    )
    return html


def main() -> None:
    for offer_id, cfg in OFFERS.items():
        geo = cfg["geo"]
        slug = f"vacuza-{offer_id}"
        source_geo = cfg.get("source_geo", geo)
        out_dir = ROOT / geo / slug
        out_dir.mkdir(parents=True, exist_ok=True)

        landing_src = fetch(f"https://gbyteit.com/{source_geo}/sweevo/landing.html")
        landing_html = transform_landing(landing_src, offer_id, cfg)
        (out_dir / "landing.html").write_text(landing_html, encoding="utf-8")

        thank_src = fetch(f"https://gbyteit.com/{source_geo}/sweevo/thank-you.html")
        thank_html = transform_thank_you(thank_src, offer_id, cfg)
        (out_dir / "thank-you.html").write_text(thank_html, encoding="utf-8")

        index_html = INDEX_TMPL.format(lang=cfg["lang"], geo=geo, slug=slug)
        (out_dir / "index.html").write_text(index_html, encoding="utf-8")

        print(f"Wrote {geo}/{slug}/")


if __name__ == "__main__":
    main()
