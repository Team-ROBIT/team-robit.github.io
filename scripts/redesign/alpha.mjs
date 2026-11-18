// assets_robots 이미지 중 투명 배경(누끼) 이미지 목록을 src/data/alpha.json 으로 저장한다.
import fs from 'node:fs';
import sharp from 'sharp';
const dir = 'src/assets/assets_robots';
const out = [];
for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.webp'))) {
  const m = await sharp(`${dir}/${f}`).metadata();
  const st = m.hasAlpha ? await sharp(`${dir}/${f}`).stats() : null;
  if (m.hasAlpha && st && !st.isOpaque) out.push(f.replace('.webp', ''));
}
fs.writeFileSync('src/data/alpha.json', JSON.stringify(out, null, 1));
console.log('alpha images:', out.length);
