/* =============================================================================
   BAUSTEIN: MathJax-Notfall-Anzeige  (MATHJAX-FALLBACK)
   Gepflegt im Wartungs-Projekt. Unverändert ans ENDE des Seiten-Skripts kopieren
   (in die Seite hinein – nie per <script src> verlinken, TEIL 8.1).
   Voraussetzung auf der Seite: das .frac-CSS mit Kind-Selektoren (TEIL 7.2):
     .frac{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;
           margin:0 .2em;line-height:1.15;}
     .frac > span{display:block;padding:0 .35em;}
     .frac > span:first-child{border-bottom:1.8px solid currentColor;padding-bottom:.1em;}
     .frac > span:last-child{padding-top:.1em;}
   ========================================================================== */
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
