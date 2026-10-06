/* Cheeko card carousel */
(function () {
  "use strict";

  function createCardRail(rail, options) {
    if (!rail) return null;
    options = options || {};
    var track = rail.querySelector(".deckrail");
    if (!track || !track.children.length) return null;

    var cards = Array.from(track.children);
    cards.forEach(function (card, index) {
      card.dataset.cardIndex = String(index);
    });
    if (options.reducedMotion) return null;

    cards.forEach(function (card) {
      var copy = card.cloneNode(true);
      copy.classList.add("in");
      copy.setAttribute("aria-hidden", "true");
      copy.setAttribute("tabindex", "-1");
      copy.removeAttribute("role");
      copy.removeAttribute("aria-pressed");
      track.appendChild(copy);
    });

    var step = track.children[cards.length].offsetLeft - cards[0].offsetLeft;
    if (!step) return null;
    var now = options.now || Date.now;
    var requestFrame = options.requestFrame || requestAnimationFrame;
    var eventTarget = options.eventTarget || window;
    var pageHidden = options.pageHidden || function () { return document.hidden; };
    var heldUntil = 0;
    var pointerHeld = false;
    var hovered = false;
    var focused = false;
    var visible = true;
    var previousFrame = null;

    function hold() { heldUntil = now() + 2000; }
    function normalize() {
      while (rail.scrollLeft >= step) rail.scrollLeft -= step;
    }
    rail.addEventListener("scroll", normalize);
    rail.addEventListener("pointerdown", function () { pointerHeld = true; hold(); });
    rail.addEventListener("wheel", hold, { passive: true });
    rail.addEventListener("keydown", hold);
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
    }
    eventTarget.addEventListener("pointerup", releasePointer);
    eventTarget.addEventListener("pointercancel", releasePointer);
    eventTarget.addEventListener("resize", function () {
      var phase = rail.scrollLeft / step;
      step = track.children[cards.length].offsetLeft - cards[0].offsetLeft;
      rail.scrollLeft = phase * step;
      normalize();
    });
    if (typeof IntersectionObserver !== "undefined") {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
      }).observe(rail);
    }

    function tick(time) {
      if (previousFrame !== null && visible && !pageHidden() && !pointerHeld &&
          !hovered && !focused && now() >= heldUntil) {
        rail.scrollLeft += Math.min(64, Math.max(0, time - previousFrame)) * 0.028;
        normalize();
      }
      previousFrame = time;
      requestFrame(tick);
    }
    requestFrame(tick);
    return { normalize: normalize };
  }

  if (typeof module !== "undefined" && module.exports) module.exports = { createCardRail: createCardRail };
  if (typeof document !== "undefined") {
    createCardRail(document.querySelector(".decktrain"), {
      reducedMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches
    });
  }
}());
