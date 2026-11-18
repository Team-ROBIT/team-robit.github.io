// _backup/img -> _backup/img-opt : shrink the raw originals so they fit in the repo.
//   png/jpg -> webp (max 1600px wide), gif -> animated webp (max 720px wide)
// Run from repo root:  node scripts/backup/optimize.mjs
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const SRC = path.resolve('_backup/img');
const OUT = path.resolve('_backup/img-opt');
fs.mkdirSync(OUT, { recursive: true });

let before = 0;
let after = 0;
const files = fs.readdirSync(SRC).filter((f) => /\.(png|jpe?g|gif|webp)$/i.test(f));

for (const f of files) {
  const src = path.join(SRC, f);
  const ext = path.extname(f).toLowerCase();
  const out = path.join(OUT, f.replace(/\.[^.]+$/, '.webp'));
  if (fs.existsSync(out)) {
    before += fs.statSync(src).size;
    after += fs.statSync(out).size;
    continue;
  }
  const isGif = ext === '.gif';
  try {
    const img = sharp(src, { animated: isGif, limitInputPixels: false });
    const meta = await img.metadata();
    const maxW = isGif ? 720 : 1600;
    let p = img;
    if ((meta.width ?? 0) > maxW) p = p.resize({ width: maxW });
    await p.webp({ quality: isGif ? 70 : 82, effort: isGif ? 4 : 5 }).toFile(out);
    // heavy animations: second, smaller pass
    if (isGif && fs.statSync(out).size > 3 * 1048576) {
      let q = sharp(src, { animated: true, limitInputPixels: false });
      if ((meta.width ?? 0) > 520) q = q.resize({ width: 520 });
      await q.webp({ quality: 55, effort: 4 }).toFile(out + '.tmp');
      fs.renameSync(out + '.tmp', out);
    }
  } catch (e) {
    console.log('FAIL', f, e.message);
    continue;
  }
  before += fs.statSync(src).size;
  after += fs.statSync(out).size;
}
console.log(`files=${files.length} before=${(before / 1048576).toFixed(0)}MB after=${(after / 1048576).toFixed(0)}MB`);
