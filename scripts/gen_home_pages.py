#!/usr/bin/env python3
"""Generate [geo]/index.html storefront homepages for all geos."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-08"
DOMAIN = "homepickdock.com"
COMPANY = "eazy commerce srls"

GEOS = [
    "it", "es", "fr", "de", "pt", "gr", "bg", "ro", "cz", "pl",
    "ee", "lv", "lt", "hr", "hu", "si", "sk", "en",
]

HREFLANG = {
    "it": "it", "es": "es", "fr": "fr", "de": "de", "pt": "pt", "gr": "el",
    "bg": "bg", "ro": "ro", "cz": "cs", "pl": "pl", "ee": "et", "lv": "lv",
    "lt": "lt", "hr": "hr", "hu": "hu", "si": "sl", "sk": "sk", "en": "en",
}

FAMILY_ORDER = [
    "hypertrimmer", "glacierair", "fold360", "vacuza", "yardmax", "dreamora", "mini-saw",
]

LEGAL_PAGES = (
    "about-us.html",
    "contact-us.html",
    "privacy-policy.html",
    "terms-conditions.html",
    "cookie-policy.html",
    "shipping-policy.html",
    "refund-policy.html",
)

CTA = {
    "it": "Scopri di più →",
    "en": "Learn more →",
    "es": "Descubre más →",
    "fr": "En savoir plus →",
    "de": "Mehr erfahren →",
    "pt": "Saiba mais →",
    "gr": "Μάθετε περισσότερα →",
    "bg": "Научете повече →",
    "ro": "Află mai multe →",
    "cz": "Zjistit více →",
    "pl": "Dowiedz się więcej →",
    "ee": "Loe edasi →",
    "lv": "Uzzināt vairāk →",
    "lt": "Sužinokite daugiau →",
    "hr": "Saznajte više →",
    "hu": "Tudj meg többet →",
    "si": "Izvedi več →",
    "sk": "Zistiť viac →",
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


def family_of(slug: str) -> str:
    return re.sub(r"-\d+$", "", slug)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_attr(html_text: str, attr: str) -> str:
    m = re.search(r'<html[^>]*\slang="([^"]+)"', html_text, re.I)
    if attr == "lang" and m:
        return m.group(1)
    return ""


def extract_site_config(privacy_html: str, geo: str) -> str:
    m = re.search(r"<script>\s*(window\.SITE_CONFIG\s*=\s*\{.*?\});\s*</script>", privacy_html, re.S)
    if m:
        return m.group(1)
    return f"window.SITE_CONFIG = {{ GEO: '{geo}' }}"


def extract_footer(privacy_html: str, geo: str) -> str:
    m = re.search(r'<footer class="site-footer">.*?</footer>', privacy_html, re.S)
    if not m:
        raise SystemExit(f"No footer in {geo}/privacy-policy.html")
    footer = m.group(0)
    footer = footer.replace('href="/"', f'href="/{geo}/"')
    return footer


def extract_nav_labels(geo: str) -> tuple[str, str]:
    about = read(ROOT / geo / "about-us.html")
    m = re.search(
        r'<nav class="site-header__nav"><a href="/[^"]*">([^<]+)</a>\s*<a href="/[^"]+/contact-us.html">([^<]+)</a>',
        about,
    )
    if m:
        return m.group(1).strip(), m.group(2).strip()
    m = re.search(
        r'<nav class="site-header__nav">\s*<a href="/[^"]*">([^<]+)</a>\s*<a href="/[^"]+/contact-us.html">([^<]+)</a>',
        about,
    )
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "Home", "Contact"


def extract_about_label(geo: str) -> str:
    contact = read(ROOT / geo / "contact-us.html")
    m = re.search(r'href="/' + geo + r'/about-us.html">([^<]+)</a>', contact)
    if m:
        return m.group(1).strip()
    about = read(ROOT / geo / "about-us.html")
    m = re.search(r"<h1>([^<]+)</h1>", about)
    return m.group(1).strip() if m else "About"


def fmt_price(value: float, geo: str) -> str:
    if geo == "en":
        return f"€{value:.2f}"
    text = f"{value:.2f}".replace(".", ",")
    return f"{text} €"


def product_page(geo: str, slug: str) -> Path | None:
    folder = ROOT / geo / slug
    landing = folder / "landing.html"
    index = folder / "index.html"
    if landing.exists():
        return landing
    if index.exists() and "window.location.replace" not in read(index):
        return index
    return None


def parse_product(geo: str, slug: str, page: Path) -> dict:
    text = read(page)
    family = family_of(slug)
    title_m = re.search(r"<title>([^<]+)</title>", text)
    title = title_m.group(1).split("|")[0].split("—")[0].strip() if title_m else slug.title()
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', text)
    if not desc_m:
        desc_m = re.search(r'<meta content="([^"]+)" name="description"', text)
    desc = desc_m.group(1).strip() if desc_m else ""
    if len(desc) > 180:
        cut = desc[:177]
        desc = cut.rsplit(" ", 1)[0] + "…"
    price_m = re.search(r"PRICE:\s*([0-9]+(?:\.[0-9]+)?)", text)
    price = float(price_m.group(1)) if price_m else None
    imgs = re.findall(r'(/assets/img/products/[^"\'?\s]+)', text)
    image = next((i for i in imgs if "/hero." in i), None)
    if not image:
        image = imgs[0] if imgs else f"/assets/img/products/{family}/hero.png"
    href = f"/{geo}/{slug}/landing.html" if page.name == "landing.html" else f"/{geo}/{slug}/"
    return {
        "slug": slug,
        "family": family,
        "title": title,
        "desc": desc,
        "price": price,
        "image": image,
        "href": href,
        "alt": title,
    }


def products_for_geo(geo: str) -> list[dict]:
    geo_dir = ROOT / geo
    by_family: dict[str, dict] = {}
    for child in sorted(geo_dir.iterdir()):
        if not child.is_dir():
            continue
        slug = child.name
        page = product_page(geo, slug)
        if not page:
            continue
        product = parse_product(geo, slug, page)
        family = product["family"]
        existing = by_family.get(family)
        if existing is None or ("-" not in slug and "-" in existing["slug"]):
            by_family[family] = product
    ordered = []
    seen = set()
    for family in FAMILY_ORDER:
        if family in by_family:
            ordered.append(by_family[family])
            seen.add(family)
    for family, product in by_family.items():
        if family not in seen:
            ordered.append(product)
    return ordered


def hreflang_tags() -> str:
    lines = []
    for geo in GEOS:
        lines.append(
            f'<link rel="alternate" hreflang="{HREFLANG[geo]}" href="https://{DOMAIN}/{geo}/">'
        )
    lines.append(f'<link rel="alternate" hreflang="x-default" href="https://{DOMAIN}/">')
    return "\n".join(lines)


def render_products(products: list[dict], geo: str, cta: str) -> str:
    cards = []
    for p in products:
        price_html = ""
        if p["price"] is not None:
            price_html = (
                f'<div class="product-card__price">'
                f'<span class="product-card__price-new">{html.escape(fmt_price(p["price"], geo))}</span>'
                f"</div>"
            )
        cards.append(
            f"""    <article class="product-card">
      <a class="product-card__image" href="{html.escape(p["href"])}">
        <img src="{html.escape(p["image"])}" alt="{html.escape(p["alt"])}" loading="lazy" decoding="async" width="640" height="480" onerror="this.src='/assets/img/placeholder.svg'">
      </a>
      <div class="product-card__body">
        <h3 class="product-card__title"><a href="{html.escape(p["href"])}">{html.escape(p["title"])}</a></h3>
        <p class="product-card__desc">{html.escape(p["desc"])}</p>
        {price_html}
        <a class="product-card__cta" href="{html.escape(p["href"])}">{html.escape(cta)}</a>
      </div>
    </article>"""
        )
    return "\n".join(cards)


def render_trust(items: list[dict]) -> str:
    blocks = []
    for item in items:
        blocks.append(
            f"""      <div class="trust-strip__item">
        <div class="trust-strip__icon">{item.get("icon", "")}</div>
        <div class="trust-strip__title">{html.escape(item.get("title", ""))}</div>
        <div class="trust-strip__sub">{html.escape(item.get("sub", ""))}</div>
      </div>"""
        )
    return "\n".join(blocks)


def render_why(items: list[dict]) -> str:
    blocks = []
    for item in items:
        blocks.append(
            f"""      <div class="why-us__item">
        <div class="why-us__icon">{item.get("icon", "")}</div>
        <h3 class="why-us__title">{html.escape(item.get("title", ""))}</h3>
        <p class="why-us__text">{html.escape(item.get("text", ""))}</p>
      </div>"""
        )
    return "\n".join(blocks)


def render_home(geo: str) -> str:
    copy = json.loads(read(ROOT / "content" / geo / "home.json"))
    privacy = read(ROOT / geo / "privacy-policy.html")
    lang = extract_attr(privacy, "lang") or HREFLANG[geo]
    home_label, contact_label = extract_nav_labels(geo)
    about_label = extract_about_label(geo)
    products = products_for_geo(geo)
    cta = (copy.get("products") or [{}])[0].get("cta") or CTA.get(geo, "→")
    meta = copy["meta"]
    hero = copy["hero"]
    why = copy["why_us"]
    reviews = copy["customer_reviews"]
    site_config = extract_site_config(privacy, geo)
    footer = extract_footer(privacy, geo)
    url = f"https://{DOMAIN}/{geo}/"
    desc = html.escape(meta["description"])
    title = html.escape(meta["title"])

    return f"""<!DOCTYPE html>
