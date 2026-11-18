// Perceptual hashes (9x8 dHash, first frame) of the original images and of every image in the repo.
// -> _backup/phash.json   (used by verify.py to recognise re-encoded copies of the same photo)
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const walk = (d) =>
  fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(d, e.name);
    return e.isDirectory() ? walk(p) : [p];
  });

async function dhash(file) {
  const { data } = await sharp(file, { limitInputPixels: false })
    .greyscale()
    .resize(9, 8, { fit: 'fill' })
    .raw()
    .toBuffer({ resolveWithObject: true });
  let bits = '';
  for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) bits += data[y * 9 + x] > data[y * 9 + x + 1] ? '1' : '0';
  return bits;
}

const out = { orig: {}, local: {} };
for (const f of walk('_backup/img-opt')) {
  try { out.orig[path.basename(f)] = await dhash(f); } catch { /* skip */ }
}
for (const base of ['src/assets', 'public']) {
  for (const f of walk(base)) {
    if (!/\.(webp|png|jpe?g|gif)$/i.test(f)) continue;
    try { out.local[f.replaceAll('\\', '/')] = await dhash(f); } catch { /* skip */ }
  }
}
fs.writeFileSync('_backup/phash.json', JSON.stringify(out));
console.log('orig', Object.keys(out.orig).length, 'local', Object.keys(out.local).length);
