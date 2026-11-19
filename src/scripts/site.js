// 공통 동작: 모바일 서랍, 검색, 링크 복사, 스크롤 등장 효과, 진행 막대, 목차 하이라이트, 홈 연표, 필터
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = (id) => document.getElementById(id);

// 모바일 서랍(사이드바)
const burger = $('burger');
const nav = $('nav');
const scrim = $('scrim');
function drawer(on) {
  if (!nav) return;
  nav.classList.toggle('on', on);
  scrim?.classList.toggle('on', on);
  burger?.classList.toggle('on', on);
  burger?.setAttribute('aria-expanded', String(on));
  document.body.style.overflow = on ? 'hidden' : '';
}
burger?.addEventListener('click', () => drawer(!nav.classList.contains('on')));
scrim?.addEventListener('click', () => drawer(false));
nav?.addEventListener('click', (e) => { if (e.target.closest('a')) drawer(false); });

// 검색 (Ctrl/⌘ + K, "/" 로도 열린다)
const sbox = $('sbox');
const sq = $('sq');
const sr = $('sr');
let data = [];
try { data = JSON.parse($('search-data')?.textContent || '[]'); } catch {}
let hv = 0;
function render(q) {
  const k = q.trim().toLowerCase();
  const hit = (k ? data.filter((d) => `${d.t} ${d.s} ${d.d} ${d.k}`.toLowerCase().includes(k)) : data.slice(0, 8)).slice(0, 10);
  sr.innerHTML = hit.length
    ? hit.map((d, i) => `<li><a href="${d.u}" class="${i === 0 ? 'hv' : ''}"><small>${d.k}</small>${d.t}<em>${d.s || d.d}</em></a></li>`).join('')
    : '<li class="none">일치하는 페이지가 없습니다.</li>';
  hv = 0;
}
function openSearch() {
  if (!sbox) return;
  sbox.hidden = false;
  sq.value = '';
  render('');
  sq.focus();
}
function closeSearch() { if (sbox) sbox.hidden = true; }
$('srch')?.addEventListener('click', openSearch);
sbox?.addEventListener('click', (e) => { if (e.target === sbox) closeSearch(); });
sq?.addEventListener('input', () => render(sq.value));
sq?.addEventListener('keydown', (e) => {
  const items = [...sr.querySelectorAll('a')];
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    if (!items.length) return;
    items[hv]?.classList.remove('hv');
    hv = (hv + (e.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length;
    items[hv].classList.add('hv');
    items[hv].scrollIntoView({ block: 'nearest' });
  } else if (e.key === 'Enter' && items[hv]) location.href = items[hv].getAttribute('href');
});
document.addEventListener('keydown', (e) => {
  const typing = /input|textarea/i.test(document.activeElement?.tagName || '');
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
  else if (e.key === '/' && !typing) { e.preventDefault(); openSearch(); }
  else if (e.key === 'Escape') { closeSearch(); drawer(false); }
});

// 링크 복사
const copy = $('copylink');
copy?.addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(location.href); copy.textContent = '복사됨'; }
  catch { copy.textContent = '복사 실패'; }
  setTimeout(() => (copy.textContent = '링크 복사'), 1600);
});

// 스크롤 등장
const io = new IntersectionObserver(
  (entries) =>
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('on');
      if (e.target.querySelector('#rail')) buildTimeline();
      io.unobserve(e.target);
    }),
  { threshold: 0.15 },
);
document.querySelectorAll('.rv').forEach((x) => io.observe(x));

// 진행 막대 + 목차 하이라이트
const prog = $('prog');
const tocLinks = [...document.querySelectorAll('.toc a[href^="#"]')];
const targets = tocLinks.map((a) => document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))));
function onScroll() {
  const max = document.body.scrollHeight - innerHeight;
  if (prog && max > 0) prog.style.width = (scrollY / max) * 100 + '%';
  if (tocLinks.length) {
    let c = 0;
    targets.forEach((t, i) => { if (t && t.getBoundingClientRect().top < 160) c = i; });
    tocLinks.forEach((a, i) => a.classList.toggle('on', i === c));
  }
}
addEventListener('scroll', onScroll, { passive: true });
onScroll();

// 필터 버튼 (로봇 목록 등)
const fb = [...document.querySelectorAll('.fl button')];
fb.forEach((b) =>
  b.addEventListener('click', () => {
    fb.forEach((x) => x.classList.toggle('on', x === b));
    document.querySelectorAll('[data-t]').forEach((c) => {
      if (c.classList.contains('rc')) c.style.display = b.dataset.f === 'all' || c.dataset.t === b.dataset.f ? '' : 'none';
    });
  }),
);

// 홈: 히어로 빛무리가 커서를 따라간다
const hero = $('hero');
const glow = $('glow');
if (hero && glow && !reduce) {
  hero.addEventListener('mousemove', (e) => {
    const r = hero.getBoundingClientRect();
    glow.style.transform = `translate(${(e.clientX - r.left - r.width * 0.75) * 0.3}px,${(e.clientY - r.top - r.height * 0.2) * 0.3}px)`;
  });
}

// 홈: 연표 눈금
let built = false;
function buildTimeline() {
  const rail = $('rail');
  if (built || !rail) return;
  built = true;
  const ms = JSON.parse(rail.dataset.m || '[]');
  ms.forEach((m, i) => {
    const t = document.createElement('div');
    t.className = 'tk' + (i === 0 ? ' on' : '');
    t.style.left = m.x + '%';
    t.innerHTML = `<span>${m.y} · ${m.t}</span>`;
    t.addEventListener('mouseenter', () => {
      rail.querySelectorAll('.tk').forEach((k) => k.classList.toggle('on', k === t));
      $('tlb').textContent = m.y;
      $('tls').textContent = m.t;
    });
    rail.appendChild(t);
  });
  requestAnimationFrame(() => ($('fill').style.width = '100%'));
}
if (reduce) buildTimeline();

// 기수 선택 띠: 현재 기수가 보이도록 가로 스크롤
const curGen = document.querySelector('.gens .gn.on');
if (curGen) {
  const strip = curGen.parentElement;
  strip.scrollLeft = curGen.offsetLeft - strip.clientWidth / 2 + curGen.clientWidth / 2;
}
