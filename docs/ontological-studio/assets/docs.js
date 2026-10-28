(function () {
  'use strict';
  var root = document.documentElement;

  // 낮/밤 테마 — 이 사이트에만 저장한다.
  document.getElementById('theme').addEventListener('click', function () {
    var cur = root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('osdocs-theme', next); } catch (e) {}
  });

  // 모바일 목차
  var btn = document.querySelector('.menu-btn');
  btn.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelector('.doc').addEventListener('click', function () { document.body.classList.remove('nav-open'); });

  // 오른쪽 목차 — 지금 읽는 절을 표시
  var links = [].slice.call(document.querySelectorAll('.toc a'));
  var heads = links.map(function (a) { return document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))); });
  function spy() {
    var y = window.scrollY + 90, idx = -1;
    heads.forEach(function (h, i) { if (h && h.offsetTop <= y) idx = i; });
    links.forEach(function (a, i) { a.classList.toggle('on', i === idx); });
  }
  if (links.length) { addEventListener('scroll', spy, { passive: true }); spy(); }

  // 검색 — assets/search.json (장 제목·절 제목·본문)
  var q = document.getElementById('q'), box = document.getElementById('results'), data = null, sel = -1;
  function load() {
    if (data) return Promise.resolve(data);
    return fetch('assets/search.json').then(function (r) { return r.json(); }).then(function (d) { data = d; return d; });
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function hi(s, words) {
    var out = esc(s);
    words.forEach(function (w) { if (w) out = out.replace(new RegExp(w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), function (m) { return '<mark>' + m + '</mark>'; }); });
    return out;
  }
  function search(text) {
    var words = text.toLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) { box.hidden = true; return; }
    load().then(function (pages) {
      var hits = [];
      pages.forEach(function (p) {
        var hay = (p.t + ' ' + p.h.join(' ') + ' ' + p.x).toLowerCase();
        if (!words.every(function (w) { return hay.indexOf(w) >= 0; })) return;
        var score = 0;
        words.forEach(function (w) { if (p.t.toLowerCase().indexOf(w) >= 0) score += 10; p.h.forEach(function (h) { if (h.toLowerCase().indexOf(w) >= 0) score += 4; }); });
        var i = p.x.toLowerCase().indexOf(words[0]);
        var snip = i >= 0 ? p.x.slice(Math.max(0, i - 40), i + 90) : p.x.slice(0, 120);
        hits.push({ p: p, score: score, snip: snip });
      });
      hits.sort(function (a, b) { return b.score - a.score; });
      sel = -1;
      box.innerHTML = hits.length ? hits.slice(0, 12).map(function (h) {
        return '<a href="' + h.p.u + '"><b>' + hi(h.p.t, words) + '</b><small>' + esc(h.p.p) + ' · …' + hi(h.snip, words) + '…</small></a>';
      }).join('') : (document.documentElement.lang === 'en' ? '<div class="none">Nothing found. Try other words.</div>' : '<div class="none">찾는 내용이 없습니다. 다른 낱말로 찾아 보세요.</div>');
      box.hidden = false;
    });
  }
  q.addEventListener('input', function () { search(q.value.trim()); });
  q.addEventListener('focus', function () { load(); if (q.value.trim()) search(q.value.trim()); });
  q.addEventListener('keydown', function (e) {
    var items = box.querySelectorAll('a');
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault(); if (!items.length) return;
      sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length;
      items.forEach(function (a, i) { a.classList.toggle('sel', i === sel); });
    } else if (e.key === 'Enter' && items.length) {
      location.href = items[Math.max(sel, 0)].getAttribute('href');
    } else if (e.key === 'Escape') { box.hidden = true; q.blur(); }
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.search')) box.hidden = true; });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT') { e.preventDefault(); q.focus(); }
  });
})();
