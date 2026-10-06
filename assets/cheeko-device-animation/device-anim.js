// Meet the device: the dial turns and the screen steps through the real main menu
// (TALK, IMAGINE, GAMES, FUNNY VOICE, RADIO, SETTINGS). Arrows are drawn from each
// label to its part of the device, so they stay right at any size.
(function () {
  var root = document.getElementById('devanim');
  if (!root) return;
  root.classList.add('dm-js');
  var dev = root.querySelector('.dm-dev');
  var knob = root.querySelector('.dm-knob');
  var screens = [].slice.call(root.querySelectorAll('.dm-scr'));
  var labels = [].slice.call(root.querySelectorAll('.dm-lab'));
  var svg = root.querySelector('.dm-arrows');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS = 'http://www.w3.org/2000/svg';
  var STEP = 30, EVERY = 1900;
  var idx = 0, rot = 0, timer = null, visible = false, holdUntil = 0;

  function show(i) {
    var prev = screens[idx];
    idx = (i + screens.length) % screens.length;
    var next = screens[idx];
    if (prev === next) return;
    screens.forEach(function (s) { if (s !== prev && s !== next) s.className = 'dm-scr'; });
    prev.className = 'dm-scr was';          // stays opaque underneath while the next fades in
    next.className = 'dm-scr on';
    setTimeout(function () { if (screens[idx] !== prev) prev.className = 'dm-scr'; }, 260);
    knob.setAttribute('aria-label', 'Turn the dial. Showing ' + next.getAttribute('data-name'));
  }

  function turn() {
    rot += STEP;
    knob.style.setProperty('--rot', rot + 'deg');
    setTimeout(function () { show(idx + 1); }, reduce ? 0 : 200);
  }

  function tick() {
    if (visible && !document.hidden && Date.now() >= holdUntil) turn();
  }
  function start() { if (!timer && !reduce) timer = setInterval(tick, EVERY); }
  function stop() { clearInterval(timer); timer = null; }

  knob.addEventListener('click', function () {
    holdUntil = Date.now() + 5000;           // let the visitor drive for a bit
    turn();
  });

  // ---- arrows ----
  function drawArrows() {
    var sr = root.querySelector('.dm-stage').getBoundingClientRect();
    if (getComputedStyle(svg).display === 'none' || !sr.width) return;
    var dr = dev.getBoundingClientRect();
    var w = sr.width, h = sr.height, sw = Math.max(1.6, w / 1600 * 3.4);
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    var out = [];
    labels.forEach(function (lab, n) {
      var t = lab.querySelector('b').getBoundingClientRect();
      var left = lab.getAttribute('data-side') === 'l';
      var x1 = (left ? t.right + w * 0.008 : t.left - w * 0.008) - sr.left;
      var y1 = t.top + t.height * 0.55 - sr.top;
      var x2 = dr.left - sr.left + dr.width * parseFloat(lab.getAttribute('data-fx'));
      var y2 = dr.top - sr.top + dr.height * parseFloat(lab.getAttribute('data-fy'));
      var mx = (x1 + x2) / 2, my = (y1 + y2) / 2, dx = x2 - x1, dy = y2 - y1;
      var bow = parseFloat(lab.getAttribute('data-bow') || '0.12');
      var cx = mx - dy * bow, cy = my + dx * bow;
      out.push('<path style="--i:' + n + '" d="M' + x1.toFixed(1) + ' ' + y1.toFixed(1) +
        ' Q' + cx.toFixed(1) + ' ' + cy.toFixed(1) + ' ' + x2.toFixed(1) + ' ' + y2.toFixed(1) + '"/>');
    });
    svg.querySelector('g').innerHTML = out.join('');
    svg.style.setProperty('--sw', sw.toFixed(2) + 'px');
  }

  var raf = 0;
  function redraw() { cancelAnimationFrame(raf); raf = requestAnimationFrame(drawArrows); }
  window.addEventListener('resize', redraw);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(redraw);
  root.querySelector('.dm-body').addEventListener('load', redraw);
  redraw();

  // ---- run only while on screen ----
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        visible = e.isIntersecting;
        if (visible) { root.classList.add('in'); redraw(); start(); } else stop();
      });
    }, { threshold: 0.35 }).observe(dev);     // the device itself, so tall mobile layouts still start
  } else {
    visible = true; root.classList.add('in'); start();
  }
})();
