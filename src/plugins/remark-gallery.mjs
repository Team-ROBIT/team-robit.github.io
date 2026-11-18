// 연속된 "이미지 한 장짜리 문단"을 하나의 갤러리(<div class="gallery">)로 묶는 remark 플러그인.
// 마크다운에 이미지를 줄바꿈(빈 줄)으로만 나열해도 자동으로 격자 갤러리가 된다.
const isImageOnlyParagraph = (node) =>
  node.type === 'paragraph' &&
  node.children.length > 0 &&
  node.children.every((c) => c.type === 'image' || (c.type === 'text' && !c.value.trim()));

export default function remarkGallery() {
  return (tree) => {
    const out = [];
    const nodes = tree.children;
    let i = 0;
    while (i < nodes.length) {
      if (isImageOnlyParagraph(nodes[i])) {
        let j = i;
        while (j < nodes.length && isImageOnlyParagraph(nodes[j])) j++;
        if (j - i >= 2) {
          out.push({ type: 'html', value: '<div class="gallery">' });
          out.push(...nodes.slice(i, j));
          out.push({ type: 'html', value: '</div>' });
          i = j;
          continue;
        }
      }
      out.push(nodes[i]);
      i++;
    }
    tree.children = out;
  };
}