<html lang="{html.escape(lang)}">
<head>
{GTAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="contact" content="info@{DOMAIN}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#16a34a">
<link rel="canonical" href="{url}">
{hreflang_tags()}
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://{DOMAIN}/assets/img/products/hypertrimmer/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap">
<link rel="stylesheet" href="/assets/css/variables.css">
<link rel="stylesheet" href="/assets/css/reset.css">
<link rel="stylesheet" href="/assets/css/components.css">
<link rel="stylesheet" href="/assets/css/home.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{DOMAIN}",
  "url": "{url}",
  "publisher": {{
    "@type": "Organization",
    "name": "{COMPANY}",
    "url": "https://{DOMAIN}/"
  }}
}}
</script>
<script>{site_config};</script>
<script src="/assets/js/main.js" defer></script>
</head>
<body>

<header class="site-header"><div class="site-header__inner">
  <a href="/{geo}/" class="site-logo" aria-label="{DOMAIN}">
    <span class="site-logo__text"><span class="site-logo__text-primary">homepickdock</span><span class="site-logo__text-accent">.com</span></span>
  </a>
  <nav class="site-header__nav" aria-label="primary">
    <a href="/{geo}/">{html.escape(home_label)}</a>
    <a href="#products">{html.escape(copy.get("products_title", "Shop"))}</a>
    <a href="/{geo}/about-us.html">{html.escape(about_label)}</a>
    <a href="/{geo}/contact-us.html">{html.escape(contact_label)}</a>
  </nav>
