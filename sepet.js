/* Uğrak sepeti (site tarafı): "Sepete ekle" + alt çubuk → odeme.ugrakjournal.com. 26 Kas 2026 */
(function(){
var ODEME='https://odeme.ugrakjournal.com/';
var F={sinop:390,amasra:390,kapadokya:390,marti56:199,marti78:199,marti910:249};
var AD={sinop:'Sinop',amasra:'Amasra',kapadokya:'Kapadokya',marti56:'Merak 5–6',marti78:'Merak 7–8',marti910:'Merak 9–10'};
var S=[];try{S=JSON.parse(localStorage.getItem('ug_sepet')||'[]').filter(function(k){return F[k]})}catch(e){}
function kaydet(){try{localStorage.setItem('ug_sepet',JSON.stringify(S))}catch(e){}}
function anahtar(href){var m=/^https:\/\/(sinop|amasra|kapadokya|marti56|marti78|marti910)\.ugrakjournal\.com\/satin-al/.exec(href||'');return m?m[1]:null}
function tl(n){return n.toLocaleString('tr-TR')+' TL'}
var st=document.createElement('style');st.textContent=
'.ugs-bar{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:80;display:flex;align-items:center;gap:12px;background:#47190F;color:#F7F2E8;border-radius:18px;padding:10px 10px 10px 18px;box-shadow:0 10px 30px rgba(40,15,8,.35);transform:translateY(140%);transition:transform .3s cubic-bezier(.2,.8,.2,1);max-width:560px;margin:0 auto}'+
'.ugs-bar.on{transform:none}.ugs-bar .t{flex:1;min-width:0;font:500 14px/1.25 "Hanken Grotesk",system-ui,sans-serif}.ugs-bar .t b{display:block;font-size:17px;font-weight:600}.ugs-bar .t small{display:block;opacity:.75;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'+
'.ugs-bar a{flex:none;display:inline-flex;align-items:center;height:46px;padding:0 18px;border-radius:14px;background:#F7F2E8;color:#47190F;text-decoration:none;font:700 15px "Hanken Grotesk",system-ui,sans-serif}'+
'.ugs-bar.pul{animation:ugsp .45s}@keyframes ugsp{40%{transform:scale(1.03)}}'+
'.ugs-ekle{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:42px;padding:0 16px;border-radius:21px;border:1.5px solid currentColor;background:transparent;font:600 14px "Hanken Grotesk",system-ui,sans-serif;cursor:pointer;white-space:nowrap;color:inherit}'+
'.ugs-ekle.on{background:#2f6b4f;border-color:#2f6b4f;color:#fff}'+
'a.city.ugs-on{outline:3px solid #2f6b4f;outline-offset:-3px}'+
'.btn.ugs-on{background:#2f6b4f!important;border-color:#2f6b4f!important;color:#fff!important}';
document.head.appendChild(st);
var bar=document.createElement('div');bar.className='ugs-bar';bar.setAttribute('role','region');bar.setAttribute('aria-label','Sepet');
bar.innerHTML='<div class="t"><b></b><small></small></div><a>Ödemeye geç →</a>';document.body.appendChild(bar);
function ciz(pul){
 var t=S.reduce(function(a,k){return a+F[k]},0);
 bar.querySelector('b').textContent=S.length+' defter · '+tl(t);
 bar.querySelector('small').textContent=S.map(function(k){return AD[k]}).join(' · ');
 bar.querySelector('a').href=ODEME+'?u='+S.join(',');
 bar.classList.toggle('on',S.length>0);if(pul){bar.classList.remove('pul');void bar.offsetWidth;bar.classList.add('pul')}
 document.querySelectorAll('[data-ugs]').forEach(function(e){var on=S.indexOf(e.getAttribute('data-ugs'))>=0;e.classList.toggle('ugs-on',on);
  var b=e.classList.contains('ugs-ekle')?e:e.querySelector('.ugs-ekle');if(b){b.classList.toggle('on',on);b.textContent=on?'✓ Sepette':'Sepete ekle'}
  if(e.tagName==='A'&&e.classList.contains('btn'))e.textContent=on?'✓ Sepette':'Sepete ekle'})}
function tog(k){var i=S.indexOf(k);if(i>=0)S.splice(i,1);else S.push(k);kaydet();ciz(i<0)}
// 1) Şehir kartları ve "Satın al" düğmeleri
document.querySelectorAll('a[href*=".ugrakjournal.com/satin-al"]').forEach(function(a){
 var k=anahtar(a.href);if(!k)return;
 if(a.classList.contains('nm')){a.href='#defterler';return}          // şehir atlası: kartlara götürsün
 a.setAttribute('data-ugs',k);
 if(a.classList.contains('city')){var go=a.querySelector('.go');if(go){var b=document.createElement('span');b.className='ugs-ekle';b.setAttribute('role','button');go.replaceWith(b)}}
 a.addEventListener('click',function(e){e.preventDefault();tog(k)})});
// 2) data-ugs-ekle düğmeleri (ör. ana sayfadaki Martı listesi)
document.querySelectorAll('button[data-ugs]').forEach(function(b){b.classList.add('ugs-ekle');b.addEventListener('click',function(e){e.preventDefault();tog(b.getAttribute('data-ugs'))})});
ciz(false);
fetch(ODEME+'api/sepet/urunler').then(function(r){return r.json()}).then(function(r){(r.urunler||[]).forEach(function(x){if(F[x.k]&&x.fiyat>0)F[x.k]=x.fiyat});ciz(false)}).catch(function(){});
})();
