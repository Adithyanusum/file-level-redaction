// Generic selector that can attach to any canvas (overlay) and map regions to original image coords
(function(){
  let canvas = null;
  let ctx = null;
  let rects = [];
  let drawing = false;
  let sx = 0, sy = 0;
  // original image size (in pixels)
  let origW = 0, origH = 0;

  function attachCanvas(c){
    if(typeof c === 'string') c = document.getElementById(c);
    if(!c) return false;
    if(canvas && canvas !== c){ detach(); }
    canvas = c;
    ctx = canvas.getContext('2d');
    canvas.style.pointerEvents = 'none'; // disabled by default
    canvas.addEventListener('mousedown', onDown);
    canvas.addEventListener('mousemove', onMove);
    canvas.addEventListener('mouseup', onUp);
    render();
    return true;
  }

  function detach(){
    if(!canvas) return;
    canvas.removeEventListener('mousedown', onDown);
    canvas.removeEventListener('mousemove', onMove);
    canvas.removeEventListener('mouseup', onUp);
    canvas.style.pointerEvents = 'none';
    canvas = null; ctx = null;
  }

  function onDown(ev){
    drawing = true;
    const r = canvas.getBoundingClientRect();
    sx = Math.round(ev.clientX - r.left);
    sy = Math.round(ev.clientY - r.top);
  }
  function onMove(ev){
    if(!drawing) return;
    const rct = canvas.getBoundingClientRect();
    const mx = Math.round(ev.clientX - rct.left);
    const my = Math.round(ev.clientY - rct.top);
    render();
    const w = mx - sx; const h = my - sy;
    ctx.strokeStyle='blue'; ctx.fillStyle='rgba(0,0,255,0.15)'; ctx.lineWidth=2;
    ctx.strokeRect(sx, sy, w, h);
    ctx.fillRect(sx, sy, w, h);
  }
  function onUp(ev){
    if(!drawing) return;
    drawing = false;
    const rct = canvas.getBoundingClientRect();
    const ex = Math.round(ev.clientX - rct.left);
    const ey = Math.round(ev.clientY - rct.top);
    let x = Math.min(sx, ex), y = Math.min(sy, ey), w = Math.abs(ex-sx), h = Math.abs(ey-sy);
    if(w>5 && h>5) rects.push([x,y,w,h]);
    render();
    if(typeof onChange === 'function') onChange(getRegions());
  }

  function render(){
    if(!canvas || !ctx) return;
    // clear overlay only
    ctx.clearRect(0,0,canvas.width, canvas.height);
    ctx.lineWidth=2; ctx.strokeStyle='red'; ctx.fillStyle='rgba(255,0,0,0.15)';
    for(const r of rects){
      ctx.strokeRect(r[0], r[1], r[2], r[3]);
      ctx.fillRect(r[0], r[1], r[2], r[3]);
    }
  }

  function getRegions(){
    if(!origW || !canvas || !canvas.width) return rects.slice();
    const scaleX = origW / canvas.width;
    const scaleY = origH / canvas.height;
    return rects.map(r=>[ Math.round(r[0]*scaleX), Math.round(r[1]*scaleY), Math.round(r[2]*scaleX), Math.round(r[3]*scaleY) ]);
  }

  // return regions in canvas coordinates (useful for preview drawing)
  function getCanvasRegions(){
    return rects.slice();
  }

  function setRegions(regions){
    rects.length = 0;
    if(!regions || !regions.length) { render(); return; }
    const scaleX = (origW && canvas.width) ? canvas.width / origW : 1;
    const scaleY = (origH && canvas.height) ? canvas.height / origH : 1;
    for(const r of regions){
      // accept [x,y,w,h] or [x0,y0,x1,y1]
      let x=r[0], y=r[1], w=r[2], h=r[3];
      if(r.length===4 && (r[2] > origW || r[3] > origH)){
        // maybe r is [x0,y0,x1,y1]
        w = r[2]-r[0]; h = r[3]-r[1];
      }
      const cx = Math.round(x*scaleX), cy = Math.round(y*scaleY), cw = Math.round(w*scaleX), ch = Math.round(h*scaleY);
      rects.push([cx,cy,cw,ch]);
    }
    render();
    if(typeof onChange === 'function') onChange(getRegions());
  }

  function enableEditing(on){
    if(!canvas) return;
    canvas.style.pointerEvents = on? 'auto':'none';
  }

  function setOriginalSize(w,h){ origW = w||0; origH = h||0; }

  let onChange = null;

  function setOnChange(fn){ onChange = fn; }

  window.selector = {
    attach: attachCanvas,
    detach: detach,
    getRegions: getRegions,
    setRegions: setRegions,
    enableEditing: enableEditing,
    setOriginalSize: setOriginalSize,
    getCanvasRegions: getCanvasRegions,
    onChange: setOnChange
  };

})();
