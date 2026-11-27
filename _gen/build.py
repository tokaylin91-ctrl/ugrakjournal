#!/usr/bin/env python3
"""ugrakjournal.com çok sayfalı yapı üreticisi (27 Kas 2026).
Çalıştır: python3 _gen/build.py  (depo kökünde). Ana sayfa (index.html) elle tutulur; bu betik
şehir rehberleri, hakkımızda, yardım, iletişim (TR + /en/), site.css, sitemap.xml ve robots.txt üretir."""
import json, os, re, html, datetime, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from sehirler import SEHIR
import nasil
from yazilar import YAZI
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.environ.get('APP', '/home/claude/ugrak-uretim/sehir-app')
RIV = os.environ.get('RIV', '/home/claude/ugrak-uretim/sunucu/rivayet/rivayet.json')
SITE = 'https://ugrakjournal.com'
BUGUN = datetime.date.today().isoformat()
KONTROL = ('27 Kasım 2026', '27 November 2026')
CSSV = '2'
E = html.escape
ENSLUG = {'sinop': 'sinop', 'amasra': 'amasra', 'kapadokya': 'cappadocia', 'safranbolu': 'safranbolu'}
URETILEN = []
EK = {'sinop': ("Sinop'ta", "Sinop'un"), 'amasra': ("Amasra'da", "Amasra'nın"), 'kapadokya': ("Kapadokya'da", "Kapadokya'nın"), 'safranbolu': ("Safranbolu'da", "Safranbolu'nun")}

def yaz(yol, icerik):
    tam = os.path.join(KOK, yol)
    os.makedirs(os.path.dirname(tam), exist_ok=True)
    open(tam, 'w').write(icerik)
    URETILEN.append(yol)

def url(yol):
    return SITE + '/' + yol.replace('index.html', '')

# ---------- içerik ----------
def icerik(c):
    p = os.path.join(APP, 'app_content_live.json' if c == 'sinop' else f'cities/{c}/content.json')
    return json.load(open(p)), json.load(open(os.path.join(APP, f'cities/{c}/city.json')))

def paragraflar(sayfa):
    """Mini görevden önceki açıklama paragrafları (tr, en)."""
    out = []
    for it in sayfa['items']:
        if it['type'] == 'label':
            break
        if it['type'] == 'p' and it.get('t'):
            out.append((it['t'], it.get('en') or ''))
    return out

def etiketli(sayfa):
    """Rota sayfası: etiket -> sonraki paragraf (En güzel zaman, Pratik not)."""
    out, son = {}, None
    for it in sayfa['items']:
        if it['type'] == 'label':
            son = (it.get('tr'), it.get('en'))
        elif it['type'] == 'p' and son:
            out[son] = (it['t'], it.get('en') or '')
            son = None
    return out

def gorsel(c, n):
    kaynak = os.path.join(APP, 'im', f'p{n}_{n}-0.webp') if c == 'sinop' else os.path.join(APP, 'im', c, f'p{n}.webp')
    if not os.path.exists(kaynak):
        return None
    hedef = f'sehirler/img/{c}-{n}.webp'
    tam = os.path.join(KOK, hedef)
    if not os.path.exists(tam):
        os.makedirs(os.path.dirname(tam), exist_ok=True)
        im = Image.open(kaynak).convert('RGB')
        im.thumbnail((360, 360))
        im.save(tam, 'WEBP', quality=72)
    return '/' + hedef

# ---------- iskelet ----------
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&family=Hanken+Grotesk:wght@400;500;600;700&display=swap">'
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "Uğrak Journal", "alternateName": "Uğrak", "url": SITE + "/",
       "logo": SITE + "/logo-kiremit.png", "email": "info@ugrakjournal.com", "founder": {"@type": "Person", "name": "Aylin Tok"},
       "address": {"@type": "PostalAddress", "addressLocality": "Sinop", "addressCountry": "TR"},
       "sameAs": ["https://instagram.com/ugrakjournal"]}

def bas(dil, baslik, aciklama, yol, karsi=None, ld=None, gorsel_url='/og-ugrak.jpg'):
    can = url(yol)
    alt = ''
    if karsi:
        tr_y, en_y = (yol, karsi) if dil == 'tr' else (karsi, yol)
        alt = (f'<link rel="alternate" hreflang="tr" href="{url(tr_y)}"><link rel="alternate" hreflang="en" href="{url(en_y)}">'
               f'<link rel="alternate" hreflang="x-default" href="{url(tr_y)}">')
    graf = [ORG] + (ld or [])
    return f'''<!doctype html>
<html lang="{dil}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(baslik)}</title>
<meta name="description" content="{E(aciklama)}">
<link rel="canonical" href="{can}">{alt}
<meta property="og:type" content="website"><meta property="og:url" content="{can}"><meta property="og:title" content="{E(baslik)}">
<meta property="og:description" content="{E(aciklama)}"><meta property="og:image" content="{SITE}{gorsel_url}"><meta property="og:locale" content="{'tr_TR' if dil=='tr' else 'en_GB'}">
<meta name="theme-color" content="#5E2318">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT}
<link rel="stylesheet" href="/site.css?v={CSSV}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script>
</head>
<body>
'''

MENU = {
 'tr': [('/sehirler/', 'Şehirler'), ('/dijital/', 'Uğrak Çocuk'), ('/nasil-alinir/', 'Nasıl alınır'), ('/hakkimizda/', 'Hakkımızda'), ('/yardim/', 'Yardım'), ('/iletisim/', 'İletişim')],
 'en': [('/en/', 'City journals'), ('/en/how-to-buy/', 'How to buy'), ('/en/about/', 'About'), ('/en/help/', 'Help'), ('/en/contact/', 'Contact')],
}

def ust(dil, aktif, karsi_url):
    linkler = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == aktif else ""}>{t}</a>' for h, t in MENU[dil])
    dil_l = f'<a class="lang" href="{karsi_url}" hreflang="{"en" if dil=="tr" else "tr"}" lang="{"en" if dil=="tr" else "tr"}">{"EN" if dil=="tr" else "TR"}</a>'
    btn = '<a class="btn" href="/magaza/">Mağaza</a>' if dil == 'tr' else '<a class="btn" href="/en/#journals">Buy</a>'
    mobil = ('<a class="shop" href="/magaza/">Mağaza · Defterini al</a>' if dil == 'tr' else '<a class="shop" href="/en/#journals">Buy a journal</a>') + ''.join(f'<a href="{h}">{t}</a>' for h, t in MENU[dil])
    ana = '/' if dil == 'tr' else '/en/'
    return f'''<header><div class="wrap nav">
 <a class="logo" href="{ana}" aria-label="Uğrak"><img src="/logo-kiremit.png" alt="Uğrak" width="72" height="32"></a>
 <nav aria-label="{"Ana menü" if dil=="tr" else "Main menu"}">{linkler}</nav>
 {dil_l}{btn}
 <details class="menu"><summary>{"Menü" if dil=="tr" else "Menu"}</summary><div>{mobil}</div></details>
</div></header>
'''

