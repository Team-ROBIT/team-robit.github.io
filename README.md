# ROːBIT Archive

광운대학교 로봇게임단 로빛(ROːBIT)의 활동 기록과 기술 자산을 보존하는 아카이브 사이트입니다.
**GitHub Organization Pages**로 호스팅되며, 저장소 이름이 `team-robit.github.io`일 때만 루트 도메인으로 배포되므로 **저장소 이름을 바꾸지 마세요.**

- **사이트 주소**: https://team-robit.github.io
- **원본(구글 사이트)**: https://sites.google.com/view/robitarchieve/main — 모든 페이지·사진·기사 PDF를 이 저장소로 백업했습니다.

---

## 기술 스택
- **Framework**: [Astro](https://astro.build/) 5 (Content Collections, MDX)
- **Styling**: 직접 작성한 테마 CSS(`src/styles`) + Tailwind CSS(일부 유틸리티)
- **Fonts**: Pretendard, Archivo
- **Deployment**: GitHub Actions (`main` 브랜치에 push하면 자동 배포)

---

## 시작하기

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # 배포 전 오류 확인 (dist/ 생성)
npm run preview    # 빌드 결과 미리보기
```

Node.js 20 이상을 권장합니다.

---

## 프로젝트 구조

```text
/
├── src/
│   ├── content/archive/   # 페이지 본문 (Markdown / MDX). 폴더 이름이 곧 URL 입니다.
│   ├── data/              # 구조화된 데이터: 수상(awards), 행사(events), 로봇(robots), 기수(generations), 메뉴(nav), 홈(home)
│   ├── components/        # SideNav(왼쪽 사이드바·검색) · TopBar · Footer · PageHeader · 각 데이터 화면(AwardsView 등) · MemberRoster
│   ├── layouts/           # BaseLayout(공통 틀) · DocsLayout(하위 페이지)
│   ├── pages/             # index.astro(홈) · [...slug].astro(모든 문서)
│   ├── plugins/           # remark-gallery.mjs — 연속된 이미지를 자동으로 갤러리로 묶음
│   ├── scripts/site.js    # 모바일 서랍, 검색(Ctrl K), 스크롤 효과 등
│   ├── styles/            # theme.css(테마, scripts/redesign/build_theme.py 로 조립한 결과물) · doc.css(본문) · views.css(데이터 화면)
│   └── assets/            # 이미지 (빌드 시 자동 최적화)
├── public/archive/articles/   # 기사 스캔 PDF (74개)
├── scripts/backup/        # 원본 구글 사이트 백업·검증 도구
└── scripts/redesign/      # 리디자인 때 쓴 변환 도구 (일회성)
```

---

## 유지보수 가이드

### 새 페이지 추가
`src/content/archive/<섹션>/<이름>.md` 파일을 만들면 `/<섹션>/<이름>` 주소의 페이지가 생깁니다.
상단 정보(frontmatter)로 페이지 머리 부분이 구성됩니다.

```md
---
title: "국방로봇경진대회"            # 큰 제목
description: "한 줄 설명"            # 메타 설명
subtitle: "Defense Robot Competition" # 영문 부제
chips: ["2019 — 2026", "KUBO"]       # 제목 아래 칩
highlight: "2026 · 1위"              # 강조 칩(그라데이션)
cover: ../../../assets/assets_contest/defense-robot-003.webp  # 상단 이미지
coverKind: cutout                    # cutout(배경 없는 로봇) 또는 photo(일반 사진)
---

## Introduction
본문은 일반 마크다운입니다. `##` 제목은 번호가 붙고 상단 탭에 자동으로 나타납니다.
이미지를 줄바꿈으로 나열하면 갤러리로 묶입니다.
```

- 메뉴(왼쪽 사이드바·모바일 서랍·검색)에 넣으려면 `src/data/nav.ts`에 항목을 추가하세요.
- 이미지는 `src/assets/` 아래에 넣고 마크다운에서 상대 경로로 불러옵니다.

### 데이터로 관리하는 화면
긴 목록은 JSON으로 관리합니다. 파일을 수정하면 화면이 자동으로 갱신됩니다.

| 화면 | 데이터 | 비고 |
|---|---|---|
| 수상 내역 | `src/data/awards.json` | 연도별 `rows`(날짜·대회·상격·수여 기관)와 `photo` |
| 참여 행사 | `src/data/events.json` | 이미지는 `assets_events/` 의 파일 이름(확장자 제외) |
| 로봇 목록 | `src/data/robots.json` | `cat`: humanoid / battle / defense / other |
| 전체 명단 | `src/data/generations.json` | 기수 카드 |
| 홈 | `src/data/home.ts` | 최근 성적표, 하이라이트 연표, 숫자 |

기수별 명단은 `src/content/archive/members/*.mdx` 안의 `<MemberRoster>` 데이터를 고칩니다.
새 기수를 추가할 때는 `generations.json`에도 한 줄 추가하세요.

---

## 백업 도구 (`scripts/backup`)
원본 구글 사이트를 수집·변환·검증하는 도구입니다. 결과물(`_backup/`)은 git에 포함하지 않습니다.

```bash
python scripts/backup/extract.py fetch      # 원본 59개 페이지 수집
python scripts/backup/extract.py convert    # Markdown 변환 + 이미지 다운로드
node scripts/backup/optimize.mjs            # 이미지 WebP 최적화
python scripts/backup/verify.py             # 원본 대비 누락 검사 (텍스트·이미지·링크)
python scripts/redesign/check_links.py      # 빌드 결과의 내부 링크 검사 (build 후)
```

---

## 인수인계 유의사항
- **일관성**: 색상·여백은 `src/styles/theme.css` 의 CSS 변수(`:root`)를 사용하세요.
- **문서화**: 새 기능을 추가하면 이 README 의 '유지보수 가이드'를 갱신해 주세요.
- **문의**: 초기 제작자 - 19기 지능팀 박기홍 (Kinesis Akashic)

---

Copyright © 2025 **ROːBIT**. All rights reserved.
