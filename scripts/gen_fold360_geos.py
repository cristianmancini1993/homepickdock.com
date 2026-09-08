#!/usr/bin/env python3
"""Generate Fold360 landing + thank-you pages for CZ, SI, HU, SK, PL."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IT_LP = (ROOT / "it/fold360/index.html").read_text(encoding="utf-8")
IT_TY = (ROOT / "it/fold360/thank-you.html").read_text(encoding="utf-8")

# Sale prices from offer sheet; old = round(sale / 0.3) for -70%
GEOS = {
    "cz": {
        "lang": "cs",
        "currency": "CZK",
        "price": 2449,
        "price_new": "2.449 Kč",
        "price_old": "8.163 Kč",
        "price_ready": "2.449 Kč",
        "country": "Česko",
        "footer_info": "Informace",
        "footer_contact": "Kontakt",
        "footer_rights": "Všechna práva vyhrazena",
        "footer_blurb": "Užitečné produkty pro každodenní život, doručení do 24–48 hodin s platbou na dobírku.",
        "links": [
            ("about-us.html", "O nás"),
            ("contact-us.html", "Kontaktujte nás"),
            ("privacy-policy.html", "Zásady ochrany osobních údajů"),
            ("terms-conditions.html", "Smluvní podmínky"),
            ("cookie-policy.html", "Zásady používání souborů cookie"),
            ("shipping-policy.html", "Zásady dopravy"),
            ("refund-policy.html", "Zásady vrácení peněz"),
        ],
        "cookie": {
            "text": "Používáme technické a cookies třetích stran ke zlepšení vašeho zážitku a pro analytiku.",
            "accept": "Přijmout",
            "learn": "Zjistit více",
        },
        "reviews": [
            ("Jan N.", "Praha", "Batteria e 3 schermi davvero utili.", "Pracuji celý den a baterie se nevybíjí: tři obrazovky jsou opravdu výhoda. Doporučuji!", "Batteria e 3 schermi davvero utili."),
            ("Marie K.", "Brno", "Comodo da usare, 5G sempre veloce.", "Je velmi pohodlný na psaní a připojení 5G je vždy rychlé. Moderní a praktický telefon.", "Comodo da usare, 5G sempre veloce."),
            ("Eva S.", "Ostrava", "Si ricarica in fretta ed è resistente.", "Rychle se nabíjí, je odolný vůči vodě a velmi pevný. Ideální pro moje tempo!", "Si ricarica in fretta ed è resistente."),
        ],
        "popups": [
            ("J", "Jan N.", "Praha"),
            ("M", "Marie K.", "Brno"),
            ("E", "Eva S.", "Ostrava"),
            ("P", "Petr H.", "Plzeň"),
            ("T", "Tomáš B.", "Liberec"),
            ("A", "Anna D.", "Olomouc"),
        ],
        "placeholders": {"name": "Např. Jan Novák", "phone": "Např. 601 123 456", "address": "Ulice, číslo, město, PSČ"},
        "lp": {},  # filled below
        "ty": {},
    },
    "si": {
        "lang": "sl",
        "currency": "EUR",
        "price": 99.99,
        "price_new": "99,99 €",
        "price_old": "333,30 €",
        "price_ready": "99,99 €",
        "country": "Slovenija",
        "footer_info": "Informacije",
        "footer_contact": "Kontakt",
        "footer_rights": "Vse pravice pridržane",
        "footer_blurb": "Uporabni izdelki za vsakdanje življenje, dostava v 24–48 urah s plačilom po povzetju.",
        "links": [
            ("about-us.html", "O nas"),
            ("contact-us.html", "Kontaktirajte nas"),
            ("privacy-policy.html", "Politika zasebnosti"),
            ("terms-conditions.html", "Pogoji in določila"),
            ("cookie-policy.html", "Politika piškotkov"),
            ("shipping-policy.html", "Politika pošiljanja"),
            ("refund-policy.html", "Politika vračil"),
        ],
        "cookie": {
            "text": "Uporabljamo tehnične piškotke in piškotke tretjih oseb za izboljšanje izkušnje in analitiko.",
            "accept": "Sprejmi",
            "learn": "Izvedi več",
        },
        "reviews": [
            ("Luka N.", "Ljubljana", "", "Cel dan delam in baterija se ne izprazni: trije zasloni so prava prednost. Priporočam!", ""),
            ("Maja K.", "Maribor", "", "Zelo priročen za pisanje in povezava 5G je vedno hitra. Sodoben in praktičen telefon.", ""),
            ("Eva P.", "Celje", "", "Hitro se polni, je vodoodporen in zelo trden. Idealno za moj tempo!", ""),
        ],
        "popups": [
            ("L", "Luka N.", "Ljubljana"),
            ("M", "Maja K.", "Maribor"),
            ("E", "Eva P.", "Celje"),
            ("A", "Andrej H.", "Koper"),
            ("T", "Tina B.", "Kranj"),
            ("S", "Simon D.", "Novo mesto"),
        ],
        "placeholders": {"name": "Npr. Luka Novak", "phone": "Npr. 041 123 456", "address": "Ulica, številka, mesto, pošta"},
    },
    "hu": {
        "lang": "hu",
        "currency": "HUF",
        "price": 36499,
        "price_new": "36.499 Ft",
        "price_old": "121.663 Ft",
        "price_ready": "36.499 Ft",
        "country": "Magyarország",
        "footer_info": "Információ",
        "footer_contact": "Kapcsolat",
        "footer_rights": "Minden jog fenntartva",
        "footer_blurb": "Hasznos termékek a mindennapokra, 24–48 órás szállítás utánvéttel.",
        "links": [
            ("about-us.html", "Rólunk"),
            ("contact-us.html", "Vegye fel velünk a kapcsolatot"),
            ("privacy-policy.html", "Adatvédelmi szabályzat"),
            ("terms-conditions.html", "Általános Szerződési Feltételek"),
            ("cookie-policy.html", "Cookie-szabályzat"),
            ("shipping-policy.html", "Szállítási szabályzat"),
            ("refund-policy.html", "Visszatérítési szabályzat"),
        ],
        "cookie": {
            "text": "Technikai és harmadik féltől származó sütiket használunk a jobb élmény és az elemzés érdekében.",
            "accept": "Elfogadom",
            "learn": "Tudjon meg többet",
        },
        "reviews": [
            ("János N.", "Budapest", "", "Egész nap dolgozom, és az akkumulátor nem merül le: a három képernyő igazi előny. Ajánlom!", ""),
            ("Mária K.", "Debrecen", "", "Nagyon kényelmes írni rajta, az 5G kapcsolat mindig gyors. Modern és praktikus telefon.", ""),
            ("Eszter P.", "Szeged", "", "Gyorsan töltődik, vízálló és nagyon masszív. Ideális az én tempómhoz!", ""),
        ],
        "popups": [
            ("J", "János N.", "Budapest"),
            ("M", "Mária K.", "Debrecen"),
            ("E", "Eszter P.", "Szeged"),
            ("P", "Péter H.", "Pécs"),
            ("A", "Anna B.", "Győr"),
            ("T", "Tamás D.", "Miskolc"),
        ],
        "placeholders": {"name": "Pl. Nagy János", "phone": "Pl. 20 123 4567", "address": "Utca, házszám, város, irányítószám"},
    },
    "sk": {
        "lang": "sk",
        "currency": "EUR",
        "price": 99.99,
        "price_new": "99,99 €",
        "price_old": "333,30 €",
        "price_ready": "99,99 €",
        "country": "Slovensko",
        "footer_info": "Informácie",
        "footer_contact": "Kontakt",
        "footer_rights": "Všetky práva vyhradené",
        "footer_blurb": "Užitočné produkty pre každodenný život, doručenie do 24–48 hodín s platbou na dobierku.",
        "links": [
            ("about-us.html", "O nás"),
            ("contact-us.html", "Kontaktujte nás"),
            ("privacy-policy.html", "Zásady ochrany osobných údajov"),
            ("terms-conditions.html", "Zmluvné podmienky"),
            ("cookie-policy.html", "Zásady používania súborov cookie"),
            ("shipping-policy.html", "Pravidlá prepravy"),
            ("refund-policy.html", "Pravidlá vrátenia peňazí"),
        ],
        "cookie": {
            "text": "Používame technické súbory cookie a súbory cookie tretích strán na zlepšenie vášho zážitku a na analýzu.",
            "accept": "Prijať",
            "learn": "Zistiť viac",
        },
        "reviews": [
            ("Ján N.", "Bratislava", "", "Pracujem celý deň a batéria sa nevybíja: tri obrazovky sú skutočná výhoda. Odporúčam!", ""),
            ("Mária K.", "Košice", "", "Je veľmi pohodlný na písanie a pripojenie 5G je vždy rýchle. Moderný a praktický telefón.", ""),
            ("Eva S.", "Žilina", "", "Rýchlo sa nabíja, je odolný voči vode a veľmi pevný. Ideálne pre moje tempo!", ""),
        ],
        "popups": [
            ("J", "Ján N.", "Bratislava"),
            ("M", "Mária K.", "Košice"),
            ("E", "Eva S.", "Žilina"),
            ("P", "Peter H.", "Prešov"),
            ("T", "Tomáš B.", "Nitra"),
            ("A", "Anna D.", "Trnava"),
        ],
        "placeholders": {"name": "Napr. Ján Novák", "phone": "Napr. 0901 123 456", "address": "Ulica, číslo, mesto, PSČ"},
    },
    "pl": {
        "lang": "pl",
        "currency": "PLN",
        "price": 429,
        "price_new": "429 zł",
        "price_old": "1.430 zł",
        "price_ready": "429 zł",
        "country": "Polska",
        "footer_info": "Informacje",
        "footer_contact": "Kontakt",
        "footer_rights": "Wszelkie prawa zastrzeżone",
        "footer_blurb": "Przydatne produkty na co dzień, dostawa w 24–48 godzin z płatnością przy odbiorze.",
        "links": [
            ("about-us.html", "O nas"),
            ("contact-us.html", "Skontaktuj się z nami"),
            ("privacy-policy.html", "Polityka prywatności"),
            ("terms-conditions.html", "Regulamin"),
            ("cookie-policy.html", "Polityka plików cookie"),
            ("shipping-policy.html", "Zasady wysyłki"),
            ("refund-policy.html", "Polityka zwrotów"),
        ],
        "cookie": {
            "text": "Używamy technicznych plików cookie i plików cookie stron trzecich w celu poprawy doświadczenia i analizy.",
            "accept": "Akceptuj",
            "learn": "Dowiedz się więcej",
        },
        "reviews": [
            ("Jan N.", "Warszawa", "", "Pracuję cały dzień, a bateria się nie wyczerpuje: trzy ekrany to prawdziwa zaleta. Polecam!", ""),
            ("Maria K.", "Kraków", "", "Bardzo wygodny do pisania, a połączenie 5G zawsze jest szybkie. Nowoczesny i praktyczny telefon.", ""),
            ("Ewa S.", "Gdańsk", "", "Szybko się ładuje, jest wodoodporny i bardzo solidny. Idealny do mojego tempa!", ""),
        ],
        "popups": [
            ("J", "Jan N.", "Warszawa"),
            ("M", "Maria K.", "Kraków"),
            ("E", "Ewa S.", "Gdańsk"),
            ("P", "Piotr H.", "Wrocław"),
            ("T", "Tomasz B.", "Poznań"),
            ("A", "Anna D.", "Łódź"),
        ],
        "placeholders": {"name": "Np. Jan Kowalski", "phone": "Np. 500 123 456", "address": "Ulica, numer, miasto, kod"},
    },
}

# Full UI copy per geo (Italian → local)
COPY = {
    "cz": {
        "title": "Fold360™ — Skládací smartphone se 3 obrazovkami | -70% Pouze dnes",
        "desc": "Fold360™: skládací smartphone se 3 obrazovkami, baterie 6800 mAh, fotoaparát 48 MP, 5G, Dual SIM, nabíjení 66W a funkce AI. Platba na dobírku, doručení 24/48 h.",
        "og_title": "Fold360™ — Skládací smartphone | -70% Pouze dnes",
        "og_desc": "Skládací smartphone se 3 obrazovkami, baterie 6800 mAh, fotoaparát 48 MP, 5G a Dual SIM. Platba na dobírku.",
        "json_name": "Fold360™ — Skládací smartphone se 3 obrazovkami",
        "json_desc": "Skládací smartphone Fold360™ se 3 obrazovkami, baterie 6800 mAh, nabíjení 66W, 5G, Dual SIM, fotoaparát 48 MP a funkce AI.",
        "banner": "🔥 ZÁRUKA 2 ROKY · PLATBA NA DOBÍRKU · -70% 🔥",
        "rating": '<strong>4,9/5</strong> — <strong>1.824</strong> pozitivních recenzí',
        "guarantee_line": "🛡️ Záruka 2 roky · Platba na dobírku",
        "h1": "Skládací smartphone se 3 obrazovkami, fotoaparátem 48 MPx a baterií 6.800 mAh",
        "sub": 'Inovativní technologie <strong>Fold360™</strong> nabízí ideální rovnováhu mezi stylem, mobilitou a funkčností: skládací design s velkým displejem, konektivita <strong>5G</strong>, funkce umělé inteligence, ultra-rychlé nabíjení a dlouhá výdrž baterie.',
        "discount_label": "SLEVA 70 % DO VYPRODÁNÍ ZÁSOB",
        "cta_order": "OBJEDNAT Fold360™ →",
        "no_prepay": "🔒 Žádná záloha · Žádná karta · Platíte až při doručení",
        "trust": [
            ("Consegna in 24-48h", "Doručení do 24–48 h", "Spedizione rapida in tutta Italia", "Rychlá doprava po celém Česku"),
            ("Pagamento alla consegna", "Platba na dobírku", "Paghi solo quando ricevi", "Platíte až při převzetí"),
            ("Garanzia 2 anni", "Záruka 2 roky", "Copertura ufficiale inclusa", "Oficiální krytí v ceně"),
            ("Reso 30 giorni", "Vrácení do 30 dnů", "Rimborso semplice e gratuito", "Jednoduché a bezplatné vrácení"),
        ],
        "countdown_label": "⏰ Nabídka -70 % vyprší za",
        "hours": "Hod",
        "mins": "Min",
        "secs": "Sek",
        "watching": "Dostupnost: <strong>Poslední 3 kusy</strong> · <strong>15 lidí</strong> právě sleduje tuto nabídku",
        "form_title": "Dokončete objednávku",
        "form_sub": "Vyplňte formulář níže, náš tým vás bude kontaktovat a potvrdí všechny detaily.",
        "label_name": "Jméno a příjmení *",
        "label_phone": "Telefonní číslo *",
        "label_address": "Doručovací adresa *",
        "err_name": "Zadejte jméno a příjmení (alespoň 3 znaky)",
        "err_phone": "Zadejte platné telefonní číslo",
        "err_address": "Zadejte úplnou adresu (alespoň 10 znaků)",
        "submit": "POTVRDIT OBJEDNÁVKU",
        "submitting": "Odesílání...",
        "f1_label": "01 — Skládací smartphone nejnovější generace",
        "f1_title": "Výkon a kontrola bez kompromisů",
        "f1_chips": ("3 obrazovky", "Skládací design", "Baterie 6800 mAh"),
        "f1_p1": "Zapomeňte na limity minulosti: Fold360™ mění práci i volný čas díky <strong>skládacímu designu se 3 obrazovkami</strong> a baterii, která vydrží celé dny. Skutečný multitasking na širokém displeji.",
        "f1_p2": "Zažijte maximum komfortu, kontroly a bezpečí v každé situaci. Svoboda a výkon vždy po ruce.",
        "f2_label": "02 — Odolnost a inteligence v jednom produktu",
        "f2_title": "5G, AI a baterie, která vás nezastaví",
        "f2_chips": ("Připojení 5G", "Funkce AI", "Nabíjení 66W"),
        "f2_p1": "Správná volba pro ty, kdo hledají spolehlivost: <strong>5G</strong>, voděodolné tělo a baterie <strong>6800 mAh</strong> pro klidné používání. Funkce AI vám pomáhají během dne.",
        "f2_p2": "<strong>Rychlé nabíjení 66W</strong> šetří hodiny: plné nabití asi za 25 minut. Více výdrže, méně čekání.",
        "f3_label": "03 — Dual SIM a připojení 5G",
        "f3_title": "Dvě čísla, jedno zařízení — vždy připojeni",
        "f3_chips": ("Dual SIM", "Internet 5G", "Fotoaparát 48 MP"),
        "f3_p1": "Spravujte dvě čísla v jednom zařízení díky <strong>Dual SIM</strong>: ideální pro oddělení práce a soukromí. Surfujte maximální rychlostí s <strong>5G</strong> bez zpomalení.",
        "f3_p2": "Dvojitý objektiv <strong>48 MP</strong> pro ostré a detailní fotky. Více svobody, více produktivity, vždy online.",
        "compare_sub": "Přímé srovnání",
        "compare_title": "Tradiční smartphone vs Fold360™",
        "traditional": "Tradiční",
        "rows": [
            ("Formát", "Pevný displej, méně praktický", "Kompaktní skládací design"),
            ("Displej", "Jeden displej", "3 skládací obrazovky"),
            ("Baterie", "Vybije se za pár hodin", "6800 mAh s vysokou výdrží"),
            ("Nabíjení", "Pomalé a nepraktické", "66W: plné za ~25 minut"),
            ("Konektivita", "4G / jedna SIM", "5G + Dual SIM"),
            ("Navíc", "Základní funkce", "AI + fotoaparát 48 MP"),
        ],
        "reviews_title": "Přes 1 800 spokojených zákazníků. Zjistěte, proč volí Fold360™.",
        "r1_title": "Baterie a 3 obrazovky opravdu pomáhají.",
        "r2_title": "Pohodlné používání, 5G vždy rychlé.",
        "r3_title": "Rychle se nabíjí a je odolný.",
        "verified": "Ověřený zákazník",
        "package_sub": "Co balení obsahuje?",
        "package_title": "Kompletní sada Fold360™, připravená k použití",
        "package_items": [
            "Skládací smartphone Fold360™",
            "Nabíječka 66W",
            "Kabel USB-C",
            "Vše potřebné pro okamžité použití",
            "Baterie 6800 mAh — vysoká výdrž",
            "Obal jako dárek",
            "<strong>Oficiální záruka 2 roky</strong>",
        ],
        "faq_title": "Často kladené otázky",
        "faqs": [
            ("Jak mohu objednat?", "Vyplňte formulář svými údaji. Konzultant vás bude kontaktovat a potvrdí objednávku Fold360™."),
            ("Mohu platit na dobírku?", "Ano, pro vaši bezpečnost nabízíme platbu v hotovosti přímo kurýrovi. Připravte si {price}."),
            ("Kdy dorazí?", "Doručení probíhá do 24–48 pracovních hodin. Kontaktujeme vás do několika hodin kvůli potvrzení."),
            ("Jak získám podporu?", "Vyplňte formulář: jeden z našich konzultantů vám pomůže s jakýmkoli dotazem před i po objednávce."),
            ("Jsou má data v bezpečí?", "Ano, vaše údaje jsou chráněny a používají se výhradně k odeslání produktu."),
        ],
        "offer_aria": "Časově omezená nabídka",
        "ty_title": "Objednávka přijata — Počkejte na potvrzovací hovor | Fold360™",
        "ty_desc": "Vaše objednávka Fold360™ byla zaznamenána. Zbývá poslední krok: přijměte potvrzovací hovor od našeho operátora.",
        "ty_h1": "Vaše objednávka byla úspěšně zaznamenána!",
        "ty_sub": "Skvělé — vaše objednávka se zpracovává. Zbývá už jen <strong>poslední krok</strong> k dokončení a odeslání.",
        "ty_eyebrow": "👇 Co máte udělat teď",
        "ty_action_title": "📞 Přijměte potvrzovací hovor",
        "ty_action_body": "Náš operátor vás bude kontaktovat <strong>v příštích hodinách</strong>, aby potvrdil objednávku.",
        "ty_action_warn": "Pokud hovor nepřijmete, objednávka bude automaticky zrušena.",
        "ty_hours_h": "🕒 Kontaktní hodiny",
        "ty_hours": "<strong>Pondělí – Sobota</strong> · 9:00 – 18:00",
        "ty_next_h": "📋 Co bude dál",
        "ty_steps": [
            "Přijměte hovor a <strong>potvrďte své údaje</strong>",
            "Vaše objednávka bude odeslána do <strong>24–48 hodin</strong>",
            "Doručení domů a <strong>platba na dobírku</strong>",
        ],
        "ty_badges": ("🔒 Platba na dobírku", "🛡️ Záruka 24 měsíců", "🔐 Ochrana SSL"),
        "ty_alt": "Tým homepickdock v práci: call centrum a logistika dobírky",
    },
}

# Build SI/HU/SK/PL similarly - to keep file manageable I'll generate via a compact approach
# Reuse structure with full dicts

def si_copy():
    return {
        "title": "Fold360™ — Zložljiv pametni telefon s 3 zasloni | -70% Samo danes",
        "desc": "Fold360™: zložljiv pametni telefon s 3 zasloni, baterija 6800 mAh, kamera 48 MP, 5G, Dual SIM, polnjenje 66W in funkcije AI. Plačilo po povzetju, dostava 24/48 h.",
        "og_title": "Fold360™ — Zložljiv pametni telefon | -70% Samo danes",
        "og_desc": "Zložljiv pametni telefon s 3 zasloni, baterija 6800 mAh, kamera 48 MP, 5G in Dual SIM. Plačilo po povzetju.",
        "json_name": "Fold360™ — Zložljiv pametni telefon s 3 zasloni",
        "json_desc": "Zložljiv pametni telefon Fold360™ s 3 zasloni, baterija 6800 mAh, polnjenje 66W, 5G, Dual SIM, kamera 48 MP in funkcije AI.",
        "banner": "🔥 GARANCIJA 2 LETI · PLAČILO PO POVZETJU · -70% 🔥",
        "rating": '<strong>4,9/5</strong> — <strong>1.824</strong> pozitivnih ocen',
        "guarantee_line": "🛡️ Garancija 2 leti · Plačilo po povzetju",
        "h1": "Zložljiv pametni telefon s 3 zasloni, kamero 48 MPx in baterijo 6.800 mAh",
        "sub": 'Inovativna tehnologija <strong>Fold360™</strong> ponuja idealno ravnovesje med stilom, mobilnostjo in funkcionalnostjo: zložljiv dizajn z velikim zaslonom, povezljivost <strong>5G</strong>, funkcije umetne inteligence, ultra-hitro polnjenje in dolgotrajna baterija.',
        "discount_label": "POPUST 70 % DO RAZPRODAJE ZALOG",
        "cta_order": "NAROČI Fold360™ →",
        "no_prepay": "🔒 Brez predplačila · Brez kartice · Plačate šele ob dostavi",
        "trust": [
            ("Consegna in 24-48h", "Dostava v 24–48 h", "Spedizione rapida in tutta Italia", "Hitra dostava po vsej Sloveniji"),
            ("Pagamento alla consegna", "Plačilo po povzetju", "Paghi solo quando ricevi", "Plačate šele ob prejemu"),
            ("Garanzia 2 anni", "Garancija 2 leti", "Copertura ufficiale inclusa", "Uradno kritje vključeno"),
            ("Reso 30 giorni", "Vračilo v 30 dneh", "Rimborso semplice e gratuito", "Enostavno in brezplačno vračilo"),
        ],
        "countdown_label": "⏰ Ponudba -70 % poteče čez",
        "hours": "Ur", "mins": "Min", "secs": "Sek",
        "watching": "Razpoložljivost: <strong>Zadnji 3 kosi</strong> · <strong>15 oseb</strong> trenutno gleda to ponudbo",
        "form_title": "Dokončajte naročilo",
        "form_sub": "Izpolnite obrazec spodaj, naša ekipa vas bo kontaktirala za potrditev vseh podrobnosti.",
        "label_name": "Ime in priimek *",
        "label_phone": "Telefonska številka *",
        "label_address": "Naslov za dostavo *",
        "err_name": "Vnesite ime in priimek (vsaj 3 znake)",
        "err_phone": "Vnesite veljavno telefonsko številko",
        "err_address": "Vnesite popoln naslov (vsaj 10 znakov)",
        "submit": "POTRDI NAROČILO",
        "submitting": "Pošiljanje...",
        "f1_label": "01 — Zložljiv pametni telefon najnovejše generacije",
        "f1_title": "Moč in nadzor brez kompromisov",
        "f1_chips": ("3 zasloni", "Zložljiv dizajn", "Baterija 6800 mAh"),
        "f1_p1": "Pozabite na omejitve preteklosti: Fold360™ spreminja delo in prosti čas z <strong>zložljivim dizajnom s 3 zasloni</strong> in baterijo, ki zdrži dni. Pravi multitasking na širokem zaslonu.",
        "f1_p2": "Doživite največ udobja, nadzora in varnosti v vsaki situaciji. Svoboda in moč vedno pri roki.",
        "f2_label": "02 — Odpornost in inteligenca v enem izdelku",
        "f2_title": "5G, AI in baterija, ki vas ne ustavi",
        "f2_chips": ("Povezava 5G", "Funkcije AI", "Polnjenje 66W"),
        "f2_p1": "Prava izbira za tiste, ki iščejo zanesljivost: <strong>5G</strong>, vodoodporno ohišje in baterija <strong>6800 mAh</strong> za brezskrben uporabo. Funkcije AI podpirajo vaš dan.",
        "f2_p2": "<strong>Hitro polnjenje 66W</strong> prihrani ure: polno polnjenje v približno 25 minutah. Več avtonomije, manj čakanja.",
        "f3_label": "03 — Dual SIM in povezava 5G",
        "f3_title": "Dve številki, ena naprava — vedno povezani",
        "f3_chips": ("Dual SIM", "Internet 5G", "Kamera 48 MP"),
        "f3_p1": "Upravljajte dve številki na eni napravi z <strong>Dual SIM</strong>: idealno za ločitev dela in zasebnosti. Brskajte z največjo hitrostjo z <strong>5G</strong> brez upočasnitev.",
        "f3_p2": "Dvojni objektiv <strong>48 MP</strong> za ostre in podrobne fotografije. Več svobode, več produktivnosti, vedno na spletu.",
        "compare_sub": "Neposredna primerjava",
        "compare_title": "Tradicionalni pametni telefon vs Fold360™",
        "traditional": "Tradicionalni",
        "rows": [
            ("Oblika", "Fiksni zaslon, manj praktičen", "Kompakten zložljiv dizajn"),
            ("Zaslon", "En zaslon", "3 zložljivi zasloni"),
            ("Baterija", "Se izprazni v nekaj urah", "6800 mAh z dolgo avtonomijo"),
            ("Polnjenje", "Počasno in nepraktično", "66W: polno v ~25 minutah"),
            ("Povezljivost", "4G / ena SIM", "5G + Dual SIM"),
            ("Dodatno", "Osnovne funkcije", "AI + kamera 48 MP"),
        ],
        "reviews_title": "Več kot 1.800 zadovoljnih strank. Odkrijte, zakaj izberejo Fold360™.",
        "r1_title": "Baterija in 3 zasloni res pomagajo.",
        "r2_title": "Priročna uporaba, 5G vedno hitro.",
        "r3_title": "Hitro se polni in je odporen.",
        "verified": "Preverjena stranka",
        "package_sub": "Kaj vsebuje paket?",
        "package_title": "Celoten komplet Fold360™, pripravljen za uporabo",
        "package_items": [
            "Zložljiv pametni telefon Fold360™",
            "Polnilec 66W",
            "Kabel USB-C",
            "Vse potrebno za takojšnjo uporabo",
            "Baterija 6800 mAh — visoka avtonomija",
            "Ovitek v darilo",
            "<strong>Uradna garancija 2 leti</strong>",
        ],
        "faq_title": "Pogosta vprašanja",
        "faqs": [
            ("Kako naročim?", "Izpolnite obrazec s svojimi podatki. Svetovalec vas bo kontaktiral za potrditev naročila Fold360™."),
            ("Ali lahko plačam po povzetju?", "Da, za vašo varnost ponujamo plačilo v gotovini neposredno kurirju. Pripravite {price}."),
            ("Kdaj prispe?", "Dostava poteka v 24–48 delovnih urah. Kontaktiramo vas v nekaj urah za potrditev."),
            ("Kako dobim pomoč?", "Izpolnite obrazec: eden od naših svetovalcev vam bo na voljo za vsa vprašanja pred ali po naročilu."),
            ("Ali so moji podatki varni?", "Da, vaši podatki so zaščiteni in se uporabljajo izključno za pošiljanje izdelka."),
        ],
        "offer_aria": "Časovno omejena ponudba",
        "ty_title": "Naročilo prejeto — Počakajte na potrditveni klic | Fold360™",
        "ty_desc": "Vaše naročilo Fold360™ je bilo zabeleženo. Ostaja še zadnji korak: sprejmite potrditveni klic našega operaterja.",
        "ty_h1": "Vaše naročilo je bilo uspešno zabeleženo!",
        "ty_sub": "Odlično — vaše naročilo se obdeluje. Ostaja še le <strong>zadnji korak</strong> do dokončanja in odpreme.",
        "ty_eyebrow": "👇 Kaj morate storiti zdaj",
        "ty_action_title": "📞 Sprejmite potrditveni klic",
        "ty_action_body": "Naš operater vas bo kontaktiral <strong>v naslednjih urah</strong>, da potrdi naročilo.",
        "ty_action_warn": "Če klica ne sprejmete, bo naročilo samodejno preklicano.",
        "ty_hours_h": "🕒 Kontaktne ure",
        "ty_hours": "<strong>Ponedeljek – Sobota</strong> · 9:00 – 18:00",
        "ty_next_h": "📋 Kaj sledi",
        "ty_steps": [
            "Sprejmite klic in <strong>potrdite svoje podatke</strong>",
            "Vaše naročilo bo odposlano v <strong>24–48 urah</strong>",
            "Dostava na dom in <strong>plačilo po povzetju</strong>",
        ],
        "ty_badges": ("🔒 Plačilo po povzetju", "🛡️ Garancija 24 mesecev", "🔐 Zaščita SSL"),
        "ty_alt": "Ekipa homepickdock pri delu: klicni center in logistika COD",
    }

COPY["si"] = si_copy()


def hu_copy():
    return {
        "title": "Fold360™ — 3 képernyős összecsukható okostelefon | -70% Csak ma",
        "desc": "Fold360™: 3 képernyős összecsukható okostelefon, 6800 mAh akkumulátor, 48 MP kamera, 5G, Dual SIM, 66W töltés és AI funkciók. Utánvét, szállítás 24/48 óra.",
        "og_title": "Fold360™ — Összecsukható okostelefon | -70% Csak ma",
        "og_desc": "3 képernyős összecsukható okostelefon, 6800 mAh, 48 MP, 5G és Dual SIM. Utánvét.",
        "json_name": "Fold360™ — 3 képernyős összecsukható okostelefon",
        "json_desc": "Fold360™ összecsukható okostelefon 3 képernyővel, 6800 mAh akkumulátor, 66W töltés, 5G, Dual SIM, 48 MP kamera és AI funkciók.",
        "banner": "🔥 2 ÉV GARANCIA · UTÁNVÉT · -70% 🔥",
        "rating": '<strong>4,9/5</strong> — <strong>1.824</strong> pozitív értékelés',
        "guarantee_line": "🛡️ 2 év garancia · Utánvét",
        "h1": "Összecsukható okostelefon 3 képernyővel, 48 MPx kamerával és 6.800 mAh akkumulátorral",
        "sub": 'Az innovatív <strong>Fold360™</strong> technológia ideális egyensúlyt kínál stílus, mobilitás és funkcionalitás között: összecsukható kialakítás nagy kijelzővel, <strong>5G</strong> kapcsolat, mesterséges intelligencia funkciók, ultragyors töltés és hosszú akkumulátor-élettartam.',
        "discount_label": "70% KEDVEZMÉNY A KÉSZLET EREJÉIG",
        "cta_order": "RENDELJE Fold360™ →",
        "no_prepay": "🔒 Nincs előleg · Nincs kártya · Csak átvételkor fizet",
        "trust": [
            ("Consegna in 24-48h", "Szállítás 24–48 óra", "Spedizione rapida in tutta Italia", "Gyors szállítás egész Magyarországon"),
            ("Pagamento alla consegna", "Utánvét", "Paghi solo quando ricevi", "Csak átvételkor fizet"),
            ("Garanzia 2 anni", "2 év garancia", "Copertura ufficiale inclusa", "Hivatalos fedezet benne"),
            ("Reso 30 giorni", "30 napos visszaküldés", "Rimborso semplice e gratuito", "Egyszerű, ingyenes visszatérítés"),
        ],
        "countdown_label": "⏰ A -70% ajánlat lejár",
        "hours": "Óra", "mins": "Perc", "secs": "Mp",
        "watching": "Elérhetőség: <strong>Utolsó 3 darab</strong> · <strong>15 ember</strong> nézi most ezt az ajánlatot",
        "form_title": "Fejezze be a rendelést",
        "form_sub": "Töltse ki az alábbi űrlapot, csapatunk felveszi Önnel a kapcsolatot a részletek megerősítéséhez.",
        "label_name": "Teljes név *",
        "label_phone": "Telefonszám *",
        "label_address": "Szállítási cím *",
        "err_name": "Adja meg a teljes nevét (legalább 3 karakter)",
        "err_phone": "Adjon meg érvényes telefonszámot",
        "err_address": "Adjon meg teljes címet (legalább 10 karakter)",
        "submit": "RENDELÉS MEGERŐSÍTÉSE",
        "submitting": "Küldés...",
        "f1_label": "01 — Legújabb generációs összecsukható okostelefon",
        "f1_title": "Erő és kontroll kompromisszumok nélkül",
        "f1_chips": ("3 képernyő", "Összecsukható kialakítás", "6800 mAh akkumulátor"),
        "f1_p1": "Felejtse el a múlt korlátait: a Fold360™ a <strong>3 képernyős összecsukható kialakítással</strong> és a napokig kitartó akkumulátorral forradalmasítja a munkát és a szabadidőt. Valódi multitasking széles kijelzőn.",
        "f1_p2": "Élje át a maximális kényelmet, kontrollt és biztonságot minden helyzetben. Szabadság és erő mindig kéznél.",
        "f2_label": "02 — Ellenállás és intelligencia egy termékben",
        "f2_title": "5G, AI és akkumulátor, ami nem hagy cserben",
        "f2_chips": ("5G kapcsolat", "AI funkciók", "66W töltés"),
        "f2_p1": "A megbízhatóságot keresők választása: <strong>5G</strong>, vízálló ház és <strong>6800 mAh</strong> akkumulátor. Az AI funkciók támogatják a napját.",
        "f2_p2": "A <strong>66W gyors töltés</strong> órákat spórol: teljes töltés kb. 25 perc alatt. Több üzemidő, kevesebb várakozás.",
        "f3_label": "03 — Dual SIM és 5G kapcsolat",
        "f3_title": "Két szám, egy készülék — mindig kapcsolódva",
        "f3_chips": ("Dual SIM", "5G internet", "48 MP kamera"),
        "f3_p1": "Kezeljen két számot egy készüléken a <strong>Dual SIM</strong> segítségével: ideális a munka és a magánélet szétválasztásához. Böngésszen maximális sebességgel <strong>5G</strong>-vel.",
        "f3_p2": "<strong>48 MP</strong> dupla objektív éles, részletes fotókhoz. Több szabadság, több produktivitás, mindig online.",
        "compare_sub": "Közvetlen összehasonlítás",
        "compare_title": "Hagyományos okostelefon vs Fold360™",
        "traditional": "Hagyományos",
        "rows": [
            ("Formátum", "Fix kijelző, kevésbé praktikus", "Kompakt összecsukható kialakítás"),
            ("Kijelző", "Egy kijelző", "3 összecsukható képernyő"),
            ("Akkumulátor", "Néhány óra alatt lemerül", "6800 mAh nagy üzemidővel"),
            ("Töltés", "Lassú és nem praktikus", "66W: tele ~25 perc alatt"),
            ("Kapcsolódás", "4G / egy SIM", "5G + Dual SIM"),
            ("Extrák", "Alapfunkciók", "AI + 48 MP kamera"),
        ],
        "reviews_title": "Több mint 1800 elégedett vásárló. Tudja meg, miért választják a Fold360™-t.",
        "r1_title": "Az akkumulátor és a 3 képernyő tényleg hasznos.",
        "r2_title": "Kényelmes használat, az 5G mindig gyors.",
        "r3_title": "Gyorsan töltődik és strapabíró.",
        "verified": "Ellenőrzött vásárló",
        "package_sub": "Mit tartalmaz a csomag?",
        "package_title": "Teljes Fold360™ készlet, azonnal használható",
        "package_items": [
            "Fold360™ összecsukható okostelefon",
            "66W töltő",
            "USB-C kábel",
            "Minden az azonnali használathoz",
            "6800 mAh akkumulátor — nagy üzemidő",
            "Tok ajándékba",
            "<strong>Hivatalos 2 év garancia</strong>",
        ],
        "faq_title": "Gyakori kérdések",
        "faqs": [
            ("Hogyan rendelhetek?", "Töltse ki az űrlapot adataival. Tanácsadónk felveszi Önnel a kapcsolatot a Fold360™ rendelés megerősítéséhez."),
            ("Fizethetek utánvéttel?", "Igen, biztonsága érdekében készpénzes fizetést kínálunk közvetlenül a futárnak. Készítsen elő {price}-ot."),
            ("Mikor érkezik?", "A szállítás 24–48 munkanapon belül történik. Néhány órán belül felvesszük Önnel a kapcsolatot."),
            ("Hogyan kaphatok segítséget?", "Töltse ki az űrlapot: tanácsadóink a rendelés előtt és után is rendelkezésre állnak."),
            ("Biztonságban vannak az adataim?", "Igen, adatai védettek, és kizárólag a termék kiszállításához használjuk őket."),
        ],
        "offer_aria": "Időkorlátos ajánlat",
        "ty_title": "Rendelés megérkezett — Várja a visszaigazoló hívást | Fold360™",
        "ty_desc": "Fold360™ rendelése rögzítve. Már csak egy lépés van hátra: vegye fel a visszaigazoló hívást.",
        "ty_h1": "Rendelését sikeresen rögzítettük!",
        "ty_sub": "Remek — rendelése feldolgozás alatt van. Már csak <strong>egy utolsó lépés</strong> van hátra a véglegesítéshez és a szállításhoz.",
        "ty_eyebrow": "👇 Mit tegyen most",
        "ty_action_title": "📞 Vegye fel a visszaigazoló hívást",
        "ty_action_body": "Operátorunk <strong>a következő órákban</strong> felhívja Önt a rendelés megerősítéséhez.",
        "ty_action_warn": "Ha nem veszi fel a telefont, a rendelés automatikusan törlődik.",
        "ty_hours_h": "🕒 Kapcsolattartási idő",
        "ty_hours": "<strong>Hétfő – Szombat</strong> · 9:00 – 18:00",
        "ty_next_h": "📋 Mi történik ezután",
        "ty_steps": [
            "Vegye fel a hívást és <strong>erősítse meg adatait</strong>",
            "Rendelése <strong>24–48 órán belül</strong> elindul",
            "Házhoz szállítás és <strong>utánvét</strong>",
        ],
        "ty_badges": ("🔒 Utánvét", "🛡️ 24 hónap garancia", "🔐 SSL védelem"),
        "ty_alt": "A homepickdock csapat munka közben: call center és COD logisztika",
    }

COPY["hu"] = hu_copy()


def sk_copy():
    c = dict(COPY["cz"])  # start from Czech then override Slovak specifics
    c.update({
        "title": "Fold360™ — Skladací smartfón s 3 obrazovkami | -70% Len dnes",
        "desc": "Fold360™: skladací smartfón s 3 obrazovkami, batéria 6800 mAh, fotoaparát 48 MP, 5G, Dual SIM, nabíjanie 66W a funkcie AI. Platba na dobierku, doručenie 24/48 h.",
        "og_title": "Fold360™ — Skladací smartfón | -70% Len dnes",
        "og_desc": "Skladací smartfón s 3 obrazovkami, batéria 6800 mAh, fotoaparát 48 MP, 5G a Dual SIM. Platba na dobierku.",
        "json_name": "Fold360™ — Skladací smartfón s 3 obrazovkami",
        "json_desc": "Skladací smartfón Fold360™ s 3 obrazovkami, batéria 6800 mAh, nabíjanie 66W, 5G, Dual SIM, fotoaparát 48 MP a funkcie AI.",
        "banner": "🔥 ZÁRUKA 2 ROKY · PLATBA NA DOBIERKU · -70% 🔥",
        "rating": '<strong>4,9/5</strong> — <strong>1.824</strong> pozitívnych recenzií',
        "guarantee_line": "🛡️ Záruka 2 roky · Platba na dobierku",
        "h1": "Skladací smartfón s 3 obrazovkami, fotoaparátom 48 MPx a batériou 6.800 mAh",
        "sub": 'Inovatívna technológia <strong>Fold360™</strong> ponúka ideálnu rovnováhu medzi štýlom, mobilitou a funkčnosťou: skladací dizajn s veľkým displejom, konektivita <strong>5G</strong>, funkcie umelej inteligencie, ultra-rýchle nabíjanie a dlhá výdrž batérie.',
        "discount_label": "ZĽAVA 70 % DO VYPREDANIA ZÁSOB",
        "cta_order": "OBJEDNAŤ Fold360™ →",
        "no_prepay": "🔒 Žiadna záloha · Žiadna karta · Platíte až pri doručení",
        "trust": [
            ("Consegna in 24-48h", "Doručenie do 24–48 h", "Spedizione rapida in tutta Italia", "Rýchla doprava po celom Slovensku"),
            ("Pagamento alla consegna", "Platba na dobierku", "Paghi solo quando ricevi", "Platíte až pri prevzatí"),
            ("Garanzia 2 anni", "Záruka 2 roky", "Copertura ufficiale inclusa", "Oficiálne krytie v cene"),
            ("Reso 30 giorni", "Vrátenie do 30 dní", "Rimborso semplice e gratuito", "Jednoduché a bezplatné vrátenie"),
        ],
        "countdown_label": "⏰ Ponuka -70 % vyprší o",
        "hours": "Hod", "mins": "Min", "secs": "Sek",
        "watching": "Dostupnosť: <strong>Posledné 3 kusy</strong> · <strong>15 ľudí</strong> práve sleduje túto ponuku",
        "form_title": "Dokončite objednávku",
        "form_sub": "Vyplňte formulár nižšie, náš tím vás bude kontaktovať a potvrdí všetky detaily.",
        "label_name": "Meno a priezvisko *",
        "label_phone": "Telefónne číslo *",
        "label_address": "Doručovacia adresa *",
        "err_name": "Zadajte meno a priezvisko (aspoň 3 znaky)",
        "err_phone": "Zadajte platné telefónne číslo",
        "err_address": "Zadajte úplnú adresu (aspoň 10 znakov)",
        "submit": "POTVRDIŤ OBJEDNÁVKU",
        "submitting": "Odosielanie...",
        "f1_label": "01 — Skladací smartfón najnovšej generácie",
        "f1_title": "Výkon a kontrola bez kompromisov",
        "f1_chips": ("3 obrazovky", "Skladací dizajn", "Batéria 6800 mAh"),
        "f1_p1": "Zabudnite na limity minulosti: Fold360™ mení prácu aj voľný čas vďaka <strong>skladaciemu dizajnu s 3 obrazovkami</strong> a batérii, ktorá vydrží celé dni. Skutočný multitasking na širokom displeji.",
        "f1_p2": "Zažite maximum komfortu, kontroly a bezpečia v každej situácii. Sloboda a výkon vždy po ruke.",
        "f2_label": "02 — Odolnosť a inteligencia v jednom produkte",
        "f2_title": "5G, AI a batéria, ktorá vás nezastaví",
        "f2_chips": ("Pripojenie 5G", "Funkcie AI", "Nabíjanie 66W"),
        "f2_p1": "Správna voľba pre tých, ktorí hľadajú spoľahlivosť: <strong>5G</strong>, vodeodolné telo a batéria <strong>6800 mAh</strong>. Funkcie AI vám pomáhajú počas dňa.",
        "f2_p2": "<strong>Rýchle nabíjanie 66W</strong> šetrí hodiny: plné nabitie asi za 25 minút. Viac výdrže, menej čakania.",
        "f3_label": "03 — Dual SIM a pripojenie 5G",
        "f3_title": "Dve čísla, jedno zariadenie — vždy pripojení",
        "f3_chips": ("Dual SIM", "Internet 5G", "Fotoaparát 48 MP"),
        "f3_p1": "Spravujte dve čísla v jednom zariadení vďaka <strong>Dual SIM</strong>: ideálne na oddelenie práce a súkromia. Surfujte maximálnou rýchlosťou s <strong>5G</strong>.",
        "f3_p2": "Dvojitý objektív <strong>48 MP</strong> pre ostré a detailné fotky. Viac slobody, viac produktivity, vždy online.",
        "compare_sub": "Priame porovnanie",
        "compare_title": "Tradičný smartfón vs Fold360™",
        "traditional": "Tradičný",
        "rows": [
            ("Formát", "Pevný displej, menej praktický", "Kompaktný skladací dizajn"),
            ("Displej", "Jeden displej", "3 skladacie obrazovky"),
            ("Batéria", "Vybije sa za pár hodín", "6800 mAh s vysokou výdržou"),
            ("Nabíjanie", "Pomalé a nepraktické", "66W: plné za ~25 minút"),
            ("Konektivita", "4G / jedna SIM", "5G + Dual SIM"),
            ("Navyše", "Základné funkcie", "AI + fotoaparát 48 MP"),
        ],
        "reviews_title": "Viac ako 1 800 spokojných zákazníkov. Zistite, prečo volia Fold360™.",
        "r1_title": "Batéria a 3 obrazovky naozaj pomáhajú.",
        "r2_title": "Pohodlné používanie, 5G vždy rýchle.",
        "r3_title": "Rýchlo sa nabíja a je odolný.",
        "verified": "Overený zákazník",
        "package_sub": "Čo balenie obsahuje?",
        "package_title": "Kompletná sada Fold360™, pripravená na použitie",
        "package_items": [
            "Skladací smartfón Fold360™",
            "Nabíjačka 66W",
            "Kábel USB-C",
            "Všetko potrebné na okamžité použitie",
            "Batéria 6800 mAh — vysoká výdrž",
            "Obal ako darček",
            "<strong>Oficiálna záruka 2 roky</strong>",
        ],
        "faq_title": "Často kladené otázky",
        "faqs": [
            ("Ako môžem objednať?", "Vyplňte formulár svojimi údajmi. Konzultant vás bude kontaktovať a potvrdí objednávku Fold360™."),
            ("Môžem platiť na dobierku?", "Áno, pre vašu bezpečnosť ponúkame platbu v hotovosti priamo kuriérovi. Pripravte si {price}."),
            ("Kedy dorazí?", "Doručenie prebieha do 24–48 pracovných hodín. Kontaktujeme vás do niekoľkých hodín kvôli potvrdeniu."),
            ("Ako získam podporu?", "Vyplňte formulár: jeden z našich konzultantov vám pomôže s akoukoľvek otázkou pred aj po objednávke."),
            ("Sú moje údaje v bezpečí?", "Áno, vaše údaje sú chránené a používajú sa výhradne na odoslanie produktu."),
        ],
        "offer_aria": "Časovo obmedzená ponuka",
        "ty_title": "Objednávka prijatá — Počkajte na potvrdzovací hovor | Fold360™",
        "ty_desc": "Vaša objednávka Fold360™ bola zaznamenaná. Zostáva posledný krok: prijmete potvrdzovací hovor od nášho operátora.",
        "ty_h1": "Vaša objednávka bola úspešne zaznamenaná!",
        "ty_sub": "Skvelé — vaša objednávka sa spracováva. Zostáva už len <strong>posledný krok</strong> k dokončeniu a odoslaniu.",
        "ty_eyebrow": "👇 Čo máte urobiť teraz",
        "ty_action_title": "📞 Prijmite potvrdzovací hovor",
        "ty_action_body": "Náš operátor vás bude kontaktovať <strong>v nasledujúcich hodinách</strong>, aby potvrdil objednávku.",
        "ty_action_warn": "Ak hovor neprijmete, objednávka bude automaticky zrušená.",
        "ty_hours_h": "🕒 Kontaktné hodiny",
        "ty_hours": "<strong>Pondelok – Sobota</strong> · 9:00 – 18:00",
        "ty_next_h": "📋 Čo bude ďalej",
        "ty_steps": [
            "Prijmite hovor a <strong>potvrďte svoje údaje</strong>",
            "Vaša objednávka bude odoslaná do <strong>24–48 hodín</strong>",
            "Doručenie domov a <strong>platba na dobierku</strong>",
        ],
        "ty_badges": ("🔒 Platba na dobierku", "🛡️ Záruka 24 mesiacov", "🔐 Ochrana SSL"),
        "ty_alt": "Tím homepickdock v práci: call centrum a logistika dobierky",
    })
    return c

COPY["sk"] = sk_copy()


def pl_copy():
    return {
        "title": "Fold360™ — Składany smartfon z 3 ekranami | -70% Tylko dziś",
        "desc": "Fold360™: składany smartfon z 3 ekranami, bateria 6800 mAh, aparat 48 MP, 5G, Dual SIM, ładowanie 66W i funkcje AI. Płatność przy odbiorze, dostawa 24/48 h.",
        "og_title": "Fold360™ — Składany smartfon | -70% Tylko dziś",
        "og_desc": "Składany smartfon z 3 ekranami, bateria 6800 mAh, aparat 48 MP, 5G i Dual SIM. Płatność przy odbiorze.",
        "json_name": "Fold360™ — Składany smartfon z 3 ekranami",
        "json_desc": "Składany smartfon Fold360™ z 3 ekranami, bateria 6800 mAh, ładowanie 66W, 5G, Dual SIM, aparat 48 MP i funkcje AI.",
        "banner": "🔥 GWARANCJA 2 LATA · PŁATNOŚĆ PRZY ODBIORZE · -70% 🔥",
        "rating": '<strong>4,9/5</strong> — <strong>1.824</strong> pozytywnych opinii',
        "guarantee_line": "🛡️ Gwarancja 2 lata · Płatność przy odbiorze",
        "h1": "Składany smartfon z 3 ekranami, aparatem 48 MPx i baterią 6.800 mAh",
        "sub": 'Innowacyjna technologia <strong>Fold360™</strong> oferuje idealną równowagę między stylem, mobilnością i funkcjonalnością: składany design z dużym ekranem, łączność <strong>5G</strong>, funkcje sztucznej inteligencji, ultraszybkie ładowanie i długo działająca bateria.',
        "discount_label": "RABAT 70% DO WYCZERPANIA ZAPASÓW",
        "cta_order": "ZAMÓW Fold360™ →",
        "no_prepay": "🔒 Bez zaliczki · Bez karty · Płacisz dopiero przy dostawie",
        "trust": [
            ("Consegna in 24-48h", "Dostawa w 24–48 h", "Spedizione rapida in tutta Italia", "Szybka wysyłka w całej Polsce"),
            ("Pagamento alla consegna", "Płatność przy odbiorze", "Paghi solo quando ricevi", "Płacisz dopiero przy odbiorze"),
            ("Garanzia 2 anni", "Gwarancja 2 lata", "Copertura ufficiale inclusa", "Oficjalne pokrycie w cenie"),
            ("Reso 30 giorni", "Zwrot w 30 dni", "Rimborso semplice e gratuito", "Prosty i bezpłatny zwrot"),
        ],
        "countdown_label": "⏰ Oferta -70% kończy się za",
        "hours": "Godz", "mins": "Min", "secs": "Sek",
        "watching": "Dostępność: <strong>Ostatnie 3 sztuki</strong> · <strong>15 osób</strong> ogląda teraz tę ofertę",
        "form_title": "Dokończ zamówienie",
        "form_sub": "Wypełnij formularz poniżej, nasz zespół skontaktuje się z Tobą, aby potwierdzić wszystkie szczegóły.",
        "label_name": "Imię i nazwisko *",
        "label_phone": "Numer telefonu *",
        "label_address": "Adres dostawy *",
        "err_name": "Wpisz imię i nazwisko (co najmniej 3 znaki)",
        "err_phone": "Wpisz prawidłowy numer telefonu",
        "err_address": "Wpisz pełny adres (co najmniej 10 znaków)",
        "submit": "POTWIERDŹ ZAMÓWIENIE",
        "submitting": "Wysyłanie...",
        "f1_label": "01 — Składany smartfon najnowszej generacji",
        "f1_title": "Moc i kontrola bez kompromisów",
        "f1_chips": ("3 ekrany", "Składany design", "Bateria 6800 mAh"),
        "f1_p1": "Zapomnij o ograniczeniach przeszłości: Fold360™ rewolucjonizuje pracę i czas wolny dzięki <strong>składanemu designowi z 3 ekranami</strong> i baterii, która działa przez dni. Prawdziwy multitasking na szerokim ekranie.",
        "f1_p2": "Doświadcz maksymalnego komfortu, kontroli i bezpieczeństwa w każdej sytuacji. Wolność i moc zawsze pod ręką.",
        "f2_label": "02 — Odporność i inteligencja w jednym produkcie",
        "f2_title": "5G, AI i bateria, która Cię nie zawodzi",
        "f2_chips": ("Łączność 5G", "Funkcje AI", "Ładowanie 66W"),
        "f2_p1": "Właściwy wybór dla tych, którzy szukają niezawodności: <strong>5G</strong>, wodoodporna obudowa i bateria <strong>6800 mAh</strong>. Funkcje AI wspierają Twój dzień.",
        "f2_p2": "<strong>Szybkie ładowanie 66W</strong> oszczędza godziny: pełne naładowanie w ok. 25 minut. Więcej autonomii, mniej czekania.",
        "f3_label": "03 — Dual SIM i łączność 5G",
        "f3_title": "Dwa numery, jedno urządzenie — zawsze w kontakcie",
        "f3_chips": ("Dual SIM", "Internet 5G", "Aparat 48 MP"),
        "f3_p1": "Zarządzaj dwoma numerami na jednym urządzeniu dzięki <strong>Dual SIM</strong>: idealne do oddzielenia pracy od życia prywatnego. Surfuuj z maksymalną prędkością dzięki <strong>5G</strong>.",
        "f3_p2": "Podwójny obiektyw <strong>48 MP</strong> dla ostrych i szczegółowych zdjęć. Więcej wolności, więcej produktywności, zawsze online.",
        "compare_sub": "Bezpośrednie porównanie",
        "compare_title": "Tradycyjny smartfon vs Fold360™",
        "traditional": "Tradycyjny",
        "rows": [
            ("Format", "Stały ekran, mniej praktyczny", "Kompaktowy składany design"),
            ("Ekran", "Jeden wyświetlacz", "3 składane ekrany"),
            ("Bateria", "Rozładowuje się w kilka godzin", "6800 mAh z dużą autonomią"),
            ("Ładowanie", "Wolne i niepraktyczne", "66W: pełne w ~25 minut"),
            ("Łączność", "4G / jedna SIM", "5G + Dual SIM"),
            ("Extra", "Podstawowe funkcje", "AI + aparat 48 MP"),
        ],
        "reviews_title": "Ponad 1800 zadowolonych klientów. Sprawdź, dlaczego wybierają Fold360™.",
        "r1_title": "Bateria i 3 ekrany naprawdę pomagają.",
        "r2_title": "Wygodne w użyciu, 5G zawsze szybkie.",
        "r3_title": "Szybko się ładuje i jest odporny.",
        "verified": "Zweryfikowany klient",
        "package_sub": "Co zawiera paczka?",
        "package_title": "Kompletny zestaw Fold360™, gotowy do użycia",
        "package_items": [
            "Składany smartfon Fold360™",
            "Ładowarka 66W",
            "Kabel USB-C",
            "Wszystko potrzebne do natychmiastowego użycia",
            "Bateria 6800 mAh — duża autonomia",
            "Etui w prezencie",
            "<strong>Oficjalna gwarancja 2 lata</strong>",
        ],
        "faq_title": "Często zadawane pytania",
        "faqs": [
            ("Jak mogę zamówić?", "Wypełnij formularz swoimi danymi. Konsultant skontaktuje się z Tobą, aby potwierdzić zamówienie Fold360™."),
            ("Czy mogę zapłacić przy odbiorze?", "Tak, dla Twojego bezpieczeństwa oferujemy płatność gotówką bezpośrednio kurierowi. Przygotuj {price}."),
            ("Kiedy dotrze?", "Dostawa odbywa się w ciągu 24–48 godzin roboczych. Skontaktujemy się w ciągu kilku godzin w celu potwierdzenia."),
            ("Jak uzyskać pomoc?", "Wypełnij formularz: jeden z naszych konsultantów pomoże w razie pytań przed lub po zamówieniu."),
            ("Czy moje dane są bezpieczne?", "Tak, Twoje dane są chronione i używane wyłącznie do wysyłki produktu."),
        ],
        "offer_aria": "Oferta ograniczona czasowo",
        "ty_title": "Zamówienie otrzymane — Poczekaj na telefon potwierdzający | Fold360™",
        "ty_desc": "Twoje zamówienie Fold360™ zostało zarejestrowane. Pozostał ostatni krok: odbierz telefon potwierdzający od naszego operatora.",
        "ty_h1": "Twoje zamówienie zostało pomyślnie zarejestrowane!",
        "ty_sub": "Świetnie — Twoje zamówienie jest przetwarzane. Pozostał już tylko <strong>ostatni krok</strong> do jego ukończenia i wysyłki.",
        "ty_eyebrow": "👇 Co masz teraz zrobić",
        "ty_action_title": "📞 Odbierz rozmowę potwierdzającą",
        "ty_action_body": "Nasz operator skontaktuje się z Tobą <strong>w ciągu najbliższych godzin</strong>, aby potwierdzić zamówienie.",
        "ty_action_warn": "Jeśli nie odbierzesz telefonu, zamówienie zostanie automatycznie anulowane.",
        "ty_hours_h": "🕒 Godziny kontaktu",
        "ty_hours": "<strong>Poniedziałek – Sobota</strong> · 9:00 – 18:00",
        "ty_next_h": "📋 Co dalej",
        "ty_steps": [
            "Odbierz telefon i <strong>potwierdź swoje dane</strong>",
            "Twoje zamówienie zostanie wysłane w ciągu <strong>24–48 godzin</strong>",
            "Dostawa do domu i <strong>płatność przy odbiorze</strong>",
        ],
        "ty_badges": ("🔒 Płatność przy odbiorze", "🛡️ Gwarancja 24 miesiące", "🔐 Ochrona SSL"),
        "ty_alt": "Zespół homepickdock w pracy: call center i logistyka COD",
    }

COPY["pl"] = pl_copy()


def footer_html(geo: str, g: dict) -> str:
    links = "\n".join(
        f'          <li><a href="/{geo}/{href}">{label}</a></li>'
        for href, label in g["links"]
    )
    return f'''      <div>
        <h4 class="site-footer__heading">{g["footer_info"]}</h4>
        <ul class="site-footer__list">
{links}
        </ul>
      </div>
      <div>
        <h4 class="site-footer__heading">{g["footer_contact"]}</h4>
        <ul class="site-footer__list">
          <li><strong>A.R.T. - FZCO</strong></li>
          <li>Dubai Silicon Oasis, DDP, Building A1</li>
          <li>Dubai, United Arab Emirates</li>
          <li><a href="mailto:info@homepickdock.com">info@homepickdock.com</a></li>
        </ul>
      </div>'''


def build_popups(geo: str, g: dict) -> str:
    msgs = {
        0: " ha appena ordinato Fold360™",
        1: " ha appena confermato l'ordine",
        2: " ha appena acquistato Fold360™",
        3: " ha completato l'ordine",
        4: " ha appena ordinato (consegna domani)",
        5: " ha confermato il suo ordine",
    }
    # localized message tails
    tails = {
        "cz": [
            " právě objednal/a Fold360™",
            " právě potvrdil/a objednávku",
            " právě koupil/a Fold360™",
            " dokončil/a objednávku",
            " právě objednal/a (doručení zítra)",
            " potvrdil/a svou objednávku",
        ],
        "si": [
            " je pravkar naročil/a Fold360™",
            " je pravkar potrdil/a naročilo",
            " je pravkar kupil/a Fold360™",
            " je dokončal/a naročilo",
            " je pravkar naročil/a (dostava jutri)",
            " je potrdil/a svoje naročilo",
        ],
        "hu": [
            " most rendelte a Fold360™-t",
            " most erősítette meg a rendelést",
            " most vásárolta a Fold360™-t",
            " befejezte a rendelést",
            " most rendelte (szállítás holnap)",
            " megerősítette a rendelését",
        ],
        "sk": [
            " práve objednal/a Fold360™",
            " práve potvrdil/a objednávku",
            " práve kúpil/a Fold360™",
            " dokončil/a objednávku",
            " práve objednal/a (doručenie zajtra)",
            " potvrdil/a svoju objednávku",
        ],
        "pl": [
            " właśnie zamówił/a Fold360™",
            " właśnie potwierdził/a zamówienie",
            " właśnie kupił/a Fold360™",
            " dokończył/a zamówienie",
            " właśnie zamówił/a (dostawa jutro)",
            " potwierdził/a swoje zamówienie",
        ],
    }
    times = {
        "cz": ["před 2 minutami", "před 5 minutami", "před 8 minutami", "před 12 minutami", "před 18 minutami", "před 24 minutami"],
        "si": ["pred 2 minutama", "pred 5 minutami", "pred 8 minutami", "pred 12 minutami", "pred 18 minutami", "pred 24 minutami"],
        "hu": ["2 perce", "5 perce", "8 perce", "12 perce", "18 perce", "24 perce"],
        "sk": ["pred 2 minútami", "pred 5 minútami", "pred 8 minútami", "pred 12 minútami", "pred 18 minútami", "pred 24 minútami"],
        "pl": ["2 minuty temu", "5 minut temu", "8 minut temu", "12 minut temu", "18 minut temu", "24 minuty temu"],
    }
    lines = []
    for i, (initial, name, city) in enumerate(g["popups"]):
        img = f"/assets/img/reviews/fold360/popup-{(i % 3) + 1}.png"
        lines.append(
            f'  {{ "initial": "{initial}", "name": "{name}", "image": "{img}", '
            f'"message": "{tails[geo][i]}", "time": "{times[geo][i]}, {city}" }}'
        )
    return ",\n".join(lines)


def transform_lp(geo: str, g: dict, c: dict) -> str:
    t = IT_LP
    t = t.replace('lang="it"', f'lang="{g["lang"]}"')
    t = t.replace("https://homepickdock.com/it/fold360/", f"https://homepickdock.com/{geo}/fold360/")
    t = t.replace("GEO: 'it'", f"GEO: '{geo}'")
    t = t.replace("CURRENCY: 'EUR'", f"CURRENCY: '{g['currency']}'")
    t = t.replace("PRICE: 419.00,", f"PRICE: {g['price']},")
    t = t.replace("OFFER_NAME: 'Fold360 IT'", f"OFFER_NAME: 'Fold360 {geo.upper()}'")
    t = t.replace("LP_ID: 'it-fold360-v1'", f"LP_ID: '{geo}-fold360-v1'")
    t = t.replace(
        "COOKIE_TEXT: 'Usiamo cookie tecnici e di terze parti per migliorare la tua esperienza e per analisi.',\n  COOKIE_ACCEPT: 'Accetta',\n  COOKIE_LEARN: 'Scopri di più'",
        f"COOKIE_TEXT: '{g['cookie']['text']}',\n  COOKIE_ACCEPT: '{g['cookie']['accept']}',\n  COOKIE_LEARN: '{g['cookie']['learn']}'",
    )
    t = t.replace("SUBMITTING_LABEL: 'Invio in corso...'", f"SUBMITTING_LABEL: '{c['submitting']}'")

    # Meta
    t = t.replace(
        "Fold360™ — Smartphone Pieghevole a 3 Schermi | -70% Solo Oggi",
        c["title"],
    )
    t = t.replace(
        "Fold360™: smartphone pieghevole a 3 schermi, batteria 6800 mAh, fotocamera 48 MP, 5G, Dual SIM, ricarica 66W e funzioni AI. Pagamento alla consegna, spedizione 24/48h.",
        c["desc"],
    )
    t = t.replace("Fold360™ — Smartphone Pieghevole | -50% Solo Oggi", c["og_title"])  # may already be 70
    t = t.replace("Fold360™ — Smartphone Pieghevole | -70% Solo Oggi", c["og_title"])
    t = t.replace(
        "Smartphone pieghevole a 3 schermi, batteria 6800 mAh, fotocamera 48 MP, 5G e Dual SIM. Pagamento alla consegna.",
        c["og_desc"],
    )
    t = t.replace("Fold360™ — Smartphone Pieghevole a 3 Schermi", c["json_name"])
    t = t.replace(
        "Smartphone pieghevole Fold360™ a 3 schermi, batteria 6800 mAh, ricarica 66W, 5G, Dual SIM, fotocamera 48 MP e funzioni AI.",
        c["json_desc"],
    )
    t = t.replace('"price": "419.00"', f'"price": "{g["price"]:.2f}"' if isinstance(g["price"], float) else f'"price": "{g["price"]}"')
    t = t.replace('"priceCurrency": "EUR"', f'"priceCurrency": "{g["currency"]}"')

    # Banner / hero
    t = t.replace("🔥 GARANZIA 2 ANNI · PAGAMENTO ALLA CONSEGNA · -70% 🔥", c["banner"])
    t = t.replace("<strong>4,9/5</strong> — <strong>1.824</strong> recensioni positive", c["rating"])
    t = t.replace("🛡️ Garanzia 2 anni · Pagamento alla consegna", c["guarantee_line"])
    t = t.replace(
        "Smartphone pieghevole con 3 schermi, fotocamera da 48mpx e batteria da 6.800mAH",
        c["h1"],
    )
    t = t.replace(
        'La tecnologia innovativa <strong>Fold360™</strong> offre il giusto equilibrio tra stile, mobilità e funzionalità: design pieghevole con grande schermo, connettività <strong>5G</strong>, funzioni di intelligenza artificiale, ricarica ultra-rapida e batteria a lunga durata.',
        c["sub"],
    )
    t = t.replace("SCONTO 70% FINO A ESAURIMENTO SCORTE", c["discount_label"])
    t = t.replace("1.397 €</span>", f'{g["price_old"]}</span>')
    t = t.replace("419 €</span>", f'{g["price_new"]}</span>')
    t = t.replace("ORDINA Fold360™ →", c["cta_order"])
    t = t.replace("🔒 Nessun anticipo · Nessuna carta · Paghi solo alla consegna", c["no_prepay"])

    for it_title, loc_title, it_sub, loc_sub in c["trust"]:
        t = t.replace(f">{it_title}</div>", f">{loc_title}</div>")
        t = t.replace(f">{it_sub}</div>", f">{loc_sub}</div>")

    t = t.replace('aria-label="Offerta a tempo"', f'aria-label="{c["offer_aria"]}"')
    t = t.replace("⏰ Offerta -70% scade tra", c["countdown_label"])
    t = t.replace("<small>Ore</small>", f'<small>{c["hours"]}</small>')
    t = t.replace("<small>Min</small>", f'<small>{c["mins"]}</small>')
    t = t.replace("<small>Sec</small>", f'<small>{c["secs"]}</small>')
    t = t.replace(
        "Disponibilità: <strong>Ultimi 3 pezzi rimasti</strong> · <strong>15 persone</strong> stanno guardando questa offerta ora",
        c["watching"],
    )

    t = t.replace("Completa il tuo ordine", c["form_title"])
    t = t.replace(
        "Compila il modulo qui sotto, il nostro team ti contatterà per confermare tutti i dettagli.",
        c["form_sub"],
    )
    t = t.replace("Nome e cognome *", c["label_name"])
    t = t.replace("Numero di telefono *", c["label_phone"])
    t = t.replace("Indirizzo di consegna *", c["label_address"])
    t = t.replace("Es. Mario Rossi", g["placeholders"]["name"])
    t = t.replace("Es. 333 1234567", g["placeholders"]["phone"])
    t = t.replace("Via, civico, città, CAP", g["placeholders"]["address"])
    t = t.replace("Inserisci nome e cognome (almeno 3 caratteri)", c["err_name"])
    t = t.replace("Inserisci un numero di telefono valido", c["err_phone"])
    t = t.replace("Inserisci un indirizzo completo (almeno 10 caratteri)", c["err_address"])
    t = t.replace("CONFERMA L'ORDINE", c["submit"])

    # Features
    t = t.replace("01 — Smartphone pieghevole di ultima generazione", c["f1_label"])
    t = t.replace("Potenza e controllo senza compromessi", c["f1_title"])
    t = t.replace(">3 schermi</span>", f'>{c["f1_chips"][0]}</span>', 1)
    t = t.replace(">Design pieghevole</span>", f'>{c["f1_chips"][1]}</span>', 1)
    t = t.replace(">Batteria 6800 mAh</span>", f'>{c["f1_chips"][2]}</span>', 1)
    t = t.replace(
        "Dimentica i limiti del passato: Fold360™ rivoluziona lavoro e tempo libero con <strong>design pieghevole a 3 schermi</strong> e una batteria che dura giorni. Multitasking vero, su uno schermo ampio.",
        c["f1_p1"],
    )
    t = t.replace(
        "Vivi il massimo di comfort, controllo e sicurezza in ogni situazione. Libertà e potenza, sempre a portata di mano.",
        c["f1_p2"],
    )
    t = t.replace("02 — Resistenza e intelligenza in un solo prodotto", c["f2_label"])
    t = t.replace("5G, AI e batteria pensata per non fermarti mai", c["f2_title"])
    t = t.replace(">Connessione 5G</span>", f'>{c["f2_chips"][0]}</span>')
    t = t.replace(">Funzioni AI</span>", f'>{c["f2_chips"][1]}</span>')
    t = t.replace(">Ricarica 66W</span>", f'>{c["f2_chips"][2]}</span>')
    t = t.replace(
        "La scelta giusta per chi cerca affidabilità: <strong>5G</strong>, scocca resistente all’acqua e batteria da <strong>6800 mAh</strong> per un uso sereno in ogni situazione. Le funzioni AI supportano la giornata in modo concreto.",
        c["f2_p1"],
    )
    t = t.replace(
        "La <strong>ricarica rapida 66W</strong> ti fa risparmiare ore: carica completa in circa 25 minuti. Più autonomia, meno attese.",
        c["f2_p2"],
    )
    t = t.replace("03 — Dual SIM e connessione 5G", c["f3_label"])
    t = t.replace("Due numeri, un solo dispositivo — sempre connesso", c["f3_title"])
    t = t.replace(">Internet 5G</span>", f'>{c["f3_chips"][1]}</span>')
    t = t.replace(">Fotocamera 48 MP</span>", f'>{c["f3_chips"][2]}</span>')
    t = t.replace(
        "Gestisci due numeri su un solo dispositivo grazie alla <strong>Dual SIM</strong>: ideale per separare lavoro e vita privata. Naviga alla massima velocità con il <strong>5G</strong>, senza rallentamenti.",
        c["f3_p1"],
    )
    t = t.replace(
        "Doppio obiettivo da <strong>48 MP</strong> per foto nitide e dettagliate. Più libertà, più produttività, sempre connesso ovunque tu sia.",
        c["f3_p2"],
    )

    # Comparison table
    t = t.replace("Confronto diretto", c["compare_sub"])
    t = t.replace("Smartphone tradizionale vs Fold360™", c["compare_title"])
    t = t.replace(">Tradizionale</th>", f'>{c["traditional"]}</th>')
    it_rows = [
        ("Formato", "Schermo fisso, poco pratico", "Design pieghevole compatto"),
        ("Schermo", "Un solo display", "3 schermi pieghevoli"),
        ("Batteria", "Si scarica in poche ore", "6800 mAh ad alta autonomia"),
        ("Ricarica", "Lenta e poco pratica", "66W: piena in ~25 minuti"),
        ("Connettività", "4G / una sola SIM", "5G + Dual SIM"),
        ("Extra", "Funzioni base", "AI + fotocamera 48 MP"),
    ]
    for (ik, ib, ig), (lk, lb, lg) in zip(it_rows, c["rows"]):
        t = t.replace(f"<strong>{ik}</strong>", f"<strong>{lk}</strong>")
        t = t.replace(f">{ib}</td>", f">{lb}</td>")
        t = t.replace(f">{ig}</td>", f">{lg}</td>")

    # Reviews
    t = t.replace(
        "Oltre 1.800 clienti soddisfatti. Scopri perché scelgono Fold360™.",
        c["reviews_title"],
    )
    t = t.replace("Batteria e 3 schermi davvero utili.", c["r1_title"])
    t = t.replace(
        "«Lavoro tutto il giorno e la batteria non si scarica: i tre schermi sono un vero vantaggio. Consigliato!»",
        f"«{g['reviews'][0][3]}»",
    )
    t = t.replace("David M. — Milano, Cliente verificato", f"{g['reviews'][0][0]} — {g['reviews'][0][1]}, {c['verified']}")
    t = t.replace("Comodo da usare, 5G sempre veloce.", c["r2_title"])
    t = t.replace(
        "«È molto comodo per scrivere e la connessione 5G è sempre rapida. Telefono moderno e pratico.»",
        f"«{g['reviews'][1][3]}»",
    )
    t = t.replace("Maria G. — Torino, Cliente verificato", f"{g['reviews'][1][0]} — {g['reviews'][1][1]}, {c['verified']}")
    t = t.replace("Si ricarica in fretta ed è resistente.", c["r3_title"])
    t = t.replace(
        "«Si carica rapidamente, è resistente all’acqua e molto solido. Ideale per i miei ritmi!»",
        f"«{g['reviews'][2][3]}»",
    )
    t = t.replace("Elena R. — Napoli, Cliente verificato", f"{g['reviews'][2][0]} — {g['reviews'][2][1]}, {c['verified']}")

    # Package
    t = t.replace("Cosa include il pacchetto?", c["package_sub"])
    t = t.replace("Kit completo Fold360™, pronto all'uso", c["package_title"])
    it_items = [
        "Smartphone Fold360™ pieghevole",
        "Caricatore 66W",
        "Cavo USB-C",
        "Tutto il necessario per l’uso immediato",
        "Batteria 6800 mAh — alta autonomia",
        "Cover in regalo",
        "<strong>Garanzia ufficiale di 2 anni</strong>",
    ]
    for ii, li in zip(it_items, c["package_items"]):
        t = t.replace(f"<li>{ii}</li>", f"<li>{li}</li>")
        t = t.replace(f'<li class="is-bonus">{ii}</li>', f'<li class="is-bonus">{li}</li>')

    # FAQ
    t = t.replace("Domande frequenti", c["faq_title"])
    it_faqs = [
        ("Come posso ordinare?", "Compila il modulo con i tuoi dati. Un consulente ti contatterà per confermare l’ordine Fold360™."),
        ("Posso pagare alla consegna?", "Sì, per la tua sicurezza offriamo il pagamento in contanti direttamente al corriere. Tieni pronti 419€."),
        ("Quando arriva?", "La consegna avviene entro 24-48 ore lavorative. Ti contattiamo entro poche ore per confermare l’ordine."),
        ("Come posso ricevere assistenza?", "Compila il modulo: uno dei nostri consulenti sarà a tua disposizione per qualsiasi domanda prima o dopo l’ordine."),
        ("I miei dati sono al sicuro?", "Sì, i tuoi dati sono protetti e vengono usati esclusivamente per la spedizione del prodotto."),
    ]
    for (iq, ia), (lq, la) in zip(it_faqs, c["faqs"]):
        t = t.replace(f"<summary>{iq}</summary>", f"<summary>{lq}</summary>")
        t = t.replace(
            f'<div class="faq-accordion__body">{ia}</div>',
            f'<div class="faq-accordion__body">{la.format(price=g["price_ready"])}</div>',
        )

    # Image alts
    for old_alt, new_alt in c.get("alts", []):
        t = t.replace(old_alt, new_alt)

    # Footer
    t = t.replace(
        "Prodotti utili per la vita quotidiana, consegna in 24-48 ore con pagamento alla consegna.",
        g["footer_blurb"],
    )
    # Replace entire information+contact footer columns
    import re

    t = re.sub(
        r'<div>\s*<h4 class="site-footer__heading">Informazioni</h4>.*?</div>\s*<div>\s*<h4 class="site-footer__heading">Contatti</h4>.*?</div>',
        footer_html(geo, g),
        t,
        count=1,
        flags=re.S,
    )
    t = t.replace("Tutti i diritti riservati.", f'{g["footer_rights"]}.')

    # Popups
    import re as _re

    t = _re.sub(
        r"window\.POPUP_PURCHASES = \[\n.*?\n\];",
        "window.POPUP_PURCHASES = [\n" + build_popups(geo, g) + "\n];",
        t,
        count=1,
        flags=_re.S,
    )

    # Fix Dual SIM chip (first chip in feature 3 stays Dual SIM - ok internationally)
    return t


def transform_ty(geo: str, g: dict, c: dict) -> str:
    t = IT_TY
    t = t.replace('lang="it"', f'lang="{g["lang"]}"')
    t = t.replace("GEO: 'it'", f"GEO: '{geo}'")
    t = t.replace("CURRENCY: 'EUR'", f"CURRENCY: '{g['currency']}'")
    t = t.replace("PRICE: 129.00,", f"PRICE: {g['price']},")
    t = t.replace("trackPurchase(129.00, 'EUR')", f"trackPurchase({g['price']}, '{g['currency']}')")
    t = t.replace(
        "COOKIE_TEXT: 'Usiamo cookie tecnici e di terze parti per migliorare la tua esperienza e per analisi.',\n  COOKIE_ACCEPT: 'Accetta',\n  COOKIE_LEARN: 'Scopri di più'",
        f"COOKIE_TEXT: '{g['cookie']['text']}',\n  COOKIE_ACCEPT: '{g['cookie']['accept']}',\n  COOKIE_LEARN: '{g['cookie']['learn']}'",
    )
    t = t.replace(
        "Ordine ricevuto — Attendi la chiamata di conferma | Fold360™",
        c["ty_title"],
    )
    t = t.replace(
        "Il tuo ordine Fold360™ è stato registrato. Manca solo un ultimo passaggio: rispondi alla chiamata di conferma del nostro operatore.",
        c["ty_desc"],
    )
    t = t.replace("Il tuo ordine è stato registrato con successo!", c["ty_h1"])
    t = t.replace(
        "Perfetto — il tuo ordine è in elaborazione. Manca solo <strong>un ultimo passaggio</strong> per completarlo e far partire la spedizione.",
        c["ty_sub"],
    )
    t = t.replace("Il team homepickdock al lavoro: call center e logistica COD", c["ty_alt"])
    t = t.replace("👇 Cosa devi fare adesso", c["ty_eyebrow"])
    t = t.replace("📞 Rispondi alla chiamata di conferma", c["ty_action_title"])
    t = t.replace(
        "Un nostro operatore ti contatterà <strong>nelle prossime ore</strong> per confermare il tuo ordine.",
        c["ty_action_body"],
    )
    t = t.replace(
        "Se non rispondi alla chiamata, l'ordine verrà automaticamente annullato.",
        c["ty_action_warn"],
    )
    t = t.replace("🕒 Orari di contatto", c["ty_hours_h"])
    t = t.replace("<strong>Lunedì – Sabato</strong> · 9:00 – 18:00", c["ty_hours"])
    t = t.replace("📋 Cosa succede dopo", c["ty_next_h"])
    it_steps = [
        "Rispondi alla chiamata e <strong>conferma i tuoi dati</strong>",
        "Il tuo ordine verrà spedito entro <strong>24–48 ore</strong>",
        "Consegna a domicilio e <strong>pagamento alla consegna</strong>",
    ]
    for ii, li in zip(it_steps, c["ty_steps"]):
        t = t.replace(f"<li>{ii}</li>", f"<li>{li}</li>")
    it_badges = ("🔒 Pagamento alla consegna", "🛡️ Garanzia 24 mesi", "🔐 Protezione SSL")
    for ib, lb in zip(it_badges, c["ty_badges"]):
        t = t.replace(ib, lb)

    import re

    # Footer: replace info+contact block (single-line compact version in TY)
    footer_links = "".join(
        f'\n        <li><a href="/{geo}/{href}">{label}</a></li>'
        for href, label in g["links"]
    )
    t = re.sub(
        r'<h4 class="site-footer__heading">Informazioni</h4>\s*<ul class="site-footer__list">.*?</ul>',
        f'<h4 class="site-footer__heading">{g["footer_info"]}</h4>\n      <ul class="site-footer__list">{footer_links}\n      </ul>',
        t,
        count=1,
        flags=re.S,
    )
    t = t.replace(
        '<h4 class="site-footer__heading">Contatti</h4>',
        f'<h4 class="site-footer__heading">{g["footer_contact"]}</h4>',
    )
    t = t.replace("Tutti i diritti riservati.", f'{g["footer_rights"]}.')
    return t


IT_ALTS = [
    "Fold360™ — kit smartphone pieghevole a 3 schermi",
    "Fold360™ Kit completo",
    "Fold360™ — smartphone pieghevole a 3 schermi in uso",
    "Fold360™ — batteria ad alta capacità 6800 mAh",
    "Fold360™ — fotocamera 48 MP su 3 schermi",
    "Cliente soddisfatto con Fold360™",
    "Unboxing Fold360™ con cover e caricatore",
    "Fold360™ con box, cavo e cover",
    "Contenuto confezione Fold360™",
]

ALTS = {
    "cz": [
        "Fold360™ — sada skládacího smartphone se 3 obrazovkami",
        "Fold360™ Kompletní sada",
        "Fold360™ — skládací smartphone se 3 obrazovkami v použití",
        "Fold360™ — baterie s vysokou kapacitou 6800 mAh",
        "Fold360™ — fotoaparát 48 MP na 3 obrazovkách",
        "Spokojený zákazník s Fold360™",
        "Unboxing Fold360™ s obalem a nabíječkou",
        "Fold360™ s krabicí, kabelem a obalem",
        "Obsah balení Fold360™",
    ],
    "si": [
        "Fold360™ — komplet zložljivega pametnega telefona s 3 zasloni",
        "Fold360™ Celoten komplet",
        "Fold360™ — zložljiv pametni telefon s 3 zasloni v uporabi",
        "Fold360™ — baterija z veliko kapaciteto 6800 mAh",
        "Fold360™ — kamera 48 MP na 3 zaslonih",
        "Zadovoljna stranka s Fold360™",
        "Unboxing Fold360™ z ovitkom in polnilcem",
        "Fold360™ s škatlo, kablom in ovitkom",
        "Vsebina paketa Fold360™",
    ],
    "hu": [
        "Fold360™ — 3 képernyős összecsukható okostelefon készlet",
        "Fold360™ Teljes készlet",
        "Fold360™ — 3 képernyős összecsukható okostelefon használatban",
        "Fold360™ — nagy kapacitású 6800 mAh akkumulátor",
        "Fold360™ — 48 MP kamera 3 képernyőn",
        "Elégedett vásárló Fold360™-nel",
        "Fold360™ kicsomagolás tokkal és töltővel",
        "Fold360™ dobozzal, kábellel és tokkal",
        "Fold360™ csomag tartalma",
    ],
    "sk": [
        "Fold360™ — sada skladacieho smartfónu s 3 obrazovkami",
        "Fold360™ Kompletná sada",
        "Fold360™ — skladací smartfón s 3 obrazovkami v použití",
        "Fold360™ — batéria s vysokou kapacitou 6800 mAh",
        "Fold360™ — fotoaparát 48 MP na 3 obrazovkách",
        "Spokojný zákazník s Fold360™",
        "Unboxing Fold360™ s obalom a nabíjačkou",
        "Fold360™ s krabicou, káblom a obalom",
        "Obsah balenia Fold360™",
    ],
    "pl": [
        "Fold360™ — zestaw składanego smartfona z 3 ekranami",
        "Fold360™ Kompletny zestaw",
        "Fold360™ — składany smartfon z 3 ekranami w użyciu",
        "Fold360™ — bateria o dużej pojemności 6800 mAh",
        "Fold360™ — aparat 48 MP na 3 ekranach",
        "Zadowolony klient z Fold360™",
        "Unboxing Fold360™ z etui i ładowarką",
        "Fold360™ z pudełkiem, kablem i etui",
        "Zawartość paczki Fold360™",
    ],
}

for _geo, _alts in ALTS.items():
    COPY[_geo]["alts"] = list(zip(IT_ALTS, _alts))


def main():
    for geo, g in GEOS.items():
        c = COPY[geo]
        out_dir = ROOT / geo / "fold360"
        out_dir.mkdir(parents=True, exist_ok=True)
        lp = transform_lp(geo, g, c)
        ty = transform_ty(geo, g, c)
        (out_dir / "index.html").write_text(lp, encoding="utf-8")
        (out_dir / "thank-you.html").write_text(ty, encoding="utf-8")
        print(f"OK {geo}/fold360/  price={g['price_new']}  old={g['price_old']}")

    # Sitemap entries
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    for geo in GEOS:
        url = f"https://homepickdock.com/{geo}/fold360/"
        if url not in text:
            entry = f'  <url><loc>{url}</loc><lastmod>2026-07-25</lastmod><changefreq>weekly</changefreq><priority>0.95</priority></url>\n'
            text = text.replace(
                "  <url><loc>https://homepickdock.com/it/fold360/</loc>",
                entry + "  <url><loc>https://homepickdock.com/it/fold360/</loc>",
                1,
            )
    sm.write_text(text, encoding="utf-8")
    print("sitemap updated")


if __name__ == "__main__":
    main()
