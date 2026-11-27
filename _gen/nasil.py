# "Nasıl alınır?" adım adım animasyonlu anlatım (Safari / Chrome). 27 Kas 2026
CSS = r'''<style>
.cap{display:none;text-align:center;margin:12px auto 0;max-width:34ch;min-height:5.5em}.cap b{display:block;font:500 19px/1.25 var(--serif)}.cap span{font-size:15px;color:#4A3A31}
.howto{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:48px;align-items:start;margin-top:26px}
@media(max-width:820px){.howto{grid-template-columns:1fr;gap:24px}.hphone-col{position:static;order:-1}.tabs{justify-self:center;order:-2}.howto .hphone{width:220px}.howto .cap{display:block}}
.tabs{grid-column:1/-1;justify-self:start;display:inline-flex;background:var(--kagit);border:1px solid var(--cizgi);border-radius:999px;padding:4px;margin:6px 0 18px}
.tabs button{border:0;background:none;border-radius:999px;padding:10px 18px;font:600 14.5px/1 var(--sans);color:var(--grav);cursor:pointer;min-height:42px}
.tabs button[aria-selected=true]{background:var(--deri);color:var(--krem)}
.steps{list-style:none;margin:0;padding:0;counter-reset:s}
.steps li{counter-increment:s;display:grid;grid-template-columns:40px minmax(0,1fr);gap:14px;padding:14px 12px;border-radius:16px;cursor:pointer;transition:background .3s}
.steps li::before{content:counter(s);width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:var(--kagit);border:1px solid var(--cizgi);font:600 15px/1 var(--sans);color:var(--deri)}
.steps li.on{background:var(--kagit)}
.steps li.on::before{background:var(--kiremit);border-color:var(--kiremit);color:#fff}
.steps b{display:block;font:500 20px/1.25 var(--serif)}
.steps span{font-size:15.5px;color:#4A3A31}
.steps [data-only]{display:none}
.howto[data-b=safari] [data-only=safari],.howto[data-b=chrome] [data-only=chrome]{display:inline}
.hphone-col{position:sticky;top:90px}
.hphone{position:relative;width:280px;max-width:100%;aspect-ratio:9/18.5;margin:0 auto;border-radius:40px;background:#1d1410;padding:10px;box-shadow:0 30px 60px -28px rgba(67,23,15,.6)}
.hscr{position:relative;width:100%;height:100%;border-radius:31px;overflow:hidden;background:#fff;font:500 12px/1.35 var(--sans);color:#222}
.sc{position:absolute;inset:0;opacity:0;transition:opacity .45s;display:flex;flex-direction:column}
.sc.on{opacity:1}
.bar{height:30px;display:flex;align-items:center;justify-content:center;font-size:10.5px;color:#555;background:#f4f4f4;border-bottom:1px solid #e5e5e5;flex:none;margin-top:22px}
.bar.top{margin-top:0;padding-top:22px;height:52px}
.pad{padding:14px;flex:1;display:flex;flex-direction:column;gap:10px}
.mini-card{border:1px solid #eadfcd;border-radius:14px;overflow:hidden;background:var(--kagit)}
.mini-card img{width:100%;aspect-ratio:3/2;object-fit:cover;mix-blend-mode:multiply}
.mini-card div{padding:8px 10px}
.mini-card b{font:500 15px/1.2 var(--serif);display:block}
.pill{display:flex;align-items:center;justify-content:center;height:36px;border-radius:999px;background:var(--kiremit);color:#fff;font-weight:700;font-size:12.5px}
.pill.dark{background:#2b2b2b}.pill.green{background:#2f6b4f}
.field{height:32px;border:1px solid #ddd;border-radius:8px;padding:0 10px;display:flex;align-items:center;color:#999;font-size:11.5px}
.shopier{font:800 16px/1 var(--sans);color:#4b2bb5;letter-spacing:-.02em}
.lock{font-size:10.5px;color:#2f6b4f}
.okbox{margin-top:auto;margin-bottom:auto;text-align:center;display:grid;gap:10px}
.code{font:700 20px/1 ui-monospace,Menlo,monospace;letter-spacing:.12em;background:var(--kagit);border:1px dashed var(--altin);border-radius:10px;padding:12px}
.notif{position:absolute;left:8px;right:8px;top:30px;background:rgba(245,245,245,.97);border-radius:14px;padding:9px 11px;box-shadow:0 8px 20px rgba(0,0,0,.18);transform:translateY(-130%);transition:transform .5s .6s}
.sc.on .notif{transform:none}
.notif b{display:block;font-size:11.5px}
.mail{background:#fafafa}
.mail h4{margin:0;font:500 16px/1.2 var(--serif)}
.sheet{position:absolute;left:0;right:0;bottom:0;background:#f2f2f6;border-radius:16px 16px 0 0;padding:10px 12px 26px;transform:translateY(100%);transition:transform .5s .7s;display:grid;gap:6px}
.sc.on .sheet{transform:none}
.sheet div{background:#fff;border-radius:10px;padding:10px 12px;display:flex;justify-content:space-between;align-items:center}
.sheet .hl{outline:2px solid var(--kiremit)}
.tbar{height:44px;border-top:1px solid #ddd;background:#f7f7f7;display:flex;justify-content:space-around;align-items:center;font-size:17px;color:#1a73e8;flex:none;margin-bottom:12px}
.menu3{position:absolute;right:8px;top:56px;width:72%;background:#fff;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.22);padding:6px 0;transform:scale(.6);transform-origin:top right;opacity:0;transition:.4s .7s}
.sc.on .menu3{transform:none;opacity:1}
.menu3 div{padding:9px 12px}
.menu3 .hl{background:#fdeee6;color:var(--kiremit);font-weight:700}
.home{background:linear-gradient(160deg,#c9b79a,#6f4a3a);padding:44px 16px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px 10px;align-content:start}
.home i{display:block;aspect-ratio:1;border-radius:12px;background:rgba(255,255,255,.35)}
.home .ug{background:var(--deri) url(/favicon.svg) center/62% no-repeat;transform:scale(0);transition:transform .5s .6s cubic-bezier(.3,1.6,.5,1);box-shadow:0 0 0 3px rgba(255,255,255,.7)}
.sc.on .home .ug{transform:none}
.home small{grid-column:1/-1;text-align:center;color:#fff;margin-top:8px}
.app{background:var(--krem)}
.typing{font:700 17px/1 ui-monospace,Menlo,monospace;letter-spacing:.12em;border:1px solid var(--cizgi);border-radius:10px;padding:12px;background:#fff;color:var(--grav)}
.typing span{display:inline-block;overflow:hidden;white-space:nowrap;vertical-align:bottom;width:0;animation:none}
.sc.on .typing span{animation:yaz 1.4s .5s steps(8) forwards}
@keyframes yaz{to{width:8.6ch}}
.tap{position:absolute;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:rgba(203,65,11,.35);box-shadow:0 0 0 0 rgba(203,65,11,.5);opacity:0;pointer-events:none}
.sc.on .tap{animation:tap 1.2s 1.5s 2 both}
@keyframes tap{0%{opacity:0;transform:scale(.6)}30%{opacity:1;transform:scale(1)}100%{opacity:0;box-shadow:0 0 0 18px rgba(203,65,11,0)}}
.ctrl{display:flex;justify-content:center;gap:10px;margin-top:14px}
.ctrl button{min-width:44px;min-height:44px;border-radius:999px;border:1px solid var(--cizgi);background:var(--kagit);font:600 14px/1 var(--sans);cursor:pointer;padding:0 14px;color:var(--grav)}
@media(prefers-reduced-motion:reduce){.sc,.notif,.sheet,.menu3,.home .ug{transition:none}.sc.on .tap,.sc.on .typing span{animation:none}.typing span{width:auto}}
</style>'''

