# homepickdock.com — COD Multi-Geo Static Site

Static HTML/CSS/JS multi-geo e-commerce site for Cash On Delivery campaigns (Meta Ads / Google Ads).

**Stack**: vanilla HTML5 + CSS (custom variables, BEM) + vanilla ES6+ JS. Zero frameworks, zero build step.

## Quick facts

- **Domain**: homepickdock.com
- **Company**: eazy commerce srls — STRADA IV DESTRA, Via Lemitone 13, 81030 Casaluce, Italia
- **Contact email**: info@homepickdock.com (auto-derived from domain)
- **First product**: HyperTrimmer™ 3000 (slug: `hypertrimmer`) — battery-powered grass trimmer
- **Geos active**: 18 (it, es, fr, de, pt, gr, bg, ro, cz, pl, ee, lv, lt, hr, hu, si, sk, en)
- **Italian (`/it/`)**: fully translated with real copy
- **Other 17 geos**: structurally complete with Italian copy + translation banner — needs translation

## Folder structure

```
/
├── index.html                    Root landing-language picker
├── robots.txt
├── sitemap.xml                   127 URLs across 18 geos
├── favicon.svg
│
├── /assets/                      Shared by all geos
│   ├── /css/                     reset · variables · components · landing · thank-you · home
│   ├── /js/                      main · form-handler · popup-purchases · tracking · countdown
│   └── /img/
│       ├── /products/hypertrimmer/   ← drop hero.jpg, detail.jpg, lifestyle.jpg, package.jpg, feature-1/2/3.jpg, og-image.jpg
│       ├── /reviews/hypertrimmer/    ← drop review-1..6.jpg + expert.jpg
│       └── placeholder.svg           Used as fallback if .jpg missing
│
├── /content/                     Translatable copy (JSON)
│   └── /[geo]/
│       ├── home.json
│       ├── policies.json
│       └── /products/hypertrimmer/
│           ├── landing.json
│           └── thank-you.json
│
└── /[geo]/                       18 geo folders (it, es, fr, de, ...)
    ├── index.html                Home page
    ├── /hypertrimmer/
    │   ├── landing.html          22-section landing
    │   └── thank-you.html        5-section TY page (noindex)
    ├── privacy-policy.html
    ├── terms-conditions.html
    ├── cookie-policy.html
    ├── shipping-policy.html
    └── refund-policy.html
```

## Before going live — TODO checklist

### 1. Drop product images
Replace placeholders in:
- `/assets/img/products/hypertrimmer/` — `hero.jpg`, `detail.jpg`, `lifestyle.jpg`, `package.jpg`, `feature-1.jpg`, `feature-2.jpg`, `feature-3.jpg`, `og-image.jpg`
- `/assets/img/reviews/hypertrimmer/` — `review-1.jpg` … `review-6.jpg`, `expert.jpg`

If a JPG is missing, the HTML falls back to `/assets/img/placeholder.svg`.

### 2. Configure tracking pixels
Edit `window.SITE_CONFIG` block at the top of every `landing.html` and `thank-you.html`:

```js
window.SITE_CONFIG = {
  META_PIXEL_ID: '123456789012345',         // ← Meta Pixel ID
  GOOGLE_TAG_ID: 'G-XXXXXXXXXX',            // ← GA4 measurement ID
  GOOGLE_ADS_CONVERSION_ID: 'AW-123456789', // ← Google Ads conversion ID
  GOOGLE_ADS_CONVERSION_LABEL: 'abc123',    // ← Lead conversion label
  TY_CONVERSION_LABEL: 'xyz789',            // ← Purchase conversion label
  NETWORK_PIXEL_URL: '',                    // ← Optional ClickFlare/Voluum URL
  ...
};
```

Easiest way to update across all 18 geos: a single `sed -i` command from the root.

### 3. Configure form endpoint
In each `landing.html`, replace the placeholder:
```js
FORM_ENDPOINT: 'https://TODO-network-endpoint.com/api/lead'
```
with the real CRM/network endpoint that should receive the lead payload.

The payload posted is:
```json
{
  "name": "...", "phone": "...", "address": "...",
  "id_offerta": "...", "offer": "...", "lp": "...", "subid": "...",
  "utm_source": "...", "utm_campaign": "...", "utm_medium": "...",
  "fingerprint": "...", "geo": "it", "product": "hypertrimmer",
  "timestamp": "2026-04-27T..."
}
```

### 5. Translate the other 17 geos
Each non-IT geo currently shows Italian copy with a yellow translation banner. To translate a geo (e.g. Spanish):
1. Translate `content/es/products/hypertrimmer/landing.json`, `thank-you.json`, `home.json`, `policies.json`.
2. Translate the inline text in `es/index.html`, `es/hypertrimmer/landing.html`, `es/hypertrimmer/thank-you.html`, `es/privacy-policy.html`, `es/terms-conditions.html`, `es/cookie-policy.html`, `es/shipping-policy.html`, `es/refund-policy.html`.
3. Remove the yellow translation banner from each HTML file.

You can ask Claude/Claude Code to do this batch-translation pass for any geo.

### 6. Legal review (mandatory for Germany / EU)
The 5 policy files are template-grade. Have a lawyer review them — especially for:
- **Germany (`/de/`)**: Impressum requirements + strict consumer-protection law + LkSG / DSGVO penalties.
- **France (`/fr/`)**: CNIL cookie consent specifics.

## Deployment

This site is **100% static**. Deploy by uploading the entire `/homepickdock.com/` folder to any static host:

- **Cloudflare Pages**: connect a Git repo or drag-drop the folder. Done.
- **Netlify**: drag-drop into the Netlify dashboard, or `netlify deploy`.
- **Hostinger / cPanel hosting**: upload via FTP/SFTP to `public_html/`.
- **Vercel**: `vercel --prod` from the root folder.

No build step required. No server runtime. Pure HTML/CSS/JS.

## Adding more products

For each new product, repeat this structure within every geo:
```
/[geo]/[new-slug]/
  ├── landing.html
  └── thank-you.html
/content/[geo]/products/[new-slug]/
  ├── landing.json
  └── thank-you.json
/assets/img/products/[new-slug]/
/assets/img/reviews/[new-slug]/
```
Then add the product card to each `[geo]/index.html` and the URLs to `sitemap.xml`.

## File counts

- 144 HTML files (8 per geo × 18 geos)
- 72 JSON content files (4 per geo × 18 geos)
- 6 CSS files + 5 JS files in `/assets/`
- Plus root files (`index.html`, `robots.txt`, `sitemap.xml`, `favicon.svg`, `.gitignore`)

## License & ownership

© 2026 eazy commerce srls — All rights reserved.

Generated with the Landing Factory multi-geo static template.