def alt(dil):
    if dil == 'tr':
        return '''<footer><div class="wrap foot">
 <div><img src="/logo-krem.png" alt="Uğrak" width="67" height="30"><p>Bir şehrin denizini, taşını ve sofrasını deftere taşırız. Sinop'ta kurulduk.</p></div>
 <div><b>Şehirler</b><a href="/sehirler/sinop/">Sinop</a><a href="/sehirler/amasra/">Amasra</a><a href="/sehirler/kapadokya/">Kapadokya</a><a href="/sehirler/safranbolu/">Safranbolu</a></div>
 <div><b>Uğrak</b><a href="/hakkimizda/">Hakkımızda</a><a href="/dijital/">Uğrak Çocuk · Martı</a><a href="/yardim/">Yardım ve SSS</a><a href="/iletisim/">İletişim</a></div>
 <div><b>Satış</b><a href="/dijital/bilgilendirme.html">Satış koşulları</a><a href="/yardim/#iade">İptal ve iade</a><a href="/yardim/#kvkk">Kişisel veriler</a><a href="/en/">English</a></div>
 <div class="copy">© 2026 Uğrak · Satıcı: Aylin Tok (Uğrak), Yeni Mahalle, Gazi Caddesi No: 49/A, Merkez / Sinop · satis@ugrakjournal.com · Ödemeler Shopier güvenli ödeme sayfasında alınır; kart bilgin bize iletilmez.</div>
</div></footer>
'''
    return '''<footer><div class="wrap foot">
 <div><img src="/logo-krem.png" alt="Uğrak" width="67" height="30"><p>Interactive city journals for Turkey, made in Sinop.</p></div>
 <div><b>City guides</b><a href="/en/cities/sinop/">Sinop</a><a href="/en/cities/amasra/">Amasra</a><a href="/en/cities/cappadocia/">Cappadocia</a><a href="/en/cities/safranbolu/">Safranbolu</a></div>
 <div><b>Uğrak</b><a href="/en/about/">About us</a><a href="/en/help/">Help & FAQ</a><a href="/en/contact/">Contact</a></div>
 <div><b>Language</b><a href="/">Türkçe</a></div>
 <div class="copy">© 2026 Uğrak · Aylin Tok · Sinop, Türkiye · Payments are taken on Shopier's secure page; we never see your card details.</div>
</div></footer>
'''

FIYAT_JS = '''<script>(function(){var d=new Date();if(d>=new Date('2026-12-11T00:00:00+03:00')){document.querySelectorAll('.pr').forEach(function(e){e.textContent='790 TL'});document.querySelectorAll('.prn').forEach(function(e){e.remove()})}})();</script>'''

def son(dil, sepet=False):
    s = '<script src="/sepet.js?v=5" defer></script>' if sepet else ''
    return alt(dil) + FIYAT_JS + s + '\n</body>\n</html>\n'

