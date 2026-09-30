/* CHEEKO · autoplaying video rail with manual scrolling */
(function () {
  "use strict";

  function createPressRail(rail, range, options) {
    if (!rail || !range) return null;
    options = options || {};
    var track = rail.querySelector(".press-track");
    if (!track || !track.children.length) return null;

    var reducedMotion = !!options.reducedMotion;
    var now = options.now || Date.now;
    var requestFrame = options.requestFrame || requestAnimationFrame;
    var eventTarget = options.eventTarget || window;
    var pageHidden = options.pageHidden || function () { return document.hidden; };
    var step = 0;
    var heldUntil = 0;
    var pointerHeld = false;
    var hovered = false;
    var focused = false;
    var previousFrame = null;

    if (!reducedMotion) {
      var leadingCopy = track.children[0].cloneNode(true);
      leadingCopy.setAttribute("data-marquee-copy", "");
      track.insertBefore(leadingCopy, track.children[0]);
      step = track.children[1].offsetLeft - track.children[0].offsetLeft;
      rail.scrollLeft = step;
    }

    function hold() { heldUntil = now() + 2000; }

    function normalize() {
      if (reducedMotion || !step) return;
      while (rail.scrollLeft < step / 2) rail.scrollLeft += step;
      while (rail.scrollLeft >= step * 1.5) rail.scrollLeft -= step;
    }

    function syncRange() {
      if (reducedMotion) {
        var maxScroll = Math.max(0, rail.scrollWidth - rail.clientWidth);
        range.value = String(maxScroll ? Math.round(rail.scrollLeft / maxScroll * 1000) : 0);
      } else if (step) {
        range.value = String(Math.max(0, Math.min(1000,
          Math.round((rail.scrollLeft / step - 0.5) * 1000))));
      }
    }

    rail.addEventListener("scroll", function () {
      normalize();
      syncRange();
    });
    range.addEventListener("input", function () {
      hold();
      if (reducedMotion) {
        rail.scrollLeft = Number(range.value) / 1000 * Math.max(0, rail.scrollWidth - rail.clientWidth);
      } else if (step) {
        rail.scrollLeft = (0.5 + Math.min(999, Number(range.value)) / 1000) * step;
      }
      syncRange();
    });

    [rail, range].forEach(function (control) {
      control.addEventListener("pointerdown", function () { pointerHeld = true; hold(); });
      control.addEventListener("wheel", hold, { passive: true });
      control.addEventListener("keydown", hold);
      control.addEventListener("mouseenter", function () { hovered = true; });
      control.addEventListener("mouseleave", function () { hovered = false; });
      control.addEventListener("focusin", function () { focused = true; });
      control.addEventListener("focusout", function (event) {
        if (!event.relatedTarget ||
          (!rail.contains(event.relatedTarget) && event.relatedTarget !== range)) focused = false;
      });
    });
    function releasePointer() {
      if (!pointerHeld) return;
      pointerHeld = false;
      hold();
    }
    eventTarget.addEventListener("pointerup", releasePointer);
    eventTarget.addEventListener("pointercancel", releasePointer);
    eventTarget.addEventListener("resize", function () {
      if (!reducedMotion) {
        var phase = step ? rail.scrollLeft / step - 1 : 0;
        step = track.children[1].offsetLeft - track.children[0].offsetLeft;
        rail.scrollLeft = step * (1 + phase);
        normalize();
      }
      syncRange();
    });

    function tick(time) {
      if (previousFrame !== null && !pageHidden() && !pointerHeld && !hovered &&
        !focused && now() >= heldUntil && !track.classList.contains("paused") && step) {
        rail.scrollLeft += Math.min(64, Math.max(0, time - previousFrame)) * 0.022;
        normalize();
        syncRange();
      }
      previousFrame = time;
      requestFrame(tick);
    }
    syncRange();
    if (!reducedMotion && step) requestFrame(tick);
    return { syncRange: syncRange };
  }

  if (typeof module !== "undefined" && module.exports) module.exports = { createPressRail: createPressRail };
  if (typeof document !== "undefined") {
    var rail = document.querySelector(".press-marquee");
    var range = document.querySelector(".press-scroll");
    createPressRail(rail, range, {
      reducedMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches
    });
  }
}());
