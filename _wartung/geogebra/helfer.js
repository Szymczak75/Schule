
function mische(arr){
  const a=arr.slice();
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a;
}
document.querySelectorAll('.tab').forEach(tab=>{
  tab.addEventListener('click',()=>{
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('aktiv'));
    document.querySelectorAll('.karte').forEach(k=>k.classList.remove('aktiv'));
    tab.classList.add('aktiv');
    document.getElementById(tab.dataset.ziel).classList.add('aktiv');
    window.scrollTo({top:0,behavior:'smooth'});
  });
});
document.querySelectorAll('.stufen-wahl').forEach(w=>{
  w.querySelectorAll('.stufe-btn').forEach(b=>{
    b.addEventListener('click',()=>{
      const k=w.dataset.karte, s=b.dataset.s;
      w.querySelectorAll('.stufe-btn').forEach(x=>x.classList.remove('aktiv'));
      b.classList.add('aktiv');
      document.querySelectorAll('.stufe-block[data-karte="'+k+'"]').forEach(bl=>{
        bl.classList.toggle('aktiv', bl.dataset.s===s);
      });
    });
  });
});
function toggleStufe(btn){ btn.parentElement.classList.toggle('offen'); }
function pruefeFortschritt(){
  Object.keys(FORTSCHRITT).forEach(d=>{
    const e=document.getElementById(d);
    if(!e) return;
    const fertig=FORTSCHRITT[d].some(k=>state[k] && state[k].erledigt);
    e.textContent = fertig ? MARKE : '';
  });
}
function parseZahlOderBruch(s){
  s=String(s).trim().replace(',', '.');
  if(s==='') return NaN;
  const bruch=s.match(/^(-?\d+(?:\.\d+)?)\s*\/\s*(-?\d+(?:\.\d+)?)$/);
  if(bruch){ const z=parseFloat(bruch[1]), n=parseFloat(bruch[2]); return n!==0 ? z/n : NaN; }
  return parseFloat(s);
}
function feldStimmt(id, erwartet, tol){
  const el=document.getElementById(id);
  if(!el) return false;
  const wert=parseZahlOderBruch(el.value);
  return el.value.trim()!=='' && !isNaN(wert) && Math.abs(wert-erwartet)<=(tol!==undefined?tol:0.0001);
}
function pruefeGruppen(gruppen, stumm){
  let alle=true;
  gruppen.forEach(gr=>{
    const ok=gr.felder.every(f=>feldStimmt(f.id,f.erwartet,f.tol));
    if(!stumm){
      const st=document.getElementById(gr.statusId);
      if(st){ st.textContent = ok ? '✅' : '❌'; st.style.color = ok ? 'var(--green)' : 'var(--red)'; }
    }
    if(!ok) alle=false;
  });
  return alle;
}
function leereGruppen(gruppen){
  gruppen.forEach(gr=>{
    gr.felder.forEach(f=>{ const e=document.getElementById(f.id); if(e){ e.value=''; e.readOnly=false; } });
    const st=document.getElementById(gr.statusId); if(st) st.textContent='';
  });
}
function baueMC(wrapId, optionen, key, feld){
  const wrap=document.getElementById(wrapId);
  if(!wrap) return;
  optionen.forEach((o,i)=>{
    const b=document.createElement('button');
    b.textContent=o.t; b.dataset.i=i;
    b.addEventListener('click',()=>{
      if(state[key].geprueft) return;
      wrap.querySelectorAll('button').forEach(x=>x.classList.remove('gewaehlt'));
      b.classList.add('gewaehlt');
      state[key].wahlen[feld]=i;
    });
    wrap.appendChild(b);
  });
}
function mcAuswerten(wrapId, optionen, wahl){
  const wrap=document.getElementById(wrapId);
  wrap.querySelectorAll('button').forEach((b,i)=>{
    if(optionen[i].korrekt) b.classList.add('richtig');
    else if(i===wahl) b.classList.add('falsch');
  });
  return wahl!==null && wahl!==undefined && optionen[wahl] && optionen[wahl].korrekt;
}
function mcLeeren(wrapId){
  const wrap=document.getElementById(wrapId);
  if(wrap) wrap.querySelectorAll('button').forEach(b=>b.classList.remove('richtig','falsch','gewaehlt'));
}
const trex=document.getElementById('trex');
if(trex) trex.addEventListener('click',()=>{
  trex.classList.add('zeig');
  setTimeout(()=>trex.classList.remove('zeig'),1800);
});