# ---------- şehir sayfası ----------
def sehir_sayfasi(c, dil):
    cfg = SEHIR[c]; d, cj = icerik(c)
    i = 0 if dil == 'tr' else 1
    ad = cfg['ad'][i]
    yol_tr = f'sehirler/{c}/index.html'; yol_en = f'en/cities/{ENSLUG[c]}/index.html'
    yol, karsi = (yol_tr, yol_en) if dil == 'tr' else (yol_en, yol_tr)
    T = (lambda tr, en: tr) if dil == 'tr' else (lambda tr, en: en)

    baslik = T(f'{ad} Gezi Rehberi: Görülecek Yerler, Rotalar, Tarih · Uğrak', f'{ad} Travel Guide: Things to Do, Walking Routes & History · Uğrak')
    aciklama = cfg['ozet'][i].split('. ')[0] + '.'
    # yerler
    gruplar = [g for g in cj['groups']['kesfet'] if g['h'][0] in cfg['gruplar']]
    yer_html, yer_ld = '', []
    for g in gruplar:
        yer_html += f'<h3 style="margin:34px 0 4px;font-size:15px;font-family:var(--sans);font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--kiremit)">{E(g["h"][i])}</h3>'
        for n in g.get('cards', []):
            s = d[str(n)]
            ps = paragraflar(s)
            if not ps:
                continue
            isim = s['title'] if dil == 'tr' else (s.get('sub') or s['title'])
            alt_ad = s.get('sub') if dil == 'tr' else s['title']
            g_url = gorsel(c, n)
            img = f'<img src="{g_url}" alt="{E(isim)} gravürü" loading="lazy" width="150" height="150">' if g_url else '<span></span>'
            metin = ''.join(f'<p>{E(p[i])}</p>' for p in ps if p[i])
            yer_html += f'<article class="place" id="yer-{n}">{img}<div><h3>{E(isim)}</h3>' + (f'<p class="en">{E(alt_ad)}</p>' if alt_ad and alt_ad != isim else '') + metin + '</div></article>'
            yer_ld.append({"@type": "TouristAttraction", "name": isim, "description": ' '.join(p[i] for p in ps if p[i])[:300]})
    # tarih
    tarih_p = ''.join(f'<p>{E(it[i] if False else (it["t"] if dil=="tr" else it.get("en","")))}</p>' for it in d['5']['items'] if it['type'] == 'p' and it.get('t') and not it['t'].startswith('Yola çıkmadan'))
    tl = next((it for it in d['6']['items'] if it['type'] == 'tl'), None)
    tl_html = ''
    if tl:
        tl_html = '<ul class="tl">' + ''.join(f'<li><b>{E(r["y"] if dil=="tr" else r["ye"])}</b>{E(r["tr"] if dil=="tr" else r["en"])}</li>' for r in tl['rows']) + '</ul>'
    # üç gün
    ucgun = ''
    if cfg.get('ucgun'):
        s = d[str(cfg['ucgun'])]; gunler, cur = [], None
        for it in s['items']:
            if it['type'] == 'label':
                cur = [it['tr'] if dil == 'tr' else it['en'], []]; gunler.append(cur)
            elif it['type'] == 'check' and cur:
                cur[1].append(it['tr'] if dil == 'tr' else it['en'])
        ucgun = (f'<h2 id="uc-gun">{E(s["title"] if dil=="tr" else s["sub"])}</h2><div class="days">' +
                 ''.join(f'<div class="day"><h3>{E(g[0])}</h3><ul>' + ''.join(f'<li>{E(x)}</li>' for x in g[1]) + '</ul></div>' for g in gunler) + '</div>')
    # rotalar
    rota = ''
    for n in cfg['rotalar']:
        s = d[str(n)]; ps = paragraflar(s) or [(next((it['t'] for it in s['items'] if it['type']=='p'), ''), next((it.get('en','') for it in s['items'] if it['type']=='p'), ''))]
        et = etiketli(s)
        ek = ''
        for (etr, een), (vtr, ven) in et.items():
            if etr in ('En güzel zaman', 'Pratik not') and (dil == 'tr' or (een and ven)):
                ek += f'<small><b>{E(etr if dil=="tr" else een)}:</b> {E(vtr if dil=="tr" else ven)}</small>'
        isim = s['title'] if dil == 'tr' else (s.get('sub') or s['title'])
        rota += f'<div class="route"><h3>{E(isim)}</h3><p>{E(ps[0][i])}</p>{ek}</div>'
    # pratik
    pratik = ''
    if cfg.get('pratik'):
        s = d[str(cfg['pratik'])]
        li = [(it['tr'] if dil == 'tr' else it['en']) for it in s['items'] if it['type'] == 'label']
        pratik = f'<h2 id="pratik">{T("Bilmekte fayda var", "Good to know")}</h2><ul>' + ''.join(f'<li>{E(x)}</li>' for x in li) + '</ul>'
    # rivayet
    rv = json.load(open(RIV)).get(c)
    riv = ''
    if rv:
        h = rv['hikayeler'][0]
        riv = (f'<section class="legend" id="rivayet"><span class="eyebrow" style="color:var(--gunes)">{T("Rivayete göre", "As the story goes")}</span><h2>{E(h["baslik"][i])}</h2>' +
               ''.join(f'<p>{E(m[i])}</p>' for m in h['metin']) + f'<p class="src">{E(h.get("kaynak", rv.get("kaynak", ["",""]))[i] if isinstance(h.get("kaynak"), list) else "")}</p></section>')
    # sss
    sss = ''.join(f'<details><summary>{E(q[i])}</summary><p>{E(a[i])}</p></details>' for q, a in cfg['sss'])
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q[i], "acceptedAnswer": {"@type": "Answer", "text": a[i]}} for q, a in cfg['sss']]}
    # bilgi kutusu
    dl = ''.join(f'<dt>{E(k[i])}</dt><dd>{E(v[i])}</dd>' for k, v in cfg['bilgi'])
    if dil == 'tr':
        satin = f'''<button class="btn" type="button" data-ugs="{c}">Sepete ekle</button>'''
        fiyat = '<span class="pr">390 TL</span><small class="prn">Tanışma fiyatı · 11 Aralık\'tan itibaren 790 TL</small>'
        cta_bas = f'{ad} Journal · Dijital'
        cta_li = ['Telefonda uygulama gibi açılır, internetsiz de çalışır', 'Türkçe + İngilizce sesli anlatım', 'Yer sayfaları, rotalar, haritalar ve küçük görevler', 'Kendi günlüğün, boyama ve çıkartmalar', 'Kişisel kod, 2 cihaz']
        not_ = 'Kart bilgisi Shopier\'in güvenli sayfasında girilir. Kod ödemeden hemen sonra ekranda ve e-postanda.'
        ikinci = '<a class="btn ghost" href="/nasil-alinir/">Nasıl alınır?</a>'
    else:
        satin = f'<a class="btn" href="https://{c}.ugrakjournal.com/satin-al">Buy the journal</a>'
        fiyat = '<span class="pr">390 TL</span><small class="prn">Launch price in Turkish lira · 790 TL from 11 December</small>'
        cta_bas = f'{ad} Journal · Digital'
        cta_li = ['Opens like an app on your phone, works offline', 'Audio stories in English and Turkish', 'Place pages, walking routes, maps and small quests', 'Your own travel diary, colouring pages and stickers', 'Personal code, works on 2 devices']
        not_ = 'Payments are processed securely through Shopier. Prices are in Turkish lira (TRY); your bank or card provider may convert the amount into your currency, and exchange rates and any foreign transaction fees are set by your provider. Uğrak is based in Sinop, Türkiye. This is a digital product; nothing is shipped.'
        ikinci = '<a class="btn ghost" href="/en/how-to-buy/">How it works</a>'
    cta = (f'<section class="cta" id="defter"><div><span class="eyebrow">{T("Uğrak dijital defteri", "Uğrak digital journal")}</span><h2>{E(cta_bas)}</h2>'
           f'<p>{T(f"Bu sayfadaki yerlerin hepsi, sesli anlatımlar, gravürler ve görevlerle birlikte telefonunda.", f"Every place on this page, with audio stories, illustrations and quests, on your phone.")}</p>'
           f'<p class="note">{T("Gravürler yapay zekâ araçlarıyla üretilip tarafımızdan seçilip düzenlenir; anlatıcı sesi yapay zekâ sesidir. ", "Illustrations are created with AI tools and edited by us; the narrator\'s voice is AI-generated. ")}<a href="{"/hakkimizda/#yapay-zeka" if dil=="tr" else "/en/about/#ai"}">{T("Ayrıntı","Details")}</a></p>'
           '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in cta_li) + f'</ul><p class="note" style="margin-top:14px">{E(not_)}</p></div>'
           f'<div class="acts"><div class="price">{fiyat}</div>{satin}{ikinci}</div></section>')
    ana_y = '/' if dil == 'tr' else '/en/'
    liste_y = '/sehirler/' if dil == 'tr' else '/en/#guides'
    hizli = (f'<div class="quick"><span class="pr">390 TL</span><button class="btn" type="button" data-ugs="{c}">{ad} defterini sepete ekle</button><a class="btn ghost" href="#defter">İçinde ne var?</a></div>' if dil == 'tr'
             else f'<div class="quick"><span class="pr">390 TL</span><a class="btn" href="https://{c}.ugrakjournal.com/satin-al">Get the {ad} journal</a><a class="btn ghost" href="#defter">What\'s inside?</a></div>')
    crumb_ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Uğrak", "item": SITE + ana_y},
        {"@type": "ListItem", "position": 2, "name": T("Şehirler", "City guides"), "item": SITE + liste_y},
        {"@type": "ListItem", "position": 3, "name": ad, "item": url(yol)}]}
    makale = {"@type": "Article", "headline": baslik.split(' · ')[0], "inLanguage": dil, "datePublished": BUGUN, "dateModified": BUGUN, "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"},
              "about": {"@type": "TouristDestination", "name": ad, "includesAttraction": yer_ld}, "image": SITE + '/' + cfg['gravur']}
    gov = f'''<main><div class="wrap">
<p class="crumb"><a href="{ana_y}">Uğrak</a> / <a href="{liste_y}">{T("Şehirler","City guides")}</a> / {E(ad)}</p>
<div class="ph ph-grid"><div><span class="eyebrow">{T("Gezi rehberi","Travel guide")} · No. {cfg["no"]}</span><h1>{E(ad)} <em>{T("gezi rehberi","travel guide")}</em></h1>
<p class="lede">{E(cfg["ozet"][i])}</p>{hizli}<p class="updated">{T("Son kontrol","Last checked")}: {KONTROL[i]} · {T("Hazırlayan: Uğrak Journal, Sinop","By Uğrak Journal, Sinop")} · <a href="{'/hakkimizda/#nasil' if dil=='tr' else '/en/about/#how'}">{T("Nasıl hazırlıyoruz?","How we research")}</a></p></div>
<figure class="ph-art" style="margin:0"><img src="/{cfg["gravur"]}" alt="{E(cfg["gcap"][i])}" width="900" height="600"><figcaption>{E(cfg["gcap"][i])} · {T("Uğrak gravürü","Uğrak illustration")}</figcaption></figure></div>
<div class="cols"><div>
<h2 id="yerler">{T(EK[c][0]+" görülecek yerler", f"Things to see in {ad}")}</h2>
{yer_html}
{ucgun}
<h2 id="rotalar">{T("Yürüyüş ve gezi rotaları","Walking and nature routes")}</h2>{rota}
<h2 id="tarih">{T(EK[c][1]+" kısa tarihi", f"A short history of {ad}")}</h2>{tarih_p}{tl_html}
{pratik}
{riv}
<h2 id="sss">{T("Sık sorulanlar","Frequently asked questions")}</h2><div class="faq">{sss}</div>
</div>
<aside class="facts" aria-label="{T("Kısa bilgiler","Quick facts")}"><h2>{T("Kısa bilgiler","Quick facts")}</h2><dl>{dl}</dl>
<a class="btn" href="#defter">{T(f"{ad} defterine bak", f"See the {ad} journal")}</a></aside>
</div>
{ilgili(c, dil)}
{cta}
</div></main>
'''
    karsi_url = '/' + karsi.replace('index.html', '')
    sayfa = bas(dil, baslik, aciklama, yol, karsi, [makale, faq_ld, crumb_ld], '/' + cfg['gravur']) + ust(dil, liste_y if dil == 'tr' else '/en/', karsi_url) + gov + son(dil, sepet=(dil == 'tr'))
    yaz(yol, sayfa)

