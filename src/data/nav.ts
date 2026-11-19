// 사이트 내비게이션 정의: 왼쪽 사이드바, 모바일 메뉴, 검색, 페이지 경로 표기에 공통으로 사용한다.
export interface NavSub { label: string; href: string }
export interface NavLink { no: string; label: string; href: string; count?: string; /** 이 링크가 "현재 위치"로 잡히는 경로 접두어 */ match: string[]; sub?: NavSub[] }
export interface NavGroup { title: string; links: NavLink[] }

export const groups: NavGroup[] = [
  {
    title: 'OVERVIEW',
    links: [
      { no: '00', label: '홈', href: '/', match: ['/'] },
      { no: '01', label: '로빛 소개', href: '/overview/information', match: ['/overview/information'] },
      { no: '02', label: 'History & Archive', href: '/overview/history', match: ['/overview/history'] },
    ],
  },
  {
    title: 'RECORDS',
    links: [
      {
        no: '03', label: '대회', href: '/contest/participation', count: '10',
        match: ['/contest/participation', '/contest/robocup', '/contest/src-irc', '/contest/irc-', '/contest/defense', '/contest/extreme', '/contest/ssireum', '/contest/turtlebot', '/contest/robotpower'],
        sub: [
          { label: 'RoboCup Humanoid', href: '/contest/robocup-humanoid' },
          { label: 'RoboCup Rescue', href: '/contest/robocup-rescue' },
          { label: 'SRCIRC 휴머노이드', href: '/contest/src-irc-humanoid' },
          { label: 'IRC 매니퓰레이터', href: '/contest/irc-manipulator' },
          { label: '국방로봇경진대회', href: '/contest/defense-robot' },
          { label: '극한로봇경진대회', href: '/contest/extreme-robot' },
          { label: '씨름로봇', href: '/contest/ssireum' },
          { label: 'TurtleBot AutoRace', href: '/contest/turtlebot-autorace' },
        ],
      },
      { no: '04', label: '수상 내역', href: '/contest/awards', count: '295', match: ['/contest/awards'] },
      { no: '05', label: '행사', href: '/events/participation', count: '16', match: ['/events/participation'] },
      { no: '06', label: '기사 · 방송', href: '/articles/press', count: '74', match: ['/articles/press', '/events/broadcast'] },
    ],
  },
  {
    title: 'PEOPLE & ROBOTS',
    links: [
      { no: '07', label: '로봇 목록', href: '/robots/list', count: '57', match: ['/robots/'] },
      { no: '08', label: '전체 명단', href: '/members/roster', count: '20기', match: ['/members/'] },
      { no: '09', label: 'Contact', href: '/contact/contact', match: ['/contact/'] },
    ],
  },
];

export const contactHref = '/contact/contact';
export const social = {
  instagram: 'https://www.instagram.com/robit_korea_official',
  youtube: 'https://www.youtube.com/@ROBIT_KOREA',
  email: 'kwrobitcontact@gmail.com',
};

/** 현재 경로가 어느 사이드바 링크에 속하는지 구한다 (가장 긴 접두어가 이긴다). */
export function currentLink(pathname: string): NavLink | undefined {
  const p = pathname.replace(/\/$/, '') || '/';
  let best: { link: NavLink; len: number } | undefined;
  for (const g of groups)
    for (const l of g.links)
      for (const m of l.match) {
        const hit = m === '/' ? p === '/' : p === m || p.startsWith(m.endsWith('/') ? m : m);
        if (hit && (!best || m.length > best.len)) best = { link: l, len: m.length };
      }
  return best?.link;
}

/** 문서 경로(slug)로 소속 섹션과 경로 표기를 구한다. */
export function sectionOf(slug: string) {
  const top = slug.split('/')[0];
  const map: Record<string, { key: string; kicker: string }> = {
    overview: { key: 'overview', kicker: 'OVERVIEW' },
    contest: { key: 'contest', kicker: 'CONTEST' },
    events: { key: 'records', kicker: 'RECORDS' },
    articles: { key: 'records', kicker: 'RECORDS' },
    robots: { key: 'robots', kicker: 'ROBOTS' },
    members: { key: 'people', kicker: 'PEOPLE' },
    contact: { key: 'contact', kicker: 'CONTACT' },
  };
  return map[top] ?? { key: '', kicker: '' };
}
