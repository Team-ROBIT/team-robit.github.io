# 🤖 ROːBIT Archive Project
광운대학교 로봇게임단 로빛(ROːBIT)의 활동 기록 및 기술 자산을 보존하기 위한 새로운 아카이브 사이트입니다.  
기존 Google Sites를 유지하며, 본 사이트는 **GitHub Organization Pages**를 통해 호스팅됩니다.

- **사이트 주소**: https://team-robit.github.io
- Organization Pages는 저장소 이름이 `team-robit.github.io`일 때만 루트 도메인으로 배포되므로, 저장소 이름을 바꾸지 마세요.

---

## 🛠 Tech Stack
- **Framework**: [Astro](https://astro.build/) (v5.0+)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Deployment**: GitHub Actions
- **Data Management**: Astro Content Collections (Markdown/MDX)

---

## 🚀 시작하기 (Getting Started)

프로젝트를 로컬 환경에서 실행하고 수정하는 방법입니다.

### 1. 의존성 설치
```bash
npm install
```

### 2. 개발 서버 실행

```bash
npm run dev
```

접속 주소: `http://localhost:4321`

### 3. 빌드 및 배포

본 저장소는 **GitHub Actions**를 통해 `main` 브랜치에 `push`될 때 자동으로 배포됩니다.

```bash
# 수동 빌드 확인 (오류 체크용)
npm run build
```

---

## 📂 프로젝트 구조 (Project Structure)

유지보수를 위해 아래 폴더 구조를 반드시 숙지해 주세요.

```text
/
├── src/
│   ├── components/   # 버튼, 네비게이션, 카드 등 재사용 가능한 UI 조각
│   ├── layouts/      # 페이지의 전체 틀 (Header, Footer 포함)
│   ├── pages/        # 실제 URL 경로 (index.astro가 메인)
│   ├── content/      # 중요: 실제 데이터(대회 기록, 프로젝트)가 담긴 마크다운 파일
│   └── styles/       # 글로벌 CSS 및 Tailwind 설정
├── public/           # 이미지, PDF, 로고 등 정적 파일
└── astro.config.mjs  # Astro 환경 설정


```


## ✍️ 유지보수 가이드 (How to Maintain)

### 1. 새로운 프로젝트/글 추가하기

이 사이트는 마크다운 기반의 **Content Collections**를 사용합니다. 새로운 기록을 남기려면 `src/content/` 내의 해당 카테고리 폴더에 `.md` 파일을 생성하세요.

### 2. 레이아웃 수정

전체적인 사이트의 디자인(헤더, 푸터 등)을 바꾸고 싶다면 `src/layouts/Layout.astro` 파일을 수정하세요. 모든 페이지에 일괄 적용됩니다.

### 3. 이미지 업로드

이미지는 `public/images/projects/` 폴더 내에 연도별로 정리하여 업로드하는 것을 권장합니다.
예: `/public/images/2026/rescue-robot.jpg`

---

## 📢 인수인계 유의사항

* **일관성 유지**: 스타일 수정 시 가급적 Tailwind CSS의 유틸리티 클래스를 사용하세요.
* **문서화**: 새로운 기능을 추가할 경우, 이 README 파일의 '유지보수 가이드' 섹션을 업데이트해 주세요.
* **문의**: 초기 제작자 - 19기 지능팀 박기홍 (Kinesis Akashic)

---

Copyright © 2025 **ROːBIT**. All rights reserved.