/* Uğrak sepeti (site tarafı): "Sepete ekle" + alt çubuk + onay kartı → doğrudan Shopier ödemesi. 26 Kas 2026 */
(function(){
var ODEME='https://odeme.ugrakjournal.com/';
var F={sinop:390,amasra:390,kapadokya:390,safranbolu:390,marti56:199,marti78:199,marti910:249};
var AD2={sinop:'Sinop Journal · Dijital',amasra:'Amasra Journal · Dijital',kapadokya:'Kapadokya Journal · Dijital',safranbolu:'Safranbolu Journal · Dijital',marti56:'Merak Defteri · 5–6 yaş',marti78:'Merak Defteri · 7–8 yaş',marti910:'Merak Defteri · 9–10 yaş'};
var AD={sinop:'Sinop',amasra:'Amasra',kapadokya:'Kapadokya',safranbolu:'Safranbolu',marti56:'Merak 5–6',marti78:'Merak 7–8',marti910:'Merak 9–10'};
var S=[];try{S=JSON.parse(localStorage.getItem('ug_sepet')||'[]').filter(function(k){return F[k]})}catch(e){}
var Q={};try{Q=JSON.parse(localStorage.getItem('ug_adet')||'{}')||{}}catch(e){}
function adet(k){var n=parseInt(Q[k],10)||1;return S.length===1?Math.max(1,Math.min(20,n)):1}
function kaydet(){Object.keys(Q).forEach(function(k){if(S.indexOf(k)<0)delete Q[k]});try{localStorage.setItem('ug_sepet',JSON.stringify(S));localStorage.setItem('ug_adet',JSON.stringify(Q))}catch(e){}}
function anahtar(href){var m=/^https:\/\/(sinop|amasra|kapadokya|safranbolu|marti56|marti78|marti910)\.ugrakjournal\.com\/satin-al/.exec(href||'');return m?m[1]:null}
function tl(n){return n.toLocaleString('tr-TR')+' TL'}
var st=document.createElement('style');st.textContent=
'.ugs-bar{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:80;display:flex;align-items:center;gap:12px;background:#47190F;color:#F7F2E8;border-radius:18px;padding:10px 10px 10px 18px;box-shadow:0 10px 30px rgba(40,15,8,.35);transform:translateY(140%);transition:transform .3s cubic-bezier(.2,.8,.2,1);max-width:560px;margin:0 auto}'+
'.ugs-bar.on{transform:none}.ugs-bar .t{flex:1;min-width:0;font:500 14px/1.25 "Hanken Grotesk",system-ui,sans-serif}.ugs-bar .t b{display:block;font-size:17px;font-weight:600}.ugs-bar .t small{display:block;opacity:.75;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'+
'.ugs-bar a{flex:none;display:inline-flex;align-items:center;height:46px;padding:0 18px;border-radius:14px;background:#F7F2E8;color:#47190F;text-decoration:none;font:700 15px "Hanken Grotesk",system-ui,sans-serif}'+
'.ugs-bar.pul{animation:ugsp .45s}@keyframes ugsp{40%{transform:scale(1.03)}}'+
'.ugs-ekle{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:42px;padding:0 16px;border-radius:21px;border:1.5px solid currentColor;background:transparent;font:600 14px "Hanken Grotesk",system-ui,sans-serif;cursor:pointer;white-space:nowrap;color:inherit}'+
'.ugs-ekle.on{background:#2f6b4f;border-color:#2f6b4f;color:#fff}'+
'a.city.ugs-on{outline:3px solid #2f6b4f;outline-offset:-3px}'+
'.btn.ugs-on{background:#2f6b4f!important;border-color:#2f6b4f!important;color:#fff!important}'+
'.ugs-ort{position:fixed;inset:0;z-index:90;background:rgba(35,20,15,.45);display:none;align-items:flex-end;justify-content:center}.ugs-ort.on{display:flex}'+
'.ugs-kart{background:#FFFCF6;color:#231A16;width:100%;max-width:560px;border-radius:22px 22px 0 0;padding:20px max(18px,env(safe-area-inset-left)) calc(18px + env(safe-area-inset-bottom));box-shadow:0 -10px 40px rgba(0,0,0,.25);font:400 16px/1.5 "Hanken Grotesk",system-ui,sans-serif;max-height:92vh;overflow:auto}'+
'.ugs-kart h3{margin:0 0 4px;font:400 26px/1.15 "Newsreader",Georgia,serif;color:#47190F}.ugs-kart .x{float:right;border:0;background:none;font-size:26px;line-height:1;color:#6b5a4c;cursor:pointer;padding:4px 6px}'+
'.ugs-kart ul{list-style:none;margin:12px 0;padding:0;border-top:1px solid #e3d6c3}.ugs-kart li{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid #e3d6c3}.ugs-kart li span:first-child{flex:1}.ugs-kart .cik{flex:none;width:44px;height:44px;border:1.5px solid #e3d6c3;border-radius:12px;background:#fff;color:#6b5a4c;font-size:20px;line-height:1;cursor:pointer}.ugs-kart .ekle2{background:none;border:0;color:#5E2318;text-decoration:underline;font:600 14px "Hanken Grotesk",system-ui,sans-serif;cursor:pointer;padding:6px 0}'+
'.ugs-bar .t{cursor:pointer}.ugs-kart li.hasad{flex-wrap:wrap}.ugs-kart li.hasad span:first-child{flex:1 1 100%}.ugs-kart li.hasad .ad{margin-right:auto}.ugs-kart .ad{display:inline-flex;align-items:center;gap:0;border:1.5px solid #e3d6c3;border-radius:12px;overflow:hidden;flex:none}.ugs-kart .ad button{width:40px;height:42px;border:0;background:#fff;color:#5E2318;font:700 20px/1 "Hanken Grotesk",system-ui,sans-serif;cursor:pointer}.ugs-kart .ad b{min-width:30px;text-align:center;font:700 16px "Hanken Grotesk",system-ui,sans-serif}.ugs-kart .hd{font-size:14px;line-height:1.45;background:#F3F8F4;border:1.5px solid #9cc3ad;border-radius:12px;padding:10px 12px;margin:10px 0 0}.ugs-kart .adim2{font-size:17px;line-height:1.5}.ugs-kart .adim2 b{color:#5E2318}.ugs-kart .buyuk{display:block;text-align:center;font:700 40px/1 "Hanken Grotesk",system-ui,sans-serif;color:#5E2318;border:2px dashed #CB410B;border-radius:14px;padding:14px;margin:12px 0}'+
'.ugs-bar .t{cursor:pointer}.ugs-kart li.top{font-weight:700;border:0}'+
'.ugs-kart label{display:flex;gap:10px;align-items:flex-start;margin:10px 0;font-size:15px;line-height:1.45}.ugs-kart input{width:22px;height:22px;flex:none;margin-top:1px;accent-color:#5E2318}.ugs-kart label a{color:#5E2318}'+
'.ugs-kart .ode{display:flex;width:100%;align-items:center;justify-content:center;min-height:54px;margin-top:12px;border:0;border-radius:14px;background:#5E2318;color:#fff;font:700 17px "Hanken Grotesk",system-ui,sans-serif;cursor:pointer}.ugs-kart .ode[disabled]{opacity:.6}'+
'.ugs-kart .bil{font-size:14px;line-height:1.45;color:#2B1D17;background:#FBF4E6;border:1.5px solid #E9C27A;border-radius:12px;padding:10px 12px;margin:12px 0 0}.ugs-kart .not{font-size:13.5px;color:#6b5a4c;margin:10px 0 0;text-align:center}.ugs-kart .m{color:#b23808;font-size:14px;min-height:1em;margin-top:6px}';
document.head.appendChild(st);
var bar=document.createElement('div');bar.className='ugs-bar';bar.setAttribute('role','region');bar.setAttribute('aria-label','Sepet');
bar.innerHTML='<div class="t" role="button" tabindex="0" aria-label="Sepeti düzenle"><b></b><small></small></div><a href="#" role="button">Ödemeye geç →</a>';document.body.appendChild(bar);
var ort=document.createElement('div');ort.className='ugs-ort';ort.setAttribute('role','dialog');ort.setAttribute('aria-modal','true');ort.setAttribute('aria-label','Ödeme');
ort.innerHTML='<div class="ugs-kart"><button class="x" type="button" aria-label="Kapat">×</button><h3>Sepetin</h3><ul></ul><button type="button" class="ekle2">+ Başka defter ekle</button>'+
 '<label><input type="checkbox" id="ugs-c1"><span><a target="_blank" rel="noopener" id="ugs-kl">Ön bilgilendirme ve satış koşullarını</a> okudum.</span></label>'+
 '<label><input type="checkbox" id="ugs-c2"><span>Kodlarımın ödemeden hemen sonra verilmesini istiyorum; dijital içerikte bu şekilde teslimle cayma hakkımın olmadığını biliyorum. Çalışmayan içerikle ilgili haklarım saklıdır.</span></label>'+
 '<p class="bil"><b>Kodun nasıl gelir?</b> Ödeme bitince Shopier sayfasında yazan <b>ugrakjournal.com/kod</b> adresine dön, kodun hemen ekranda. Kod ayrıca e-postana <b>en geç 1 saat içinde</b> gelir. Shopier\'in “ödemeniz onaylandı” e-postasında kod yazmaz; bu normal.</p>'+
 '<button class="ode" type="button">Shopier\'de öde →</button><div class="m" role="status"></div>'+
 '<p class="not">🔒 Adını, e-postanı ve kart bilgini yalnız Shopier\'in güvenli sayfasında yazarsın.</p></div>';
document.body.appendChild(ort);
function kapat(){ort.classList.remove('on')}
ort.addEventListener('click',function(e){if(e.target===ort)kapat()});ort.querySelector('.x').onclick=kapat;
function ac(){
 var ul=ort.querySelector('ul');ul.innerHTML='';var t=0;
 if(!S.length){kapat();return}
 S.forEach(function(k){var n=adet(k);t+=F[k]*n;var li=document.createElement('li');if(S.length===1)li.className='hasad';li.innerHTML='<span></span>'+(S.length===1?'<span class="ad"><button type="button" class="az" aria-label="Azalt">−</button><b></b><button type="button" class="ar" aria-label="Arttır">+</button></span>':'')+'<span></span><button type="button" class="cik">×</button>';
  li.children[0].textContent=AD2[k]||AD[k];li.lastElementChild.previousElementSibling.textContent=tl(F[k]*n);
  if(S.length===1){li.querySelector('.ad b').textContent=n;li.querySelector('.az').onclick=function(){Q[k]=Math.max(1,n-1);kaydet();ciz(false);ac()};li.querySelector('.ar').onclick=function(){Q[k]=Math.min(20,n+1);kaydet();ciz(false);ac()}}
  var c=li.querySelector('.cik');c.setAttribute('aria-label',(AD2[k]||AD[k])+' sepetten çıkar');c.onclick=function(){var i=S.indexOf(k);if(i>=0)S.splice(i,1);kaydet();ciz(false);ac()};ul.appendChild(li)});
 var hd=ort.querySelector('.hd');if(!hd){hd=document.createElement('p');hd.className='hd';ul.parentNode.insertBefore(hd,ul.nextSibling)}
 if(S.length===1&&adet(S[0])>1){hd.hidden=false;hd.innerHTML='<b>Hediye alımı:</b> '+adet(S[0])+' ayrı kod gelir, her biri ayrı bir kişi içindir. Her kod için bir hediye kartı bağlantısı alırsın; arkadaşlarına gönderirsin.'}
 else if(S.length>1){hd.hidden=false;hd.innerHTML='Aynı defterden birden fazla (ör. hediye için) almak istersen sepette yalnız o defter olsun; adet seçimi o zaman açılır.'}
 else{hd.hidden=false;hd.innerHTML='Hediye mi alıyorsun? <b>+</b> ile adet seç; her adete ayrı kod ve hediye kartı gelir.'}
 var li=document.createElement('li');li.className='top';li.innerHTML='<span>Toplam</span><span></span><span style="width:44px"></span>';li.children[1].textContent=tl(t);ul.appendChild(li);
 ort.querySelector('#ugs-kl').href=ODEME+'?u='+S.join(',')+'#kosullar';ort.querySelector('.m').textContent='';
 var b=ort.querySelector('.ode');b.disabled=false;b.textContent='Shopier\'de öde · '+tl(t)+' →';
 ort.classList.add('on')}
bar.querySelector('a').addEventListener('click',function(e){e.preventDefault();if(S.length)ac()});
bar.querySelector('.t').addEventListener('click',function(){if(S.length)ac()});
ort.querySelector('.ekle2').onclick=function(){kapat();if(!/\/magaza\/?$/.test(location.pathname))location.href='/magaza/'};
ort.querySelector('.ode').addEventListener('click',function(){
 var m=ort.querySelector('.m'),b=this;
 if(!document.getElementById('ugs-c1').checked||!document.getElementById('ugs-c2').checked){m.textContent='Devam etmek için iki kutuyu da işaretle.';return}
 b.disabled=true;b.textContent='Shopier açılıyor…';
 fetch(ODEME+'api/sepet/baslat',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({u:S,adet:S.length===1?adet(S[0]):1,c1:true,c2:true,v:'2026-11-27'})}).then(function(r){return r.json()}).then(function(r){
  if(!r||!r.ok||!r.url)throw new Error(r&&r.err||'hata');
  var nA=r.adet||1,url=r.url;S=[];Q={};kaydet();try{localStorage.setItem('ug_son',JSON.stringify({t:r.t,z:Date.now()}))}catch(x){}
  if(nA>1&&!/products=/.test(url)){var kr=ort.querySelector('.ugs-kart');kr.innerHTML='<button class="x" type="button" aria-label="Kapat">×</button><h3>Son bir adım</h3><p class="adim2">Shopier sayfasında <b>Adet</b> kutusunu şuna getir:</p><span class="buyuk">'+nA+'</span><p class="adim2">Sonra <b>Hemen al</b>\'a dokun ve öde. Adet 1 kalırsa yalnız 1 kod gelir.</p><a class="ode" href="'+url+'" style="text-decoration:none">Shopier\'e geç · Adet '+nA+' →</a><p class="not">Ödemeden sonra ugrakjournal.com/kod adresine dön; '+nA+' kodun ve hediye kartların orada.</p>';kr.querySelector('.x').onclick=function(){location.reload()};ciz(false);return}
  location.href=url;
 }).catch(function(x){b.disabled=false;b.textContent='Shopier\'de öde →';m.textContent=String(x&&x.message)==='kapali'?'Sepet şu an kapalı; birazdan tekrar dene.':'Bir sorun oldu, tekrar dene. Sürerse satis@ugrakjournal.com'})});
function ciz(pul){
 var t=S.reduce(function(a,k){return a+F[k]*adet(k)},0),n=S.reduce(function(a,k){return a+adet(k)},0);
 bar.querySelector('b').textContent=n+' defter · '+tl(t);
 bar.querySelector('small').textContent=S.map(function(k){return AD[k]+(adet(k)>1?' ×'+adet(k):'')}).join(' · ')+'  ·  düzenle';
 bar.querySelector('a').href='#';
 bar.classList.toggle('on',S.length>0);if(typeof hepCiz==='function')hepCiz();if(pul){bar.classList.remove('pul');void bar.offsetWidth;bar.classList.add('pul')}
 document.querySelectorAll('[data-ugs]').forEach(function(e){var on=S.indexOf(e.getAttribute('data-ugs'))>=0;e.classList.toggle('ugs-on',on);
  var b=e.classList.contains('ugs-ekle')?e:e.querySelector('.ugs-ekle');if(b){b.classList.toggle('on',on);b.textContent=on?'✓ Sepette':'Sepete ekle'}
  if(e.tagName==='A'&&e.classList.contains('btn'))e.textContent=on?'✓ Sepette':'Sepete ekle'})}
function hepCiz(){document.querySelectorAll('button[data-ugs-hep]').forEach(function(b){var hep=b.getAttribute('data-ugs-hep').split(',').every(function(k){return S.indexOf(k)>=0});b.textContent=hep?'✓ 4 şehir defteri sepette':'4 şehir defterini birlikte seç'})}
function tog(k){var i=S.indexOf(k);if(i>=0)S.splice(i,1);else S.push(k);kaydet();ciz(i<0)}
// 1) Şehir kartları ve "Satın al" düğmeleri
document.querySelectorAll('a[href*=".ugrakjournal.com/satin-al"]').forEach(function(a){
 var k=anahtar(a.href);if(!k)return;
 if(a.classList.contains('nm')){a.href='#defterler';return}          // şehir atlası: kartlara götürsün
 a.setAttribute('data-ugs',k);
 if(a.classList.contains('city')){var go=a.querySelector('.go');if(go){var b=document.createElement('span');b.className='ugs-ekle';b.setAttribute('role','button');go.replaceWith(b)}}
 a.addEventListener('click',function(e){e.preventDefault();tog(k)})});
// 2) data-ugs-ekle düğmeleri (ör. ana sayfadaki Martı listesi)
document.querySelectorAll('button[data-ugs-hep]').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();var ek=0;b.getAttribute('data-ugs-hep').split(',').forEach(function(k){if(F[k]&&S.indexOf(k)<0){S.push(k);ek=1}});kaydet();ciz(ek)})});
document.querySelectorAll('button[data-ugs]').forEach(function(b){b.classList.add('ugs-ekle');b.addEventListener('click',function(e){e.preventDefault();tog(b.getAttribute('data-ugs'))})});
ciz(false);
(function(){var s=null;try{s=JSON.parse(localStorage.getItem('ug_son')||'null')}catch(e){}
 var don=/[?&]odeme=tamam\b/.test(location.search);
 if(don&&s&&s.t&&Date.now()-s.z<3*864e5){location.replace(ODEME+'tamam?t='+encodeURIComponent(s.t));return}
 if(don){var n=document.createElement('div');n.setAttribute('role','status');
  n.style.cssText='position:fixed;left:12px;right:12px;top:calc(10px + env(safe-area-inset-top));z-index:85;max-width:560px;margin:0 auto;background:#2f6b4f;color:#fff;border-radius:16px;padding:14px 44px 14px 18px;font:500 15.5px/1.45 "Hanken Grotesk",system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.25)';
  n.innerHTML='<b>✓ Siparişin için teşekkürler!</b><br>Kodun e-postana en geç 1 saat içinde gelir. Shopier\'in “ödemeniz onaylandı” e-postasında kod yazmaz; bu normal. Gelmezse satis@ugrakjournal.com\'a yaz.<button type="button" aria-label="Kapat" style="position:absolute;right:10px;top:8px;border:0;background:none;color:#fff;font-size:24px;cursor:pointer">×</button>';
  n.querySelector('button').onclick=function(){n.remove()};document.body.appendChild(n);return}
 if(!s||!s.t||Date.now()-s.z>3*864e5)return;
 fetch(ODEME+'api/sepet/durum?t='+encodeURIComponent(s.t)).then(function(r){return r.json()}).then(function(r){
  var kp=0;try{kp=sessionStorage.getItem('ug_bant')===s.t}catch(e){}
  if(!r||!r.ok||!r.paid||kp)return;function gor(){try{sessionStorage.setItem('ug_bant',s.t)}catch(e){}}
  var d=document.createElement('a');d.href=ODEME+'tamam?t='+encodeURIComponent(s.t);
  d.style.cssText='position:fixed;left:12px;right:12px;top:calc(10px + env(safe-area-inset-top));z-index:85;display:flex;align-items:center;justify-content:space-between;gap:10px;max-width:560px;margin:0 auto;background:#2f6b4f;color:#fff;border-radius:16px;padding:14px 48px 14px 18px;text-decoration:none;font:600 16px "Hanken Grotesk",system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.25)';
  d.innerHTML='<span>✓ Ödemen alındı, defterlerin hazır</span><b>Kodunu gör →</b><button type="button" aria-label="Kapat" style="position:absolute;right:6px;top:50%;transform:translateY(-50%);width:40px;height:40px;border:0;background:none;color:#fff;font-size:24px;cursor:pointer">×</button>';
  d.querySelector('button').onclick=function(e){e.preventDefault();e.stopPropagation();gor();d.remove()};
  document.body.appendChild(d)}).catch(function(){})})();
fetch(ODEME+'api/sepet/urunler').then(function(r){return r.json()}).then(function(r){(r.urunler||[]).forEach(function(x){if(F[x.k]&&x.fiyat>0)F[x.k]=x.fiyat});ciz(false)}).catch(function(){});
})();