def sahneler(dil):
    T = (lambda a, b: a) if dil == 'tr' else (lambda a, b: b)
    return f'''
<div class="sc on" data-s="0"><div class="bar">ugrakjournal.com</div><div class="pad">
 <div class="mini-card"><img src="/g/safranbolu-carsi-g.webp" alt=""><div><b>Safranbolu Journal</b>{T("Dijital · 390 TL","Digital · 390 TL")}</div></div>
 <div class="pill" style="position:relative">{T("Sepete ekle","Add to cart")}</div>
 <div class="pill dark">{T("Ödemeye geç →","Checkout →")}</div></div><span class="tap" style="left:50%;top:62%"></span></div>
<div class="sc" data-s="1"><div class="bar">shopier.com</div><div class="pad">
 <div class="shopier">shopier</div><span class="lock">🔒 {T("Güvenli ödeme","Secure payment")}</span>
 <div class="field">{T("Ad Soyad","Full name")}</div><div class="field">{T("E-posta","Email")}</div><div class="field">•••• •••• •••• ••••</div>
 <div style="display:flex;gap:8px"><div class="field" style="flex:1">AA/YY</div><div class="field" style="flex:1">CVC</div></div>
 <div class="pill" style="background:#4b2bb5;margin-top:auto">{T("Öde · 390 TL","Pay · 390 TL")}</div></div><span class="tap" style="left:50%;top:88%"></span></div>
<div class="sc" data-s="2"><div class="bar">ugrakjournal.com</div><div class="pad"><div class="okbox">
 <div style="font-size:26px">✓</div><b style="font:500 18px/1.2 var(--serif)">{T("Ödemen alındı","Payment received")}</b>
 <span>{T("Kişisel kodun:","Your personal code:")}</span><div class="code">UGRK••••</div><span style="color:#777">{T("Kod e-postana da gönderildi.","Your code has also been emailed to you.")}</span></div></div>
 <div class="notif"><b>✉︎ Uğrak Journal</b>{T("Defterin hazır, kodun içeride","Your journal is ready, code inside")}</div></div>
<div class="sc mail" data-s="3"><div class="bar">{T("Posta","Mail")}</div><div class="pad">
 <span style="color:#777">Uğrak Journal · satis@ugrakjournal.com</span><h4>{T("Safranbolu defterin hazır","Your Safranbolu journal is ready")}</h4>
 <span>{T("Kodun:","Your code:")} <b>UGRK••••</b></span><span>{T("Aşağıdaki düğmeye telefonundan dokun.","Tap the button below on your phone.")}</span>
 <div class="pill" style="margin-top:8px">{T("Defterini aç →","Open your journal →")}</div></div><span class="tap" style="left:50%;top:60%"></span></div>
<div class="sc" data-s="4" data-b="safari"><div class="bar">safranbolu.ugrakjournal.com</div><div class="pad app"><div class="mini-card"><img src="/g/safranbolu-carsi-g.webp" alt=""><div><b>Safranbolu Journal</b></div></div></div>
 <div class="tbar"><span>‹</span><span>›</span><span title="Paylaş">⬆︎</span><span>☐</span><span>⧉</span></div>
 <div class="sheet"><div>{T("Kopyala","Copy")}</div><div>{T("Okuma Listesine Ekle","Add to Reading List")}</div><div class="hl">{T("Ana Ekrana Ekle","Add to Home Screen")} <span>⊞</span></div></div>
 <span class="tap" style="left:50%;top:91%"></span></div>
<div class="sc" data-s="4" data-b="chrome"><div class="bar top">safranbolu.ugrakjournal.com <span style="margin-left:auto;padding-right:10px;font-size:16px">⋮</span></div><div class="pad app"><div class="mini-card"><img src="/g/safranbolu-carsi-g.webp" alt=""><div><b>Safranbolu Journal</b></div></div></div>
 <div class="menu3"><div>{T("Yeni sekme","New tab")}</div><div>{T("Yer işaretleri","Bookmarks")}</div><div class="hl">{T("Ana ekrana ekle","Add to home screen")}</div><div>{T("Ayarlar","Settings")}</div></div>
 <span class="tap" style="left:91%;top:7%"></span></div>
<div class="sc" data-s="5"><div class="home" style="flex:1"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i class="ug"></i><small>Safranbolu</small></div><span class="tap" style="left:84%;top:21%"></span></div>
<div class="sc app" data-s="6"><div class="pad" style="justify-content:center;text-align:center;gap:12px">
 <b style="font:500 20px/1.2 var(--serif)">{T("Kodunu gir","Enter your code")}</b><div class="typing"><span>UGRK7Q4M</span></div>
 <div class="pill">{T("Defteri aç","Open journal")}</div><span style="color:#777">{T("Bir kez girersin; sonra internetsiz de açılır.","Enter it once; after that it opens offline too.")}</span></div></div>
'''

