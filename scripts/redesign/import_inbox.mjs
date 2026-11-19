// _inbox 의 원본 사진을 WebP 로 변환해 src/assets/assets_contest 로 옮긴다.
//   node scripts/redesign/import_inbox.mjs
//
// 1) 이름이 정해진 개별 파일(jobs)
// 2) 슬롯 폴더:  _inbox/<페이지>/<연도>/<슬롯>/*.jpg|png|webp|gif
//      슬롯 = robot(로봇) · debug(개발·디버깅) · venue(대회 현장) · award(시상)
//    → src/assets/assets_contest/<페이지>-<연도>-<슬롯>-<번호>.webp
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const OUT = 'src/assets/assets_contest';
const jobs = [
  ['_inbox/defense-robot/2026/award/수상사진_로봇과같이.jpg', 'defense-2026-award.webp', 1600],
  ['_inbox/defense-robot/2025/award/2025국방단체사진.jpg', 'defense-2025-award.webp', 1600],
  ['_inbox/extreme-robot/2025/award/극한단체사진.jpg', 'extreme-2025-award.webp', 1600],
  ['_inbox/irc-manipulator/발표사진.png', 'irc-2026-presentation.webp', 1280],
  ['_inbox/irc-manipulator/수상사진.png', 'irc-2026-award.webp', 960],
  ['_inbox/irc-manipulator/시연사진.png', 'irc-2026-demo.webp', 1280],
];

async function convert(from, to, width) {
  const animated = from.toLowerCase().endsWith('.gif');
  const img = sharp(from, { animated, limitInputPixels: false }).rotate(); // EXIF 방향 보정
  const meta = await img.metadata();
  const w = animated ? Math.min(width, 720) : width;
  await (meta.width > w ? img.resize({ width: w }) : img).webp({ quality: animated ? 70 : 82 }).toFile(`${OUT}/${to}`);
  const out = await sharp(`${OUT}/${to}`).metadata();
  console.log(to, `${out.width}x${out.height}`);
}

for (const [from, to, w] of jobs) {
  if (fs.existsSync(from) && !fs.existsSync(`${OUT}/${to}`)) await convert(from, to, w);
}

// 슬롯 폴더
const IMG = /\.(jpe?g|png|webp|gif)$/i;
const slotWidth = { robot: 1200, debug: 1280, venue: 1600, award: 1600 };
for (const page of fs.readdirSync('_inbox', { withFileTypes: true }).filter((d) => d.isDirectory())) {
  for (const year of fs.existsSync(`_inbox/${page.name}`) ? fs.readdirSync(`_inbox/${page.name}`, { withFileTypes: true }).filter((d) => d.isDirectory() && /^\d{4}$/.test(d.name)) : []) {
    for (const slot of Object.keys(slotWidth)) {
      const dir = path.join('_inbox', page.name, year.name, slot);
      if (!fs.existsSync(dir)) continue;
      const files = fs.readdirSync(dir).filter((f) => IMG.test(f)).sort();
      const done = new Set(jobs.map((j) => path.basename(j[0])));
      for (let i = 0; i < files.length; i++) {
        if (done.has(files[i])) continue; // 이름이 정해진 파일(jobs)은 위에서 처리
        const to = `${page.name}-${year.name}-${slot}-${String(i + 1).padStart(2, '0')}.webp`;
        if (!fs.existsSync(`${OUT}/${to}`)) await convert(path.join(dir, files[i]), to, slotWidth[slot]);
      }
    }
  }
}
