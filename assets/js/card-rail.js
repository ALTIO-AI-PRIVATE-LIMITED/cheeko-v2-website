/* Cheeko card slider: whole cards only, arrows, gentle autoplay, infinite loop */
(function () {
  "use strict";

  /* How many whole cards fit in the row at a given width. */
  function cardsPerView(width) {
    if (width >= 1000) return 6;
    if (width >= 760) return 5;
    if (width >= 520) return 3;
    return 2;
  }

  function createCardRail(rail, options) {
    if (!rail) return null;
    options = options || {};
    var track = rail.querySelector(".deckrail");
    if (!track || !track.children.length) return null;

    var cards = Array.from(track.children);
    cards.forEach(function (card, index) {
      card.dataset.cardIndex = String(index);
    });

    var reducedMotion = !!options.reducedMotion;
    var now = options.now || Date.now;
    var requestFrame = options.requestFrame || function (cb) { return requestAnimationFrame(cb); };
    var eventTarget = options.eventTarget || window;
    var pageHidden = options.pageHidden || function () { return document.hidden; };
    var gapOf = options.gap || function () {
      var g = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap);
      return isNaN(g) ? 16 : g;
    };
    var interval = options.interval || 3200;
    var duration = options.duration || 520;

    /* Infinite loop: append one copy of the deck (not on reduced motion). */
    if (!reducedMotion) {
      cards.forEach(function (card) {
        var copy = card.cloneNode(true);
        copy.classList.add("in");
        copy.setAttribute("aria-hidden", "true");
        copy.setAttribute("tabindex", "-1");
        copy.removeAttribute("role");
        copy.removeAttribute("aria-pressed");
        track.appendChild(copy);
      });
    }

    var cardStep = 0;   /* one card + gap */
    var loop = 0;       /* width of one full deck */
    var animating = false;
    var heldUntil = 0;
    var pointerHeld = false;
    var hovered = false;
    var focused = false;
    var visible = true;
    var settleTimer = null;

    /* Size cards so a whole number fits the row exactly. */
    function layout() {
      var width = rail.clientWidth || 0;
      var gap = gapOf();
      if (width) {
        var n = cardsPerView(width);
        var cardWidth = (width - gap * (n - 1)) / n;
        track.style.setProperty("--fcw", cardWidth.toFixed(2) + "px");
        cardStep = cardWidth + gap;
      } else {
        cardStep = (cards[1] ? cards[1].offsetLeft - cards[0].offsetLeft : 0) || cardStep;
      }
      loop = cardStep * cards.length;
      if (cardStep) rail.scrollLeft = Math.round(rail.scrollLeft / cardStep) * cardStep;
      normalize();
    }

    function normalize() {
      if (reducedMotion || !loop) return;
      while (rail.scrollLeft >= loop) rail.scrollLeft -= loop;
      while (rail.scrollLeft < 0) rail.scrollLeft += loop;
    }

    function ease(t) { return 1 - Math.pow(1 - t, 3); }

    function animateTo(target, done) {
      var from = rail.scrollLeft;
      var distance = target - from;
      if (!distance) { if (done) done(); return; }
      animating = true;
      var start = null;
      function frame(time) {
        if (start === null) start = time;
        var t = Math.min(1, (time - start) / duration);
        rail.scrollLeft = from + distance * ease(t);
        if (t < 1) { requestFrame(frame); return; }
        rail.scrollLeft = target;
        animating = false;
        normalize();
        if (done) done();
      }
      requestFrame(frame);
    }

    /* Move by one card; dir = 1 (next) or -1 (previous). */
    function go(dir) {
      if (!cardStep || animating) return;
      var base = Math.round(rail.scrollLeft / cardStep) * cardStep;
      if (reducedMotion) {
        var max = Math.max(0, rail.scrollWidth - rail.clientWidth);
        rail.scrollLeft = Math.max(0, Math.min(max, base + dir * cardStep));
        return;
      }
      if (dir < 0 && base <= 0) { rail.scrollLeft += loop; base += loop; }
      animateTo(base + dir * cardStep);
    }

    function hold() { heldUntil = now() + 4000; }

    /* After a manual swipe or drag, settle on a whole card. */
    function settle() {
      if (animating || pointerHeld || !cardStep) return;
      var target = Math.round(rail.scrollLeft / cardStep) * cardStep;
      if (Math.abs(target - rail.scrollLeft) > 0.5) animateTo(target);
    }

    rail.addEventListener("scroll", function () {
      if (animating) return;
      normalize();
      if (settleTimer) clearTimeout(settleTimer);
      settleTimer = setTimeout(settle, 140);
    });
    rail.addEventListener("pointerdown", function () { pointerHeld = true; hold(); });
    rail.addEventListener("wheel", hold, { passive: true });
    rail.addEventListener("keydown", function (event) {
      hold();
      if (event.key === "ArrowRight") { event.preventDefault(); go(1); }
      if (event.key === "ArrowLeft") { event.preventDefault(); go(-1); }
    });
    rail.addEventListener("mouseenter", function () { hovered = true; });
    rail.addEventListener("mouseleave", function () { hovered = false; });
    rail.addEventListener("focusin", function () { focused = true; });
    rail.addEventListener("focusout", function (event) {
      if (!event.relatedTarget || !rail.contains(event.relatedTarget)) focused = false;
    });
    function releasePointer() {
      if (!pointerHeld) return;
      pointerHeld = false;
      hold();
      setTimeout(settle, 60);
    }
    eventTarget.addEventListener("pointerup", releasePointer);
    eventTarget.addEventListener("pointercancel", releasePointer);
    eventTarget.addEventListener("resize", layout);

    if (typeof IntersectionObserver !== "undefined") {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
      }).observe(rail);
    }

    /* Arrow buttons live next to the rail, in the same .deckwrap. */
    var wrap = rail.parentNode && rail.parentNode.querySelectorAll ? rail.parentNode : null;
    if (wrap) {
      var prev = wrap.querySelector(".deckarrow.prev");
      var next = wrap.querySelector(".deckarrow.next");
      if (prev) prev.addEventListener("click", function () { hold(); go(-1); });
      if (next) next.addEventListener("click", function () { hold(); go(1); });
    }

    function tick() {
      if (!reducedMotion && visible && !pageHidden() && !pointerHeld &&
          !hovered && !focused && now() >= heldUntil) {
        go(1);
      }
    }
    var timer = reducedMotion ? null : setInterval(tick, interval);

    layout();
    return { go: go, tick: tick, layout: layout, normalize: normalize, stop: function () { if (timer) clearInterval(timer); } };
  }

  if (typeof module !== "undefined" && module.exports) module.exports = { createCardRail: createCardRail, cardsPerView: cardsPerView };
  if (typeof document !== "undefined") {
    createCardRail(document.querySelector(".decktrain"), {
      reducedMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches
    });
  }
}());
