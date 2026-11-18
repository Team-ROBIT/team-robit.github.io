// 팀 프로필 저장소(Team-ROBIT/.github)의 2025~2026 로봇 사진을 사이트 에셋으로 가져온다.
//   node scripts/redesign/import_contest_images.mjs [원본 폴더]
// 투명 배경(누끼) PNG 는 알파를 유지한 채 WebP 로 변환한다.
import sharp from 'sharp';

const SRC = process.argv[2] ?? 'C:/Users/Kinesis/Github/.github/images';
const OUT = 'src/assets/assets_contest';
const jobs = [
  ['2026_rescue.png', 'eclipse-2026-rescue.webp', 800],
  ['2026_defense.png', 'eclipse-2026-defense.webp', 800],
  ['2025_luco.png', 'luco-2025-defense.webp', 800],
  ['2026_safelab_card.png', 'safelab-2026-gripper.webp', 800],
  ['safelab_demo.jpg', 'safelab-2026-demo.webp', 1280],
];
for (const [from, to, w] of jobs) {
  const meta = await sharp(`${SRC}/${from}`).metadata();
  const img = sharp(`${SRC}/${from}`);
  await (meta.width > w ? img.resize({ width: w }) : img).webp({ quality: 85, alphaQuality: 90 }).toFile(`${OUT}/${to}`);
  const out = await sharp(`${OUT}/${to}`).metadata();
  console.log(to, `${out.width}x${out.height}`, 'alpha:', out.hasAlpha);
}
