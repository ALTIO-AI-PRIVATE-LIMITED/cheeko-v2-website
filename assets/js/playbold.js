/* CHEEKO · Playbold interactions */
(function () {
  "use strict";

  /* Scroll reveal */
  var rv = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add("in"); });
  }

  /* Mobile nav */
  var burger = document.querySelector(".nav-burger");
  var links = document.querySelector(".nav-links");
  if (burger && links) {
    burger.addEventListener("click", function () {
      links.classList.toggle("open");
      burger.setAttribute("aria-expanded", links.classList.contains("open") ? "true" : "false");
    });
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") links.classList.remove("open");
    });
  }

  /* Film: click-to-play (no preload — India mobile first) */
  var filmFrames = document.querySelectorAll("[data-film]");
  filmFrames.forEach(function (frame) {
    var video = frame.querySelector("video");
    var badge = frame.querySelector(".play-badge");
    var track = frame.closest(".press-track");
    if (!video || !badge) return;
    badge.addEventListener("click", function () {
      filmFrames.forEach(function (otherFrame) {
        var otherVideo = otherFrame.querySelector("video");
        if (otherVideo && otherVideo !== video && !otherVideo.paused) otherVideo.pause();
      });
      video.setAttribute("controls", "controls");
      video.muted = false;
      if (track) track.classList.add("paused");
      var playRequest = video.play();
      if (playRequest && typeof playRequest.catch === "function") {
        playRequest.catch(function () {
          badge.classList.remove("hidden");
          video.load();
          if (track) track.classList.remove("paused");
        });
      }
    });
    video.addEventListener("playing", function () {
      badge.classList.add("hidden");
      if (track) track.classList.add("paused");
    });
    video.addEventListener("pause", function () {
      if (track) track.classList.remove("paused");
    });
    video.addEventListener("ended", function () {
      if (track) track.classList.remove("paused");
      badge.classList.remove("hidden");
      video.removeAttribute("controls");
      video.currentTime = 0;
      video.load();
    });
  });

  /* Audio samples: honest coming-soon until real recordings land */
  document.querySelectorAll("[data-sample]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var tag = btn.closest(".sample").querySelector(".serial");
      if (tag && !tag.dataset.flipped) {
        tag.dataset.flipped = "1";
        var prev = tag.textContent;
        tag.textContent = "REAL SAMPLE LANDS BEFORE LAUNCH";
        setTimeout(function () { tag.textContent = prev; delete tag.dataset.flipped; }, 2200);
      }
    });
  });

  /* Confetti on preorder clicks (tasteful, one burst) */
  var confettiOk = typeof window.confetti === "function" &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll(".buy-link").forEach(function (a) {
    a.addEventListener("click", function () {
      if (confettiOk) {
        window.confetti({ particleCount: 70, spread: 65, origin: { y: 0.7 },
          colors: ["#FFC81A", "#FF5C00", "#6C3DFF", "#17130E"] });
      }
    });
  });

  /* Card deck tabs */
  document.querySelectorAll("[data-deck]").forEach(function (deck) {
    var btns = deck.querySelectorAll("[data-card]");
    var panels = deck.querySelectorAll("[data-panel]");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.classList.toggle("on", x === b); });
        panels.forEach(function (p) { p.classList.toggle("on", p.getAttribute("data-panel") === b.getAttribute("data-card")); });
      });
    });
  });

  /* Card flip on tap */
  var deckTrain = document.querySelector(".decktrain");
  document.querySelectorAll(".fcardw").forEach(function (w) {
    w.addEventListener("click", function () {
      w.classList.toggle("flipped");
      if (deckTrain) deckTrain.classList.toggle("hold", !!document.querySelector(".fcardw.flipped"));
    });
  });

  /* Auto-advance swipe rows on mobile (honest screens, card deck) */
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduceMotion) {
    var autoRows = [
      { sel: ".screenrow", every: 2600 }
    ];
    autoRows.forEach(function (cfg) {
      document.querySelectorAll(cfg.sel).forEach(function (row) {
        var held = false, holdT = null, hover = false;
        function hold() {
          held = true;
          clearTimeout(holdT);
          holdT = setTimeout(function () { held = false; }, 6000);
        }
        ["pointerdown", "touchstart", "wheel"].forEach(function (e) {
          row.addEventListener(e, hold, { passive: true });
        });
        row.addEventListener("mouseenter", function () { hover = true; });
        row.addEventListener("mouseleave", function () { hover = false; });
        setInterval(function () {
          if (held || hover || document.hidden) return;
          if (row.scrollWidth <= row.clientWidth + 8) return;
          var r = row.getBoundingClientRect();
          if (r.bottom < 0 || r.top > window.innerHeight) return;
          var first = row.firstElementChild;
          var gap = parseFloat(getComputedStyle(row).columnGap) || 14;
          var step = first ? first.getBoundingClientRect().width + gap : row.clientWidth * 0.7;
          var max = row.scrollWidth - row.clientWidth;
          if (row.scrollLeft >= max - 8) row.scrollTo({ left: 0, behavior: "smooth" });
          else row.scrollBy({ left: step, behavior: "smooth" });
        }, cfg.every);
      });
    });
  }

  /* Character shelf pop-up */
  var popEl = document.getElementById("pop");
  if (popEl) {
    var PCH = [
      {k:"cheeko",n:"Cheeko",r:"The fox · ask anything",c:"In every Cheeko",pc:"#F0521D",
       l:"Press the button and ask. He answers in your family's language.",
       sk:["Speaking","Curiosity"],
       fx:[{t:"bub",v:"?",x:12,y:14,d:0},{t:"bub",v:"\u0915",x:76,y:8,d:.4},{t:"bub",v:"A",x:84,y:44,d:.8},{t:"bub",v:"!",x:5,y:52,d:1.2}]},
      {k:"quizzy",n:"Quizzy Bee",r:"The quiz bee · general knowledge",c:"In every Cheeko",pc:"#FFC81A",
       l:"Ten quick questions a day. No scores, no pressure.",
       sk:["General knowledge","Memory"],
       fx:[{t:"q",v:"?",x:10,y:10,d:0},{t:"q",v:"?",x:80,y:20,d:.5},{t:"em",v:"\uD83D\uDCA1",x:70,y:0,d:.9},{t:"q",v:"?",x:16,y:52,d:1.3}]},
      {k:"nani",n:"Nani",r:"The storyteller",c:"In your box",pc:"#6C3DFF",
       l:"Stories your child can interrupt, question and steer.",
       sk:["Listening","Imagination"],
       fx:[{t:"em",v:"\uD83D\uDCD6",x:12,y:12,d:0},{t:"em",v:"\u2728",x:80,y:6,d:.4},{t:"em",v:"\uD83C\uDF1F",x:86,y:46,d:.8},{t:"em",v:"\u2728",x:6,y:50,d:1.2}]},
      {k:"mitthu",n:"Mitthu",r:"The spelling parrot",c:"In your box",pc:"#2FA84F",
       l:"Says a word. Your child spells it back.",
       sk:["Spelling","Vocabulary"],
       fx:[{t:"tile",v:"A",x:10,y:14,d:0},{t:"tile",v:"B",x:80,y:6,d:.35},{t:"tile",v:"C",x:86,y:44,d:.7},{t:"tile",v:"Z",x:6,y:52,d:1.05}]},
      {k:"chanda",n:"Chanda",r:"The bedtime panda",c:"In the card shop",pc:"#3E63C4",
       l:"Slow stories and soft songs to end the day.",
       sk:["Calm","Sleep routine"],
       fx:[{t:"em",v:"\uD83C\uDF19",x:12,y:8,d:0},{t:"em",v:"\uD83D\uDCA4",x:78,y:14,d:.4},{t:"em",v:"\u2B50",x:86,y:48,d:.8},{t:"em",v:"\uD83D\uDCA4",x:6,y:48,d:1.2}]},
      {k:"masti",n:"Masti",r:"The mischief monkey",c:"In the card shop",pc:"#FF8A00",
       l:"Jokes, games and giggly challenges.",
       sk:["Confidence","Play"],
       fx:[{t:"em",v:"\uD83C\uDF89",x:10,y:10,d:0},{t:"em",v:"\uD83D\uDE02",x:80,y:8,d:.4},{t:"em",v:"\uD83C\uDFB5",x:86,y:46,d:.8},{t:"em",v:"\uD83C\uDF4C",x:6,y:50,d:1.2}]},
      {k:"tara",n:"Tara",r:"The space star",c:"In the card shop",pc:"#7B5CFF",
       l:"Space, stars and the biggest why questions.",
       sk:["Curiosity","Science"],
       fx:[{t:"em",v:"\uD83E\uDE90",x:10,y:10,d:0},{t:"em",v:"\uD83D\uDE80",x:80,y:6,d:.4},{t:"em",v:"\u2B50",x:86,y:46,d:.8},{t:"em",v:"\u2604\uFE0F",x:6,y:50,d:1.2}]}
    ];
    var pcur = 0, paudio = null;
    var pplayer = document.getElementById("pplayer");
    var plabel = document.getElementById("plabel");
    var ptoast = document.createElement("div");
    ptoast.className = "ptoast";
    ptoast.textContent = "Real voices land before launch";
    document.body.appendChild(ptoast);
    function pStop() {
      if (paudio) { paudio.pause(); paudio = null; }
      pplayer.classList.remove("playing"); plabel.textContent = "Hear me";
    }
    function pSampleUnavailable() {
      ptoast.classList.add("show");
      setTimeout(function () { ptoast.classList.remove("show"); }, 2200);
    }
    function pShow(i) {
      pcur = (i + PCH.length) % PCH.length;
      var ch = PCH[pcur];
      pStop();
      pplayer.hidden = ch.k === "cheeko";
      document.getElementById("pglow").style.setProperty("--pc", ch.pc);
      var stage = document.getElementById("pstage");
      stage.querySelectorAll(".pfx").forEach(function (e) { e.remove(); });
      var img = document.getElementById("pimg");
      img.src = "assets/img/live/char-" + ch.k + ".png"; img.alt = ch.n;
      ch.fx.forEach(function (f) {
        var s = document.createElement("span");
        s.className = "pfx " + f.t; s.textContent = f.v;
        s.style.left = f.x + "%"; s.style.top = f.y + "%";
        s.style.animationDelay = f.d + "s, " + (f.d + .5) + "s";
        stage.appendChild(s);
      });
      document.getElementById("pchip").textContent = ch.c;
      document.getElementById("pname").textContent = ch.n;
      document.getElementById("prole").textContent = ch.r;
      document.getElementById("pline").textContent = ch.l;
      var sk = document.getElementById("pskills");
      sk.innerHTML = "<b>Builds</b>";
      ch.sk.forEach(function (s2) { var el = document.createElement("i"); el.textContent = s2; sk.appendChild(el); });
      document.dispatchEvent(new CustomEvent("cheeko:character-change", { detail: { character: ch.k } }));
      popEl.classList.remove("open"); void popEl.offsetWidth; popEl.classList.add("open");
      document.body.classList.add("plocked");
    }
    function pClose() {
      pStop();
      document.dispatchEvent(new CustomEvent("cheeko:modal-close"));
      popEl.classList.remove("open");
      document.body.classList.remove("plocked");
    }
    document.querySelectorAll("[data-char]").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-char");
        pShow(PCH.findIndex(function (c) { return c.k === k; }));
      });
    });
    document.getElementById("pclose").addEventListener("click", pClose);
    document.getElementById("pscrim").addEventListener("click", pClose);
    document.getElementById("pprev").addEventListener("click", function () { pShow(pcur - 1); });
    document.getElementById("pnext").addEventListener("click", function () { pShow(pcur + 1); });
    document.addEventListener("cheeko:talk-open", pStop);
    document.addEventListener("keydown", function (e) {
      if (!popEl.classList.contains("open")) return;
      if (e.key === "Escape") pClose();
      if (e.key === "ArrowRight") pShow(pcur + 1);
      if (e.key === "ArrowLeft") pShow(pcur - 1);
    });
    pplayer.addEventListener("click", function () {
      if (pplayer.classList.contains("playing")) { pStop(); return; }
      var sample = PCH[pcur].audio;
      if (!sample) { pSampleUnavailable(); return; }
      paudio = new Audio(sample);
      paudio.play().then(function () {
        pplayer.classList.add("playing"); plabel.textContent = "Playing";
        paudio.onended = pStop;
      }).catch(function () {
        paudio = null;
        pSampleUnavailable();
      });
    });
  }

  /* Cinema hero crossfade */
  var cine = document.querySelector(".cine");
  if (cine && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var cslides = cine.querySelectorAll(".slide");
    var cdots = cine.querySelectorAll(".cn-dots i");
    var ci = 0;
    setInterval(function () {
      if (document.hidden) return;
      ci = (ci + 1) % cslides.length;
      cslides.forEach(function (s, j2) { s.classList.toggle("on", j2 === ci); });
      cdots.forEach(function (d, j2) { d.classList.toggle("on", j2 === ci); });
    }, 4200);
  }

  /* Buy bar appears only after the hero has scrolled away */
  var buybar = document.querySelector(".buybar");
  var heroEl = document.getElementById("top");
  if (buybar && heroEl) {
    var barTick = false;
    function syncBar() {
      barTick = false;
      buybar.classList.toggle("show", heroEl.getBoundingClientRect().bottom <= 40);
    }
    function onBarScroll() {
      if (barTick) return;
      barTick = true;
      requestAnimationFrame(syncBar);
    }
    ["scroll", "resize"].forEach(function (e) {
      window.addEventListener(e, onBarScroll, { passive: true });
      document.body.addEventListener(e, onBarScroll, { passive: true });
    });
    syncBar();
  }

  /* Honest screen: cycle the device screens */
  var hsStage = document.querySelector(".hsstage");
  if (hsStage && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var hsScreens = hsStage.querySelectorAll(".devscreen");
    var hsDots = hsStage.querySelectorAll(".hs-dots i");
    var hsI = 0;
    setInterval(function () {
      if (document.hidden) return;
      hsI = (hsI + 1) % hsScreens.length;
      hsScreens.forEach(function (s, k) { s.classList.toggle("on", k === hsI); });
      hsDots.forEach(function (d, k) { d.classList.toggle("on", k === hsI); });
    }, 2600);
  }

  /* Imagine tile: cycle the wish and the picture it actually drew */
  var wishText = document.getElementById("wishtext");
  var wishPic = document.getElementById("wishpic");
  if (wishText && wishPic && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var WISHES = [
      ["a red cat", "im-01"],
      ["a flying elephant", "im-02"],
      ["a house made of chocolate", "im-06"],
      ["a dinosaur wearing a birthday hat", "im-08"],
      ["a castle in the clouds", "im-13"],
      ["my school bag walking to school by itself", "im-15"],
      ["a rocket going past a purple planet", "im-11"],
      ["a banana wearing shoes", "im-18"]
    ];
    WISHES.forEach(function (w) { var p = new Image(); p.src = "assets/img/imagine/" + w[1] + ".jpg"; });
    var wi = 0;
    setInterval(function () {
      if (document.hidden) return;
      wi = (wi + 1) % WISHES.length;
      wishText.classList.add("fade"); wishPic.classList.add("fade");
      setTimeout(function () {
        wishText.textContent = "\u201C" + WISHES[wi][0] + "\u201D";
        wishPic.src = "assets/img/imagine/" + WISHES[wi][1] + ".jpg";
        wishPic.alt = "A picture Cheeko drew: " + WISHES[wi][0];
        wishText.classList.remove("fade"); wishPic.classList.remove("fade");
      }, 360);
    }, 3200);
  }

  /* Imagine film: thumbnail opens the video full size */
  var vbox = document.getElementById("vbox");
  if (vbox) {
    var vplayer = document.getElementById("vplayer");
    document.querySelectorAll("[data-play]").forEach(function (b) {
      b.addEventListener("click", function () {
        vbox.classList.add("open");
        document.body.classList.add("plocked");
        vplayer.currentTime = 0;
        vplayer.play();
      });
    });
    function closeFilm() {
      vbox.classList.remove("open");
      document.body.classList.remove("plocked");
      vplayer.pause();
    }
    document.getElementById("vclose").addEventListener("click", closeFilm);
    vbox.addEventListener("click", function (e) { if (e.target === vbox) closeFilm(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && vbox.classList.contains("open")) closeFilm(); });
  }

  /* Footer year */
  var yr = document.getElementById("yr");
  if (yr) yr.textContent = new Date().getFullYear();
})();
