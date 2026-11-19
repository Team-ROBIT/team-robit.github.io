// 1.2MB 이상인 움직이는 WebP 의 프레임을 절반으로 줄이고(재생 속도는 그대로) 다시 압축한다.
//   node scripts/redesign/thin_animations.mjs [--dry]
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

sharp.cache(false);
const dry = process.argv.includes('--dry');
const LIMIT = 1.2 * 1024 * 1024;

function* walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (/\.webp$/i.test(e.name)) yield p;
  }
}

let before = 0, after = 0, n = 0;
for (const file of walk('src/assets')) {
  const size = fs.statSync(file).size;
  if (size < LIMIT) continue;
  const meta = await sharp(file, { animated: true, limitInputPixels: false }).metadata();
  const pages = meta.pages ?? 1;
  if (pages < 40) continue; // 정지 사진이거나 이미 짧은 움직임
  const delay = meta.delay ?? Array(pages).fill(100);
  const frames = [];
  const delays = [];
  for (let i = 0; i < pages; i += 2) {
    frames.push(await sharp(file, { page: i, limitInputPixels: false }).png().toBuffer());
    delays.push((delay[i] ?? 100) + (delay[i + 1] ?? 0)); // 건너뛴 프레임의 시간을 합쳐 같은 속도로 재생
  }
  const out = await sharp(frames, { join: { animated: true } })
    .webp({ quality: 45, effort: 4, delay: delays, loop: meta.loop ?? 0 })
    .toBuffer();
  before += size;
  if (out.length < size * 0.9) {
    after += out.length;
    n++;
    if (!dry) { fs.writeFileSync(file + '.tmp', out); fs.renameSync(file + '.tmp', file); }
    console.log(`${path.basename(file)}  ${pages}f  ${(size / 1048576).toFixed(2)}MB -> ${(out.length / 1048576).toFixed(2)}MB`);
  } else after += size;
}
console.log(`${dry ? '[dry] ' : ''}${n}개 변경, ${(before / 1048576).toFixed(1)}MB -> ${(after / 1048576).toFixed(1)}MB`);