def yazi_url(y, dil):
    return f'/yazilar/{y["slug"][0]}/' if dil == 'tr' else f'/en/guides/{y["slug"][1]}/'

def ilgili(c, dil):
    ys = [y for y in YAZI if c in y['sehir']]
    if not ys:
        return ''
    i = 0 if dil == 'tr' else 1
    return ('<section class="box" style="margin-top:56px"><span class="eyebrow">' + ('İlgili yazılar' if dil == 'tr' else 'Related guides') + '</span>' +
            ''.join(f'<p style="margin:6px 0"><a href="{yazi_url(y, dil)}" style="font:500 21px/1.3 var(--serif)">{E(y["baslik"][i])}</a></p>' for y in ys) + '</section>')

def yazi_sayfalari():
    for dil in ('tr', 'en'):
        i = 0 if dil == 'tr' else 1
        for y in YAZI:
            yol = yazi_url(y, dil).strip('/') + '/index.html'
            karsi = yazi_url(y, 'en' if dil == 'tr' else 'tr').strip('/') + '/index.html'
            gov = f'<p class="lede" style="font-size:20px;color:#4A3A31"><b>{"Kısa cevap" if dil=="tr" else "Short answer"}:</b> {E(y["kisa"][i])}</p>'
            gov += f'<figure class="ph-art" style="margin:26px 0"><img src="/{y["gravur"]}" alt="" width="900" height="600"></figure>'
            for (h, ps) in y['bolum']:
                gov += f'<h2>{E(h[i])}</h2><p>{E(ps[i])}</p>'
            sl = [(('Şehir rehberi: ' if dil=='tr' else 'City guide: ') + SEHIR[c]['ad'][i], f'/sehirler/{c}/' if dil == 'tr' else f'/en/cities/{ENSLUG[c]}/') for c in y['sehir']]
            gov += '<p class="note">' + ('Ziyaret saatleri, ulaşım ve etkinlik bilgileri değişebilir; yola çıkmadan önce ilgili kurumdan kontrol et.' if dil == 'tr' else 'Opening hours, transport and event details can change; check with the relevant institution before you go.') + '</p>'
            gov += '<h2>' + ('Devamı' if dil == 'tr' else 'Read more') + '</h2><ul>' + ''.join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in sl) + '</ul>'
            dj = ' / '.join(f'<a href="{u}#defter">{E(SEHIR[c]["ad"][i])} Journal</a>' for c, (t, u) in zip(y['sehir'], sl))
            gov += '<div class="box">' + (f'Şehri kendi temponla, sesli anlatım ve küçük görevlerle keşfetmek istersen dijital deftere göz at: {dj}.' if dil == 'tr' else f'To explore at your own pace, with audio stories and small quests, take a look at the digital journal: {dj}.') + '</div>'
            gov += '<h2>' + ('Kaynaklar' if dil == 'tr' else 'Sources') + '</h2><ul>' + ''.join(f'<li><a href="{u}" rel="noopener">{E(t)}</a></li>' for t, u in y['kaynak']) + \
                   ('<li>Uğrak şehir rehberleri ve dijital defter içerikleri (kaynaklarla doğrulanmış)</li>' if dil == 'tr' else '<li>Uğrak city guides and journal content (checked against sources)</li>') + '</ul>'
            gov += f'<p class="updated">{"Son kontrol" if dil=="tr" else "Last checked"}: {KONTROL[i]} · {"Hazırlayan: Uğrak Journal, Sinop" if dil=="tr" else "By Uğrak Journal, Sinop"} · <a href="{"/hakkimizda/#nasil" if dil=="tr" else "/en/about/#how"}">{"Nasıl hazırlıyoruz?" if dil=="tr" else "How we research"}</a></p>'
            ld = [{"@type": "Article", "headline": y['baslik'][i], "inLanguage": dil, "datePublished": BUGUN, "dateModified": BUGUN,
                   "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "image": SITE + '/' + y['gravur'], "description": y['kisa'][i]}]
            sabit(dil, yol, karsi, '/sehirler/' if dil == 'tr' else '/en/', y['baslik'][i] + ' · Uğrak', y['kisa'][i][:155], E(y['baslik'][i]), gov, ld)

def yazi_listesi():
    gov = '<ul style="list-style:none;padding:0">' + ''.join(f'<li class="route"><h3><a href="{yazi_url(y,"tr")}">{E(y["baslik"][0])}</a></h3><p>{E(y["kisa"][0])}</p></li>' for y in YAZI) + '</ul>'
    sabit('tr', 'yazilar/index.html', 'en/guides/index.html', '/sehirler/', 'Gezi yazıları · Uğrak', 'Uğrak gezi yazıları: kaç gün kalınmalı, hangi şehir kime uygun, ilk kez gidenler için öneriler.', 'Gezi <em>yazıları</em>', gov)
    gov = '<ul style="list-style:none;padding:0">' + ''.join(f'<li class="route"><h3><a href="{yazi_url(y,"en")}">{E(y["baslik"][1])}</a></h3><p>{E(y["kisa"][1])}</p></li>' for y in YAZI) + '</ul>'
    sabit('en', 'en/guides/index.html', 'yazilar/index.html', '/en/', 'Travel guides & tips · Uğrak', 'Uğrak travel tips for Türkiye: how many days to stay, which town suits you, and advice for first-time visitors.', 'Travel <em>guides</em>', gov)

# ---------- liste sayfaları ----------
def kartlar(dil):
    i = 0 if dil == 'tr' else 1
    out = ''
    for c, cfg in SEHIR.items():
        h = f'/sehirler/{c}/' if dil == 'tr' else f'/en/cities/{ENSLUG[c]}/'
        out += f'<a class="card" href="{h}"><img src="/{cfg["gravur"]}" alt="{E(cfg["gcap"][i])}" loading="lazy" width="900" height="600"><div><span class="eyebrow">No. {cfg["no"]}</span><h3>{E(cfg["ad"][i])}</h3><p>{E(cfg["kart"][i])}</p></div></a>'
    return f'<div class="grid4">{out}</div>'

def sehirler_tr():
    yol = 'sehirler/index.html'
    YL_TR = ''.join(f'<li><a href="{yazi_url(y,"tr")}">{E(y["baslik"][0])}</a></li>' for y in YAZI)
    gov = f'''<main><div class="wrap"><p class="crumb"><a href="/">Uğrak</a> / Şehirler</p>
<div class="ph"><span class="eyebrow">Şehir rehberleri</span><h1>Uğradığımız <em>şehirler</em></h1>
<p class="lede">Her şehri baştan araştırıyoruz: yerler, rotalar, kısa tarih, bir rivayet ve pratik bilgiler. Rehberler ücretsiz; aynı şehrin sesli anlatımlı, görevli ve günlüklü dijital defteri telefonunda.</p></div>
{kartlar('tr')}
<h2>Gezi yazıları</h2><ul>{YL_TR}</ul>
<p class="note" style="margin-top:26px">Sıradaki şehirler araştırılıyor. Bir şehir önermek için <a href="/iletisim/">bize yaz</a>.</p>
</div></main>'''
    yaz(yol, bas('tr', 'Şehir Rehberleri: Sinop, Amasra, Kapadokya, Safranbolu · Uğrak', 'Sinop, Amasra, Kapadokya ve Safranbolu için ücretsiz gezi rehberleri: görülecek yerler, rotalar, kısa tarih ve rivayetler.', yol, None) + ust('tr', '/sehirler/', '/en/') + gov + son('tr'))

def en_ana():
    yol = 'en/index.html'
    gov = f'''<main><div class="wrap">
<div class="ph ph-grid"><div><span class="eyebrow">Uğrak Journal · Made in Sinop, Türkiye</span><h1>City journals for <em>Türkiye</em></h1>
<p class="lede">Free travel guides and interactive digital city journals for Sinop, Amasra, Cappadocia and Safranbolu. Not a PDF: each journal opens like an app on your phone, with audio stories in English and Turkish, walking routes, illustrated place pages and a travel diary that works offline.</p>
<p style="margin-top:24px"><a class="btn" href="#guides">Read the free guides</a></p></div>
<figure class="ph-art" style="margin:0"><img src="/ekran-safranbolu.webp" alt="The Safranbolu journal open on a phone" width="600" height="1200" style="max-height:520px;width:auto;margin:auto;mix-blend-mode:normal"><figcaption>The Safranbolu journal on a phone</figcaption></figure></div>
<h2 id="guides">Free city guides</h2>
{kartlar('en')}
<h2 id="tips">Travel tips</h2><ul>{''.join(f'<li><a href="{yazi_url(y,"en")}">{E(y["baslik"][1])}</a></li>' for y in YAZI)}</ul>
<h2 id="journals">The digital journals</h2>
<div class="box"><p>Each journal costs <b class="pr">390 TL</b> <span class="prn">(launch price, 790 TL from 11 December)</span>. Buy it from the city guide page; checkout is on Shopier's secure page in Turkish lira. Your personal code appears right after payment, is emailed to you and works on two devices.</p>
<p style="margin:0">Available journals: <a href="https://sinop.ugrakjournal.com/satin-al">Sinop</a> · <a href="https://amasra.ugrakjournal.com/satin-al">Amasra</a> · <a href="https://kapadokya.ugrakjournal.com/satin-al">Cappadocia</a> · <a href="https://safranbolu.ugrakjournal.com/satin-al">Safranbolu</a>. See <a href="/en/help/">how it works</a>.</p></div>
</div></main>'''
    yaz(yol, bas('en', 'Uğrak Journal · Interactive City Journals & Travel Guides for Türkiye', 'Free travel guides and app-like digital city journals for Sinop, Amasra, Cappadocia and Safranbolu, with audio stories in English and Turkish.', yol, 'index.html') + ust('en', '/en/', '/') + gov + son('en'))

# ---------- sabit sayfalar ----------
def sabit(dil, yol, karsi, aktif, baslik, aciklama, h1, gov, ld=None, genis=False):
    karsi_url = '/' + karsi.replace('index.html', '')
    crumb = f'<p class="crumb"><a href="{"/" if dil=="tr" else "/en/"}">Uğrak</a> / {E(html.unescape(re.sub("<[^>]+>", "", h1)))}</p>'
    yaz(yol, bas(dil, baslik, aciklama, yol, karsi, ld) + ust(dil, aktif, karsi_url) +
        f'<main><div class="wrap{"" if genis else " narrow"} prose">{crumb}<div class="ph"><h1>{h1}</h1></div>{gov}</div></main>' + son(dil))

def sabitler():
    sabit('tr', 'hakkimizda/index.html', 'en/about/index.html', '/hakkimizda/', 'Hakkımızda · Uğrak Journal, Sinop',
          'Uğrak, Sinop\'ta kurulmuş bir şehir defteri markası. Kim olduğumuz, şehirleri nasıl araştırdığımız ve yapay zekâyı nerede kullandığımız.',
          'Biz <em>kimiz?</em>', '''
<p class="lede" style="font-size:20px;color:#4A3A31">Uğrak, Sinop'ta kurulmuş küçük bir şehir defteri markası. Kurucusu Aylin Tok. Uğramak, yolun üstünde durup gerçekten bakmak demek; defterlerimiz bir şehre gidenin etrafına yeniden bakması için var.</p>
<h2>Ne yapıyoruz?</h2>
<p>Şehir şehir dijital defterler hazırlıyoruz: Sinop, Amasra, Kapadokya ve Safranbolu. Her defter telefonda uygulama gibi açılır; yer sayfaları, rotalar, sesli anlatımlar, küçük görevler ve kendi günlüğünü içerir. Çocuklar için de Martı'nın Defterleri'ni yapıyoruz (Uğrak Çocuk). Basılı Sinop Journal hazırlanıyor.</p>
<h2 id="nasil">Şehirleri nasıl araştırıyoruz?</h2>
<ul>
<li>Her şehri baştan araştırıyoruz. Belediye, müze ve bakanlık kaynakları, akademik yayınlar ve dergilerden yararlanıyoruz.</li>
<li>Tarihler, ölçüler ve adlar kaynakla karşılaştırılıyor. Emin olamadığımız bilgiyi yazmıyoruz ya da "rivayet" diye açıkça belirtiyoruz.</li>
<li>Rivayet sayfalarında kaynağı ve "tarih değil, halk anlatısı" notunu yazıyoruz.</li>
<li>Her metin yayından önce ikinci bir gözden geçirmeden geçiyor; açılış saati ve ücret gibi değişen bilgiler için "gitmeden kontrol et" diyoruz.</li>
<li>Bir hata görürsen <a href="/iletisim/">bize yaz</a>; düzeltip sayfadaki "son kontrol" tarihini güncelleriz.</li>
</ul>
<h2 id="yapay-zeka">Yapay zekâyı nerede kullanıyoruz?</h2>
<div class="box"><ul style="margin:0">
<li><b>Gravür illüstrasyonlar:</b> yapay zekâ araçlarıyla üretiliyor, sonra tarafımızdan seçilip düzenleniyor.</li>
<li><b>Sesli anlatım:</b> anlatıcı sesi yapay zekâ sesidir; metinleri biz yazıp kontrol ediyoruz.</li>
<li><b>Metinler:</b> yapay zekâ yardımıyla taslaklanıyor; her bilgi kaynakla doğrulanıyor ve tarafımızdan düzenleniyor.</li>
</ul></div>
<p>Yapay zekâyı üretim sürecimizin bir aracı olarak kullanıyoruz; araştırma, seçim, doğrulama, düzenleme ve son yayın kararı bize ait. Bunu açıkça yazıyoruz, çünkü bir rehbere güvenmenin ilk şartı nasıl yapıldığını bilmek.</p>
<h2>İletişim</h2>
<p>info@ugrakjournal.com · WhatsApp 0546 846 62 88 · <a href="https://instagram.com/ugrakjournal">@ugrakjournal</a> · Sinop</p>
''', [{"@type": "AboutPage", "name": "Hakkımızda", "about": {"@id": SITE + "/#org"}}])
    sabit('en', 'en/about/index.html', 'hakkimizda/index.html', '/en/about/', 'About Uğrak Journal · Made in Sinop, Türkiye',
          'Uğrak is a small city journal brand from Sinop, Türkiye. Who we are, how we research each city and where we use AI.',
          'About <em>us</em>', '''
<p class="lede" style="font-size:20px;color:#4A3A31">Uğrak is a small city journal brand founded in Sinop, on Türkiye's Black Sea coast, by Aylin Tok. In Turkish, <i>uğramak</i> means to stop by on your way and really look. Our journals exist to help travellers look at a city again.</p>
<h2>What we make</h2>
<p>Digital city journals for Sinop, Amasra, Cappadocia and Safranbolu. Each opens like an app on your phone, with place pages, walking routes, audio stories in English and Turkish, small quests and your own travel diary.</p>
<h2 id="how">How we research</h2>
<ul>
<li>We research every city from scratch, using municipal, museum and ministry sources, academic publications and magazines.</li>
<li>Dates, measurements and names are checked against sources. If we can't confirm something, we leave it out or clearly label it as a legend.</li>
<li>Legend pages name their source and note that they are folk tales, not history.</li>
<li>Every text gets a second review before publishing. For things that change, such as opening hours and fees, we tell you to check before you go.</li>
<li>Spotted a mistake? <a href="/en/contact/">Tell us</a> and we'll fix it and update the "last checked" date.</li>
</ul>
<h2 id="ai">Where we use AI</h2>
<div class="box"><ul style="margin:0">
<li><b>Illustrations:</b> created with AI tools, then selected and edited by us.</li>
<li><b>Audio narration:</b> the narrator's voice is AI-generated; we write and check the scripts.</li>
<li><b>Texts:</b> drafted with the help of AI tools; every fact is checked against sources and edited by us.</li>
</ul></div>
<p>We use AI as a tool in our process; research, selection, fact-checking, editing and the final decision to publish are ours. We say this openly because trusting a guide starts with knowing how it was made.</p>
<h2>Contact</h2>
<p>info@ugrakjournal.com · WhatsApp +90 546 846 62 88 · <a href="https://instagram.com/ugrakjournal">@ugrakjournal</a> · Sinop, Türkiye</p>
''', [{"@type": "AboutPage", "name": "About", "about": {"@id": SITE + "/#org"}}])

    yardim_tr = [
      ("Defteri nasıl açarım?", "Ödemeden hemen sonra kişisel kodun ekranda görünür ve e-postana gelir. Defterin adresini telefonunda aç, kodu gir, sonra \"Ana ekrana ekle\" ile uygulama gibi kur."),
      ("Hangi telefonlarda çalışır?", "iPhone'da Safari, Android'de Chrome ile çalışır. İlk açılışta internet gerekir; sonra defter internetsiz de açılır."),
      ("Kaç cihazda kullanabilirim?", "Bir kod en fazla 2 cihazda çalışır. Kod kişiseldir; paylaşılamaz, devredilemez."),
      ("Kodum gelmedi ya da kayboldu.", "Önce e-postanın gereksiz (spam) klasörüne bak. Bulamazsan sipariş numaranla info@ugrakjournal.com adresine ya da WhatsApp'tan yaz; kodunu yeniden göndeririz."),
      ("Birden fazla defter alabilir miyim?", "Evet. Sepete eklediğin defterleri tek ödemeyle alırsın; hepsi tek kodla açılır."),
      ("Basılı defter var mı?", "Basılı Sinop Journal hazırlanıyor. Çıkınca duyuracağız."),
    ]
    yardim_en = [
      ("How do I open my journal?", "Your personal code appears on screen right after payment and is emailed to you. Open the journal's address on your phone, enter the code, then use \"Add to Home Screen\" to install it like an app."),
      ("Which phones does it work on?", "iPhone with Safari and Android with Chrome. You need internet the first time; after that the journal also opens offline."),
      ("How many devices can I use?", "One code works on up to 2 devices. Codes are personal and cannot be shared or transferred."),
      ("My code didn't arrive or I lost it.", "Check your spam folder first. If it isn't there, write to info@ugrakjournal.com or WhatsApp us with your order number and we'll resend it."),
      ("Is it a PDF or an App Store app?", "Neither. It is a web app (PWA) that opens in your phone's browser and can be added to your home screen."),
      ("What languages are included?", "City journals are in Turkish and English, including the audio stories. The children's journals (Martı) are Turkish only."),
    ]
    def sss_html(liste):
        return '<div class="faq">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in liste) + '</div>'
    def faq_ld(liste):
        return [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in liste]}]
    bilg = ''.join(f'<li><a href="https://{c}.ugrakjournal.com/bilgilendirme">{SEHIR[c]["ad"][0]} Journal ön bilgilendirme</a></li>' for c in SEHIR)
    sabit('tr', 'yardim/index.html', 'en/help/index.html', '/yardim/', 'Yardım ve Sık Sorulanlar · Uğrak',
          'Uğrak dijital defterleri nasıl açılır, hangi telefonlarda çalışır, kod, iade ve destek.', 'Yardım ve <em>sık sorulanlar</em>',
          sss_html(yardim_tr) + f'''
<h2 id="iade">İptal ve iade</h2>
<p>Defterler dijital içeriktir ve kod ödemeden hemen sonra teslim edilir. Kod çalışmıyorsa ya da defter açılmıyorsa önce sorunu çözeriz; çözemezsek ücretini iade ederiz. Ayrıntılı koşullar her defterin ön bilgilendirme sayfasında:</p>
<ul>{bilg}<li><a href="/dijital/bilgilendirme.html">Uğrak Çocuk satış koşulları</a></li></ul>
<h2 id="kvkk">Kişisel veriler</h2>
<p>Siparişi almak, kodu göndermek ve destek vermek için ad, e-posta, telefon ve sipariş bilgisi işlenir; kart bilgisi Shopier'de kalır, bize iletilmez. Verilerin reklam için kullanılmaz. Aydınlatma metni ön bilgilendirme sayfalarındadır.</p>
<h2>Destek</h2>
<p>info@ugrakjournal.com · WhatsApp 0546 846 62 88 · Genelde aynı gün yanıt veririz.</p>''', faq_ld(yardim_tr))
    sabit('en', 'en/help/index.html', 'yardim/index.html', '/en/help/', 'Help & FAQ · Uğrak Journal',
          'How Uğrak digital city journals work: opening your journal, supported phones, codes, devices, refunds and support.', 'Help & <em>FAQ</em>',
          sss_html(yardim_en) + '''
<h2 id="refunds">Refunds</h2>
<p>The journals are digital content delivered immediately after payment. If your code doesn't work or the journal won't open, we fix it first; if we can't, we refund you. Full terms (in Turkish) are on each journal's information page.</p>
<h2 id="payment">Payment & currency</h2>
<p>Payments are processed securely through Shopier. Prices are displayed in Turkish lira (TRY). Your bank or card provider may automatically convert the amount into your local currency; exchange rates and any foreign transaction fees are set by your payment provider. Your card details are never shared with us.</p>
<p>Uğrak is based in Sinop, Türkiye. Your purchase is a digital product; no physical item is shipped. Support is available in English by email.</p>
<h2>Support</h2>
<p>info@ugrakjournal.com · WhatsApp +90 546 846 62 88. We usually reply the same day.</p>''', faq_ld(yardim_en))
    sabit('tr', 'iletisim/index.html', 'en/contact/index.html', '/iletisim/', 'İletişim · Uğrak Journal, Sinop',
          'Uğrak ile iletişim: e-posta, WhatsApp, Instagram. Sorular, kurumsal hediye ve şehir önerileri.', 'Bize <em>yaz</em>', '''
<p>Sorular, kurumsal hediye istekleri ya da bir şehir önerisi için.</p>
<div class="box"><p><b>E-posta</b><br>info@ugrakjournal.com</p><p><b>Sipariş ve satış</b><br>satis@ugrakjournal.com</p><p><b>Telefon · WhatsApp</b><br>0546 846 62 88</p><p><b>Instagram</b><br><a href="https://instagram.com/ugrakjournal">@ugrakjournal</a></p><p style="margin:0"><b>Şehir</b><br>Sinop, Türkiye</p></div>
<h2>Kurumsal hediye</h2><p>Valilik, belediye, otel ve şirketler için kişiselleştirilmiş şehir defteri, ajanda ve çocuk defteri hazırlıyoruz. Numuneyi getiririz.</p>
<p class="note">Satıcı bilgileri ve adres <a href="/dijital/bilgilendirme.html">satış koşulları</a> sayfasındadır.</p>''', [{"@type": "ContactPage", "name": "İletişim"}])
    sabit('en', 'en/contact/index.html', 'iletisim/index.html', '/en/contact/', 'Contact · Uğrak Journal',
          'Contact Uğrak Journal: email, WhatsApp and Instagram.', 'Contact <em>us</em>', '''
<p>Questions about a journal, a correction to a guide, or a city you'd like us to cover.</p>
<div class="box"><p><b>Email</b><br>info@ugrakjournal.com</p><p><b>WhatsApp</b><br>+90 546 846 62 88</p><p><b>Instagram</b><br><a href="https://instagram.com/ugrakjournal">@ugrakjournal</a></p><p style="margin:0"><b>Based in</b><br>Sinop, Türkiye</p></div>''', [{"@type": "ContactPage", "name": "Contact"}])