ADIMLAR = {
 'tr': [
  ("Defterini seç", "Şehir sayfasında ya da mağazada \"Sepete ekle\"ye dokun. Birden fazla defter seçebilirsin: tek ödeme yaparsın, aldığın defterlerin hepsi aynı tek kodla açılır."),
  ("Shopier'de öde", "\"Ödemeye geç\" seni Shopier'in güvenli ödeme sayfasına götürür. Kart bilgin Shopier'de kalır, bize iletilmez."),
  ("Kodun ekranda ve e-postanda", "Ödeme tamamlandığında kişisel kodun ekranda görünür. Kod ayrıca siparişte yazdığın e-posta adresine gönderilir. E-postayı göremezsen gereksiz (spam) klasörüne bak; koduna ulaşamazsan bize yaz, hemen yardımcı olalım."),
  ("E-postadaki düğmeye dokun", "Telefonunda e-postayı aç ve \"Defterini aç\" düğmesine dokun."),
  ("Ana ekrana ekle", "<span data-only=\"safari\">Safari'de alttaki Paylaş düğmesine (kare ve yukarı ok) dokun, listeden \"Ana Ekrana Ekle\"yi seç.</span><span data-only=\"chrome\">Chrome'da sağ üstteki üç noktaya (⋮) dokun, \"Ana ekrana ekle\"yi ya da \"Uygulamayı yükle\"yi seç.</span>"),
  ("Ana ekrandaki simgeye dokun", "Defter artık bir uygulama gibi ana ekranında."),
  ("Kodunu gir, defterin açılsın", "Kodu bir kez girersin. İlk açılıştan sonra defter internetsiz de çalışır; en fazla 2 cihazda kullanabilirsin."),
 ],
 'en': [
  ("Choose your journal", "Tap \"Add to cart\" on a city page. You can pick several journals: you pay once, and one code opens all of them."),
  ("Pay on Shopier", "\"Checkout\" takes you to Shopier's secure payment page. Your card details stay with Shopier; we never see them."),
  ("Your code: on screen and by email", "When payment is complete, your personal code appears on screen. It is also sent to the email address you gave at checkout. If you can't see the email, check your spam folder; if you still can't find your code, write to us and we'll help right away."),
  ("Tap the button in the email", "Open the email on your phone and tap \"Open your journal\"."),
  ("Add it to your home screen", "<span data-only=\"safari\">In Safari, tap the Share button at the bottom (square with an up arrow) and choose \"Add to Home Screen\".</span><span data-only=\"chrome\">In Chrome, tap the three dots (⋮) at the top right and choose \"Add to home screen\" or \"Install app\".</span>"),
  ("Tap the new icon", "The journal now sits on your home screen like an app."),
  ("Enter your code and open it", "You enter the code once. After the first load the journal works offline too, on up to 2 devices."),
 ],
}

