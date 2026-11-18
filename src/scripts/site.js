// 공통 동작: 메가메뉴, 모바일 메뉴, 스크롤 등장 효과, 숫자 카운트업, 진행 막대, 목차 하이라이트, 필터
const dataEl = document.getElementById('mega-data');
const M = dataEl ? JSON.parse(dataEl.textContent || '{}') : {};
const mega = document.getElementById('mega');
const scrim = document.getElementById('scrim');
const links = [...document.querySelectorAll('#menu a[data-m]')];
let hideTimer;

function show(key, anchor) {
  const d = M[key];
  if (!d || !mega) return;
  clearTimeout(hideTimer);
  document.getElementById('mh').textContent = d.h;
  document.getElementById('mt').textContent = d.t;
  document.getElementById('mp').textContent = d.p;
  const list = document.getElementById('ml');
  list.innerHTML = d.list
    .map((x, i) => `<a href="${x.href}"><i>${String(i + 1).padStart(2, '0')}</i>${x.label}<em>${x.meta}</em></a>`)
    .join('');
  const feat = document.getElementById('mf');
  feat.innerHTML = d.list.map((x, i) => `<img src="${x.img}" class="${i === 0 ? 'on' : ''}" alt="" loading="lazy">`).join('');
  feat.dataset.t = d.list[0].label;
  [...list.children].forEach((el, i) =>
    el.addEventListener('mouseenter', () => {
      [...feat.children].forEach((m, k) => m.classList.toggle('on', k === i));
      feat.dataset.t = d.list[i].label;
      [...list.children].forEach((z) => z.classList.toggle('hv', z === el));
    }),
  );
  mega.classList.add('on');
  mega.setAttribute('aria-hidden', 'false');
  scrim.classList.add('on');
  links.forEach((l) => l.classList.toggle('open', l === anchor));
}
function hide() {
  hideTimer = setTimeout(() => {
    mega.classList.remove('on');
    mega.setAttribute('aria-hidden', 'true');
    scrim.classList.remove('on');
    links.forEach((l) => l.classList.remove('open'));
  }, 140);
}
links.forEach((a) => {
  a.addEventListener('mouseenter', () => show(a.dataset.m, a));
  a.addEventListener('mouseleave', hide);
  a.addEventListener('focus', () => show(a.dataset.m, a));
});
if (mega) {
  mega.addEventListener('mouseenter', () => clearTimeout(hideTimer));
  mega.addEventListener('mouseleave', hide);
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') hide();
});

// 모바일 메뉴
const burger = document.getElementById('burger');
const drawer = document.getElementById('drawer');
if (burger && drawer) {
  burger.addEventListener('click', () => {
    const on = burger.classList.toggle('on');
    drawer.classList.toggle('on', on);
    burger.setAttribute('aria-expanded', String(on));
    document.body.style.overflow = on ? 'hidden' : '';
  });
}

// 숫자 카운트업 + 스크롤 등장
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
function count(el) {
  const to = +el.dataset.c;
  if (reduce) { el.textContent = to; return; }
  const start = performance.now();
  (function step(now) {
    const p = Math.min(1, (now - start) / 1700);
    el.textContent = Math.round(to * (1 - Math.pow(1 - p, 4)));
    if (p < 1) requestAnimationFrame(step);
  })(start);
}
const io = new IntersectionObserver(
  (entries) =>
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('on');
      e.target.querySelectorAll('[data-c]').forEach(count);
      io.unobserve(e.target);
    }),
  { threshold: 0.12 },
);
document.querySelectorAll('.rv,.stats').forEach((x) => io.observe(x));

// 진행 막대 + 목차(탭) 하이라이트
const prog = document.getElementById('prog');
const tabs = [...document.querySelectorAll('.tabs a[href^="#"]')];
const targets = tabs.map((a) => document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))));
function onScroll() {
  const max = document.body.scrollHeight - innerHeight;
  if (prog && max > 0) prog.style.width = (scrollY / max) * 100 + '%';
  if (tabs.length) {
    let c = 0;
    targets.forEach((t, i) => { if (t && t.getBoundingClientRect().top < 240) c = i; });
    tabs.forEach((a, i) => a.classList.toggle('on', i === c));
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

// 홈 히어로 사진 기울기
const stage = document.getElementById('stage');
const frame = document.getElementById('frame');
if (stage && frame && !reduce) {
  stage.addEventListener('mousemove', (e) => {
    const r = stage.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    frame.style.transform = `rotateY(${x * 9}deg) rotateX(${-y * 9}deg)`;
  });
  stage.addEventListener('mouseleave', () => (frame.style.transform = ''));
}

// 기수 선택 띠: 현재 기수가 보이도록 가로 스크롤
const curGen = document.querySelector('.gens .gn.on');
if (curGen) {
  const strip = curGen.parentElement;
  strip.scrollLeft = curGen.offsetLeft - strip.clientWidth / 2 + curGen.clientWidth / 2;
}