</div></header>

<main>
  <section class="hero-home">
    <div class="container">
      <h1 class="hero-home__title">{html.escape(hero["title"])}</h1>
      <p class="hero-home__subtitle">{html.escape(hero["subtitle"])}</p>
    </div>
  </section>

  <section class="trust-strip">
    <div class="container">
      <div class="trust-strip__grid">
{render_trust(copy.get("trust_strip") or [])}
      </div>
    </div>
  </section>

  <section class="products-grid" id="products">
    <div class="container">
      <h2 class="section-title" style="text-align:center;margin-bottom:0.5rem">{html.escape(copy.get("products_title", ""))}</h2>
      <p class="section-subtitle" style="text-align:center;color:var(--color-text-muted);margin-bottom:2rem">{html.escape(copy.get("products_subtitle", ""))}</p>
      <div class="products-grid__list">
{render_products(products, geo, cta)}
      </div>
    </div>
  </section>

  <section class="why-us" id="why">
    <div class="container">
      <h2 class="section-title" style="text-align:center;margin-bottom:2rem">{html.escape(why["title"])}</h2>
      <div class="why-us__grid">
{render_why(why.get("items") or [])}
      </div>
    </div>
  </section>

  <section class="customer-reviews">
    <div class="container">
      <div class="customer-reviews__rating">
        <div class="customer-reviews__score">{html.escape(str(reviews.get("score", "")))}</div>
        <div class="customer-reviews__stars">{html.escape(reviews.get("stars", "★★★★★"))}</div>
        <div class="customer-reviews__count">{html.escape(reviews.get("count", ""))}</div>
      </div>
    </div>
  </section>
</main>

{footer}

</body>
</html>
"""


def patch_policy_home_links() -> None:
    for geo in GEOS:
        for name in LEGAL_PAGES:
            path = ROOT / geo / name
            if not path.exists():
                continue
            text = read(path)
            updated = re.sub(
                r'(<nav class="site-header__nav">)\s*<a href="/">',
                rf'\1<a href="/{geo}/">',
                text,
                count=1,
            )
            updated = updated.replace('href="/"', f'href="/{geo}/"')
            if updated != text:
                path.write_text(updated, encoding="utf-8")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = read(path)
    block_lines = [
        f'  <url><loc>https://{DOMAIN}/{geo}/</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>'
        for geo in GEOS
    ]
    block = "\n".join(block_lines) + "\n"
    text = re.sub(
        rf"  <url><loc>https://{DOMAIN}/(?:it|es|fr|de|pt|gr|bg|ro|cz|pl|ee|lv|lt|hr|hu|si|sk|en)/</loc>.*?</url>\n",
        "",
        text,
    )
    needle = f'  <url><loc>https://{DOMAIN}/</loc><lastmod>2026-04-28</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
    if needle not in text:
        raise SystemExit("Root sitemap URL not found")
    text = text.replace(needle, needle + block, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for geo in GEOS:
        html_out = render_home(geo)
        dest = ROOT / geo / "index.html"
        dest.write_text(html_out, encoding="utf-8")
        print(f"wrote {dest.relative_to(ROOT)}")
    patch_policy_home_links()
    update_sitemap()
    print("updated sitemap.xml and policy home links")


if __name__ == "__main__":
    main()
