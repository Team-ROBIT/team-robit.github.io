"""theme.css 를 설계도(C) 레이아웃용으로 다시 조립한다.
   - 새 크롬(사이드바 · 상단 바 · 제목 카드 · 목차 · 홈)은 아래 CHROME 문자열
   - 기존 본문 컴포넌트(상세 · 수상 · 멤버 · 행사 · 로봇) 스타일은 old 파일에서 가져와 폰트 변수를 바꿔 쓴다
   python -I scripts/redesign/build_theme.py <old_theme.css> <out>"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
old = open(sys.argv[1], encoding='utf-8').read().split('\n')

CHROME = r'''/* ROːBIT Archive theme — 설계도(Blueprint) 레이아웃: 왼쪽 사이드바 · 상단 바 · 제목 카드 · 오른쪽 목차 */
@property --ang{syntax:"<angle>";inherits:false;initial-value:0deg}
:root{--bg:#f5f6f8;--panel:#fff;--ink:#14161a;--mute:#667085;--line:#e3e6ec;--maroon:#7a2233;--coral:#ff6b5e;--amber:#ffb15c;--blush:#fbeff0;--sk:0deg;
--grad:linear-gradient(90deg,#7a2233,#d6404f 45%,#ff6b5e 70%,#ffb15c);
--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Consolas,monospace;--sans:"Pretendard Variable",Pretendard,system-ui,sans-serif;--disp:var(--sans)}
*{box-sizing:border-box;margin:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased;display:grid;grid-template-columns:272px minmax(0,1fr);min-height:100vh}
a{color:inherit;text-decoration:none}button{font:inherit;color:inherit}
main{min-width:0;min-height:60vh}
.prog{position:fixed;top:0;left:0;height:3px;width:0;background:var(--grad);z-index:300}
.rv{opacity:0;transform:translateY(24px);transition:opacity .7s,transform .7s cubic-bezier(.2,.8,.2,1)}.rv.on{opacity:1;transform:none}

/* ---------- 사이드바 ---------- */
aside.nav{position:sticky;top:0;height:100vh;background:var(--panel);border-right:1px solid var(--line);padding:26px 18px;display:flex;flex-direction:column;gap:22px;overflow:auto;z-index:130}
.brand{display:flex;align-items:center;gap:11px;padding:0 8px;font-weight:800;letter-spacing:-.02em;font-size:17px}.brand img{width:34px;height:34px;border-radius:50%}.brand span{color:var(--maroon)}
.srch{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;color:var(--mute);font-size:13.5px;background:var(--bg);cursor:pointer;text-align:left;transition:.25s}
.srch:hover{border-color:#c9ced8;box-shadow:0 0 0 4px rgba(122,34,51,.07)}.srch kbd{margin-left:auto;font:500 11px var(--mono);border:1px solid var(--line);background:#fff;border-radius:6px;padding:2px 6px}
.grp small{display:block;font:500 11px var(--mono);letter-spacing:.14em;color:#98a2b3;padding:0 10px 8px}
.grp a{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:9px;font-size:14px;color:#3c4350;position:relative;transition:.2s}
.grp a i{font:500 11px var(--mono);color:#98a2b3;width:20px;font-style:normal}.grp a em{margin-left:auto;font:500 11px var(--mono);color:#98a2b3;font-style:normal}
.grp a:hover{background:var(--bg);color:var(--ink)}
.grp a.cur{background:var(--blush);color:var(--maroon);font-weight:700}.grp a.cur::before{content:"";position:absolute;left:-18px;top:8px;bottom:8px;width:3px;border-radius:0 3px 3px 0;background:var(--grad)}
.grp a.sub{padding:6px 10px 6px 40px;font-size:13.5px;color:var(--mute)}.grp a.sub.cur{color:var(--maroon);font-weight:700}
.side-foot{margin-top:auto;font:500 11px/1.7 var(--mono);color:#98a2b3;padding:14px 10px;border-top:1px dashed var(--line)}.side-foot b{color:var(--maroon)}
.scrim{position:fixed;inset:0;background:rgba(20,22,26,.35);opacity:0;visibility:hidden;transition:.3s;z-index:120}.scrim.on{opacity:1;visibility:visible}

/* ---------- 상단 바 ---------- */
.bar{height:60px;display:flex;align-items:center;justify-content:space-between;gap:14px;padding:0 44px;border-bottom:1px solid var(--line);background:rgba(245,246,248,.88);backdrop-filter:blur(10px);position:sticky;top:0;z-index:30}
.crumb{font:500 12px var(--mono);color:var(--mute);letter-spacing:.04em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.crumb b{color:var(--ink);font-weight:500}
.bar .r{display:flex;gap:10px;font-size:13px;margin-left:auto}.bar .r a,.bar .r button{white-space:nowrap;padding:7px 14px;border-radius:8px;border:1px solid var(--line);background:#fff;font-weight:600;cursor:pointer;transition:.25s}.bar .r a:hover,.bar .r button:hover{border-color:var(--maroon);color:var(--maroon)}
.burger{display:none;width:40px;height:40px;border-radius:10px;border:1px solid var(--line);background:#fff;align-items:center;justify-content:center;flex-direction:column;gap:4px;cursor:pointer}.burger i{width:17px;height:2px;background:var(--ink);border-radius:2px;transition:.3s}
.burger.on i:nth-child(1){transform:translateY(6px) rotate(45deg)}.burger.on i:nth-child(2){opacity:0}.burger.on i:nth-child(3){transform:translateY(-6px) rotate(-45deg)}

/* ---------- 검색 ---------- */
.sbox{position:fixed;inset:0;z-index:400;background:rgba(20,22,26,.45);display:flex;justify-content:center;align-items:flex-start;padding:12vh 20px 20px}.sbox[hidden]{display:none}
.sbox .sp{width:min(580px,100%);background:#fff;border-radius:16px;box-shadow:0 40px 80px -30px rgba(0,0,0,.5);overflow:hidden}
.sbox input{width:100%;border:0;border-bottom:1px solid var(--line);padding:18px 22px;font:500 16px var(--sans);outline:0}
.sbox ul{list-style:none;max-height:50vh;overflow:auto;padding:8px}.sbox li a{display:flex;align-items:baseline;gap:12px;padding:11px 14px;border-radius:10px;font-weight:600}.sbox li a small{font:500 11px var(--mono);color:#98a2b3;letter-spacing:.08em;flex:none;width:76px}.sbox li a em{font-style:normal;font-weight:400;font-size:13px;color:var(--mute);margin-left:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:46%}
.sbox li a:hover,.sbox li a.hv{background:var(--blush);color:var(--maroon)}.sbox li.none{padding:18px;color:var(--mute);font-size:14px}

/* ---------- 문서 틀 · 제목 카드 · 목차 ---------- */
.dl{display:grid;grid-template-columns:minmax(0,1fr) 210px;gap:50px;padding:40px 44px 20px;max-width:1240px}.dl.notoc{grid-template-columns:minmax(0,1fr)}
.dl-main{min-width:0}
.title{position:relative;border-radius:22px;background:var(--panel);border:1px solid var(--line);padding:44px 48px;overflow:hidden;display:grid;grid-template-columns:1fr minmax(0,300px);gap:30px;align-items:center;margin-bottom:46px;isolation:isolate}.title.one{grid-template-columns:1fr}
.title::before{content:"";position:absolute;inset:0;z-index:-2;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:32px 32px;mask-image:radial-gradient(80% 100% at 85% 50%,#000,transparent 80%)}
.title::after{content:"";position:absolute;z-index:-1;width:380px;height:380px;right:-60px;top:-80px;border-radius:50%;filter:blur(60px);background:radial-gradient(circle,rgba(255,107,94,.4),rgba(255,177,92,.22) 55%,transparent 70%);animation:gl 7s ease-in-out infinite alternate}@keyframes gl{to{transform:translate(-40px,30px)}}
.lbl{font:500 11.5px var(--mono);letter-spacing:.12em;color:var(--maroon);display:flex;gap:12px;align-items:center;text-transform:uppercase}.lbl i{display:inline-block;width:28px;height:2px;background:var(--grad);flex:none}
.title h1{font-size:clamp(32px,4.2vw,54px);font-weight:800;letter-spacing:-.05em;line-height:1.12;margin:16px 0 14px;word-break:keep-all}
.badges{display:flex;gap:8px;flex-wrap:wrap}.badges span{font:500 12px var(--mono);padding:6px 11px;border-radius:8px;background:var(--bg);border:1px solid var(--line);color:#3c4350}.badges span.hl{background:var(--blush);border-color:#efc9cd;color:var(--maroon)}
.tfig img{width:100%;filter:drop-shadow(0 20px 18px rgba(20,22,26,.3));animation:hov 5s ease-in-out infinite alternate;display:block}@keyframes hov{to{transform:translateY(-10px) rotate(-1.5deg)}}
.tfig.photo img{aspect-ratio:4/3;object-fit:cover;border-radius:14px;filter:none;animation:none;box-shadow:0 24px 40px -26px rgba(20,22,26,.55)}
aside.toc{position:sticky;top:96px;align-self:start;font-size:13.5px}.toc p{font:500 11px var(--mono);letter-spacing:.14em;color:#98a2b3;margin-bottom:12px}
.toc a{display:block;padding:7px 0 7px 16px;border-left:2px solid var(--line);color:var(--mute);transition:.25s}.toc a.on{border-color:var(--maroon);color:var(--maroon);font-weight:700}.toc a:hover{color:var(--ink)}

/* ---------- 홈 ---------- */
.home{padding:34px 44px 20px;max-width:1240px}
.hero{position:relative;border-radius:22px;background:var(--panel);border:1px solid var(--line);overflow:hidden;padding:56px 56px 0;min-height:500px;display:grid;grid-template-columns:1fr 1fr;align-items:center;isolation:isolate}
.hero::before{content:"";position:absolute;inset:0;z-index:-2;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:36px 36px;mask-image:radial-gradient(90% 90% at 70% 50%,#000 20%,transparent 80%);opacity:.8}
.glow{position:absolute;z-index:-1;width:520px;height:520px;border-radius:50%;filter:blur(70px);right:-60px;top:-60px;background:radial-gradient(circle,rgba(255,107,94,.45),rgba(255,177,92,.25) 50%,transparent 70%);transition:transform .25s ease-out}
.chip{display:inline-flex;align-items:center;gap:10px;font:500 11.5px var(--mono);letter-spacing:.08em;color:var(--maroon);padding:7px 12px;border-radius:999px;border:1px solid #efc9cd;background:#fff7f7}
.chip i{width:7px;height:7px;border-radius:50%;background:var(--coral);box-shadow:0 0 0 0 rgba(255,107,94,.6);animation:ping 1.8s infinite}@keyframes ping{to{box-shadow:0 0 0 9px rgba(255,107,94,0)}}
.hero h1{font-size:clamp(40px,5vw,72px);font-weight:800;letter-spacing:-.05em;line-height:1.08;margin:24px 0 20px;word-break:keep-all}
.hero h1 span{display:inline-block;background:var(--grad);-webkit-background-clip:text;color:transparent;background-size:200% 100%;animation:sweep 6s ease-in-out infinite alternate;padding-right:.05em}@keyframes sweep{to{background-position:100% 0}}
.hero p{color:var(--mute);line-height:1.8;max-width:430px;font-size:16px}
.act{display:flex;gap:12px;margin-top:30px;flex-wrap:wrap}.btn{font-weight:700;font-size:14.5px;padding:14px 22px;border-radius:12px;transition:.3s;display:inline-flex;gap:8px;align-items:center}
.btn.p{background:var(--ink);color:#fff;box-shadow:0 12px 24px -12px rgba(20,22,26,.6)}.btn.p:hover{background:var(--maroon);transform:translateY(-2px)}.btn.s{border:1px solid var(--line);background:#fff}.btn.s:hover{border-color:var(--ink)}
.mini{display:flex;gap:30px;margin-top:40px;padding:18px 0 40px;border-top:1px dashed var(--line);font:500 12px var(--mono);color:var(--mute)}.mini b{display:block;font:800 28px var(--sans);letter-spacing:-.04em;color:var(--ink);margin-bottom:2px}
.fig{position:relative;align-self:stretch;min-height:420px}
.fig img.r{position:absolute;left:50%;top:52%;width:78%;height:auto;transform:translate(-50%,-50%);filter:drop-shadow(0 30px 26px rgba(20,22,26,.28));animation:hov2 5s ease-in-out infinite alternate}@keyframes hov2{to{transform:translate(-50%,-53%)}}
.fig svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.fig path{fill:none;stroke:var(--maroon);stroke-width:1.2;stroke-dasharray:4 4;stroke-dashoffset:200;animation:draw 2s .6s forwards;vector-effect:non-scaling-stroke}@keyframes draw{to{stroke-dashoffset:0}}
.dot{position:absolute;width:12px;height:12px;border-radius:50%;background:#fff;border:2px solid var(--maroon);transform:translate(-50%,-50%)}.dot::after{content:"";position:absolute;inset:-7px;border-radius:50%;border:1px solid var(--maroon);animation:ring 2s infinite}@keyframes ring{from{transform:scale(.6);opacity:1}to{transform:scale(1.7);opacity:0}}
.lab{position:absolute;font:500 11.5px var(--mono);background:#fff;border:1px solid var(--line);padding:6px 10px;border-radius:8px;white-space:nowrap;box-shadow:0 8px 20px -12px rgba(20,22,26,.4);opacity:0;animation:fi .6s forwards}.lab b{color:var(--maroon);margin-right:6px}@keyframes fi{to{opacity:1}}
.sec{margin-top:70px}.sh{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:22px}.sh small{font:500 11.5px var(--mono);letter-spacing:.14em;color:var(--maroon)}.sh h2{font-size:30px;font-weight:800;letter-spacing:-.04em;margin-top:6px}.sh a{font-size:13.5px;color:var(--mute);font-weight:600;white-space:nowrap}.sh a:hover{color:var(--maroon)}
.cards{display:grid;grid-template-columns:repeat(6,1fr);gap:16px}
.hc{position:relative;background:var(--panel);border-radius:18px;padding:1px;overflow:hidden;grid-column:span 2;transition:transform .4s cubic-bezier(.2,.8,.2,1)}.hc.w{grid-column:span 3}
.hc::before{content:"";position:absolute;inset:0;border-radius:18px;background:conic-gradient(from var(--ang),transparent 0 60%,#7a2233,#ff6b5e,#ffb15c,transparent);opacity:0;transition:opacity .4s;animation:rot 3s linear infinite}@keyframes rot{to{--ang:360deg}}
.hc:hover::before{opacity:1}.hc:hover{transform:translateY(-5px)}
.hc .in{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:17px;height:100%;overflow:hidden;display:flex;flex-direction:column}.hc:hover .in{border-color:transparent}
.hc .ph{height:170px;overflow:hidden;background:#eef0f4}.hc.w .ph{height:210px}
.hc .ph img{width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.2,.8,.2,1)}.hc:hover .ph img{transform:scale(1.07)}
.hc .ph.cutph{display:grid;place-items:center;background:linear-gradient(135deg,#fff3ef,#ffe0d3)}.hc .ph.cutph img{object-fit:contain;width:75%;height:auto;max-height:100%;filter:drop-shadow(0 14px 12px rgba(20,22,26,.3))}
.hc .tx{padding:18px 20px 20px}.hc .ix{font:500 11px var(--mono);color:#98a2b3;letter-spacing:.1em;display:flex;justify-content:space-between}.hc .ix em{font-style:normal;color:var(--maroon)}
.hc h3{font-size:20px;font-weight:800;letter-spacing:-.03em;margin:10px 0 6px}.hc p{font-size:13.5px;color:var(--mute);line-height:1.65}
.tlb{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:34px 30px 26px}
.tlb .rail{position:relative;height:2px;background:var(--line);margin:62px 8px 14px}.tlb .fill{position:absolute;left:0;top:0;height:2px;width:0;background:var(--grad);transition:width 2.2s cubic-bezier(.2,.8,.2,1)}
.tlb .tk{position:absolute;top:-4px;width:10px;height:10px;border-radius:50%;background:#fff;border:2px solid #c3c9d4;transform:translateX(-50%);transition:.3s;cursor:pointer}.tlb .tk:hover,.tlb .tk.on{border-color:var(--maroon);background:var(--maroon);transform:translateX(-50%) scale(1.5)}
.tlb .tk span{position:absolute;bottom:22px;left:50%;transform:translateX(-50%) translateY(6px);background:var(--ink);color:#fff;font:500 11px var(--mono);padding:6px 9px;border-radius:7px;white-space:nowrap;opacity:0;pointer-events:none;transition:.25s}.tlb .tk:hover span{opacity:1;transform:translateX(-50%)}
.tlb .yl{display:flex;justify-content:space-between;font:500 11px var(--mono);color:#98a2b3;padding:0 4px}
.tlb .big{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:-24px}.tlb .big b{font-size:44px;font-weight:800;letter-spacing:-.05em;line-height:1}.tlb .big span{font:500 12px var(--mono);color:var(--mute);text-align:right}
.tb{background:var(--panel);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.tr{display:grid;grid-template-columns:90px 1fr 190px 110px;gap:16px;padding:18px 26px;align-items:center;border-top:1px solid var(--line);font-size:14.5px;transition:background .25s;position:relative}.tr.hd{border-top:0;background:#fafbfc;font:500 11px var(--mono);letter-spacing:.12em;color:#98a2b3;padding:13px 26px}
.tr:not(.hd):hover{background:#fff8f6}.tr:not(.hd):hover::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--grad)}
.tr .d{font:500 13px var(--mono);color:var(--mute)}.tr .n{font-weight:700;letter-spacing:-.02em}.tr .o{color:var(--mute);font-size:13.5px}
.tag{justify-self:end;font:700 12px var(--mono);padding:6px 12px;border-radius:999px;background:var(--blush);color:var(--maroon);border:1px solid #efc9cd;white-space:nowrap}.tag.g{background:linear-gradient(90deg,#fff0d6,#ffe1c2);color:#8a4b0a;border-color:#f6cf9d}

footer.site{margin:70px 44px 0;padding:22px 0 40px;border-top:1px solid var(--line);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;font:500 12px var(--mono);color:#98a2b3}
footer.site span:last-child{display:flex;gap:18px;flex-wrap:wrap}footer.site a:hover{color:var(--maroon)}
'''

def convert(line):
    # 기울임 큰 숫자 글꼴은 일반 굵은 산세리프로, 작은 라벨용 display 글꼴은 모노로
    line = re.sub(r'font:italic (\d+) ([^;}]*?)var\(--disp\)', r'font:\1 \2var(--sans)', line)
    line = re.sub(r'font:(\d+) ([^;}]*?)var\(--disp\)', r'font:500 \2var(--mono)', line)
    line = line.replace('transform:skewX(var(--sk))', '').replace(';;', ';')
    return line

# old 파일에서 "detail page parts" ~ "robots" 구간(헤더 주석 포함)만 쓴다
start = next(i for i, l in enumerate(old) if 'detail page parts' in l)
end = next(i for i, l in enumerate(old) if '/* ---------- responsive' in l)
legacy = '\n'.join(convert(l) for l in old[start:end]).replace('padding:4px 40px 18px;margin:0 -40px', 'padding:4px 0 18px;margin:0 0 6px')

RESP = r'''
/* ---------- responsive ---------- */
@media(max-width:1180px){.dl{grid-template-columns:minmax(0,1fr)}aside.toc{display:none}}
@media(max-width:1000px){
 body{grid-template-columns:minmax(0,1fr)}
 aside.nav{position:fixed;left:0;top:0;width:292px;max-width:86vw;transform:translateX(-102%);transition:transform .4s cubic-bezier(.2,.8,.2,1);box-shadow:0 0 60px -20px rgba(0,0,0,.4)}aside.nav.on{transform:none}
 .burger{display:flex}.bar{padding:0 18px}
 .dl,.home{padding:22px 18px 10px}.title{grid-template-columns:1fr;padding:30px 24px}.tfig{max-width:300px}
 .hero{grid-template-columns:1fr;padding:34px 24px 0}.fig{min-height:340px}.cards{grid-template-columns:1fr}.hc,.hc.w{grid-column:auto}
 .tr{grid-template-columns:64px 1fr 82px}.tr .o{display:none}.sh{flex-direction:column;align-items:flex-start}
 .two,.tech,.rb,.tech.wide .ms{grid-template-columns:1fr}.rb figure{aspect-ratio:1.2}.tech .ms{grid-template-columns:1fr 1fr}
 .yr>summary{grid-template-columns:74px 1fr 36px;padding:18px}.yr>summary .y{font-size:30px}.yr>summary .cnt{display:none}.yr .body{grid-template-columns:1fr;padding:4px 14px 18px}.ar{grid-template-columns:48px 1fr 64px;padding:12px 8px}.ar .o{display:none}
 .mg{grid-template-columns:1fr 1fr}.capbox{grid-template-columns:1fr}.team .tp{aspect-ratio:16/10}
 .evl .e{grid-template-columns:1fr;gap:12px}.evl .dt{position:static}.mos{grid-template-columns:repeat(2,1fr);grid-auto-rows:120px}.mos figure:nth-child(n){grid-column:span 1;grid-row:span 1}.mos figure:nth-child(1){grid-column:span 2;grid-row:span 2}
 .rg{grid-template-columns:1fr 1fr}
 footer.site{margin:50px 18px 0}
}
@media(max-width:560px){.fig .lab[style*="left:76%"]{left:auto!important;right:0}.rg{grid-template-columns:1fr}.mg{grid-template-columns:1fr 1fr}.title h1{font-size:34px}.mini{gap:20px}.lab{font-size:10.5px}}
.skip{position:absolute;left:-999px}

/* 모션 최소화 설정을 존중 */
@media (prefers-reduced-motion: reduce){*,*::before,*::after{animation:none!important;transition:none!important}.rv{opacity:1!important;transform:none!important}.lab{opacity:1}.fig path{stroke-dashoffset:0}}
'''

open(sys.argv[2], 'w', encoding='utf-8').write(CHROME + '\n' + legacy + '\n' + RESP)
print('ok', len(legacy.split('\n')), 'legacy lines')