/* ---------- weitere Helfer (Erarbeitungsseiten) ---------- */
function toggleWz(id){ document.getElementById(id).classList.toggle('offen'); }
function toggleTipp(id){ document.getElementById(id).classList.toggle('offen'); }
function karteAuswerten(kartenKey, gruppen, ids, textOk, textNok){
  const ok=pruefeGruppen(gruppen);
  state[kartenKey].geprueft=true;
  const fb=document.getElementById(ids.fb);
  if(ok){
    fb.className='feedback zeig ok'; fb.textContent=textOk;
    state[kartenKey].erledigt=true;
    if(ids.leeren) document.getElementById(ids.leeren).style.display='none';
    if(ids.tipps) document.getElementById(ids.tipps).classList.remove('zeig');
  }else{
    fb.className='feedback zeig nok'; fb.textContent=textNok;
    if(ids.leeren) document.getElementById(ids.leeren).style.display='inline-block';
    if(ids.tipps) document.getElementById(ids.tipps).classList.add('zeig');
  }
  pruefeFortschritt();
  return ok;
}
function karteLeeren(kartenKey, gruppen, ids){
  leereGruppen(gruppen);
  document.getElementById(ids.fb).className='feedback';
  if(ids.leeren) document.getElementById(ids.leeren).style.display='none';
  state[kartenKey].geprueft=false; state[kartenKey].erledigt=false;
  pruefeFortschritt();
}
function baueWF(kartenKey, scope){
  document.querySelectorAll(scope+' [data-aussage]').forEach((box,i)=>{
    box.querySelectorAll('.wf-buttons button').forEach(b=>{
      b.addEventListener('click',()=>{
        if(state[kartenKey].geprueft) return;
        box.querySelectorAll('.wf-buttons button').forEach(x=>x.classList.remove('gewaehlt'));
        b.classList.add('gewaehlt');
        state[kartenKey].wahlen[i]=b.dataset.w;
      });
    });
  });
}
function wfAuswerten(kartenKey, scope, fbId){
  const boxen=document.querySelectorAll(scope+' [data-aussage]');
  if(Object.values(state[kartenKey].wahlen).some(v=>v===null)) return false;
  state[kartenKey].geprueft=true;
  let richtig=0;
  boxen.forEach((box,i)=>{
    const soll=box.dataset.richtig;
    box.querySelectorAll('.wf-buttons button').forEach(b=>{
      if(b.dataset.w===soll) b.classList.add('richtig');
      else if(b.dataset.w===state[kartenKey].wahlen[i]) b.classList.add('falsch');
    });
    if(state[kartenKey].wahlen[i]===soll) richtig++;
  });
  const fb=document.getElementById(fbId);
  if(richtig===boxen.length){
    fb.className='feedback zeig ok';
    fb.textContent='✅ Alle Aussagen richtig eingeschätzt.';
    state[kartenKey].erledigt=true;
  }else{
    fb.className='feedback zeig nok';
    fb.textContent='❌ '+richtig+' von '+boxen.length+' richtig. Grün zeigt jeweils die korrekte Antwort.';
  }
  pruefeFortschritt();
  return richtig===boxen.length;
}
function mitMC(key, gruppen, opt, wrapId, ids, textOk, textNok){
  if(state[key].wahlen[0]===null) return;
  const okZahlen = pruefeGruppen(gruppen);
  state[key].geprueft = true;
  const okMC = mcAuswerten(wrapId, opt, state[key].wahlen[0]);
  const ok = okZahlen && okMC;
  const fb = document.getElementById(ids.fb);
  fb.className = 'feedback zeig ' + (ok ? 'ok' : 'nok');
  fb.textContent = ok ? textOk : textNok;
  document.getElementById(ids.leeren).style.display = ok ? 'none' : 'inline-block';
  if(ids.tipps) document.getElementById(ids.tipps).classList.toggle('zeig', !ok);
  state[key].erledigt = ok;
  pruefeFortschritt();
}
function mitMCleeren(key, gruppen, opt, wrapId, ids){
  leereGruppen(gruppen);
  document.getElementById(ids.fb).className='feedback';
  document.getElementById(ids.leeren).style.display='none';
  document.querySelectorAll('#'+wrapId+' button').forEach(b=>b.classList.remove('richtig','falsch','gewaehlt'));
  state[key].wahlen={0:null};
  state[key].geprueft=false; state[key].erledigt=false;
  pruefeFortschritt();
}
function checkAuswerten(fragen, zsfId){
  if(Object.values(state.k4.wahlen).some(v=>v===null)) return;
  state.k4.geprueft=true;
  let richtig=0;
  fragen.forEach((f,idx)=>{ if(mcAuswerten('c'+(idx+1)+'-wahl', f.optionen, state.k4.wahlen[idx])) richtig++; });
  const zsf=document.getElementById(zsfId);
  zsf.classList.add('zeig');
  zsf.textContent='Du hast '+richtig+' von '+fragen.length+' richtig beantwortet.'
    + (richtig===fragen.length ? ' Stark!' : ' Schau dir die roten Antworten an und blättere auf die passende Karte zurück.');
  state.k4.mcRichtig=(richtig===fragen.length);
  k4Status();
}
function rechnenAuswerten(gruppen, textOk, textNok){
  const ok=pruefeGruppen(gruppen);
  const fb=document.getElementById('fbRechnen');
  fb.className='feedback zeig '+(ok?'ok':'nok');
  fb.textContent = ok ? textOk : textNok;
  document.getElementById('leerenRechnen').style.display = ok ? 'none' : 'inline-block';
  const t=document.getElementById('tippsRechnen');
  if(t) t.classList.toggle('zeig', !ok);
  state.k4.rechnenOk=ok;
  k4Status();
}
function rechnenLeeren(gruppen){
  leereGruppen(gruppen);
  document.getElementById('fbRechnen').className='feedback';
  document.getElementById('leerenRechnen').style.display='none';
  state.k4.rechnenOk=false; k4Status();
}
function k4Status(){
  state.k4.erledigt = state.k4.mcRichtig && state.k4.rechnenOk;
  pruefeFortschritt();
}

