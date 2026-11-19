// src/assets 의 WebP 를 다시 압축해 용량을 줄인다.
//   node scripts/redesign/compress_images.mjs          (실제로 덮어쓴다)
//   node scripts/redesign/compress_images.mjs --dry    (줄어드는 양만 본다)
// 규칙
//   · 150KB 미만은 건드리지 않는다.
//   · 사진: 가로 1600px 이하, quality 74
//   · 움직이는 WebP(gif 변환본): 가로 480px 이하, quality 45
//   · 결과가 원본의 92% 이하일 때만 바꾼다 (더 커지거나 거의 같으면 그대로 둔다)
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

sharp.cache(false); // Windows 에서 입력 파일이 잠기지 않도록 캐시를 끈다
const dry = process.argv.includes('--dry');
const ROOT = 'src/assets';
const MIN = 150 * 1024;

function* walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (/\.webp$/i.test(e.name)) yield p;
  }
}

let before = 0, after = 0, changed = 0, anim = 0;
for (const file of walk(ROOT)) {
  const size = fs.statSync(file).size;
  if (size < MIN) { before += size; after += size; continue; }
  const meta = await sharp(file, { animated: true, limitInputPixels: false }).metadata();
  const animated = (meta.pages ?? 1) > 1;
  const maxW = animated ? 480 : 1600;
  let img = sharp(file, { animated, limitInputPixels: false });
  if (meta.width > maxW) img = img.resize({ width: maxW });
  const buf = await img.webp({ quality: animated ? 45 : 74, effort: animated ? 4 : 5, alphaQuality: 80 }).toBuffer();
  before += size;
  if (buf.length <= size * 0.92) {
    after += buf.length;
    changed++;
    if (animated) anim++;
    if (!dry) { fs.writeFileSync(file + '.tmp', buf); fs.renameSync(file + '.tmp', file); }
    if (size > 1024 * 1024) console.log(`${animated ? 'GIF ' : 'IMG '}${path.basename(file)}  ${(size / 1048576).toFixed(2)}MB -> ${(buf.length / 1048576).toFixed(2)}MB`);
  } else after += size;
}
console.log(`\n${dry ? '[dry] ' : ''}${changed}개 변경 (움직이는 이미지 ${anim}개), ${(before / 1048576).toFixed(1)}MB -> ${(after / 1048576).toFixed(1)}MB`);