JS = r'''<script>(function(){
var w=document.querySelector('.howto');if(!w)return;
var sc=[].slice.call(w.querySelectorAll('.sc')),li=[].slice.call(w.querySelectorAll('.steps li')),i=0,t=null,b='safari';
var az=matchMedia('(prefers-reduced-motion: reduce)').matches;
function goster(n){i=(n+li.length)%li.length;li.forEach(function(x,k){x.classList.toggle('on',k===i)});
 var cp=w.querySelector('.cap');if(cp)cp.innerHTML='<b>'+(i+1)+'. '+li[i].querySelector('b').innerHTML+'</b>'+li[i].querySelector('span').innerHTML;
 sc.forEach(function(s){var ok=+s.dataset.s===i&&(!s.dataset.b||s.dataset.b===b);s.classList.toggle('on',ok);s.setAttribute('aria-hidden',!ok)})}
function oyna(){clearInterval(t);if(!az)t=setInterval(function(){goster(i+1)},3600)}
li.forEach(function(x,k){x.addEventListener('click',function(){goster(k);oyna()})});
w.querySelectorAll('.tabs button').forEach(function(x){x.addEventListener('click',function(){b=x.dataset.b;w.dataset.b=b;
 w.querySelectorAll('.tabs button').forEach(function(y){y.setAttribute('aria-selected',y===x)});goster(i);oyna()})});
w.querySelector('[data-g=p]').onclick=function(){goster(i-1);oyna()};w.querySelector('[data-g=n]').onclick=function(){goster(i+1);oyna()};
var dur=w.querySelector('[data-g=d]');dur.onclick=function(){if(t){clearInterval(t);t=null;dur.textContent=dur.dataset.o}else{oyna();dur.textContent=dur.dataset.d}};
if(/Android/i.test(navigator.userAgent))w.querySelector('.tabs [data-b=chrome]').click();
goster(0);oyna();})();</script>'''