/* =============================================================================
   Notfall-Anzeige für Formeln (MATHJAX-FALLBACK)
   Lädt MathJax nicht (Schul-WLAN, Vorschau, Offline-Kopie), blieben sonst
   \( ... \) als Rohtext mit Backslashes stehen. Dann werden die TeX-Ausdrücke
   hier in lesbares HTML gewandelt: √ mit Klammer, Brüche als .frac-Konstrukt
   (kein Schrägstrich!), Hoch-/Tiefstellungen als sup/sub, Sonderzeichen direkt.
   Ist MathJax da, passiert nichts.
   ========================================================================== */
(function(){
  var AUF = '\u0001', ZU = '\u0002';   /* Platzhalter fuer { } aus \left\{ */

  function leseGruppe(t, i){
    if (t.charAt(i) !== '{') return null;
    var tiefe = 0;
    for (var j = i; j < t.length; j++){
      if (t.charAt(j) === '{') tiefe++;
      else if (t.charAt(j) === '}'){ tiefe--; if (tiefe === 0) return [t.slice(i+1, j), j+1]; }
    }
    return null;
  }

  function strukturen(t){
    var aus = '', i = 0;
    while (i < t.length){
      var m = /^\\(dfrac|tfrac|frac|sqrt)/.exec(t.slice(i));
      if (m){
        var a = leseGruppe(t, i + m[0].length);
        if (a){
          if (m[1] === 'sqrt'){
            var inn = strukturen(a[0]);
            aus += /^[0-9A-Za-z]+$/.test(a[0]) ? '√' + inn : '√(' + inn + ')';
            i = a[1]; continue;
          }
          var b = leseGruppe(t, a[1]);
          if (b){
            aus += '<span class="frac"><span>' + strukturen(a[0]) + '</span><span>'
                 + strukturen(b[0]) + '</span></span>';
            i = b[1]; continue;
          }
        }
      }
      aus += t.charAt(i); i++;
    }
    return aus;
  }

  function texHtml(t){
    t = t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    t = t.replace(/\\rightarrow/g, '→').replace(/\\leftarrow/g, '←')
         .replace(/\\Rightarrow/g, '⇒').replace(/\\Leftarrow/g, '⇐')
         .replace(/\\left\\\{/g, AUF).replace(/\\right\\\}/g, ZU)
         .replace(/\\left(?![a-zA-Z])/g, '').replace(/\\right(?![a-zA-Z])/g, '')
         .replace(/\\\{/g, AUF).replace(/\\\}/g, ZU);
    t = t.replace(/\\cdot/g, '·').replace(/\\times/g, '·')
         .replace(/\\approx/g, '≈').replace(/\\neq/g, '≠')
         .replace(/\\leq/g, '≤').replace(/\\le\b/g, '≤')
         .replace(/\\geq/g, '≥').replace(/\\ge\b/g, '≥')
         .replace(/\\pm/g, '±').replace(/\\mp/g, '∓')
         .replace(/\\ldots/g, '…').replace(/\\dots/g, '…')
         .replace(/\\to\b/g, '→')
         .replace(/\\infty/g, '∞')
         .replace(/\\pi/g, 'π').replace(/\\alpha/g, 'α')
         .replace(/\\beta/g, 'β').replace(/\\gamma/g, 'γ')
         .replace(/\\Delta/g, 'Δ').replace(/\\delta/g, 'δ')
         .replace(/\\min/g, 'min').replace(/\\max/g, 'max')
         .replace(/\\text\{([^{}]*)\}/g, '$1')
         .replace(/\\mathrm\{([^{}]*)\}/g, '$1');
    t = strukturen(t);
    t = t.replace(/\^\{([^{}]*)\}/g, '<sup>$1</sup>')
         .replace(/\^(-?[0-9A-Za-z])/g, '<sup>$1</sup>')
         .replace(/_\{([^{}]*)\}/g, '<sub>$1</sub>')
         .replace(/_(-?[0-9A-Za-z])/g, '<sub>$1</sub>');
    t = t.replace(/\{,\}/g, ',').replace(/\\,/g, ' ').replace(/\\;/g, ' ')
         .replace(/\\ /g, ' ').replace(/[{}]/g, '')
         .replace(new RegExp(AUF, 'g'), '{').replace(new RegExp(ZU, 'g'), '}');
    return t;
  }

  function mathNotfall(){
    if (window.MathJax && window.MathJax.typesetPromise) return;  /* MathJax ist da */
    var lauf = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function(n){
        var tag = n.parentNode && n.parentNode.nodeName;
        if (tag === 'SCRIPT' || tag === 'STYLE') return NodeFilter.FILTER_REJECT;
        return n.nodeValue.indexOf('\\(') > -1 ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
      }
    });
    var treffer = [], n;
    while ((n = lauf.nextNode())) treffer.push(n);
    treffer.forEach(function(k){
      var teile = k.nodeValue.split(/\\\(([\s\S]+?)\\\)/);
      if (teile.length < 2) return;
      var html = '';
      for (var i = 0; i < teile.length; i++){
        html += (i % 2)
          ? '<span class="tex-ersatz">' + texHtml(teile[i]) + '</span>'
          : teile[i].replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      }
      var huelle = document.createElement('span');
      huelle.innerHTML = html;
      var frag = document.createDocumentFragment();
      while (huelle.firstChild) frag.appendChild(huelle.firstChild);
      k.parentNode.replaceChild(frag, k);
    });
  }
  window.addEventListener('load', function(){ setTimeout(mathNotfall, 3500); });
})();
