import sys
CSS = r"""
<style id="kl-anim">
  /* Animasi — Kulmina Labs */
  .rv{opacity:0;transform:translateY(28px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
  .rv.in{opacity:1;transform:none}
  .rv-l{transform:translateX(-36px)} .rv-r{transform:translateX(36px)} .rv-s{transform:scale(.94)}
  .rv-l.in,.rv-r.in,.rv-s.in{transform:none}
  .hero-in>*{opacity:0;transform:translateY(22px);animation:klUp .8s cubic-bezier(.2,.7,.2,1) forwards}
  @keyframes klUp{to{opacity:1;transform:none}}
  @keyframes klFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
  @keyframes klPulse{0%{box-shadow:0 0 0 0 rgba(37,211,102,.55)}80%,100%{box-shadow:0 0 0 18px rgba(37,211,102,0)}}
  @keyframes klShine{from{left:-60%}to{left:130%}}
  .fab{animation:klPulse 2.2s infinite}
  .btn{position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s,background .2s,filter .2s}
  .btn:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,.18)}
  .btn:after{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.45),transparent);transform:skewX(-20deg);pointer-events:none;opacity:0}
  .btn:hover:after{opacity:1;animation:klShine .8s ease}
  nav{transition:box-shadow .3s,background .3s}
  nav.scrolled{box-shadow:0 8px 30px rgba(0,0,0,.18)}
  .kl-progress{position:fixed;top:0;left:0;height:3px;width:0;z-index:99;transition:width .1s linear}
  @media (prefers-reduced-motion:reduce){
    .rv,.hero-in>*{opacity:1!important;transform:none!important;animation:none!important;transition:none!important}
    .fab,.float{animation:none!important}
  }
</style>
"""
JS = r"""
<script id="kl-anim-js">
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cfg = window.KL_ANIM || {};
  // progress bar
  var bar = document.createElement('div'); bar.className='kl-progress'; bar.style.background = cfg.bar || '#F2B233'; document.body.appendChild(bar);
  var nav = document.querySelector('nav');
  function onScroll(){
    var h = document.documentElement; var p = h.scrollTop/(h.scrollHeight-h.clientHeight||1);
    bar.style.width = (p*100)+'%';
    if(nav) nav.classList.toggle('scrolled', h.scrollTop>10);
  }
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();
  // hero entrance (staggered)
  (cfg.hero||[]).forEach(function(sel){
    var el = document.querySelector(sel); if(!el) return; el.classList.add('hero-in');
    [].forEach.call(el.children, function(c,i){ c.style.animationDelay = (0.12+i*0.12)+'s'; });
  });
  if(reduce) return;
  // scroll reveal with stagger per group
  (cfg.reveal||[]).forEach(function(group){
    var sel=group[0], kind=group[1]||'';
    [].forEach.call(document.querySelectorAll(sel), function(el,i){
      el.classList.add('rv'); if(kind) el.classList.add(kind);
      el.style.transitionDelay = ((i%4)*0.09)+'s';
    });
  });
  var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} }); }, {threshold:.14, rootMargin:'0px 0px -40px 0px'});
  [].forEach.call(document.querySelectorAll('.rv'), function(el){ io.observe(el); });
  // floating elements
  (cfg.float||[]).forEach(function(sel){ [].forEach.call(document.querySelectorAll(sel), function(el,i){ el.classList.add('float'); el.style.animation='klFloat '+(4+i*0.7)+'s ease-in-out '+(i*0.4)+'s infinite'; }); });
  // subtle parallax on hero background layer
  if(cfg.parallax){ var pl=document.querySelector(cfg.parallax); if(pl){ window.addEventListener('scroll',function(){ pl.style.backgroundPosition='0 '+(window.scrollY*0.25)+'px'; },{passive:true}); } }
})();
</script>
"""
def inject(path, cfg_js, extra_css=""):
    s=open(path).read()
    if 'id="kl-anim"' in s: print('already', path); return
    s=s.replace('</head>', CSS + extra_css + '</head>',1)
    s=s.replace('</body>', '<script>window.KL_ANIM='+cfg_js+';</script>\n'+JS+'</body>',1)
    open(path,'w').write(s); print('ok',path)
if __name__=='__main__':
    pass
