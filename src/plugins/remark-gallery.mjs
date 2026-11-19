// 마크다운 이미지 배치 규칙
//  1) 연속된 "이미지 한 장짜리 문단"은 하나의 갤러리(<div class="gallery">)로 묶인다.
//  2) 직전 제목에 "현장"이 들어 있고 사진이 5장·9장(=큰 사진 1 + 4의 배수)이면 첫 사진을 크게 보여 준다 (class="gallery feature").
//     5장이면("현장"이 아닐 때) 윗줄 3장 + 아랫줄 2장으로 맞춘다 (class="gallery n5").
//  3) 이미지에 title 을 달면 캡션이 된다:  ![대체 텍스트](경로 "캡션 문장")
const isImageOnlyParagraph = (node) =>
  node.type === 'paragraph' &&
  node.children.length > 0 &&
  node.children.every((c) => c.type === 'image' || (c.type === 'text' && !c.value.trim()));

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const textOf = (node) => (node.children ?? []).map((c) => c.value ?? textOf(c)).join('');
const caption = (p) => p.children.find((c) => c.type === 'image')?.title ?? '';

// 문단 하나를 <figure>(+캡션)로 감싼 노드 배열로 바꾼다. 캡션이 없으면 그대로 둔다.
function figure(p) {
  const cap = caption(p);
  if (!cap) return [p];
  return [{ type: 'html', value: '<figure>' }, p, { type: 'html', value: `<figcaption>${esc(cap)}</figcaption></figure>` }];
}

export default function remarkGallery() {
  return (tree) => {
    const out = [];
    const nodes = tree.children;
    let heading = '';
    let i = 0;
    while (i < nodes.length) {
      const node = nodes[i];
      if (node.type === 'heading') heading = textOf(node);
      if (isImageOnlyParagraph(node)) {
        let j = i;
        while (j < nodes.length && isImageOnlyParagraph(nodes[j])) j++;
        if (j - i >= 2) {
          const n = j - i;
          const feature = /현장/.test(heading) && n >= 5 && (n - 1) % 4 === 0;
          out.push({ type: 'html', value: `<div class="gallery${feature ? ' feature' : n === 5 ? ' n5' : ''}">` });
          for (const p of nodes.slice(i, j)) out.push(...figure(p));
          out.push({ type: 'html', value: '</div>' });
        } else {
          out.push(...figure(node));
        }
        i = j;
        continue;
      }
      out.push(node);
      i++;
    }
    tree.children = out;
  };
}