def govde(dil):
    T = (lambda a, b: a) if dil == 'tr' else (lambda a, b: b)
    adim = ''.join(f'<li><div><b>{a}</b><span>{b}</span></div></li>' for a, b in ADIMLAR[dil])
    return CSS + f'''
<p class="lede" style="font-size:20px;color:#4A3A31;margin:0">{T("Seçiyorsun, Shopier'de ödüyorsun, kodun geliyor, defteri telefonunun ana ekranına ekliyorsun. Hepsi birkaç dakika.","Choose, pay on Shopier, get your code, add the journal to your home screen. It takes a few minutes.")}</p>
<div class="howto" data-b="safari">
 <div class="tabs" role="tablist" aria-label="{T("Tarayıcı","Browser")}"><button type="button" role="tab" data-b="safari" aria-selected="true">iPhone · Safari</button><button type="button" role="tab" data-b="chrome" aria-selected="false">Android · Chrome</button></div>
 <div><ol class="steps">{adim}</ol></div>
 <div class="hphone-col"><div class="hphone" aria-label="{T("Adımların canlandırması","Animation of the steps")}"><div class="hscr">{sahneler(dil)}</div></div>
 <div class="cap" aria-live="polite"></div><div class="ctrl"><button type="button" data-g="p" aria-label="{T("Önceki adım","Previous step")}">‹</button><button type="button" data-g="d" data-d="{T("Durdur","Pause")}" data-o="{T("Oynat","Play")}">{T("Durdur","Pause")}</button><button type="button" data-g="n" aria-label="{T("Sonraki adım","Next step")}">›</button></div></div>
</div>
<p class="note" style="margin-top:30px">{T("Ekranlar temsilîdir; Shopier ve tarayıcı görünümü cihazına göre biraz farklı olabilir. Takılırsan <a href=\"/yardim/\">Yardım</a> sayfasına bak ya da WhatsApp'tan yaz: 0546 846 62 88.","Screens are illustrative; Shopier and your browser may look slightly different on your device. Stuck? See <a href=\"/en/help/\">Help</a> or WhatsApp us: +90 546 846 62 88.")}</p>
''' + JS
