// 홈 화면에 쓰는 요약 데이터. 수치와 항목은 수상 내역·기사 아카이브의 실제 기록을 따른다.
export const stats = [
  { n: 20, label: '기수' },
  { n: 295, label: '수상 (2025 기준)' },
  { n: 74, label: '기사 스캔' },
];

// 최근 성적. 날짜 열에는 해당 연도를 쓴다.
export const latest = [
  { year: '2026', name: '국방로봇경진대회', org: '산업통상부장관상 · Eclipse', rank: '1위 · 대상', gold: true, href: '/contest/defense-robot' },
  { year: '2026', name: 'SRCIRC 휴머노이드', org: '2개 팀 출전', rank: '1위 · 2위', gold: true, href: '/contest/src-irc-humanoid' },
  { year: '2026', name: 'IRC 매니퓰레이터 · SAFE LAB', org: '국가기술표준원장상', rank: '2위', gold: false, href: '/contest/irc-manipulator' },
  { year: '2026', name: '한국로보컵오픈 휴머노이드 축구 Kid Size', org: '—', rank: '1위', gold: true, href: '/contest/robocup-humanoid' },
  { year: '2025', name: '극한로봇 경진대회', org: '서울시장상 · Eclipse', rank: '대상', gold: true, href: '/contest/extreme-robot' },
  { year: '2025', name: '국방로봇경진대회', org: '육군참모총장상 · LUCO', rank: '1위 · 최우수상', gold: true, href: '/contest/defense-robot' },
];

// 연표 눈금: 해마다 가장 큰 성과
export const milestones = [
  { year: 2006, title: '창단 (11월 1일)', text: '광운대학교 로봇게임단 로빛 창단' },
  { year: 2007, title: 'EBS 로봇파워 · 대한민국로봇대전', text: '휴머노이드 최강, 로봇대전 휴머노이드 대상' },
  { year: 2009, title: '국제로봇컨테스트', text: '휴머노이드 단체전 우승, 대통령상' },
  { year: 2016, title: 'IRC 국제로봇컨테스트', text: '지능형 휴머노이드 1위 · DST 멀티미션챌린지 1위' },
  { year: 2023, title: 'RoboCup Asia-Pacific', text: '휴머노이드 Kid Size 우승' },
  { year: 2025, title: '극한로봇 · 국방로봇', text: '극한로봇 대상, 국방로봇 최우수상' },
  { year: 2026, title: '국방로봇 대상', text: '국방로봇경진대회 대상, SRCIRC 1·2위' },
];
