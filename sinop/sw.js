const V='ugrak-sinop-v4';
const CORE=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','../logo-krem.png','../kusak-kale.webp','../kusak-hamsaroz.webp','../favicon.svg','ses/diyojen.mp3','ses/kotra.mp3','ses/sofra.mp3'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('ugrak-sinop-')&&k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request; if(r.method!=='GET')return;
  const u=new URL(r.url);
  const range=r.headers.get('range');
  if(range&&u.origin===location.origin&&u.pathname.endsWith('.mp3')){
    e.respondWith(caches.match(u.origin+u.pathname).then(async hit=>{
      if(!hit)return fetch(r);
      const buf=await hit.arrayBuffer();const m=/bytes=(\d*)-(\d*)/.exec(range)||[];
      const start=Number(m[1]||0),end=m[2]?Math.min(Number(m[2]),buf.byteLength-1):buf.byteLength-1;
      return new Response(buf.slice(start,end+1),{status:206,headers:{'Content-Type':'audio/mpeg','Content-Range':`bytes ${start}-${end}/${buf.byteLength}`,'Content-Length':String(end-start+1),'Accept-Ranges':'bytes'}});
    }));
    return;
  }
  if(r.mode==='navigate'&&u.origin===location.origin){
    // Sayfa: önce ağ (3 sn), olmazsa önbellek. Böylece güncelleme ilk açılışta gelir.
    e.respondWith(Promise.race([fetch(r).then(res=>{if(res&&res.ok){const cp=res.clone();caches.open(V).then(c=>c.put('index.html',cp))}return res}),new Promise((_,rej)=>setTimeout(rej,3000))]).catch(()=>caches.match('index.html').then(h=>h||caches.match('./'))));
    return;
  }
  if(u.origin===location.origin||u.host.endsWith('fonts.googleapis.com')||u.host.endsWith('fonts.gstatic.com')){
    e.respondWith(caches.match(r,{ignoreSearch:u.origin===location.origin}).then(hit=>{
      const net=fetch(r).then(res=>{if(res&&(res.ok||res.type==='opaque')){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp))}return res}).catch(()=>hit||(r.mode==='navigate'?caches.match('index.html'):undefined));
      return hit||net;
    }));
  }
});
