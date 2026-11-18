// _inbox 에 넣은 원본 사진을 WebP 로 변환해 src/assets/assets_contest 로 옮긴다.
//   node scripts/redesign/import_inbox.mjs
import sharp from 'sharp';

const OUT = 'src/assets/assets_contest';
const jobs = [
  ['_inbox/defense-robot/수상사진_로봇과같이.jpg', 'defense-2026-award.webp', 1600],
  ['_inbox/irc-manipulator/발표사진.png', 'irc-2026-presentation.webp', 1280],
  ['_inbox/irc-manipulator/수상사진.png', 'irc-2026-award.webp', 960],
  ['_inbox/irc-manipulator/시연사진.png', 'irc-2026-demo.webp', 1280],
];
for (const [from, to, w] of jobs) {
  const img = sharp(from);
  const meta = await img.metadata();
  await (meta.width > w ? img.resize({ width: w }) : img).webp({ quality: 82 }).toFile(`${OUT}/${to}`);
  const out = await sharp(`${OUT}/${to}`).metadata();
  console.log(to, `${out.width}x${out.height}`);
}