def nasil_sayfalari():
    for dil, yol, karsi, aktif, bas_, ac, h1 in [
        ('tr', 'nasil-alinir/index.html', 'en/how-to-buy/index.html', '/nasil-alinir/', 'Nasıl alınır? Adım adım dijital defter · Uğrak',
         'Uğrak dijital defteri nasıl alınır ve telefona nasıl kurulur: seç, Shopier\'de öde, kodunu al, ana ekrana ekle. iPhone Safari ve Android Chrome için adım adım.', 'Nasıl <em>alınır?</em>'),
        ('en', 'en/how-to-buy/index.html', 'nasil-alinir/index.html', '/en/how-to-buy/', 'How to buy and install a Uğrak journal · Step by step',
         'How to buy a Uğrak digital city journal and add it to your phone: choose, pay on Shopier, get your code, add to home screen. Steps for iPhone Safari and Android Chrome.', 'How to <em>buy and install</em>')]:
        steps = [{"@type": "HowToStep", "position": k + 1, "name": a, "text": re.sub('<[^>]+>', ' ', b)} for k, (a, b) in enumerate(nasil.ADIMLAR[dil])]
        sabit(dil, yol, karsi, aktif, bas_, ac, h1, nasil.govde(dil), [{"@type": "HowTo", "name": re.sub('<[^>]+>', '', h1), "step": steps}], genis=True)

def magaza():
    def kart(key, img, ad, alt, fiyat, fcls, link):
        return (f'<article class="prod"><img src="/{img}" alt="" loading="lazy" width="900" height="600"><div><h3>{E(ad)}</h3><p>{E(alt)}</p>'
                + (f'<a class="more" href="{link}">Rehberi oku →</a>' if link else '')
                + f'<div class="row"><span class="{fcls}">{fiyat}</span><button class="btn" type="button" data-ugs="{key}">Sepete ekle</button></div></div></article>')
    sehir = ''.join(kart(c, SEHIR[c]['gravur'], f"{SEHIR[c]['ad'][0]} Journal", SEHIR[c]['kart'][0], '390 TL', 'pr', f'/sehirler/{c}/') for c in SEHIR)
    marti = (kart('marti56', 'dijital/m56-0.webp', 'Merak Defteri · 5–6 yaş', 'Martı ile oyunlar, sesli balonlar, boyama ve çıkartmalar.', '199 TL', 'fy', '/dijital/') +
             kart('marti78', 'dijital/merak-0.webp', 'Merak Defteri · 7–8 yaş', 'Merak soruları, görevler, boyama ve çıkartmalar.', '199 TL', 'fy', '/dijital/') +
             kart('marti910', 'dijital/m910-0.webp', 'Merak Defteri · 9–10 yaş', 'Daha uzun görevler, bulmacalar ve keşif kartları.', '249 TL', 'fy', '/dijital/'))
    gov = f'''<p class="lede" style="font-size:19px;color:#4A3A31;margin:0">Defterini seç, sepete ekle, Shopier'de tek ödemeyle al. Kodun ödemeden hemen sonra ekranda ve e-postanda; <a href="/nasil-alinir/">nasıl alınır?</a></p>
<h2>Şehir defterleri <small style="font:500 15px/1 var(--sans);color:var(--mut)">· Türkçe + İngilizce · telefonda uygulama gibi</small></h2>
<div class="shopgrid">{sehir}</div><p class="note prn" style="margin-top:10px">Şehir defterlerinde tanışma fiyatı; 11 Aralık'tan itibaren 790 TL.</p>
<h2>Uğrak Çocuk · Martı'nın Defterleri <small style="font:500 15px/1 var(--sans);color:var(--mut)">· Türkçe</small></h2>
<div class="shopgrid">{marti}</div>
<div class="box" style="margin-top:34px"><b>Birden fazla defter mi?</b> Hepsini sepete ekle; tek ödeme yaparsın, hepsi aynı kodla açılır. Kart bilgin Shopier'in güvenli sayfasında girilir, bize iletilmez. Kod en fazla 2 cihazda çalışır. <a href="/yardim/">Sık sorulanlar</a></div>'''
    sabit('tr', 'magaza/index.html', 'en/index.html', '/magaza/', 'Mağaza: Dijital şehir defterleri ve çocuk defterleri · Uğrak',
          'Sinop, Amasra, Kapadokya ve Safranbolu dijital şehir defterleri ile Martı çocuk defterleri. Sepete ekle, Shopier ile tek ödeme, kod hemen.',
          'Mağaza', gov, None, genis=True)
    p = os.path.join(KOK, 'magaza/index.html'); h = open(p).read().replace(FIYAT_JS, FIYAT_JS + '<script src="/sepet.js?v=5" defer></script>', 1); open(p, 'w').write(h)

# ---------- sitemap / robots ----------
def sitemap():
    yollar = [''] + [y.replace('index.html', '') for y in URETILEN if y.endswith('.html')] + ['dijital/']
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for y in dict.fromkeys(yollar):
        xml += f' <url><loc>{SITE}/{y}</loc><lastmod>{BUGUN}</lastmod></url>\n'
    open(os.path.join(KOK, 'sitemap.xml'), 'w').write(xml + '</urlset>\n')
    open(os.path.join(KOK, 'robots.txt'), 'w').write('''User-agent: *
Allow: /
Disallow: /yayin-gecici/
Disallow: /panel-gecici/
Disallow: /onizleme/

# Arama ve yapay zekâ arama botları açıkça serbest
User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /

Sitemap: https://ugrakjournal.com/sitemap.xml
''')

if __name__ == '__main__':
    shutil.copy(os.path.join(KOK, '_gen', 'site.css'), os.path.join(KOK, 'site.css'))
    for c in SEHIR:
        sehir_sayfasi(c, 'tr'); sehir_sayfasi(c, 'en')
    sehirler_tr(); en_ana(); sabitler(); nasil_sayfalari(); yazi_sayfalari(); yazi_listesi(); magaza(); sitemap()
    print('\n'.join(URETILEN))
